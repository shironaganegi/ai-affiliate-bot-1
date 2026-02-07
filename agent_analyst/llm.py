from google import genai
from google.genai import types
import logging
from shared.config import config
import time

logger = logging.getLogger(__name__)

class LLMClient:
    def __init__(self):
        if not config.GEMINI_API_KEY:
            logger.error("GEMINI_API_KEY is missing!")
            raise ValueError("GEMINI_API_KEY is not set.")
        
        # Initialize the new GenAI client
        self.client = genai.Client(api_key=config.GEMINI_API_KEY)
        
        # Priority list of models to try
        self.models_to_try = [
            'gemini-2.0-flash',
            'gemini-1.5-flash',
            'gemini-1.5-pro'
        ]

    def generate_content(self, prompt: str) -> str:
        """
        Generates content using Gemini with exponential backoff and model fallback.
        Uses the new google-genai SDK.
        """
        for model_name in self.models_to_try:
            logger.info(f"Attempting valid generation with model: {model_name}")
            
            # Retry loop for a specific model
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    # New SDK call format
                    response = self.client.models.generate_content(
                        model=model_name,
                        contents=prompt
                    )
                    
                    if response and response.text:
                        return response.text
                        
                except Exception as e:
                    error_msg = str(e)
                    wait_time = 2 ** (attempt + 2) # Start at 4s
                    
                    # Log the error details
                    logger.warning(f"Gemini API Error ({model_name} - Attempt {attempt+1}): {error_msg}")

                    # Detect 429 Rate Limit (Quota Exceeded)
                    if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg or "quota" in error_msg.lower():
                        logger.warning(f"Rate Limit hit for {model_name}. Switching to next model...")
                        time.sleep(5) # Short pause before switching
                        break # Break retry loop to try next model
                    
                    # Detect Server Errors
                    if "500" in error_msg or "503" in error_msg:
                         logger.warning(f"Server Error ({model_name}). Retrying in {wait_time}s...")
                         time.sleep(wait_time)
                         continue

                    # For other errors, wait and retry
                    time.sleep(wait_time)
            
            # If we break or finish retries without return, loop continues to next model

        logger.error("All Gemini models and retries failed.")
        return ""

    def load_prompt(self, filename: str) -> str:
        try:
            with open(filename, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            logger.error(f"Prompt file not found: {filename}")
            return ""

# Singleton
llm_client = LLMClient()
