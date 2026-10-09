# ZPHISHING APEX v4.0

> The Most Advanced Phishing Framework Ever Created

[![Version](https://img.shields.io/badge/version-4.0.0-red.svg)](https://github.com/wormshadow/zphishing-apex)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Kali%20Linux%20%7C%20Arch%20Linux%20%7C%20All%20Linux-lightgrey.svg)]()

## ⚠️ DISCLAIMER

**FOR EDUCATIONAL AND AUTHORIZED SECURITY TESTING ONLY**

This tool is designed for:
- ✅ Authorized penetration testing
- ✅ Security research
- ✅ Red team operations
- ✅ Security awareness training

**DO NOT** use this tool for illegal activities. Unauthorized access to computer systems is illegal.

## 🚀 Features

### Core Features
| Feature | Description |
|---------|-------------|
| **50+ Templates** | Google, Microsoft, Facebook, Instagram, Twitter, LinkedIn, Apple, Amazon, Netflix, PayPal, and more |
| **AI Template Generator** | GPT-4 Vision clones any website in real-time |
| **Blockchain Verification** | Verify captured credentials on blockchain |
| **Quantum Crypto** | Post-quantum encryption for sensitive data |

### Advanced Features
| Feature | Description |
|---------|-------------|
| **Multi-Channel** | Email, SMS, Voice, QR, Social Media |
| **MFA Bypass** | Relay attacks, push fatigue, token theft |
| **Distributed Infra** | Auto-spin cloud instances (AWS, GCP, Azure, DO) |
| **Advanced Evasion** | Sandbox detection, fingerprint spoofing, WAF bypass |
| **Real-Time Analytics** | Live dashboard, geographic distribution |
| **Payload Delivery** | Multi-stage, fileless, macro-embedded, QR codes |

## 📦 Quick Install

```bash
git clone https://github.com/wormshadow/zphishing-apex.git
cd zphishing-apex
chmod +x install.sh
sudo ./install.sh
```

## 🎯 Quick Start

```bash
# Start web server
python3 zphishing.py serve --host 0.0.0.0 --port 8080

# Interactive shell
python3 zphishing.py shell

# Create campaign
python3 zphishing.py create-campaign --name "Test" --template google

# Start campaign
python3 zphishing.py start-campaign CAMPAIGN_ID
```

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     ZPHISHING APEX                          │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   Web UI    │  │   CLI       │  │   REST API          │  │
│  └──────┬──────┘  └──────┬──────┘  └──────────┬──────────┘  │
│         └─────────────────┼────────────────────┘            │
│                           ▼                                 │
│  ┌─────────────────────────────────────────────────────────┐│
│  │              Core Engine (Flask + SocketIO)             ││
│  └─────────────────────────┬───────────────────────────────┘│
│                            ▼                                │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │ AI Engine   │  │ Blockchain  │  │ Quantum Crypto      │  │
│  │ (GPT-4)     │  │ Verifier    │  │ (Post-Quantum)      │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
│                            ▼                                │
│  ┌─────────────────────────────────────────────────────────┐│
│  │              Modules                                    ││
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
- [Contributing](docs/CONTRIBUTING.md)

## 🧪 Testing

```bash
pytest tests/ --cov=zphishing
```

## 📄 License

MIT License - see [LICENSE](LICENSE)

## 🙏 Acknowledgments

Built with ❤️ by worm shadow

---

**Remember: With great power comes great responsibility.**
