"""
Pydantic models matching TypeScript interface definitions from xai-benchmark.
Ensures strict type compliance for the API data contract.
"""
from datetime import datetime
from enum import Enum
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field, field_validator

# =============================================================================
# ENUMS
# =============================================================================

class ModelType(str, Enum):
    """Model architecture types."""
    CLASSICAL = "classical"
    CNN = "cnn"
    TRANSFORMER = "transformer"
    RNN = "rnn"

class Dataset(str, Enum):
    """Available datasets for benchmarking."""
    IMAGENET = "ImageNet"
    CIFAR_10 = "CIFAR-10"
    CIFAR_100 = "CIFAR-100"
    MNIST = "MNIST"
    FASHION_MNIST = "FashionMNIST"
    CELEB_A = "CelebA"
    IMDB = "IMDB"
    REUTERS = "Reuters"
    AG_NEWS = "AG-News"
    SST_2 = "SST-2"
    COLA = "CoLA"
    TABULAR_SYNTHETIC = "TabularSynthetic"
    ADULT_INCOME = "AdultIncome"
    WINE_QUALITY = "WineQuality"
    BREAST_CANCER = "BreastCancer"
    DIABETES = "Diabetes"

class XaiMethod(str, Enum):
    """XAI explanation methods."""
    LIME = "LIME"
    SHAP = "SHAP"
    GRAD_CAM = "GradCAM"
    RISE = "RISE"
    INTEGRATED_GRADIENTS = "Integrated Gradients"

class RunStatus(str, Enum):
    """Run execution status."""
    COMPLETED = "completed"
    RUNNING = "running"
    FAILED = "failed"
    PENDING = "pending"

# =============================================================================
# MODELS
# =============================================================================

class MetricSet(BaseModel):
    """Core metric set with all explainability measurements."""
    Fidelity: float = Field(..., ge=0, le=1, description="How well the explanation represents the model's behavior (0-1)")
    Stability: float = Field(..., ge=0, le=1, description="Consistency of explanations across similar inputs (0-1)")
    Sparsity: float = Field(..., ge=0, le=1, description="Conciseness of explanation (lower = more sparse, 0-1)")
    CausalAlignment: float = Field(..., ge=0, le=1, description="Alignment with known causal relationships (0-1)")
    CounterfactualSensitivity: float = Field(..., ge=0, le=1, description="Sensitivity to counterfactual changes (0-1)")
    EfficiencyMS: float = Field(..., ge=0, description="Processing time efficiency in milliseconds")

    model_config = {
        "json_schema_extra": {
            "example": {
                "Fidelity": 0.85,
                "Stability": 0.92,
                "Sparsity": 0.7,
                "CausalAlignment": 0.6,
                "CounterfactualSensitivity": 0.5,
                "EfficiencyMS": 150.5
            }
        }
    }

class LikertScores(BaseModel):
    """Likert scale ratings for different evaluation dimensions (1-5)."""
    clarity: int = Field(..., ge=1, le=5)
    usefulness: int = Field(..., ge=1, le=5)
    completeness: int = Field(..., ge=1, le=5)
    trustworthiness: int = Field(..., ge=1, le=5)
    overall: int = Field(..., ge=1, le=5)

class LlmEval(BaseModel):
    """LLM-based evaluation with Likert scales and justifications."""
    Likert: LikertScores
    Justification: str = Field(..., min_length=10, max_length=1000, description="Textual justification for the ratings")

class Run(BaseModel):
    """Complete benchmark run with all metadata and results."""
    id: str = Field(..., min_length=1)
    modelName: str = Field(..., min_length=1)
    modelType: ModelType
    dataset: Dataset
    method: XaiMethod
    accuracy: float = Field(..., ge=0, le=100, description="Model accuracy on the dataset (0-100)")
    explainabilityScore: float = Field(..., ge=0, le=1, description="Overall explainability score (0-1)")
    processingTime: float = Field(..., ge=0, description="Total processing time in milliseconds")
    status: RunStatus
    timestamp: datetime
    metrics: MetricSet
    llmEval: LlmEval
    config: Optional[Dict[str, Any]] = None
    errorMessage: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

    @field_validator('accuracy')
    @classmethod
    def validate_accuracy(cls, v):
        if not 0 <= v <= 100:
            raise ValueError('Accuracy must be between 0 and 100')
        return v

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "run_123",
                "modelName": "RandomForest_v1",
                "modelType": "classical",
                "dataset": "AdultIncome",
                "method": "SHAP",
                "accuracy": 88.5,
                "explainabilityScore": 0.75,
                "processingTime": 1250.0,
                "status": "completed",
                "timestamp": "2023-10-27T10:00:00Z",
                "metrics": {
                    "Fidelity": 0.9,
                    "Stability": 0.8,
                    "Sparsity": 0.7,
                    "CausalAlignment": 0.6,
                    "CounterfactualSensitivity": 0.5,
                    "EfficiencyMS": 100
                },
                "llmEval": {
                    "Likert": {
                        "clarity": 4,
                        "usefulness": 4,
                        "completeness": 3,
                        "trustworthiness": 4,
                        "overall": 4
                    },
                    "Justification": "Good explanation but slightly complex."
                }
            }
        }
    }

# =============================================================================
# REFONSE WRAPPERS
# =============================================================================

class RunsResponse(BaseModel):
    data: List[Run]
    pagination: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None

class RunResponse(BaseModel):
    data: Run
    metadata: Optional[Dict[str, Any]] = None

class HealthResponse(BaseModel):
    status: str
    version: str
    timestamp: datetime
