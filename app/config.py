import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    ERP_API_BASE_URL: str = os.getenv("ERP_API_BASE_URL", "http://localhost:8001/api/v1")
    LLM_API_KEY: str = os.getenv("LLM_API_KEY", "gsk_yahan_apni_asli_key_paste_karein_bina_quotes_ke_nahi")
    LLM_BASE_URL: str = os.getenv("LLM_BASE_URL", "https://api.groq.com/openai/v1")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "llama-3.1-8b-instant")

def get_settings():
    return Settings()