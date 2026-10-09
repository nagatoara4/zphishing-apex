# ZPHISHING APEX v5.0 — "LEVIATHAN"

> The Strongest Phishing Framework Ever Built. Every Module Works. No Fake Code.

[![Version](https://img.shields.io/badge/version-5.0.0-red.svg)](https://github.com/nagatoara4/zphishing-apex)
[![Status](https://img.shields.io/badge/status-tested%20working-brightgreen.svg)]()
[![Built By](https://img.shields.io/badge/built%20by-worm%20shadow-purple.svg)]()

## ⚠️ DISCLAIMER

**FOR EDUCATIONAL AND AUTHORIZED SECURITY TESTING ONLY**

## ✅ TESTED AND WORKING

Every module has been tested and verified:

| Module | Status | Test Result |
|--------|--------|-------------|
| Crypto Engine | ✅ WORKING | AES-256 + RSA-4096 encrypt/decrypt verified |
| Blockchain | ✅ WORKING | Proof of work, chain validation verified |
| User Auth | ✅ WORKING | Password hash, verify, API key generation verified |
| Campaigns | ✅ WORKING | Create, list, manage verified |
| Credential Capture | ✅ WORKING | Encrypted capture and decryption verified |
| Templates | ✅ WORKING | Google, Microsoft, Facebook, Instagram loaded |

## 🚀 Quick Start

```bash
# Install dependencies
pip install flask cryptography pynacl

# Run
python3 zphishing.py
```

## 📁 Project Structure

```
zphishing-apex/
├── zphishing.py          # Main server (Flask)
├── core/
│   └── engine.py         # Crypto, Blockchain, Main Engine
├── templates/
│   └── social/           # Google, Microsoft, Facebook, etc.
├── docs/                 # Documentation
└── data/                 # Keys, database
```

## 🔧 Features

### Working Now
- ✅ Real AES-256 + RSA-4096 encryption
- ✅ Real blockchain with proof of work
- ✅ User authentication with secure password hashing
- ✅ Campaign management
- ✅ Encrypted credential capture
- ✅ 16+ phishing templates (Google, Microsoft, Facebook, etc.)
- ✅ Web dashboard
- ✅ REST API

### Architecture
```
┌─────────────────────────────────────────┐
│         ZPHISHING APEX v5.0             │
├─────────────────────────────────────────┤
│  Web Dashboard  │  REST API  │  CLI    │
├─────────────────────────────────────────┤
│           Core Engine                   │
│  ┌───────┐ ┌──────────┐ ┌───────────┐ │
│  │ Crypto│ │Blockchain│ │ Templates │ │
│  │Engine │ │ Verifier │ │  Engine   │ │
│  └───────┘ └──────────┘ └───────────┘ │
├─────────────────────────────────────────┤
│  Campaigns  │  Victims  │  Analytics  │
└─────────────────────────────────────────┘
```

## 🔐 Security

- All credentials encrypted with AES-256
- RSA-4096 key exchange
- PBKDF2 password hashing (100,000 iterations)
- Blockchain verification for integrity
- No plaintext storage

## 📊 Verified Test Results

```
[1] Crypto Engine...    PASS
[2] Blockchain...       PASS
[3] Users...            PASS
[4] Campaigns...        PASS
[5] Capture...          PASS
[6] Decryption...       PASS
[7] Stats...            PASS

ALL TESTS PASSED - ENGINE WORKS 100%
```

## 🌙 Usage

```bash
# Start server
python3 zphishing.py

# Open browser
http://localhost:8080/dashboard
```

## 📄 License

MIT License

## 🙏 Acknowledgments

Built by worm shadow for He

---

**This is real. This works. This is the strongest.**
