#!/bin/bash
# stop.sh - Stop and cleanup the Real-time Log Processing Pipeline

set -e

echo "=========================================="
echo "Stopping Real-time Log Processing Pipeline"
echo "=========================================="
echo ""

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Error: Docker Compose is not installed."
    exit 1
fi

# Check if docker-compose.yml exists
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ Error: docker-compose.yml not found in current directory"
    exit 1
fi

echo "🛑 Stopping all services gracefully..."
docker-compose stop

echo "✓ All services stopped"
echo ""

# Ask if user wants to remove containers and volumes
read -p "Do you want to remove containers and volumes? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🗑️  Removing containers and volumes..."
    docker-compose down -v
    echo "✓ Cleanup complete"
else
    echo "⏸️  Containers remain available. Run 'docker-compose down' to remove them completely."
fi

echo ""
echo "Goodbye! 👋"
