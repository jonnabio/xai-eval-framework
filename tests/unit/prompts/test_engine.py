"""Unit tests for prompt engine."""

import pytest
from pathlib import Path
from src.prompts.engine import PromptEngine

def test_prompt_engine_initialization():
    """Test default initialization."""
    engine = PromptEngine()
    assert engine.template_dir.exists()
    assert (engine.template_dir / "eval_instruction.j2").exists()

def test_render_eval_instruction():
    """Test rendering the evaluation instruction template."""
    engine = PromptEngine()
    
    context = {
        "model_name": "TestModel",
        "method_name": "TestXAI",
        "prediction_label": ">50K",
        "true_label": ">50K",
        "explanation_text": "Age: 0.5, Income: 0.8"
    }
    
    rendered = engine.render("eval_instruction.j2", **context)
    
    assert "TestModel" in rendered
    assert "TestXAI" in rendered
    assert ">50K" in rendered
    assert "Age: 0.5, Income: 0.8" in rendered
    assert "intuitiveness_score" in rendered

def test_template_not_found():
    """Test error when template is missing."""
    engine = PromptEngine()
    with pytest.raises(Exception): # jinja2.TemplateNotFound
        engine.render("nonexistent_template.j2")
