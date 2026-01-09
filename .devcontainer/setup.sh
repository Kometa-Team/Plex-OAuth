#!/bin/bash

# Dev container setup script
echo "🚀 Setting up Plex-OAuth development environment..."

# Install uv
echo "📦 Installing uv..."
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="/home/vscode/.cargo/bin:$PATH"

# Add uv to PATH for future sessions
echo 'export PATH="/home/vscode/.cargo/bin:$PATH"' >> ~/.bashrc

# Install project dependencies
echo "📚 Installing project dependencies..."
uv sync

# Create .env file from example if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    # Generate a random secret key
    SECRET_KEY=$(python3 -c 'import os; print(os.urandom(24).hex())')
    sed -i "s/your-secret-key-here-change-in-production/$SECRET_KEY/" .env
fi

echo "✅ Development environment ready!"
echo ""
echo "To start the Flask app, run:"
echo "  uv run python app.py"
echo ""
echo "The app will be available at http://localhost:8080"
