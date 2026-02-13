#!/usr/bin/env python3
"""
Generate Radar Plots and consolidated tables for Paper B.
Aggregates results from multiple experiment runs and normalizes metrics for comparison.
"""

import os
import json
import argparse
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from pathlib import Path
from typing import List, Dict, Any

def load_results(results_dir: Path) -> List[Dict[str, Any]]:
    """Scan directory for results.json files."""
    results = []
    for p in results_dir.glob("**/results.json"):
        try:
            with open(p, 'r') as f:
                data = json.load(f)
            
            # Extract metadata and metrics
            meta = data.get("experiment_metadata", {})
            model_info = data.get("model_info", {})
            metrics = data.get("aggregated_metrics", {})
            
            # Handle different metric formats (flat vs nested with mean/std)
            formatted_metrics = {}
            for k, v in metrics.items():
                if isinstance(v, dict) and "mean" in v:
                    formatted_metrics[k.lower()] = v["mean"]
                else:
                    formatted_metrics[k.lower()] = v
            
            # Map legacy names to consistent scale
            # (e.g. EfficiencyMS -> cost)
            if 'efficiencyms' in formatted_metrics:
                formatted_metrics['cost'] = formatted_metrics.pop('efficiencyms')
                
            entry = {
                "name": meta.get("name", p.parent.name),
                "model": model_info.get("name", "unknown"),
                "explainer": model_info.get("explainer_method", "unknown"),
                "metrics": formatted_metrics,
                "path": str(p)
            }
            results.append(entry)
        except Exception as e:
            print(f"Error loading {p}: {e}")
            
    return results

def normalize_metrics(results: List[Dict[str, Any]]) -> pd.DataFrame:
    """Normalize metrics to 0-1 scale where 1 is 'better'."""
    data = []
    for r in results:
        row = {
            "Model": r["model"],
            "Explainer": r["explainer"],
            "Name": r["name"]
        }
        m = r["metrics"]
        
        # 1. Fidelity (0-1, Higher is Better)
        row["Fidelity"] = m.get("fidelity", 0)
        
        # 2. Stability (0-1, Higher is Better)
        row["Stability"] = m.get("stability", 0)
        
        # 3. Sparsity (Lower is Better -> Invert)
        # Ideally Sparsity = % features with 0 weight. 
        # If mean sparsity is 0.09 (Adult), only 9% are 0.
        # We want "Interpretability" = 1 - Sparsity? 
        # Actually Sparsity usually means "The amount of 0s". So higher IS better logic?
        # Let's check the code: Sparsity = count(abs(w) < threshold) / total
        # So higher Sparsity = more zeros = more interpretable.
        row["Sparsity"] = m.get("sparsity", 0)
        
        # 4. Cost (Lower is Better -> Invert relative to max)
        cost = m.get("cost", 1)
        row["Cost_Raw"] = cost
        
        # 5. Causal Alignment (Higher is Better)
        row["Causal"] = m.get("causalalignment", 0)
        
        data.append(row)
        
    df = pd.DataFrame(data)
    
    # Global normalization for Cost
    # High cost = 0, Low cost = 1
    if not df.empty and "Cost_Raw" in df.columns:
        max_cost = df["Cost_Raw"].max()
        min_cost = df["Cost_Raw"].min()
        if max_cost != min_cost:
            df["Efficiency"] = 1 - (df["Cost_Raw"] - min_cost) / (max_cost - min_cost)
        else:
            df["Efficiency"] = 1.0
            
    return df

def generate_radar_plot(df: pd.DataFrame, output_path: Path):
    """Generate interactive radar plot using Plotly."""
    if df.empty:
        print("No data to plot.")
        return

    categories = ['Fidelity', 'Stability', 'Sparsity', 'Efficiency', 'Causal']
    
    fig = go.Figure()

    for _, row in df.iterrows():
        label = f"{row['Model']} + {row['Explainer'].upper()}"
        values = [row[cat] for cat in categories]
        
        fig.add_trace(go.Scatterpolar(
            r=values + [values[0]], # Close the loop
            theta=categories + [categories[0]],
            fill='toself',
            name=label
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )
        ),
        showlegend=True,
        title="XAI Method Comparison (Paper B Radar Plot)"
    )

    # Save as HTML and Static PNG (if possible)
    fig.write_html(str(output_path.with_suffix('.html')))
    print(f"Radar plot saved to {output_path.with_suffix('.html')}")

def main():
    parser = argparse.ArgumentParser(description="Aggregate XAI results for Paper B")
    parser.add_argument("--results_dir", type=Path, default=Path("experiments"), help="Root results directory")
    parser.add_argument("--output_name", type=str, default="paper_comparison", help="Output file basename")
    
    args = parser.parse_args()
    
    print(f"Scanning for results in {args.results_dir}...")
    results = load_results(args.results_dir)
    print(f"Found {len(results)} finalized experiments.")
    
    df = normalize_metrics(results)
    
    # Save CSV table
    output_dir = Path("outputs") / "paper_analysis"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    csv_path = output_dir / f"{args.output_name}.csv"
    df.to_csv(csv_path, index=False)
    print(f"Consolidated table saved to {csv_path}")
    
    # Generate Radar Plot
    plot_path = output_dir / f"{args.output_name}_radar"
    generate_radar_plot(df, plot_path)

if __name__ == "__main__":
    main()
