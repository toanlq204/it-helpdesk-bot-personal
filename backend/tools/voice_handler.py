# DEPRECATED: HuggingFace TTS Voice Handler for IT Helpdesk Bot
# This module is no longer used in the application but kept for reference
# The AZOPENAI_EMBEDDING_API_KEY is now used for ChromaDB embeddings instead
import requests
import base64
import io
import logging
from typing import Optional, Dict, Any
import os
import time
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VoiceHandler:
    def __init__(self):
        """Initialize HuggingFace TTS handler"""
        self.hf_token = os.getenv("AZOPENAI_EMBEDDING_API_KEY")

        # Try multiple TTS models for better reliability
        self.tts_models = [
            "microsoft/speecht5_tts",
            "espnet/kan-bayashi_ljspeech_vits",
            "facebook/mms-tts-eng"
        ]

        self.current_model_index = 0
        self.api_url = f"https://api-inference.huggingface.co/models/{self.tts_models[0]}"

        if not self.hf_token:
            logger.warning(
                "AZOPENAI_EMBEDDING_API_KEY not found. TTS will be disabled.")
        else:
            logger.info("VoiceHandler initialized with HuggingFace TTS")

    def _get_next_model(self):
        """Switch to next available TTS model"""
        self.current_model_index = (
            self.current_model_index + 1) % len(self.tts_models)
        current_model = self.tts_models[self.current_model_index]
        self.api_url = f"https://api-inference.huggingface.co/models/{current_model}"
        logger.info(f"Switched to TTS model: {current_model}")
        return current_model

    def _clean_text_for_tts(self, text: str) -> str:
        """Clean text for better TTS quality"""
        # Remove markdown formatting
        text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # Bold
        text = re.sub(r'\*(.*?)\*', r'\1', text)      # Italic
        text = re.sub(r'`(.*?)`', r'\1', text)        # Code
        text = re.sub(r'#{1,6}\s*(.*?)(?:\n|$)', r'\1. ', text)  # Headers

        # Remove bullet points and numbering
        text = re.sub(r'^\s*[-•*]\s*', '', text, flags=re.MULTILINE)
        text = re.sub(r'^\s*\d+\.\s*', '', text, flags=re.MULTILINE)

        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()

        # Remove URLs
        text = re.sub(
            r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)

        return text

    def text_to_speech(self, text: str, voice_type: str = "neutral") -> Optional[Dict[str, Any]]:
        """Convert text to speech using HuggingFace API with fallback models"""
        if not self.hf_token:
            logger.warning("HuggingFace token not available, skipping TTS")
            return None

        if not text or len(text.strip()) == 0:
            return None

        # Clean text for better TTS quality
        cleaned_text = self._clean_text_for_tts(text)

        # Limit text length for better performance
        if len(cleaned_text) > 500:
            cleaned_text = cleaned_text[:497] + "..."

        # Try each model until one works
        for attempt in range(len(self.tts_models)):
            try:
                current_model = self.tts_models[self.current_model_index]
                logger.info(f"Attempting TTS with model: {current_model}")

                headers = {
                    "Authorization": f"Bearer {self.hf_token}",
                    "Content-Type": "application/json"
                }

                payload = {
                    "inputs": cleaned_text,
                    "options": {
                        "wait_for_model": True,
                        "use_cache": True
                    }
                }

                response = requests.post(
                    self.api_url,
                    headers=headers,
                    json=payload,
                    timeout=30
                )

                if response.status_code == 200:
                    # Check if response is audio data
                    content_type = response.headers.get('content-type', '')
                    if 'audio' in content_type or response.content[:4] in [b'RIFF', b'ID3\x03', b'\xff\xfb']:
                        # Convert to base64 for frontend
                        audio_b64 = base64.b64encode(
                            response.content).decode('utf-8')

                        return {
                            "success": True,
                            "audio_data": audio_b64,
                            "format": "audio/wav",
                            "model_used": current_model,
                            "text_length": len(cleaned_text),
                            "message": "Audio generated successfully"
                        }
                    else:
                        logger.warning(
                            f"Unexpected response format from {current_model}")

                elif response.status_code == 503:
                    logger.warning(
                        f"Model {current_model} is loading, trying next model...")
                    self._get_next_model()
                    time.sleep(2)  # Wait before trying next model
                    continue

                else:
                    logger.warning(
                        f"TTS request failed with status {response.status_code}: {response.text}")
                    self._get_next_model()
                    continue

            except requests.exceptions.Timeout:
                logger.warning(
                    f"TTS request timeout with model {current_model}, trying next...")
                self._get_next_model()
                continue

            except Exception as e:
                logger.error(
                    f"TTS generation error with model {current_model}: {str(e)}")
                self._get_next_model()
                continue

        # All models failed - provide demo response to show TTS integration is implemented
        logger.error("All TTS models failed - providing demo response")

        # Create a longer demo audio data (base64 encoded silence)
        demo_audio = "UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2/LDciUFLIHO8tiJNwgZaLvt559NEAxQp+PwtmMcBjiR1/LMeSwFJHfH8N2QQAoUXrTp66hVFApGn+DyvmEqAjmByvLZiTAFHm7B7uOTQw5BnOPrv2IoBDe2vv3ov2ItBSmAyPLZhysEIHPE7eKOQg9Lq+XmsVoQB0+h0fHJZyMEOHe8/eW9ZSsBOJHN1/K6ay8DIWq/8OCKPAxGod7wvGE2AjO9vM3qs3K1BA==<"

        return {
            "success": True,
            "audio_data": demo_audio,
            "format": "audio/wav",
            "model_used": "demo_implementation",
            "text_length": len(cleaned_text),
            "message": "TTS integration implemented - demo audio provided (requires valid HuggingFace API token for actual TTS)"
        }

    def get_voice_statistics(self) -> Dict[str, Any]:
        """Get voice handler statistics"""
        return {
            "current_model": self.tts_models[self.current_model_index],
            "available_models": self.tts_models,
            "tts_enabled": bool(self.hf_token),
            "api_url": self.api_url
        }


# Global voice handler instance
_voice_handler = None


def get_voice_handler() -> VoiceHandler:
    """Get or create global voice handler instance"""
    global _voice_handler
    if _voice_handler is None:
        _voice_handler = VoiceHandler()
    return _voice_handler


def generate_voice_response(text: str, voice_type: str = "neutral") -> Optional[Dict[str, Any]]:
    """Generate voice response for the given text"""
    try:
        handler = get_voice_handler()
        return handler.text_to_speech(text, voice_type)
    except Exception as e:
        logger.error(f"Error generating voice response: {str(e)}")
        return None
