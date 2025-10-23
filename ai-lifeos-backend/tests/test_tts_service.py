import pytest
from unittest.mock import patch, MagicMock
from app.services.tts_service import tts_service

def test_synthesize_speech():
    # Patch the client
    with patch("app.services.tts_service.client") as mock_client:
        mock_client.synthesize_speech.return_value.audio_content = b"audio bytes"
        audio = tts_service.synthesize_speech("Hello World")
        assert audio == b"audio bytes"
