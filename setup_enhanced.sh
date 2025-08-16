#!/bin/bash

# IT Helpdesk Bot - Enhanced Features Installation Script
# This script installs the new dependencies and sets up the enhanced features

echo "🤖 Setting up Enhanced IT Helpdesk Bot..."

# Check if Python virtual environment exists
if [ ! -d ".venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Install Python dependencies
echo "📚 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js to continue."
    exit 1
fi

# Install frontend dependencies
echo "🎨 Installing frontend dependencies..."
cd frontend
npm install
cd ..

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p chromadb_data
mkdir -p logs

# Copy environment template if .env doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp env.template .env
    echo "⚠️  Please edit .env file with your actual API keys and configuration"
fi

echo "✅ Enhanced IT Helpdesk Bot setup complete!"
echo ""
echo "🚀 Next steps:"
echo "1. Edit .env file with your Azure OpenAI and HuggingFace API keys"
echo "2. Run the backend: .venv/bin/uvicorn backend.main:app --reload --port 8000"
echo "3. Run the frontend: cd frontend && npm run dev"
echo ""
echo "🌟 New Features Available:"
echo "- ChromaDB Knowledge Base"
echo "- HuggingFace Text-to-Speech"
echo "- Enhanced Session Management"
echo "- Voice Response Capabilities"
