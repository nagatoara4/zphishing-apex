#!/bin/bash

# ZPHISHING APEX v4.0 — Installation Script
# Works on Kali Linux, Arch Linux, and all Linux distributions

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║   ███████╗██████╗ ██╗  ██╗██╗███████╗██╗  ██╗██╗███╗   ██╗ ██████╗  ║"
echo "║   ╚══███╔╝██╔══██╗██║  ██║██║██╔════╝██║  ██║██║████╗  ██║██╔════╝  ║"
echo "║     ███╔╝ ██████╔╝███████║██║███████╗███████║██║██╔██╗ ██║██║       ║"
echo "║    ███╔╝  ██╔═══╝ ██╔══██║██║╚════██║██╔══██║██║██║╚██╗██║██║       ║"
echo "║   ███████╗██║     ██║  ██║██║███████║██║  ██║██║██║ ╚████║╚██████╗  ║"
echo "║   ╚══════╝╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝  ║"
echo "║                                                              ║"
echo "║              A P E X   P R O T O C O L   v 4 . 0              ║"
echo "║                                                              ║"
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
    VER=$VERSION_ID
else
    echo -e "${RED}[!] Cannot detect OS${NC}"
    exit 1
fi

echo -e "${CYAN}[*] Detected OS: $OS $VER${NC}"

# Update system
echo -e "${YELLOW}[*] Updating system packages...${NC}"
if [[ "$OS" == *"Kali"* ]] || [[ "$OS" == *"Debian"* ]] || [[ "$OS" == *"Ubuntu"* ]]; then
    apt-get update -y
    apt-get upgrade -y
elif [[ "$OS" == *"Arch"* ]]; then
    pacman -Syu --noconfirm
elif [[ "$OS" == *"Fedora"* ]]; then
    dnf update -y
elif [[ "$OS" == *"CentOS"* ]] || [[ "$OS" == *"Red Hat"* ]]; then
    yum update -y
else
    echo -e "${YELLOW}[!] Unknown OS, skipping system update${NC}"
fi

# Install dependencies
echo -e "${YELLOW}[*] Installing dependencies...${NC}"
if [[ "$OS" == *"Kali"* ]] || [[ "$OS" == *"Debian"* ]] || [[ "$OS" == *"Ubuntu"* ]]; then
    apt-get install -y python3 python3-pip python3-venv python3-dev git curl wget \
        build-essential libssl-dev libffi-dev libxml2-dev libxslt1-dev \
        libjpeg-dev zlib1g-dev libpng-dev libtesseract-dev \
        tesseract-ocr ffmpeg libsm6 libxext6 libxrender-dev \
        libgl1-mesa-glx libglib2.0-0 chromium-browser \
        nginx certbot python3-certbot-nginx docker.io docker-compose \
        postgresql postgresql-contrib redis-server \
        tor proxychains4 openvpn wireguard-tools
elif [[ "$OS" == *"Arch"* ]]; then
    pacman -S --noconfirm python python-pip python-virtualenv git curl wget \
        base-devel openssl libffi libxml2 libxslt \
        libjpeg-turbo zlib libpng tesseract \
        tesseract-data-eng ffmpeg libsm libxext libxrender \
        mesa glib2 chromium nginx certbot certbot-nginx docker docker-compose \
        postgresql redis tor proxychains-ng openvpn wireguard-tools
elif [[ "$OS" == *"Fedora"* ]]; then
    dnf install -y python3 python3-pip python3-virtualenv git curl wget \
        gcc gcc-c++ openssl-devel libffi-devel libxml2-devel libxslt-devel \
        libjpeg-turbo-devel zlib-devel libpng-devel tesseract-devel \
        tesseract ffmpeg libSM libXext libXrender \
        mesa-libGL glib2 chromium nginx certbot python3-certbot-nginx docker docker-compose \
        postgresql postgresql-server redis tor proxychains-ng openvpn wireguard-tools
fi

# Install Python packages
echo -e "${YELLOW}[*] Installing Python packages...${NC}"
pip3 install --upgrade pip
pip3 install -r requirements.txt

# Install Playwright browsers
echo -e "${YELLOW}[*] Installing Playwright browsers...${NC}"
playwright install chromium
playwright install firefox

# Download NLTK data
echo -e "${YELLOW}[*] Downloading NLTK data...${NC}"
python3 -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger'); nltk.download('wordnet'); nltk.download('vader_lexicon')"

# Download spaCy model
echo -e "${YELLOW}[*] Downloading spaCy model...${NC}"
python3 -m spacy download en_core_web_sm

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

# Create necessary directories
echo -e "${YELLOW}[*] Creating directories...${NC}"
mkdir -p templates/{social,corporate,custom,ai_generated}
mkdir -p payloads/{credential_stealer,session_hijacker,mfa_bypass,custom}
mkdir -p evasion/{domain_rotation,fingerprint_spoofer,traffic_obfuscator,sandbox_detector,waf_bypass}
mkdir -p infrastructure/{cloud_deployer,docker_manager,kubernetes_orchestrator,ssl_manager}
mkdir -p api/{rest_api,websocket,graphql}
mkdir -p cli/{interactive,commands}
mkdir -p web/{dashboard,operator_panel,victim_tracker}
mkdir -p utils/{logger,config_manager,crypto_utils,helpers}
mkdir -p docs

# Set permissions
chmod +x zphishing.py
chmod +x install.sh

# Create .env file
echo -e "${YELLOW}[*] Creating environment configuration...${NC}"
cat > .env << 'EOF'
# ZPHISHING APEX Configuration
FLASK_APP=zphishing.py
FLASK_ENV=production
SECRET_KEY=$(openssl rand -hex 32)
DATABASE_URL=postgresql://zphishing:zphishing@localhost/zphishing_db
REDIS_URL=redis://localhost:6379/0
JWT_SECRET_KEY=$(openssl rand -hex 32)

# AI API Keys (optional)
OPENAI_API_KEY=your-openai-api-key-here
ANTHROPIC_API_KEY=your-anthropic-api-key-here
REPLICATE_API_TOKEN=your-replicate-api-token-here

# Cloud Provider Keys (optional)
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
DIGITALOCEAN_TOKEN=your-do-token
GOOGLE_APPLICATION_CREDENTIALS=path-to-gcp-credentials
AZURE_SUBSCRIPTION_ID=your-azure-subscription

# Communication Keys (optional)
TWILIO_ACCOUNT_SID=your-twilio-sid
TWILIO_AUTH_TOKEN=your-twilio-token
VONAGE_API_KEY=your-vonage-key
VONAGE_API_SECRET=your-vonage-secret
SLACK_BOT_TOKEN=your-slack-token
DISCORD_WEBHOOK_URL=your-discord-webhook
TELEGRAM_BOT_TOKEN=your-telegram-token

# Security
ENCRYPTION_KEY=$(openssl rand -base64 32)
TOR_SOCKS_PROXY=socks5://127.0.0.1:9050
EOF

echo -e "${GREEN}[+] Installation complete!${NC}"
echo -e "${CYAN}[*] To start ZPHISHING APEX, run:${NC}"
echo -e "${YELLOW}    python3 zphishing.py${NC}"
echo ""
echo -e "${PURPLE}[!] For educational and authorized security testing only${NC}"
