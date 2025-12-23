from datetime import datetime
from src.api.models.schemas import (
    Run, MetricSet, LlmEval, LikertScores, 
    ModelType, Dataset, XaiMethod, RunStatus
)
import json

def test_schemas():
    print("Testing Pydantic Schemas...")

    # 1. Test MetricSet
    try:
        metrics = MetricSet(
            Fidelity=0.9,
            Stability=0.8,
            Sparsity=0.7,
            CausalAlignment=0.6,
            CounterfactualSensitivity=0.5,
            EfficiencyMS=100
        )
        print("PASS: MetricSet creation")
    except Exception as e:
        print(f"FAIL: MetricSet creation - {e}")

    # 2. Test LikertScores and LlmEval
    try:
        likert = LikertScores(
            clarity=5, usefulness=4, completeness=3, 
            trustworthiness=4, overall=4
        )
        llm_eval = LlmEval(
            Likert=likert,
            Justification="This is a valid justification text with enough characters."
        )
        print("PASS: LlmEval creation")
    except Exception as e:
        print(f"FAIL: LlmEval creation - {e}")

    # 3. Test Run Model
    try:
        run = Run(
            id="test_run_1",
            modelName="TestModel",
            modelType=ModelType.CLASSICAL,
            dataset=Dataset.ADULT_INCOME,
            method=XaiMethod.SHAP,
            accuracy=85.5,
            explainabilityScore=0.8,
            processingTime=150.0,
            status=RunStatus.COMPLETED,
            timestamp=datetime.now(),
            metrics=metrics,
            llmEval=llm_eval
        )
        print("PASS: Run creation")
    except Exception as e:
        print(f"FAIL: Run creation - {e}")

    # 4. JSON Serialization
    try:
        json_str = run.model_dump_json()
        print("PASS: JSON Serialization")
    except Exception as e:
        print(f"FAIL: JSON Serialization - {e}")

    # 5. JSON Deserialization
    try:
        run2 = Run.model_validate_json(json_str)
        assert run2.id == run.id
        print("PASS: JSON Deserialization")
    except Exception as e:
        print(f"FAIL: JSON Deserialization - {e}")

    # 6. Validation Error Test (Accuracy > 100)
    try:
        Run(
            id="invalid_run",
            modelName="BadModel",
            modelType=ModelType.CLASSICAL,
            dataset=Dataset.ADULT_INCOME,
            method=XaiMethod.SHAP,
            accuracy=150.0, # Invalid
            explainabilityScore=0.8,
            processingTime=150.0,
            status=RunStatus.COMPLETED,
            timestamp=datetime.now(),
            metrics=metrics,
            llmEval=llm_eval
        )
        print("FAIL: Validation did not catch invalid accuracy")
    except ValueError as e:
        print("PASS: Validation correctly caught invalid accuracy")
    except Exception as e:
        print(f"FAIL: Unexpected error during validation test - {e}")

if __name__ == "__main__":
    test_schemas()
