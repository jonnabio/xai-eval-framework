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
    Fidelity: float = Field(..., description="How well the explanation represents the model's behavior")
    Stability: float = Field(..., description="Consistency of explanations across similar inputs")
    Sparsity: float = Field(..., description="Conciseness of explanation (lower = more sparse)")
    CausalAlignment: float = Field(..., description="Alignment with known causal relationships")
    CounterfactualSensitivity: float = Field(..., description="Sensitivity to counterfactual changes")
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


# =============================================================================
# DETAILED RESULT MODELS
# =============================================================================

class ModelInfo(BaseModel):
    """Model information."""
    name: str
    path: Optional[str] = None
    explainer_method: Optional[str] = None

class MetricStatistics(BaseModel):
    """Aggregated statistics for a metric."""
    mean: float
    std: float
    min: float
    max: float
    median: Optional[float] = None

class ComputedMetrics(BaseModel):
    """Container for aggregated metrics (mapping metric name to stats)."""
    # Using Dict for flexibility as metric names might evolve
    metrics: Dict[str, MetricStatistics]

class InstanceEvaluation(BaseModel):
    """Detailed evaluation for a single instance."""
    instance_id: int
    true_label: Optional[int] = None
    prediction: Optional[int] = None
    prediction_correct: Optional[bool] = None
    quadrant: Optional[str] = None  # TP, TN, FP, FN
    metrics: Dict[str, float]       # Per-instance scores
    explanation: Optional[Dict[str, Any]] = None # Explanation details

class ExperimentMetadata(BaseModel):
    """Metadata from the experiment runner."""
    name: str
    dataset: str
    timestamp: datetime
    config_version: Optional[str] = None
    random_seed: Optional[int] = None
    duration_seconds: Optional[float] = None

class ExperimentResult(BaseModel):
    """Complete experiment result data structure."""
    metadata: ExperimentMetadata
    model_info: ModelInfo
    aggregated_metrics: Dict[str, Any] # Can be simple dict or ComputedMetrics
    instance_evaluations: List[InstanceEvaluation] = []

    model_config = {
        "json_schema_extra": {
            "example": {
                "metadata": {
                    "name": "exp1_adult_rf_lime",
                    "dataset": "adult",
                    "timestamp": "2023-10-27T10:00:00"
                },
                "model_info": {
                    "name": "random_forest",
                    "explainer_method": "lime"
                },
                "aggregated_metrics": {
                    "fidelity": {"mean": 0.85, "std": 0.05, "min": 0.8, "max": 0.9}
                },
                "instance_evaluations": [
                    {
                        "instance_id": 1,
                        "metrics": {"fidelity": 0.88},
                        "explanation": {"top_features": ["age", "income"]}
                    }
                ]
            }
        }
    }

class ExperimentResultResponse(BaseModel):
    """Response wrapper for detailed experiment results."""
    data: ExperimentResult
    metadata: Optional[Dict[str, Any]] = None

class InstancesResponse(BaseModel):
    """Response wrapper for paginated instances."""
    data: List[InstanceEvaluation]
    pagination: Dict[str, Any]
    metadata: Optional[Dict[str, Any]] = None

# =============================================================================
# HUMAN EVALUATION MODELS
# =============================================================================

