"""
LLM Client wrappers for OpenAI and Google Gemini.
"""

from abc import ABC, abstractmethod
import os
import time
import logging
import json
from typing import Optional, Dict

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
        self.total_cost = 0.0
        self.total_tokens = 0
        
    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Generate text from prompt."""
        pass
        
    def get_cost(self) -> float:
        """Get accumulated cost."""
        return self.total_cost
        
    def _track_usage(self, input_tokens: int, output_tokens: int, cost: float):
        """Update usage stats."""
        self.total_tokens += (input_tokens + output_tokens)
        self.total_cost += cost
        logger.debug(f"Cost += ${cost:.4f} | Total: ${self.total_cost:.4f}")

class OpenAIClient(BaseLLMClient):
    """Client for OpenAI API."""
    
    # Pricing (approximate for gpt-4o as of late 2024 / 2025)
    # $5.00 / 1M input tokens
    # $15.00 / 1M output tokens
    INPUT_PRICE_PER_M = 5.00
    OUTPUT_PRICE_PER_M = 15.00
    
    def __init__(self, config: LLMConfig):
        super().__init__(config)
        if openai is None:
            raise ImportError("openai package is not installed.")
        
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set.")
            
        self.client = openai.OpenAI(api_key=api_key)
        
    def generate(self, prompt: str) -> str:
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.config.model_name,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=self.config.temperature,
                    max_tokens=self.config.max_tokens
                )
                
                # Track Usage
                usage = response.usage
                if usage:
                    cost = (
                        (usage.prompt_tokens / 1_000_000 * self.INPUT_PRICE_PER_M) +
                        (usage.completion_tokens / 1_000_000 * self.OUTPUT_PRICE_PER_M)
                    )
                    self._track_usage(usage.prompt_tokens, usage.completion_tokens, cost)
                
                return response.choices[0].message.content.strip()
                
            except Exception as e:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    logger.warning(f"OpenAI API error: {e}. Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    logger.error(f"OpenAI API error: {e}")
                    raise

class GeminiClient(BaseLLMClient):
    """Client for Google Gemini API."""
    
    # Pricing (approximate for Gemini Pro)
    # Input: $0.125 / 1M chars (~$0.50 / 1M tokens)
    # Output: $0.375 / 1M chars (~$1.50 / 1M tokens)
    # Simplified token estimation
    INPUT_PRICE_PER_M = 0.50
    OUTPUT_PRICE_PER_M = 1.50
    
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
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.model.generate_content(
                    prompt,
                    generation_config=self.generation_config
                )
                
                # Estimate Usage (Gemini doesn't always return token counts easily in basic response)
                # Rough est: 1 token ~= 4 chars
                input_chars = len(prompt)
                output_chars = len(response.text)
                
                input_tokens = input_chars // 4
                output_tokens = output_chars // 4
                
                cost = (
                    (input_tokens / 1_000_000 * self.INPUT_PRICE_PER_M) +
                    (output_tokens / 1_000_000 * self.OUTPUT_PRICE_PER_M)
                )
                self._track_usage(input_tokens, output_tokens, cost)

                return response.text.strip()
            except Exception as e:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    logger.warning(f"Gemini API error: {e}. Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    logger.error(f"Gemini API error: {e}")
                    raise

class OpenRouterClient(BaseLLMClient):
    """Client for OpenRouter API."""
    
    def __init__(self, config: LLMConfig):
        super().__init__(config)
        if openai is None:
            raise ImportError("openai package is not installed (required for OpenRouter).")
            
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY environment variable not set.")
            
        # OpenRouter uses OpenAI SDK with custom base URL
        self.client = openai.OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
            default_headers={
                "HTTP-Referer": "https://github.com/jonnabio/xai-eval-framework",
                "X-Title": "XAI Eval Framework",
            }
        )
        
    def generate(self, prompt: str) -> str:
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.config.model_name,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=self.config.temperature,
                    max_tokens=self.config.max_tokens
                )
                
                # Track Usage
                usage = response.usage
                if usage:
                    # Cost is variable per model on OpenRouter. 
                    # Defaulting to 0 for now as we can't easily know the price without lookup.
                    # Or we could assume a default if we knew the model.
                    # For now, just track tokens.
                    cost = 0.0 
                    self._track_usage(usage.prompt_tokens, usage.completion_tokens, cost)
                
                return response.choices[0].message.content.strip()
                
            except Exception as e:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    logger.warning(f"OpenRouter API error: {e}. Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    logger.error(f"OpenRouter API error: {e}")
                    raise

class DummyClient(BaseLLMClient):
    """Dummy client for testing/dry-runs."""
    
    def generate(self, prompt: str) -> str:
        # Return a valid JSON response to test the parsing logic
        return json.dumps({
            "coherence": 5,
            "faithfulness": 5,
            "usefulness": 5,
            "reasoning": "This is a dummy response for testing purposes."
        })

class LLMClientFactory:
    """Factory for creating LLM clients."""
    
    @staticmethod
    def create(config: LLMConfig) -> BaseLLMClient:
        if config.provider == "openai":
            return OpenAIClient(config)
        elif config.provider == "gemini":
            return GeminiClient(config)
        elif config.provider == "openrouter":
            return OpenRouterClient(config)
        elif config.provider == "dummy":
            return DummyClient(config)
        else:
            raise ValueError(f"Unsupported LLM provider: {config.provider}")
