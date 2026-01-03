
import pytest
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from src.analysis.visualization import plot_radar_chart, PUBLICATION_STYLE

# Note: normalize_for_radar_helper_logic is hypothetical, we might need to expose it or test the plot function implicitly
# Better to refactor normalize logic in visualization.py to be testable, 
# but for now let's test the artifact creation or just mock.

# Wait, I didn't verify if I should expose the normalize logic. 
# The function `plot_radar_chart` has the logic inside. 
# I will create a test that calls the plot function and checks execution, 
# and maybe inspects the axis data if possible, or just smoke test.

def test_publication_style_constants():
    assert PUBLICATION_STYLE['single_column_width'] == 3.5
    assert PUBLICATION_STYLE['font_family'] == 'serif'

def test_plot_radar_chart_smoke(tmp_path):
    """Test standard radar chart generation."""
    data = {
        'RF+LIME': {'fidelity': 0.8, 'stability': 0.7, 'sparsity': 0.2, 'cost': 1000},
        'RF+SHAP': {'fidelity': 0.9, 'stability': 0.9, 'sparsity': 0.5, 'cost': 5000}
    }
    metrics = ['fidelity', 'stability', 'sparsity', 'cost']
    methods = ['RF+LIME', 'RF+SHAP']
    
    save_path = tmp_path / "radar.png"
    plot_radar_chart(data, metrics, methods, save_path=str(save_path))
    
    assert save_path.exists()
    assert save_path.stat().st_size > 0

def test_plot_heatmap_smoke(tmp_path):
    df = pd.DataFrame(
        [[0.8, 0.2], [0.9, 0.5]],
        index=['m1', 'm2'],
        columns=['met1', 'met2']
    )
    save_path = tmp_path / "heatmap.png"
    
    from src.analysis.visualization import plot_metric_heatmap
    plot_metric_heatmap(df, save_path=str(save_path))
    assert save_path.exists()