class AnnotationStatus(str, Enum):
    """Status of a human annotation sample."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    SKIPPED = "skipped"

class HumanAnnotationRatings(BaseModel):
    """
    Likert scale ratings for explanation quality (1-5).
    Matches LLM evaluation dimensions for comparison.
    """
    coherence: int = Field(..., ge=1, le=5, description="How understandable and logically consistent (1=Poor, 5=Excellent)")
    faithfulness: int = Field(..., ge=1, le=5, description="How well it reflects model's actual reasoning (1=Poor, 5=Excellent)")
    usefulness: int = Field(..., ge=1, le=5, description="How helpful for understanding prediction (1=Poor, 5=Excellent)")

    model_config = {
        "json_schema_extra": {
            "example": {
                "coherence": 4,
                "faithfulness": 3,
                "usefulness": 4
            }
        }
    }

class HumanAnnotationSubmission(BaseModel):
    """Request model for submitting a human annotation."""
    sample_id: str = Field(..., min_length=1, description="Unique sample identifier (e.g., 'rf_lime_7834')")
    annotator_id: str = Field(..., min_length=1, max_length=50, description="Annotator identifier")
    ratings: HumanAnnotationRatings
    comments: Optional[str] = Field(None, max_length=2000, description="Optional comments about the explanation")
    time_spent_seconds: Optional[int] = Field(None, ge=0, description="Time spent annotating (seconds)")

    model_config = {
        "json_schema_extra": {
            "example": {
                "sample_id": "rf_lime_7834",
                "annotator_id": "annotator1",
                "ratings": {
                    "coherence": 4,
                    "faithfulness": 3,
                    "usefulness": 4
                },
                "comments": "Clear explanation but lacks some context",
                "time_spent_seconds": 180
            }
        }
    }

class HumanEvalSample(BaseModel):
    """A sample for human annotation (excludes LLM scores to maintain blindness)."""
    sample_id: str
    experiment: str = Field(..., description="Experiment name (e.g., 'rf_lime')")
    instance_id: int
    quadrant: Optional[str] = Field(None, description="Confusion matrix quadrant (TP/TN/FP/FN)")
    prediction: Optional[int] = None
    true_label: Optional[int] = None
    prediction_correct: Optional[bool] = None
    explanation: Dict[str, Any] = Field(..., description="Explanation data (top features, etc.)")
    classical_metrics: Dict[str, float] = Field(..., description="Classical XAI metrics (fidelity, stability, etc.)")
    assigned_to: Optional[str] = Field(None, description="Annotator this sample is assigned to")
    status: AnnotationStatus = Field(default=AnnotationStatus.PENDING)

    # NOT included: llm_scores (must remain blind during annotation)

    model_config = {
        "json_schema_extra": {
            "example": {
                "sample_id": "rf_lime_7834",
                "experiment": "rf_lime",
                "instance_id": 7834,
                "quadrant": "TP",
                "prediction": 1,
                "true_label": 1,
                "prediction_correct": True,
                "explanation": {
                    "top_features": [
                        "capital-gain: 0.4535",
                        "education-num: 0.0981",
                        "marital-status_Married-civ-spouse: 0.0881"
                    ],
                    "method": "LIME"
                },
                "classical_metrics": {
                    "fidelity": 0.95,
                    "stability": 0.86,
                    "sparsity": 0.09
                },
                "assigned_to": "annotator1",
                "status": "pending"
            }
        }
    }

class AnnotationProgress(BaseModel):
    """Progress tracking for an annotator."""
    annotator_id: str
    total_assigned: int
    completed: int
    in_progress: int
    pending: int
    completion_rate: float = Field(..., ge=0, le=1)
    avg_time_per_annotation: Optional[float] = None

class AnnotationSubmissionResponse(BaseModel):
    """Response after submitting an annotation."""
    status: str = Field(default="success")
    annotation_id: str = Field(..., description="Unique ID for this annotation")
    message: str
    progress: Dict[str, int] = Field(..., description="Updated progress (completed, remaining)")

class HumanEvalSamplesResponse(BaseModel):
    """Response containing samples for annotation."""
    data: List[HumanEvalSample]
    metadata: Dict[str, Any]

class ProgressResponse(BaseModel):
    """Response containing progress information."""
    data: AnnotationProgress
    metadata: Dict[str, Any]

class AdminStatsResponse(BaseModel):
    """Admin dashboard statistics."""
    data: Dict[str, Any]
    metadata: Dict[str, Any]

class AdminAnnotationsResponse(BaseModel):
    """Admin export of all annotations."""
    data: List[Dict[str, Any]]
    metadata: Dict[str, Any]
