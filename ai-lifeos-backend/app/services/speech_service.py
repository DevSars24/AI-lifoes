import assemblyai as aai
from typing import Dict, Any
from app.core.config import config
from app.core.utils import get_redis_client, cache_result
from app.services.db_service import db_service
from app.models.schemas import TranscriptResponse
from app.models.mongo_models import TranscriptDoc
from loguru import logger
import asyncio

# Init AssemblyAI
aai.settings.api_key = config.ASSEMBLYAI_API_KEY

class SpeechService:
    @staticmethod
    async def transcribe_audio(audio_url: str) -> TranscriptResponse:
        """Transcribe audio using AssemblyAI with caching and error handling."""
        cache_key = f"transcript_{audio_url}"
        redis_client = None

        # Redis client setup
        try:
            redis_client = await get_redis_client()
        except Exception as e:
            logger.warning(f"Redis connection failed: {e}. Proceeding without cache.")

        # Check cache first
        if redis_client:
            try:
                cached = await redis_client.get(cache_key)
                if cached:
                    logger.info("Returning cached transcript")
                    return TranscriptResponse(**eval(cached))
            except Exception as e:
                logger.warning(f"Redis cache read failed: {e}")

        # AssemblyAI transcription
        try:
            config_obj = aai.TranscriptionConfig(audio_url=audio_url, language_code="en")
            transcript = aai.Transcriber().transcribe(config_obj)
        except Exception as e:
            logger.error(f"AssemblyAI transcription request failed: {e}")
            raise ValueError("Failed to start transcription service")

        # Poll until completion
        try:
            while transcript.status != aai.TranscriptStatus.completed:
                if transcript.status == aai.TranscriptStatus.error:
                    raise ValueError(f"Transcription error: {transcript.error}")
                await asyncio.sleep(1)
                transcript = aai.Transcriber().get_transcript(transcript.id)
        except Exception as e:
            logger.error(f"Error during transcription polling: {e}")
            raise ValueError("Transcription process failed")

        # Build response
        response = TranscriptResponse(
            transcript_id=transcript.id,
            text=transcript.text,
            confidence=transcript.confidence or 0.0,
            duration=transcript.audio_duration or 0.0
        )

        # Cache result
        if redis_client:
            try:
                await cache_result(redis_client, cache_key, str(response.dict()))
            except Exception as e:
                logger.warning(f"Redis cache write failed: {e}")

        # Store in DB
        try:
            doc = TranscriptDoc(**response.dict())
            await db_service.insert_transcript(doc)
        except Exception as e:
            logger.error(f"Database insert failed: {e}")

        logger.info(f"Transcribed audio successfully: {transcript.id}")
        return response

speech_service = SpeechService()
