"""Application configuration using environment variables"""
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """Application settings loaded from environment variables"""
    CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY", "")
    MODEL_NAME = os.getenv("MODEL_NAME", "claude-3-opus-20240229")
    APP_ENV = os.getenv("APP_ENV", "development")
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"

settings = Settings()