"""
Unit tests for the LIME Tabular Wrapper (EXP1-12).
"""
import pytest
import numpy as np
from src.xai.lime_tabular import LIMETabularWrapper, generate_lime_explanations

# --- Fixtures ---

@pytest.fixture(scope="module")
def sample_data():
    """Provides valid training data and feature names."""
    n_samples = 100
    n_features = 5
    X = np.random.rand(n_samples, n_features)
    feature_names = [f"feature_{i}" for i in range(n_features)]
    return X, feature_names

@pytest.fixture
def mock_model():
    """Provides a mock model with predict_proba."""
    class MockModel:
        def predict_proba(self, X):
            # Return pseudo-probabilities summing to 1
            # Shape (n_samples, 2)
            n = X.shape[0]
            # Deterministic calculation based on feature sum to maintain consistency for reproducibility checks if needed
            logits = np.sum(X, axis=1)
            probs_1 = 1 / (1 + np.exp(-logits))
            probs_0 = 1 - probs_1
            return np.vstack([probs_0, probs_1]).T
            
    return MockModel()

# --- Tests ---

class TestLIMETabularWrapper:
    
    def test_initialization(self, sample_data):
        """Test wrapper initializes without errors and sets attributes."""
        X, features = sample_data
        wrapper = LIMETabularWrapper(
            training_data=X,
            feature_names=features,
            num_features=3,
            num_samples=100,
            random_state=42
        )
        assert wrapper.num_features == 3
        assert wrapper.num_samples == 100
        assert wrapper.random_state == 42
        assert len(wrapper.feature_names) == len(features)
        
    def test_input_validation(self, sample_data):
        """Test it raises ValueError on mismatched dimensions."""
        X, features = sample_data
        # Create mismatch
        bad_features = features + ["extra"]
        
        with pytest.raises(ValueError, match="Mismatch"):
            LIMETabularWrapper(X, bad_features)
            
    def test_explain_instance_output_shape(self, sample_data, mock_model):
        """Test explain_instance returns one dense vector of correct shape."""
        X, features = sample_data
        wrapper = LIMETabularWrapper(X, features, num_samples=50) # Low samples for speed
        
        instance = X[0]
        explanation = wrapper.explain_instance(mock_model, instance)
        
        assert isinstance(explanation, np.ndarray)
        assert explanation.shape == (len(features),)
        assert explanation.ndim == 1

    def test_generate_explanations_output_keys(self, sample_data, mock_model):
        """Test generate_explanations return structure."""
        X, features = sample_data
        wrapper = LIMETabularWrapper(X, features, num_samples=50) # default num_features=10
        
        batch = X[:5]
        explanations = wrapper.generate_explanations(mock_model, batch)
        
        assert "feature_importance" in explanations
        assert "top_features" in explanations
        assert "metadata" in explanations
        
        effective_k = min(wrapper.num_features, len(features))
        assert explanations["feature_importance"].shape == (5, len(features))
        assert explanations["top_features"].shape == (5, effective_k)
        
    def test_reproducibility(self, sample_data, mock_model):
        """Test that fixing random_state produces identical explanations."""
        X, features = sample_data
        target_instance = X[0]
        
        # Wrapper 1
        w1 = LIMETabularWrapper(X, features, num_samples=50, random_state=42)
        exp1 = w1.explain_instance(mock_model, target_instance)
        
        # Wrapper 2
        w2 = LIMETabularWrapper(X, features, num_samples=50, random_state=42)
        exp2 = w2.explain_instance(mock_model, target_instance)
        
        np.testing.assert_array_almost_equal(exp1, exp2, decimal=5)
        
    def test_config_retrieval(self, sample_data):
        """Test get_config returns expected values."""
        X, features = sample_data
        wrapper = LIMETabularWrapper(X, features, num_features=7)
        config = wrapper.get_config()
        
        assert config['num_features'] == 7
        assert config['n_features'] == len(features)
        assert config['n_training_samples'] == X.shape[0]

def test_convenience_function(sample_data, mock_model):
    """Test the functional interface."""
    X, features = sample_data
    batch = X[:2]
    
    result = generate_lime_explanations(
        model=mock_model,
        X_samples=batch,
        training_data=X,
        feature_names=features,
        num_samples=50
    )
    
    # default num_features=10, data has 5 features. effective=5.
    assert result["feature_importance"].shape == (2, len(features))
    assert result["top_features"].shape == (2, min(10, len(features)))
