import google.generativeai as genai
import logging
from shared.config import config
import time

logger = logging.getLogger(__name__)

class LLMClient:
    def __init__(self):
        if not config.GEMINI_API_KEY:
            logger.error("GEMINI_API_KEY is missing!")
            raise ValueError("GEMINI_API_KEY is not set.")
        
        genai.configure(api_key=config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-2.0-flash')

    def generate_content(self, prompt: str) -> str:
        """
        Generates content using Gemini with exponential backoff.
        """
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.model.generate_content(prompt)
                return response.text
            except Exception as e:
                wait_time = 2 ** attempt
                logger.warning(f"Gemini API Error (Attempt {attempt+1}/{max_retries}): {e}. Retrying in {wait_time}s...")
                time.sleep(wait_time)
        
        logger.error("All Gemini API retries failed.")
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
