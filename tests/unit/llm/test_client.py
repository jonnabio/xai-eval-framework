"""Unit tests for LLM client wrapper."""

import pytest
from unittest.mock import patch, MagicMock
import os
from src.experiment.config import LLMConfig
from src.llm.client import LLMClientFactory, OpenAIClient, GeminiClient

@pytest.fixture
def openai_config():
    return LLMConfig(
        provider="openai",
        model_name="gpt-4",
        temperature=0.7,
        max_tokens=100
    )

@pytest.fixture
def gemini_config():
    return LLMConfig(
        provider="gemini",
        model_name="gemini-pro",
        temperature=0.5,
        max_tokens=200
    )

def test_factory_create_openai(openai_config):
    with patch.dict(os.environ, {"OPENAI_API_KEY": "dummy"}), \
         patch("src.llm.client.openai") as mock_openai:
        client = LLMClientFactory.create(openai_config)
        assert isinstance(client, OpenAIClient)

def test_factory_create_gemini(gemini_config):
    with patch.dict(os.environ, {"GOOGLE_API_KEY": "dummy"}), \
         patch("src.llm.client.genai") as mock_genai:
        client = LLMClientFactory.create(gemini_config)
        assert isinstance(client, GeminiClient)

def test_openai_generate(openai_config):
    with patch.dict(os.environ, {"OPENAI_API_KEY": "dummy"}), \
         patch("src.llm.client.openai") as mock_openai:
        
        # Mock response
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "Test response"
        mock_openai.OpenAI.return_value.chat.completions.create.return_value = mock_response
        
        client = OpenAIClient(openai_config)
        response = client.generate("Test prompt")
        
        assert response == "Test response"
        mock_openai.OpenAI.return_value.chat.completions.create.assert_called_once()

def test_gemini_generate(gemini_config):
    with patch.dict(os.environ, {"GOOGLE_API_KEY": "dummy"}), \
         patch("src.llm.client.genai") as mock_genai:
        
        # Mock response
        mock_response = MagicMock()
        mock_response.text = "Gemini response"
        mock_genai.GenerativeModel.return_value.generate_content.return_value = mock_response
        
        client = GeminiClient(gemini_config)
        response = client.generate("Test prompt")
        
        assert response == "Gemini response"
        mock_genai.GenerativeModel.return_value.generate_content.assert_called_once()
