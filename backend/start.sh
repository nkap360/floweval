#!/bin/bash
# Production startup script for Flow Builder Backend

set -e

echo "================================================"
echo "  Flow Builder Backend - Starting..."
echo "================================================"

# Check required environment variables
REQUIRED_VARS=("GOOGLE_API_KEY" "SUPABASE_URL" "SUPABASE_KEY")

for var in "${REQUIRED_VARS[@]}"; do
    if [ -z "${!var}" ]; then
        echo "ERROR: Required environment variable $var is not set"
        exit 1
    fi
done

echo "✓ Environment variables validated"

# Create necessary directories (in case they don't exist)
mkdir -p /app/data /app/logs /app/.deepeval /app/.cache

# Verify flow_engine directory exists
if [ -d "/flow_engine/templates" ]; then
    FLOW_ENGINE_COUNT=$(find /flow_engine/templates -name "*.json" 2>/dev/null | wc -l)
    echo "✓ flow_engine found with $FLOW_ENGINE_COUNT template files"
else
    echo "✗ ERROR: flow_engine/templates directory not found at /flow_engine/templates"
    exit 1
fi

# Set HOME to a writable directory to avoid permission issues with cache dirs
export HOME=/app
export XDG_CACHE_HOME=/app/.cache
export XDG_DATA_HOME=/app/.cache

echo "✓ Directories validated"

# Run database migrations if needed
# python -m backend.migrations.run

echo "✓ Ready to start server"

# Set PYTHONPATH to root for package imports
export PYTHONPATH=/

# Start the application - run as package module from /app directory
exec python -m uvicorn app.main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --workers 1 \
    --log-level info \
    --access-log \
    --proxy-headers \
    --forwarded-allow-ips='*'
