"""Integration test for LLM evaluation script."""

import pytest
import subprocess
import sys
import json
from unittest.mock import patch, MagicMock
from pathlib import Path
from src.llm.client import OpenAIClient

def test_run_llm_eval_script(tmp_path):
    """Test the run_llm_eval.py script with mocked LLM client."""
    
    # 1. Create dummy results.json
    results_dir = tmp_path / "results"
    results_dir.mkdir()
    
    results_data = {
        "model_info": {"name": "test_model", "explainer_method": "shap"},
        "instance_evaluations": [
            {
                "instance_id": 1,
                "prediction": 1,
                "true_label": 0,
                "explanation": {
                    "top_features": ["Age: 0.5", "Income: 0.2"]
                }
            }
        ]
    }
    
    with open(results_dir / "results.json", "w") as f:
        json.dump(results_data, f)
        
    # 2. Mock LLMClientFactory to return a mock client
    # Since we run via subprocess, mocking is hard unless we import main().
    # Let's import main from the script instead of running subprocess to allow mocking.
    
    from scripts.run_llm_eval import main
    
    # Mock args
    test_args = [
        "scripts/run_llm_eval.py",
        "--input_dir", str(results_dir),
        "--provider", "openai",
        "--model", "gpt-test",
        "--output_file", "eval_out.json"
    ]
    
    with patch.object(sys, 'argv', test_args):
        # Mock the factory
        with patch("src.llm.client.LLMClientFactory.create") as mock_create:
            mock_client = MagicMock()
            mock_client.generate.return_value = '{"intuitiveness_score": 5, "clarity_score": 4}'
            mock_create.return_value = mock_client
            
            # Run
            main()
            
    # 3. Verify Output
    output_file = results_dir / "eval_out.json"
    assert output_file.exists()
    
    with open(output_file, 'r') as f:
        out_data = json.load(f)
        
    assert len(out_data['results']) == 1
    assert out_data['results'][0]['llm_eval']['intuitiveness_score'] == 5
