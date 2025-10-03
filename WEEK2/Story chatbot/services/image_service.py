import os
import requests
import logging
from typing import Optional
from config import Config

logger = logging.getLogger(__name__)

class ImageService:
    def __init__(self):
        self.openai_api_key = Config.OPENAI_API_KEY
    
    def generate_image(self, prompt: str, size: str = "1024x1024", quality: str = "standard") -> str:
        """Generate image using OpenAI DALL-E API"""
        
        if not self.openai_api_key:
            logger.warning("OpenAI API key not configured for image generation")
            placeholder_url = self._get_placeholder_image_url()
            logger.info(f"Returning placeholder URL: {placeholder_url}")
            return placeholder_url
        
        try:
            headers = {
                'Authorization': f'Bearer {self.openai_api_key}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'model': 'dall-e-3',
                'prompt': prompt,
                'size': size,
                'quality': quality,
                'n': 1
            }
            
            response = requests.post(
                'https://api.openai.com/v1/images/generations',
                headers=headers,
                json=data
            )
            
            response.raise_for_status()
            result = response.json()
            
            if 'data' in result and len(result['data']) > 0:
                return result['data'][0]['url']
            else:
                logger.error("No image URL returned from OpenAI")
                return self._get_placeholder_image_url()
                
        except requests.RequestException as e:
            logger.error(f"OpenAI API error for image generation: {str(e)}")
            return self._get_placeholder_image_url()
        except Exception as e:
            logger.error(f"Image generation error: {str(e)}")
            return self._get_placeholder_image_url()
    
    def _get_placeholder_image_url(self) -> str:
        """Return a placeholder image URL when image generation fails"""
        # Using a placeholder service
        return "https://via.placeholder.com/1024x1024/4A90E2/FFFFFF?text=Image+Generation+Unavailable"
    
    def download_image(self, image_url: str, save_path: str) -> bool:
        """Download image from URL to local path"""
        try:
            response = requests.get(image_url, timeout=30)
            response.raise_for_status()
            
            with open(save_path, 'wb') as f:
                f.write(response.content)
            
            return True
            
        except Exception as e:
            logger.error(f"Error downloading image: {str(e)}")
            return False
    
    def validate_image_prompt(self, prompt: str) -> tuple[bool, str]:
        """Validate image generation prompt for safety and appropriateness"""
        
        # Basic length check
        if len(prompt) < 10:
            return False, "Prompt too short"
        
        if len(prompt) > 1000:
            return False, "Prompt too long"
        
        # Check for inappropriate content
        inappropriate_keywords = [
            'nude', 'naked', 'explicit', 'sexual', 'adult',
            'violence', 'blood', 'gore', 'weapon', 'kill'
        ]
        
        prompt_lower = prompt.lower()
        for keyword in inappropriate_keywords:
            if keyword in prompt_lower:
                return False, f"Inappropriate content detected: {keyword}"
        
        return True, "Valid prompt"
