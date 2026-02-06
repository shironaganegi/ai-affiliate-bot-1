import os
import requests
import json
from shared.utils import load_config

# Load configuration to ensure env vars are available
load_config()

def get_gemini_response(prompt, model_name, generation_config=None):
    """
    Sends a direct REST API request to Google Gemini.
    Handles authentication and JSON payload construction.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found.")
        return None

    # Determine endpoint based on model name (handling both simple and full names)
    # Ensure usage of v1beta endpoint which is currently most stable for these models
    if "models/" not in model_name:
        model_name = f"models/{model_name}"
        
    url = f"https://generativelanguage.googleapis.com/v1beta/{model_name}:generateContent?key={api_key}"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    
    if generation_config:
        payload["generationConfig"] = generation_config

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        
        if response.status_code != 200:
            print(f"API Error ({response.status_code}): {response.text}")
            return None
            
        return response.json()
        
    except Exception as e:
        print(f"Request failed: {e}")
        return None
