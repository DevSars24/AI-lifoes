from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from app.services.speech_service import speech_service
from app.models.schemas import AudioUploadRequest, TranscriptResponse
from loguru import logger

router = APIRouter(prefix="/api/speech", tags=["speech"])

@router.post("/upload-and-transcribe", response_model=TranscriptResponse)
async def upload_and_transcribe(audio_file: UploadFile = File(...)):
    """Upload audio file and get transcription via AssemblyAI."""
    # In prod: Save file to temp/S3, get URL
    temp_path = f"/tmp/{audio_file.filename}"
    with open(temp_path, "wb") as f:
        content = await audio_file.read()
        f.write(content)
    
    try:
        # Assume URL for AssemblyAI; in real, upload to S3 first
        # For demo, use local path if supported, or mock URL
        audio_url = "https://your-s3-bucket/audio.wav"  # Replace with actual upload logic
        transcript = await speech_service.transcribe_audio(audio_url)
        return transcript
    except Exception as e:
        logger.error(f"Transcription failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))