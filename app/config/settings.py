from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    BACKEND_API_URL = os.getenv("BACKEND_API_URL", "http://127.0.0.1:8000/chat")
    ALLOWED_MODEL_NAMES = [
        # `llama3-70b-8192` was decommissioned, keep the replacement only
        "llama3-70b-8192",
        "llama-3.3-70b-versatile"
    ]

settings=Settings()