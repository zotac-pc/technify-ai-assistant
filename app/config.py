import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    ERP_API_BASE_URL: str = os.getenv("ERP_API_BASE_URL", "http://localhost:8001")
    LLM_API_KEY: str = os.getenv("LLM_API_KEY", "sk-placeholder")
    LLM_BASE_URL: str = os.getenv("LLM_BASE_URL", "https://openrouter.ai/api/v1")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "meta-llama/llama-3.2-3b-instruct:free")

def get_settings():
    return Settings()
