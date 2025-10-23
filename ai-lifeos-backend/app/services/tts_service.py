from google.cloud import texttospeech
from app.core.config import config
from loguru import logger
import os

# Setup Google Cloud TTS
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = config.GOOGLE_CLOUD_CREDENTIALS_PATH

try:
    client = texttospeech.TextToSpeechClient()
except Exception as e:
    logger.error(f"Failed to initialize Google TTS client: {e}")
    client = None

class TTSService:
    @staticmethod
    def synthesize_speech(text: str, voice_name: str = "en-US-Standard-A") -> bytes:
        if not client:
            raise RuntimeError("TTS client not initialized")

        try:
            synthesis_input = texttospeech.SynthesisInput(text=text)
            voice = texttospeech.VoiceSelectionParams(language_code="en-US", name=voice_name)
            audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.LINEAR16)
            response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
            logger.info(f"Synthesized speech for: {text[:50]}...")
            return response.audio_content
        except Exception as e:
            logger.error(f"TTS synthesis failed: {e}")
            raise RuntimeError("Failed to synthesize speech")

tts_service = TTSService()
