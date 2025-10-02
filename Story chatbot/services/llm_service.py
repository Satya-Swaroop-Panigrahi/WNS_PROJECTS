import os
import logging
from typing import Dict, Any
from groq import Groq
import google.generativeai as genai
from openai import OpenAI
from config import Config

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        self.groq_client = None
        self.openai_client = None
        
        # Initialize Groq
        if Config.GROQ_API_KEY:
            self.groq_client = Groq(api_key=Config.GROQ_API_KEY)
        
        # Initialize OpenAI
        if Config.OPENAI_API_KEY:
            self.openai_client = OpenAI(api_key=Config.OPENAI_API_KEY)
        
        # Initialize Gemini
        if Config.GOOGLE_API_KEY:
            genai.configure(api_key=Config.GOOGLE_API_KEY)
    
    def generate_content(self, prompt: str, model_provider: str, model_name: str, 
                        content_type: str, genre: str = "General", age_group: str = "Adult (26-50)",
                        temperature: float = 0.7, max_tokens: int = 500) -> Dict[str, Any]:
        """Generate content using the specified LLM"""
        
        # Create system prompt based on content type and parameters
        system_prompt = self._create_system_prompt(content_type, genre, age_group)
        
        try:
            if model_provider == "groq":
                return self._generate_with_groq(system_prompt, prompt, model_name, temperature, max_tokens)
            elif model_provider == "openai":
                return self._generate_with_openai(system_prompt, prompt, model_name, temperature, max_tokens)
            elif model_provider == "gemini":
                return self._generate_with_gemini(system_prompt, prompt, model_name, temperature, max_tokens)
            else:
                raise ValueError(f"Unsupported model provider: {model_provider}")
                
        except Exception as e:
            logger.error(f"Error generating content with {model_provider}: {str(e)}")
            return {
                "error": f"Model currently unavailable. Please switch to a different model or try later. Error: {str(e)}",
                "success": False
            }
    
    def _create_system_prompt(self, content_type: str, genre: str, age_group: str) -> str:
        """Create system prompt based on content type and parameters"""
        
        base_prompt = f"""You are a creative AI assistant that generates {content_type.lower()} content.
        
        Guidelines:
        - Content should be appropriate for {age_group}
        - Genre: {genre}
        - Avoid any content that could be harmful, offensive, or inappropriate
        - Be creative, engaging, and original
        - Respect all religions, cultures, and backgrounds equally
        """
        
        if content_type.lower() == "story":
            base_prompt += """
            - Create engaging stories with clear characters, setting, and plot
            - Include dialogue and descriptive language
            - End with a satisfying conclusion
            """
        elif content_type.lower() == "joke":
            base_prompt += """
            - Create clean, funny jokes and puns
            - Avoid offensive humor or stereotypes
            - Make jokes that appeal to a broad audience
            """
        elif content_type.lower() == "chat":
            base_prompt += """
            - Provide helpful, informative responses
            - Be conversational and friendly
            - Ask follow-up questions when appropriate
            """
        
        return base_prompt
    
    def _generate_with_groq(self, system_prompt: str, user_prompt: str, 
                           model_name: str, temperature: float, max_tokens: int) -> Dict[str, Any]:
        """Generate content using Groq API"""
        if not self.groq_client:
            raise Exception("Groq client not initialized. Please check your API key.")
        
        if model_name not in Config.GROQ_MODELS:
            raise Exception(f"Model {model_name} not available in Groq")
        
        try:
            response = self.groq_client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return {
                "content": response.choices[0].message.content,
                "model_used": model_name,
                "provider": "groq",
                "success": True
            }
        except Exception as e:
            raise Exception(f"Groq API error: {str(e)}")
    
    def _generate_with_openai(self, system_prompt: str, user_prompt: str, 
                             model_name: str, temperature: float, max_tokens: int) -> Dict[str, Any]:
        """Generate content using OpenAI API"""
        if not self.openai_client:
            raise Exception("OpenAI client not initialized. Please check your API key.")
        
        if model_name not in Config.OPENAI_MODELS:
            raise Exception(f"Model {model_name} not available in OpenAI")
        
        try:
            response = self.openai_client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return {
                "content": response.choices[0].message.content,
                "model_used": model_name,
                "provider": "openai",
                "success": True
            }
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
    
    def _generate_with_gemini(self, system_prompt: str, user_prompt: str, 
                             model_name: str, temperature: float, max_tokens: int) -> Dict[str, Any]:
        """Generate content using Gemini API"""
        if not Config.GOOGLE_API_KEY:
            raise Exception("Gemini API key not configured")
        
        if model_name not in Config.GEMINI_MODELS:
            raise Exception(f"Model {model_name} not available in Gemini")
        
        try:
            # Use the model name directly from config (free tier models only)
            actual_model = model_name
            
            model = genai.GenerativeModel(actual_model)
            
            # Combine system and user prompts for Gemini
            full_prompt = f"{system_prompt}\n\nUser Request: {user_prompt}"
            
            generation_config = genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens
            )
            
            response = model.generate_content(
                full_prompt,
                generation_config=generation_config
            )
            
            return {
                "content": response.text,
                "model_used": actual_model,
                "provider": "gemini",
                "success": True
            }
        except Exception as e:
            # Provide helpful error message for Gemini API issues
            error_msg = str(e)
            if "404" in error_msg or "not found" in error_msg:
                raise Exception("Gemini models are currently unavailable due to API changes. Please use Groq models instead.")
            else:
                raise Exception(f"Gemini API error: {error_msg}")
