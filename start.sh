#!/bin/bash
# start.sh - Start the Real-time Log Processing Pipeline

set -e

echo "=========================================="
echo "Real-time Log Processing Pipeline"
echo "=========================================="
echo ""

# Check if Docker and Docker Compose are installed
if ! command -v docker &> /dev/null; then
    echo "❌ Error: Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Error: Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✓ Docker and Docker Compose are installed"
echo ""

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📋 Creating .env file from .env.example..."
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "✓ .env file created"
    else
        echo "⚠️  .env.example not found, using defaults"
    fi
else
    echo "✓ .env file exists"
fi

echo ""
echo "🚀 Starting services..."
echo ""

# Build and start services
docker-compose up --build

echo ""
echo "✓ All services started successfully!"
echo ""
echo "Next steps:"
echo "  1. Wait for services to be healthy (check docker-compose ps)"
echo "  2. In another terminal, run: docker-compose exec consumer tail -f /data/processed_errors_warnings.jsonl"
echo "  3. To stop services: docker-compose down"
echo ""
