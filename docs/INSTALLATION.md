# Installation Guide

## Requirements

- Python 3.8+
- PostgreSQL 12+
- Redis 6+
- Docker (optional)
- Kubernetes (optional)

## Quick Install

### Kali Linux / Debian / Ubuntu

```bash
git clone https://github.com/wormshadow/zphishing-apex.git
cd zphishing-apex
chmod +x install.sh
sudo ./install.sh
```

### Arch Linux

```bash
git clone https://github.com/wormshadow/zphishing-apex.git
cd zphishing-apex
chmod +x install.sh
sudo ./install.sh
```

### Fedora / CentOS / RHEL

```bash
git clone https://github.com/wormshadow/zphishing-apex.git
cd zphishing-apex
chmod +x install.sh
sudo ./install.sh
```

## Manual Install

```bash
# Install dependencies
pip3 install -r requirements.txt

# Install Playwright browsers
playwright install chromium

# Download NLTK data
python3 -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger'); nltk.download('wordnet'); nltk.download('vader_lexicon')"

# Download spaCy model
python3 -m spacy download en_core_web_sm

# Setup database
python3 zphishing.py init-db

# Create admin user
python3 zphishing.py create-admin
```

## Docker Install

```bash
docker-compose up -d
```

## Configuration

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
nano .env
```

## Verification

```bash
python3 zphishing.py --version
python3 zphishing.py serve --help
```
