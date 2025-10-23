from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.speech_service import speech_service
from app.models.schemas import TranscriptResponse
from loguru import logger
import aiofiles

router = APIRouter(prefix="/api/speech", tags=["speech"])

@router.post("/upload-and-transcribe", response_model=TranscriptResponse)
async def upload_and_transcribe(audio_file: UploadFile = File(...)):
    """Upload audio file and get transcription via AssemblyAI."""
    temp_path = f"/tmp/{audio_file.filename}"

    # Non-blocking write
    async with aiofiles.open(temp_path, "wb") as f:
        content = await audio_file.read()
        await f.write(content)

    try:
        # Replace with actual S3/public URL upload
        audio_url = "https://your-s3-bucket/audio.wav"
        transcript = await speech_service.transcribe_audio(audio_url)
        return transcript
    except Exception as e:
        logger.error(f"Transcription failed: {e}")
        raise HTTPException(status_code=500, detail="Transcription failed")
