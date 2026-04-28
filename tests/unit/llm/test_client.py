"""Unit tests for LLM client wrapper."""

import pytest
from unittest.mock import patch, MagicMock
import os
from src.experiment.config import LLMConfig
from src.llm.client import LLMClientFactory, OpenAIClient, GeminiClient, load_llm_env_files

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
        mock_response.usage = None
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


def test_load_llm_env_files_reads_exp4_secret_file(tmp_path, monkeypatch):
    repo_root = tmp_path / "repo"
    secret_dir = repo_root / "configs" / "secrets"
    secret_dir.mkdir(parents=True)
    (secret_dir / "exp4.local.env").write_text("OPENROUTER_API_KEY=test-key\n", encoding="utf-8")
    fake_client_file = repo_root / "src" / "llm" / "client.py"
    fake_client_file.parent.mkdir(parents=True)
    fake_client_file.write_text("", encoding="utf-8")

    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    monkeypatch.setattr("src.llm.client.__file__", str(fake_client_file))

    load_llm_env_files()

    assert os.getenv("OPENROUTER_API_KEY") == "test-key"
