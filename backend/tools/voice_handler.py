# HuggingFace TTS Voice Handler for IT Helpdesk Bot
import requests
import base64
import io
import logging
from typing import Optional, Dict, Any
import os
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VoiceHandler:
    def __init__(self):
        """Initialize HuggingFace TTS handler"""
        self.hf_token = os.getenv("HUGGINGFACE_API_TOKEN")
        self.tts_model = "microsoft/speecht5_tts"  # Using SpeechT5 as it's reliable
        self.api_url = f"https://api-inference.huggingface.co/models/{self.tts_model}"

        if not self.hf_token:
            logger.warning(
                "HUGGINGFACE_API_TOKEN not found. TTS will be disabled.")

        logger.info("VoiceHandler initialized")

    def text_to_speech(self, text: str, voice_type: str = "neutral") -> Optional[Dict[str, Any]]:
        """Convert text to speech using HuggingFace API"""
        if not self.hf_token:
            logger.warning("HuggingFace token not available, skipping TTS")
            return None

        if not text or len(text.strip()) == 0:
            return None

        # Clean text for better TTS quality
        cleaned_text = self._clean_text_for_tts(text)

        # Limit text length for better performance
        if len(cleaned_text) > 500:
            cleaned_text = cleaned_text[:500] + "..."

        try:
            headers = {
                "Authorization": f"Bearer {self.hf_token}",
                "Content-Type": "application/json"
            }

            payload = {
                "inputs": cleaned_text,
                "parameters": {
                    "voice": voice_type
                }
            }

            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                # Convert audio bytes to base64 for JSON transport
                audio_bytes = response.content
                audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')

                return {
                    "audio_data": audio_base64,
                    "format": "wav",
                    # Rough estimate
                    "duration_estimate": len(cleaned_text) * 0.1,
                    "text_length": len(cleaned_text),
                    "timestamp": datetime.now().isoformat()
                }

            else:
                logger.error(
                    f"TTS API error: {response.status_code} - {response.text}")
                return None

        except requests.exceptions.Timeout:
            logger.error("TTS request timed out")
            return None
        except Exception as e:
            logger.error(f"Error in text_to_speech: {str(e)}")
            return None

    def _clean_text_for_tts(self, text: str) -> str:
        """Clean text for better TTS quality"""
        # Remove markdown formatting
        cleaned = text.replace("**", "").replace("*", "")
        cleaned = cleaned.replace("###", "").replace("##", "").replace("#", "")
        cleaned = cleaned.replace("`", "")

        # Remove emoji patterns
        import re
        cleaned = re.sub(r':[a-z_]+:', '', cleaned)
        cleaned = re.sub(r'[🔧🎯🛠️💡📚❓💻📋📄]', '', cleaned)

        # Replace bullet points with natural speech
        cleaned = cleaned.replace("- ", "First, ")
        cleaned = cleaned.replace("• ", "Next, ")

        # Clean up whitespace
        cleaned = ' '.join(cleaned.split())

        return cleaned.strip()

    def is_available(self) -> bool:
        """Check if TTS service is available"""
        return self.hf_token is not None

# Alternative: Use local TTS if HuggingFace is not available


class LocalVoiceHandler:
    def __init__(self):
        """Initialize local TTS handler as fallback"""
        self.available = False
        try:
            import pyttsx3
            self.engine = pyttsx3.init()
            self.available = True
            logger.info("Local TTS engine initialized")
        except ImportError:
            logger.info("pyttsx3 not available, local TTS disabled")

    def text_to_speech(self, text: str, voice_type: str = "neutral") -> Optional[Dict[str, Any]]:
        """Convert text to speech using local TTS (fallback)"""
        if not self.available:
            return None

        try:
            # This would save to a temporary file and return base64
            # For now, just return a placeholder
            return {
                "audio_data": "",
                "format": "wav",
                "duration_estimate": len(text) * 0.1,
                "text_length": len(text),
                "timestamp": datetime.now().isoformat(),
                "source": "local_tts"
            }
        except Exception as e:
            logger.error(f"Error in local TTS: {str(e)}")
            return None


# Global instances
_voice_handler = None
_local_voice_handler = None


def get_voice_handler() -> VoiceHandler:
    """Get or create global voice handler instance"""
    global _voice_handler
    if _voice_handler is None:
        _voice_handler = VoiceHandler()
    return _voice_handler


def get_local_voice_handler() -> LocalVoiceHandler:
    """Get or create local voice handler instance"""
    global _local_voice_handler
    if _local_voice_handler is None:
        _local_voice_handler = LocalVoiceHandler()
    return _local_voice_handler


def generate_voice_response(text: str) -> Optional[Dict[str, Any]]:
    """Generate voice response, trying HuggingFace first, then local TTS"""
    # Try HuggingFace TTS first
    voice_handler = get_voice_handler()
    if voice_handler.is_available():
        result = voice_handler.text_to_speech(text)
        if result:
            result["source"] = "huggingface"
            return result

    # Fallback to local TTS
    local_handler = get_local_voice_handler()
    if local_handler.available:
        result = local_handler.text_to_speech(text)
        if result:
            return result

    logger.info("No TTS service available")
    return None
