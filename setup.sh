#!/bin/bash
# Check if virtual environment exists
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "Created .env file. Please update it with your API keys."
fi

echo "Environment setup complete. Virtual environment is activated."