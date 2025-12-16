#!/bin/bash

# Quick Start Script for Portfolio Generator

echo "🚀 Portfolio Generator - Quick Start"
echo "====================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

echo "🔌 Activating virtual environment..."
source venv/bin/activate

echo "📚 Installing dependencies..."
pip install -q -r requirements.txt

# Check if config.properties exists
if [ ! -f "config.properties" ]; then
    echo "⚙️  Creating config.properties file..."
    cp config.properties.example config.properties
    echo ""
    echo "⚠️  IMPORTANT: Please edit config.properties and add your GEMINI_API_KEY"
    echo "   Get your API key from: https://makersuite.google.com/app/apikey"
    echo ""
fi

# Check if migrations are needed
if [ ! -f "db.sqlite3" ]; then
    echo "🗄️  Running database migrations..."
    python3 manage.py makemigrations
    python3 manage.py migrate
    
    echo "📋 Initializing templates..."
    python3 manage.py init_templates
    
    echo ""
    echo "👤 Create a superuser? (for admin access) [y/N]"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        python3 manage.py createsuperuser
    fi
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start the server, run:"
echo "  python3 manage.py runserver"
echo ""
echo "Then visit: http://127.0.0.1:8000/"
echo ""
