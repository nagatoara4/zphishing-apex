#!/bin/bash
# ZPHISHING APEX — Quick Deploy Script

set -e

echo "🚀 Deploying ZPHISHING APEX..."

# Build Docker image
echo "📦 Building Docker image..."
docker build -t zphishing-apex:latest .

# Start services
echo "🔄 Starting services..."
docker-compose up -d

echo "✅ Deployment complete!"
echo "🌐 Web UI: http://localhost:8080/dashboard"
echo "📊 API: http://localhost:8080/api"
echo ""
echo "To view logs: docker-compose logs -f"
echo "To stop: docker-compose down"
