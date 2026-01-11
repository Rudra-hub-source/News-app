#!/bin/bash

echo "Starting News Hub Application..."

# Kill any existing processes
pkill -f "python app.py" 2>/dev/null
sleep 1

# Start the application
cd /workspaces/News-app
export FLASK_APP=app.py
export FLASK_ENV=development

echo "Application starting on port 5000..."
echo "Access your app at: https://turbo-engine-v69xvg5j7v973x475-5000.app.github.dev/"

python app.py