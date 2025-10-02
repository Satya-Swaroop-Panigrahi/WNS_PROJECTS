import os
import tempfile
import logging
from typing import Optional
from gtts import gTTS
import io

logger = logging.getLogger(__name__)

class TTSService:
    def __init__(self):
        self.default_language = 'en'
        self.default_slow = False
    
    def text_to_speech(self, text: str, language: str = 'en', slow: bool = False) -> str:
        """Convert text to speech and return audio file path"""
        
        try:
            # Validate input
            if not text or len(text.strip()) == 0:
                raise ValueError("Text cannot be empty")
            
            if len(text) > 5000:
                text = text[:5000] + "..."
                logger.warning("Text truncated to 5000 characters for TTS")
            
            # Create gTTS object
            tts = gTTS(text=text, lang=language, slow=slow)
            
            # Create temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            temp_file.close()
            
            # Save audio to temporary file
            tts.save(temp_file.name)
            
            logger.info(f"TTS audio saved to: {temp_file.name}")
            return temp_file.name
            
        except Exception as e:
            logger.error(f"TTS error: {str(e)}")
            raise Exception(f"Text-to-speech conversion failed: {str(e)}")
    
    def get_audio_bytes(self, text: str, language: str = 'en', slow: bool = False) -> bytes:
        """Convert text to speech and return audio bytes"""
        
        try:
            # Validate input
            if not text or len(text.strip()) == 0:
                raise ValueError("Text cannot be empty")
            
            if len(text) > 5000:
                text = text[:5000] + "..."
                logger.warning("Text truncated to 5000 characters for TTS")
            
            # Create gTTS object
            tts = gTTS(text=text, lang=language, slow=slow)
            
            # Save to bytes buffer
            audio_buffer = io.BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0)
            
            return audio_buffer.getvalue()
            
        except Exception as e:
            logger.error(f"TTS bytes error: {str(e)}")
            raise Exception(f"Text-to-speech conversion failed: {str(e)}")
    
    def get_supported_languages(self) -> dict:
        """Get list of supported languages for TTS"""
        return {
            'en': 'English',
            'es': 'Spanish',
            'fr': 'French',
            'de': 'German',
            'it': 'Italian',
            'pt': 'Portuguese',
            'ru': 'Russian',
            'ja': 'Japanese',
            'ko': 'Korean',
            'zh': 'Chinese',
            'ar': 'Arabic',
            'hi': 'Hindi'
        }
    
    def validate_text_for_tts(self, text: str) -> tuple[bool, str]:
        """Validate text for TTS conversion"""
        
        if not text or len(text.strip()) == 0:
            return False, "Text cannot be empty"
        
        if len(text) > 5000:
            return False, "Text too long for TTS (max 5000 characters)"
        
        # Check for special characters that might cause issues
        problematic_chars = ['<', '>', '{', '}', '[', ']', '|', '\\', '/']
        for char in problematic_chars:
            if char in text:
                return False, f"Text contains problematic character: {char}"
        
        return True, "Valid text for TTS"
    
    def cleanup_temp_file(self, file_path: str):
        """Clean up temporary audio file"""
        try:
            if os.path.exists(file_path):
                os.unlink(file_path)
                logger.info(f"Cleaned up temporary file: {file_path}")
        except Exception as e:
            logger.error(f"Error cleaning up temporary file: {str(e)}")
