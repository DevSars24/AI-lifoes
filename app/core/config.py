import os
from dotenv import load_dotenv
from loguru import logger

# Load environment variables from .env
load_dotenv()

class Config:
    MONGO_URI: str = os.getenv("MONGO_URI")
    if not MONGO_URI:
        logger.error("MONGO_URI not set in .env")
        raise ValueError("Please set MONGO_URI in .env")

    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")

    ASSEMBLYAI_API_KEY: str = os.getenv("ASSEMBLYAI_API_KEY")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")
    GOOGLE_CLOUD_PROJECT_ID: str = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    GOOGLE_CLOUD_CREDENTIALS_PATH: str = os.getenv("GOOGLE_CLOUD_CREDENTIALS_PATH")

    REQUIRED_KEYS = [MONGO_URI, ASSEMBLYAI_API_KEY, GEMINI_API_KEY, GOOGLE_CLOUD_PROJECT_ID]
    if any(not key for key in REQUIRED_KEYS):
        logger.error("Missing required config in .env")
        raise ValueError("Set all required keys in .env")

config = Config()
logger.info("Config loaded successfully")
