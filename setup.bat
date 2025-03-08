@echo off
:: Check if virtual environment exists
if not exist venv (
    python -m venv venv
)

:: Activate virtual environment
call venv\Scripts\activate

:: Install setuptools first to avoid distutils error in Python 3.12
pip install --upgrade setuptools

:: Install dependencies
pip install -r requirements.txt

:: Create .env if it doesn't exist
if not exist .env (
    copy .env.example .env
    echo Created .env file. Please update it with your API keys.
)

echo Environment setup complete. Virtual environment is activated.