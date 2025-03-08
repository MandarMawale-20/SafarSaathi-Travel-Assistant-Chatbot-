import os
import requests
from dotenv import load_dotenv

# Load API Key
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def get_gemini_response(prompt):
    url = "https://api.google.com/gemini/v1/chat"
    headers = {"Authorization": f"Bearer {GEMINI_API_KEY}"}
    payload = {"prompt": prompt}

    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        return response.json().get("response", "No response received")
    else:
        return f"Error: {response.status_code}, {response.text}"
