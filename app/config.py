import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    ERP_API_BASE_URL: str = "http://localhost:8001"
    LLM_API_KEY: str = os.getenv("LLM_API_KEY")
    LLM_BASE_URL: str = "https://api.groq.com/openai/v1"
    LLM_MODEL: str = "llama-3.1-8b-instant"

def get_settings():
    return Settings()