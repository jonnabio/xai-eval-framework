"""
Experiment configuration schemas using Pydantic.

Defines the structure for experiment YAML configs with validation.
"""

from typing import Dict, Optional, Literal
from pydantic import BaseModel, Field, field_validator
from pathlib import Path
import yaml

class ModelConfig(BaseModel):
    """Model selection and loading configuration."""
    name: str = Field(..., description="Model identifier (rf, xgboost)")
    path: Path = Field(..., description="Path to saved model file")
    
    @field_validator('path')
    @classmethod
    def path_exists(cls, v):
        # We might not enforce existence at config load time for flexibility,
        # but let's enforce it for robustness if the file is expected to exist.
        # For unit tests involving fake paths, this might be tricky.
        # Let's keep it simple: valid Path object. Existence checked by Runner.
        return v

class ExplainerConfig(BaseModel):
    """XAI method configuration."""
    method: Literal["shap", "lime"] = Field(..., description="XAI method")
    params: Dict = Field(default_factory=dict, description="Method-specific parameters")
    
    # SHAP-specific details
    explainer_type: Optional[str] = Field(None, description="tree/kernel for SHAP")
    
    # LIME-specific details
    num_samples: Optional[int] = Field(1000, description="Samples for LIME generation")
    num_features: Optional[int] = Field(10, description="Top features for LIME")

class SamplingConfig(BaseModel):
    """Evaluation instance sampling configuration."""
    strategy: Literal["stratified"] = "stratified"
    samples_per_class: int = Field(25, ge=1, description="Samples per TP/TN/FP/FN")
    random_seed: int = 42

class MetricsConfig(BaseModel):
    """Metrics to compute."""
    fidelity: bool = True
    stability: bool = True
    sparsity: bool = True
    sparsity: bool = True
    cost: bool = True
    domain: bool = True # Domain Alignment (Expert Priors)
    counterfactual: bool = False # Counterfactual Sensitivity (Experimental)
    
    # Metric-specific
    stability_perturbations: int = Field(10, ge=1)
    stability_noise_level: float = Field(0.1, ge=0.0)

class LLMConfig(BaseModel):
    """LLM provider configuration."""
    provider: Literal["openai", "gemini", "dummy", "openrouter"] = Field("openai", description="LLM provider")
    model_name: str = Field(..., description="Model name (e.g. gpt-4, gemini-pro)")
    temperature: float = Field(0.0, ge=0.0, le=2.0)
    max_tokens: int = Field(1000, ge=1)

class ExperimentConfig(BaseModel):
    """Root experiment configuration."""
    name: str = Field(..., description="Experiment identifier")
    description: str = Field("", description="Experiment purpose")
    dataset: str = Field("adult", description="Dataset name")
    
    model: ModelConfig
    explainer: ExplainerConfig
    sampling: SamplingConfig
    metrics: MetricsConfig
    llm: Optional[LLMConfig] = None
    
    # Output
    output_dir: Path = Field(Path("outputs/experiments"), description="Results directory")
    
    # Reproducibility
    random_seed: int = 42
    version: str = Field("1.0.0", description="Experiment schema version")
    
    class Config:
        extra = "forbid" # Strict validation

def load_config(config_path: Path) -> ExperimentConfig:
    """
    Load and validate experiment configuration from YAML.
    
    Args:
        config_path: Path to YAML config file
        
    Returns:
        Validated ExperimentConfig instance
        
    Raises:
        FileNotFoundError: Config file not found
        ValidationError: Invalid configuration
    """
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    
    with open(config_path, 'r') as f:
        config_dict = yaml.safe_load(f)
    
    return ExperimentConfig(**config_dict)
