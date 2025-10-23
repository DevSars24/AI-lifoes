from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import config
from loguru import logger

client = AsyncIOMotorClient(config.MONGO_URI)
db = client.get_default_database()

notes_collection = db["notes"]
tasks_collection = db["tasks"]
transcripts_collection = db["transcripts"]

logger.info("MongoDB connected successfully")

async def close_db_connection():
    logger.info("Closing MongoDB connection...")
    client.close()
