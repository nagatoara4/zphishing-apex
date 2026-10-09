#!/bin/bash
# ZPHISHING APEX — Backup Script

set -e

BACKUP_DIR="backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

echo "💾 Creating backup..."

# Backup database
pg_dump -U zphishing zphishing_db > "$BACKUP_DIR/database.sql" 2>/dev/null || echo "Database backup skipped"

# Backup config
cp .env "$BACKUP_DIR/" 2>/dev/null || echo "No .env file"
cp config.yaml "$BACKUP_DIR/" 2>/dev/null || echo "No config.yaml"

# Backup templates
cp -r templates "$BACKUP_DIR/" 2>/dev/null || echo "No templates"

# Backup logs
cp -r logs "$BACKUP_DIR/" 2>/dev/null || echo "No logs"

# Create archive
tar -czf "$BACKUP_DIR.tar.gz" -C backups "$(basename $BACKUP_DIR)"
rm -rf "$BACKUP_DIR"

echo "✅ Backup created: $BACKUP_DIR.tar.gz"
