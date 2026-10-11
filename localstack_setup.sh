#!/bin/bash
set -e

echo "=================================================="
echo "🚀 Starting Aero-Match LocalStack & SAM Environment"
echo "=================================================="

# 1. Check if LocalStack is running
if ! docker ps | grep -q localstack; then
    echo "Starting LocalStack via Docker Compose / CLI..."
    docker run --rm -d -p 4566:4566 -p 4510-4559:4510-4559 --name localstack-main localstack/localstack
    echo "Waiting for LocalStack to warm up..."
    sleep 5
else
    echo "✅ LocalStack is already running."
fi

# 2. Build SAM Application locally
echo "Building SAM application..."
sam build --template-file template.yaml

echo "=================================================="
echo "✨ Local Stack Deployment & Testing Ready!"
echo "=================================================="
echo "To run locally via LocalStack & SAM, execute:"
echo "   sam local start-api --warm-containers EAGER --skip-pull-image"
echo ""
echo "To test your endpoint via curl, run:"
echo "   curl -G \"http://127.0.0.1:3000/diagnose\" --data-urlencode \"symptoms=My eyes are burning and I have a headache\""
