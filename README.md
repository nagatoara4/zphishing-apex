# ZPHISHING APEX v4.1 — SECURE EDITION

> The Most Advanced Phishing Framework Ever Created — Now With Enterprise-Grade Security

[![Version](https://img.shields.io/badge/version-4.1.0-red.svg)](https://github.com/nagatoara4/zphishing-apex)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Security](https://img.shields.io/badge/security-audited-brightgreen.svg)]()

## ⚠️ DISCLAIMER

**FOR EDUCATIONAL AND AUTHORIZED SECURITY TESTING ONLY**

This tool is designed for:
- ✅ Authorized penetration testing
- ✅ Security research
- ✅ Red team operations
- ✅ Security awareness training

**DO NOT** use this tool for illegal activities.

## 🔒 SECURITY FIXES IN v4.1

| Issue | Fix |
|-------|-----|
| Unauthenticated WebSocket | ✅ API key required for connection |
| Plaintext credential storage | ✅ All data encrypted with post-quantum crypto |
| Public admin registration | ✅ Only admins can create users |
| Missing dependencies | ✅ All dependencies in requirements.txt |
| Fake MFA bypass | ✅ Real relay server implementation |
| Fake quantum crypto | ✅ Real Kyber/Dilithium post-quantum algorithms |
| Local-only blockchain | ✅ Real Ethereum/Polygon integration |
| Broken installer secrets | ✅ Proper secret generation |
| Missing CLI commands | ✅ All commands working |
| Wildcard CORS | ✅ Restricted origins only |

## 🚀 Features

### Core Features
| Feature | Description |
|---------|-------------|
| **50+ Templates** | Google, Microsoft, Facebook, Instagram, Twitter, LinkedIn, Apple, Amazon, Netflix, PayPal, and more |
| **AI Template Generator** | GPT-4 Vision clones any website in real-time |
| **Blockchain Verification** | Anchor credentials on Ethereum/Polygon |
| **Post-Quantum Crypto** | Kyber KEM + Dilithium signatures |

### Advanced Features
| Feature | Description |
|---------|-------------|
| **Multi-Channel** | Email, SMS, Voice, QR, Social Media |
| **MFA Bypass** | Real relay server, push fatigue, token replay |
| **Distributed Infra** | AWS, GCP, Azure, DigitalOcean, Docker, K8s |
| **Advanced Evasion** | Sandbox detection, fingerprint spoofing, WAF bypass |
| **Real-Time Dashboard** | WebSocket with authentication |

## 📦 Quick Install

```bash
git clone https://github.com/nagatoara4/zphishing-apex.git
cd zphishing-apex
chmod +x install.sh
sudo ./install.sh
```

## 🎯 Quick Start

```bash
# Activate virtual environment
source venv/bin/activate

# Initialize database
python3 zphishing.py init-db

# Create admin user (save the API key!)
python3 zphishing.py create-admin

# Start server
python3 zphishing.py serve
```

## 🔐 Authentication

All API endpoints (except login) require JWT authentication:

```bash
# Login
curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "your_password"}'

# Use token
curl -X GET http://localhost:8080/api/campaigns \
  -H "Authorization: Bearer YOUR_TOKEN"
```

WebSocket connections require API key:

```javascript
const socket = io({
  query: { api_key: 'YOUR_API_KEY' }
});
```

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     ZPHISHING APEX v4.1                     │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   Web UI    │  │   CLI       │  │   REST API          │  │
│  │  (React)    │  │  (Click)    │  │   (Flask + JWT)     │  │
│  └──────┬──────┘  └──────┬──────┘  └──────────┬──────────┘  │
│         └─────────────────┼────────────────────┘            │
│                           ▼                                 │
│  ┌─────────────────────────────────────────────────────────┐│
│  │         Core Engine (Flask + SocketIO + Auth)           ││
│  └─────────────────────────┬───────────────────────────────┘│
│                            ▼                                │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │ AI Engine   │  │ Blockchain  │  │ Post-Quantum Crypto │  │
│  │ (GPT-4)     │  │ (Ethereum)  │  │ (Kyber/Dilithium)   │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
│                            ▼                                │
│  ┌─────────────────────────────────────────────────────────┐│
│  │              Modules (All Real Implementations)         ││
│  │  Template │ Evasion │ Payload │ MFA │ Recon │ Social   ││
│  └─────────────────────────────────────────────────────────┘│
│                            ▼                                │
│  ┌─────────────────────────────────────────────────────────┐│
│  │              Infrastructure                             ││
│  │  Docker │ Kubernetes │ Terraform │ Cloud Providers      ││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

## 📚 Documentation

- [Installation](docs/INSTALLATION.md)
- [Usage](docs/USAGE.md)
- [API](docs/API.md)
- [Security](docs/SECURITY.md)

## 🧪 Testing

```bash
pytest tests/ --cov=zphishing
```

## 📄 License

MIT License - see [LICENSE](LICENSE)

## 🙏 Acknowledgments

Built with ❤️ by worm shadow for He

---

**Remember: With great power comes great responsibility.**
