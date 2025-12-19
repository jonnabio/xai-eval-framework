"""
LLM Client wrappers for OpenAI and Google Gemini.
"""

from abc import ABC, abstractmethod
import os
import logging
from typing import Optional

# Import official SDKs (assuming they are installed/will be mocked)
# We use conditional imports or assume existence based on requirements
try:
    import openai
except ImportError:
    openai = None

try:
    import google.generativeai as genai
except ImportError:
    genai = None

from src.experiment.config import LLMConfig

logger = logging.getLogger(__name__)

class BaseLLMClient(ABC):
    """Abstract base class for LLM clients."""
    
    def __init__(self, config: LLMConfig):
        self.config = config
        
    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Generate text from prompt."""
        pass
        
    def get_cost(self) -> float:
        """Get accumulated cost (if tracked)."""
        return 0.0

class OpenAIClient(BaseLLMClient):
    """Client for OpenAI API."""
    
    def __init__(self, config: LLMConfig):
        super().__init__(config)
        if openai is None:
            raise ImportError("openai package is not installed.")
        
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set.")
            
        self.client = openai.OpenAI(api_key=api_key)
        
    def generate(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.config.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise

class GeminiClient(BaseLLMClient):
    """Client for Google Gemini API."""
    
    def __init__(self, config: LLMConfig):
        super().__init__(config)
        if genai is None:
            raise ImportError("google-generativeai package is not installed.")
            
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set.")
            
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(self.config.model_name)
        self.generation_config = genai.types.GenerationConfig(
            temperature=self.config.temperature,
            max_output_tokens=self.config.max_tokens
        )
        
    def generate(self, prompt: str) -> str:
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=self.generation_config
            )
            return response.text.strip()
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            raise

class LLMClientFactory:
    """Factory for creating LLM clients."""
    
    @staticmethod
    def create(config: LLMConfig) -> BaseLLMClient:
        if config.provider == "openai":
            return OpenAIClient(config)
        elif config.provider == "gemini":
            return GeminiClient(config)
        else:
            raise ValueError(f"Unsupported LLM provider: {config.provider}")
