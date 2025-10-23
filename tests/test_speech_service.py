import pytest
from unittest.mock import AsyncMock, patch
from app.services.speech_service import speech_service
from app.models.schemas import TranscriptResponse

@pytest.mark.asyncio
@patch("app.services.speech_service.get_redis_client")
@patch("app.services.speech_service.db_service.insert_transcript", new_callable=AsyncMock)
@patch("assemblyai.Transcriber.transcribe")
def test_transcribe_audio(mock_transcribe, mock_db, mock_redis):
    # Mock Redis client
    mock_redis.return_value.get = AsyncMock(return_value=None)
    mock_redis.return_value.setex = AsyncMock(return_value=None)

    # Mock AssemblyAI transcript
    mock_transcript = AsyncMock()
    mock_transcript.id = "123"
    mock_transcript.text = "Hello World"
    mock_transcript.status = "completed"
    mock_transcript.confidence = 0.95
    mock_transcript.audio_duration = 5.0
    mock_transcribe.return_value = mock_transcript

    # Run function
    response = asyncio.run(speech_service.transcribe_audio("fake_url"))

    assert isinstance(response, TranscriptResponse)
    assert response.text == "Hello World"
    assert response.confidence == 0.95
