# Usage Guide

## Quick Start

### Start Web Server

```bash
python3 zphishing.py serve --host 0.0.0.0 --port 8080
```

### Interactive Shell

```bash
python3 zphishing.py shell
```

## Commands

### Campaigns

```bash
# List campaigns
python3 zphishing.py list-campaigns

# Create campaign
python3 zphishing.py create-campaign --name "Test" --template google

# Start campaign
python3 zphishing.py start-campaign CAMPAIGN_ID

# Stop campaign
python3 zphishing.py stop-campaign CAMPAIGN_ID
```

### Templates

```bash
# List templates
python3 zphishing.py list-templates

# Create template
python3 zphishing.py create-template --name "Custom" --html template.html
```

### AI Engine

```bash
# Generate template from URL
python3 zphishing.py ai-generate --url https://example.com/login

# Generate from description
python3 zphishing.py ai-generate --description "Bank login page" --platform banking
```

### Infrastructure

```bash
# Deploy to Docker
python3 zphishing.py deploy --provider docker

# Deploy to Kubernetes
python3 zphishing.py deploy --provider kubernetes

# Destroy infrastructure
python3 zphishing.py destroy --id DEPLOYMENT_ID
```

## API Usage

### Authentication

```bash
curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "password"}'
```

### Create Campaign

```bash
curl -X POST http://localhost:8080/api/campaigns \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{"name": "Test Campaign", "template": "google", "redirect_url": "https://www.google.com"}'
```

### Get Victims

```bash
curl -X GET http://localhost:8080/api/victims \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Web Dashboard

Access the web dashboard at `http://localhost:8080/dashboard`

## Shell Commands

```
apex> campaigns     - List all campaigns
apex> create        - Create new campaign
apex> start <id>    - Start campaign
apex> victims       - List victims
apex> templates     - List templates
apex> ai            - AI template generator
apex> evasion       - Evasion settings
apex> deploy        - Deploy infrastructure
apex> stats         - Show statistics
apex> exit          - Exit shell
```
