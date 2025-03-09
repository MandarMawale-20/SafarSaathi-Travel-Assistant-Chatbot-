import os
import requests
import google.generativeai as genai
from dotenv import load_dotenv

# Load API Key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")


# genai.configure(api_key=api_key)
# models = genai.list_models()

# for model in models:
#     print(model.name)  # List all available models

def get_gemini_response(prompt):
    url = "https://api.google.com/gemini/v1/chat"
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {"prompt": prompt}

    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        return response.json().get("response", "No response received")
    else:
        return f"Error: {response.status_code}, {response.text}"


