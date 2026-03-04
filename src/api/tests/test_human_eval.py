"""
Unit tests for human evaluation system.
"""

import pytest
import json
from src.api.services import human_eval_service as service
from src.api.models.schemas import HumanAnnotationSubmission, HumanAnnotationRatings

@pytest.fixture
def mock_samples_file(tmp_path, monkeypatch):
    """Create temporary samples.json for testing."""
    samples_dir = tmp_path / "human_eval"
    samples_dir.mkdir()

    samples = [
        {
            "sample_id": "test_sample_1",
            "experiment": "rf_lime",
            "instance_id": 123,
            "quadrant": "TP",
            "prediction": 1,
            "true_label": 1,
            "prediction_correct": True,
            "explanation": {"top_features": ["feature1: 0.5"]},
            "classical_metrics": {"fidelity": 0.9},
            "llm_scores": {"coherence": 4, "faithfulness": 3, "usefulness": 4}
        }
    ]

    samples_file = samples_dir / "samples.json"
    with open(samples_file, 'w') as f:
        json.dump(samples, f)

    # Mock paths
    monkeypatch.setattr(service, 'get_human_eval_dir', lambda: samples_dir)
    monkeypatch.setattr(service, 'get_samples_file', lambda: samples_file)
    monkeypatch.setattr(service, 'get_annotations_dir', lambda: samples_dir / "annotations")
    monkeypatch.setattr(service, 'get_metadata_file', lambda: samples_dir / "metadata.json")

    # Create annotations dir
    (samples_dir / "annotations").mkdir()

    return samples_dir

def test_load_samples(mock_samples_file):
    """Test loading samples from file."""
    # Clear cache to ensure we read from new mock file
    service.load_samples_from_file.cache_clear()
    
    samples = service.get_all_samples()
    assert len(samples) == 1
    assert samples[0].sample_id == "test_sample_1"
    assert samples[0].experiment == "rf_lime"
    # Ensure LLM scores are excluded
    assert not hasattr(samples[0], 'llm_scores')

def test_save_annotation(mock_samples_file):
    """Test saving an annotation."""
    service.load_samples_from_file.cache_clear()
    
    submission = HumanAnnotationSubmission(
        sample_id="test_sample_1",
        annotator_id="test_annotator",
        ratings=HumanAnnotationRatings(
            coherence=4,
            faithfulness=3,
            usefulness=5
        ),
        comments="Test comment",
        time_spent_seconds=120
    )

    success, annotation_id, message = service.save_annotation(submission)

    assert success
    assert annotation_id.startswith("anno_")
    assert "success" in message.lower()
    
    # Verify file created
    annotations_dir = service.get_annotations_dir()
    files = list(annotations_dir.glob("*.json"))
    assert len(files) == 1

def test_get_progress(mock_samples_file):
    """Test progress calculation."""
    # Save an annotation first
    submission = HumanAnnotationSubmission(
        sample_id="test_sample_1",
        annotator_id="test_annotator",
        ratings=HumanAnnotationRatings(
            coherence=4,
            faithfulness=3,
            usefulness=5
        ),
        comments="Test comment",
        time_spent_seconds=120
    )
    service.save_annotation(submission)
    
    progress = service.get_annotator_progress("test_annotator")

    assert progress.total_assigned >= 0
    assert progress.completed >= 0
    # Since we have only 1 sample and we annotated it:
    assert progress.completed == 1
    assert progress.total_assigned == 1 # Assuming assigned to all if None
    assert progress.completion_rate == 1.0
