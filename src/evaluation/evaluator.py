"""
LLM Evaluator Module.

This module helps evaluate explanation quality using LLMs.
"""
import json
import logging
import re
from pathlib import Path
from typing import Any, Dict

from jinja2 import Environment, FileSystemLoader

from src.llm.client import BaseLLMClient

logger = logging.getLogger(__name__)

class LLMEvaluator:
    """
    Evaluator that uses an LLM to assess explanation quality.
    """
    
    def __init__(
        self, 
        client: BaseLLMClient, 
        template_dir: Path, 
        template_name: str = "explanation_eval.j2"
    ):
        """
        Initialize the evaluator.
        
        Args:
            client: Configured LLM client.
            template_dir: Directory containing Jinja2 templates.
            template_name: Name of the template file to use.
        """
        self.client = client
        self.env = Environment(loader=FileSystemLoader(template_dir))
        self.template = self.env.get_template(template_name)
        
    def _parse_json_response(self, response: str) -> Dict[str, Any]:
        """
        Parse JSON from LLM response, handling markdown code blocks.
        """
        # Strip markdown code blocks if present
        clean_response = response.strip()
        if clean_response.startswith("```"):
            # Regex to capture content inside ```json ... ``` or just ``` ... ```
            match = re.search(r"```(?:json)?\s*(.*?)\s*```", clean_response, re.DOTALL)
            if match:
                clean_response = match.group(1)
        
        try:
            return json.loads(clean_response)
        except json.JSONDecodeError:
            logger.error(f"Failed to parse JSON response: {response}")
            # Return partial failure structure
            return {
                "error": "JSON parse error", 
                "raw_response": response
            }

    def format_explanation_text(self, instance_data: Dict[str, Any]) -> str:
        """
        Format the explanation data into a readable string for the prompt.
        """
        # Depending on how explanation is stored in results.json
        # It's typically a list of (feature, value) or similar.
        # We need to adapt based on actual data structure.
        
        # Looking at data structure from previous tool output (snippet):
        # "metrics": { ... }, "explanation": { "feature_importance": [...], "top_features": [...] }
        
        # But wait, run_batch_experiments output didn't show deep structure. 
        # SHAP wrapper returns { 'feature_importance': ..., 'top_features': ... }
        # The runner saves this under 'explanation' key.
        
        explanation = instance_data.get('explanation', {})
        
        # If it's a list (LIME output sometimes formats differently depending on wrapper version)
        # But let's assume standard dictionary from our wrappers.
        
        # Construct text
        lines = []
        
        # We might have feature names and importance values.
        # If we have 'top_features' indices, we need feature names to map.
        # Ideally, the saved result has feature names resolved or we passed them.
        
        # Let's handle a specific case: The saved results.json likely has the raw explanation object.
        # For LIME, it returns a list of tuples (feature_name, weight) if discretize_continuous=True
        # For SHAP, we return a numpy array of importances. 
        # The ExperimentRunner usually saves the raw return.
        
        # This formatting might need to be robust.
        # If 'explanation' has 'feature_importance' and it's a list.
        
        # Fallback: Just dump the text representation
        return str(explanation) 

    def evaluate_instance(self, instance_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate a single instance.
        
        Args:
            instance_data: Dictionary containing 'true_label', 'prediction', 'explanation', etc.
            
        Returns:
            Dictionary with evaluation scores.
        """
        # Prepare context variables
        # We need: model_name, true_label, prediction, explanation_text
        
        # 1. Format Explanation
        # For prompt, we want a nice text list:
        # 1. Age (0.23)
        # 2. Capital Gain (0.15)
        
        # We need to know feature names. 
        # In results.json, 'explanation' might be complex. 
        # Let's assume for now we try to extract a string representation.
        
        expl_data = instance_data.get('explanation', {})
        
        # Attempt to format logic (can be refined after seeing actual data)
        # For now, let's just dump the raw structure if we can't parse it nicely.
        # Ideally, we should have standardized this in ExperimentRunner.
        
        expl_text = json.dumps(expl_data, indent=2) 
        
        context = {
            "model_name": instance_data.get("model", "Unknown Model"),
            "true_label": instance_data.get("true_label"),
            "prediction": instance_data.get("prediction"),
            "prediction_prob": instance_data.get("metrics", {}).get("probability", 0.0), # Assuming metrics has prob
            "explanation_text": expl_text
        }
        
        # Render Prompt
        prompt = self.template.render(**context)
        
        # Call LLM
        response_text = self.client.generate(prompt)
        
        # Parse Response
        result = self._parse_json_response(response_text)
        
        return result
