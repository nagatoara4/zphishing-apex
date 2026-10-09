#!/bin/bash

# ZPHISHING APEX — Deploy to GitHub Script
# Usage: ./deploy-to-github.sh YOUR_GITHUB_USERNAME YOUR_REPO_NAME

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║         ZPHISHING APEX — GitHub Deployment Script            ║"
echo "╚══════════════════════════════════════════════════════════════╝"

# Check arguments
if [ $# -lt 2 ]; then
    echo -e "${RED}[!] Usage: $0 YOUR_GITHUB_USERNAME YOUR_REPO_NAME${NC}"
    echo -e "${YELLOW}[*] Example: $0 wormshadow zphishing-apex${NC}"
    exit 1
fi

USERNAME=$1
REPO_NAME=$2
REPO_URL="https://github.com/$USERNAME/$REPO_NAME.git"

echo -e "${CYAN}[*] Deploying to: $REPO_URL${NC}"

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo -e "${RED}[!] Git is not installed${NC}"
    exit 1
fi

# Initialize git if not already done
if [ ! -d .git ]; then
    echo -e "${YELLOW}[*] Initializing git repository...${NC}"
    git init
fi

# Add all files
echo -e "${YELLOW}[*] Adding files...${NC}"
git add .

# Commit
echo -e "${YELLOW}[*] Committing...${NC}"
git commit -m "🚀 ZPHISHING APEX v4.0 — Initial Release

The Most Advanced Phishing Framework Ever Created

Features:
- 50+ pre-built phishing templates
- AI-powered template generation (GPT-4 Vision)
- Blockchain credential verification
- Quantum-resistant encryption
- Multi-channel payload delivery (Email/SMS/QR/Social)
- MFA bypass suite (Relay/Push Fatigue/Token Theft)
- Distributed infrastructure (AWS/GCP/Azure/DO/Docker/K8s)
- Advanced evasion (Sandbox Detection/Fingerprint Spoofing/WAF Bypass)
- Real-time web dashboard with live victim tracking
- Full REST API with JWT authentication

Built by worm shadow for He

For educational and authorized security testing only." || echo "Nothing to commit"

# Set branch to main
echo -e "${YELLOW}[*] Setting branch to main...${NC}"
git branch -M main

# Add remote
echo -e "${YELLOW}[*] Adding remote origin...${NC}"
git remote remove origin 2>/dev/null || true
git remote add origin "$REPO_URL"

# Push
echo -e "${YELLOW}[*] Pushing to GitHub...${NC}"
echo -e "${CYAN}[*] You may be prompted for your GitHub credentials${NC}"
git push -u origin main

echo -e "${GREEN}[+] Deployment complete!${NC}"
echo -e "${GREEN}[+] Repository: https://github.com/$USERNAME/$REPO_NAME${NC}"
echo ""
echo -e "${CYAN}[*] Next steps:${NC}"
echo -e "${YELLOW}  1. Go to https://github.com/$USERNAME/$REPO_NAME${NC}"
echo -e "${YELLOW}  2. Add description and topics${NC}"
echo -e "${YELLOW}  3. Enable GitHub Pages in Settings > Pages${NC}"
echo -e "${YELLOW}  4. Share with the world!${NC}"
