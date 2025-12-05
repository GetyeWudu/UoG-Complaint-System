#!/usr/bin/env bash

# Debug: Show what's available
echo "🔍 Checking gunicorn..."
which gunicorn || echo "❌ gunicorn not found in PATH"
python -m gunicorn --version || echo "❌ gunicorn module not found"

# Debug: Show Python environment
echo "🐍 Python version:"
python --version

echo "📦 Installed packages:"
pip list | grep gunicorn

# Start the server
echo "🚀 Starting gunicorn..."
gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 2 --timeout 120
