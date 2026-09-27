import numpy as np

from src.xai.anchors_wrapper import AnchorsTabularWrapper


def test_anchors_sanitize_sample_snaps_binary_and_continuous_features():
    training_data = np.array(
        [
            [0.0, 0.0, -1.0],
            [1.0, 0.0, 0.5],
            [0.0, 1.0, 2.0],
        ]
    )
    wrapper = AnchorsTabularWrapper(
        training_data=training_data,
        feature_names=["bin_a", "bin_b", "cont_c"],
    )

    sanitized = wrapper._sanitize_sample(np.array([0.9, 0.2, 0.7]))

    assert sanitized[0] == 1.0
    assert sanitized[1] == 0.0
    assert sanitized[2] == 0.5
