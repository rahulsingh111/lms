#!/bin/sh

URL="${HEALTH_URL:-http://localhost:5000/health}"

echo "Checking $URL..."

if curl --fail --silent --show-error "$URL" > /dev/null; then
    echo "Health check passed!"
    exit 0
else
    echo "Health check failed!"
    exit 1
fi