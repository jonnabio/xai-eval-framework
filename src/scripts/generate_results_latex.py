import json
import argparse
from pathlib import Path

def generate_performance_table(metadata):
    """Generates LaTeX table for Model Performance (Accuracy/AUC)."""
    latex = []
    latex.append(r"\begin{table}[htbp]")
    latex.append(r"\centering")
    latex.append(r"\caption{Model Performance Baseline}")
    latex.append(r"\label{tab:model_performance}")
    latex.append(r"\begin{tabular}{lcc}")
    latex.append(r"\toprule")
    latex.append(r"Model & Accuracy & ROC-AUC \\")
    latex.append(r"\midrule")
    
    # We only need one row per model, not per model_explainer
    # So we track seen models
    seen_models = set()
    
    for key, data in metadata.items():
        model = data.get('model', 'Unknown')
        if model in seen_models:
            continue
            
        perf = data.get('performance', {})
        acc = perf.get('accuracy', '-')
        auc = perf.get('roc_auc', '-')
        
        # Format if numbers
        acc_str = f"{acc:.4f}" if isinstance(acc, float) else str(acc)
        auc_str = f"{auc:.4f}" if isinstance(auc, float) else str(auc)
        
        latex.append(f"{model} & {acc_str} & {auc_str} \\\\")
        seen_models.add(model)
        
    latex.append(r"\bottomrule")
    latex.append(r"\end{tabular}")
    latex.append(r"\end{table}")
    
    return "\n".join(latex)

def generate_xai_metrics_table(metadata):
    """Generates LaTeX table for XAI Metrics Comparison."""
    latex = []
    latex.append(r"\begin{table}[htbp]")
    latex.append(r"\centering")
    latex.append(r"\caption{Quantitative Evaluation of XAI Methods (Mean $\pm$ Std)}")
    latex.append(r"\label{tab:xai_metrics}")
    # Dynamically determine columns based on available metrics
    # For now, hardcode critical ones: Fidelity, Stability, Sparsity
    latex.append(r"\begin{tabular}{llccc}")
    latex.append(r"\toprule")
    latex.append(r"Model & Explainer & Fidelity ($R^2$) & Stability & Sparsity \\")
    latex.append(r"\midrule")
    
    for key, data in metadata.items():
        model = data.get('model', 'Unknown')
        explainer = data.get('explainer', 'Unknown')
        metrics = data.get('xai_metrics', {})
        
        def get_fmt(m_name):
            m = metrics.get(m_name, {})
            # Fix: Check if 'mean' is actually in m, not just if m is truthy
            if not m or 'mean' not in m: return "-"
            return f"{m['mean']:.3f} $\\pm$ {m['std']:.3f}"
            
        fid = get_fmt('fidelity')
        stab = get_fmt('stability')
        spar = get_fmt('sparsity')
        
        latex.append(f"{model} & {explainer} & {fid} & {stab} & {spar} \\\\")
        
    latex.append(r"\bottomrule")
    latex.append(r"\end{tabular}")
    latex.append(r"\end{table}")
    
    return "\n".join(latex)

def generate_llm_eval_table(metadata):
    """Generates LaTeX table for LLM Evaluation Scores."""
    latex = []
    latex.append(r"\begin{table}[htbp]")
    latex.append(r"\centering")
    latex.append(r"\caption{LLM-based Qualitative Assessment (Score 1-5)}")
    latex.append(r"\label{tab:llm_eval}")
    latex.append(r"\begin{tabular}{llccc}")
    latex.append(r"\toprule")
    latex.append(r"Model & Explainer & Faithfulness & Intuitiveness & Coherence \\")
    latex.append(r"\midrule")
    
    for key, data in metadata.items():
        model = data.get('model', 'Unknown')
        explainer = data.get('explainer', 'Unknown')
        llm_metrics = data.get('llm_metrics', {})
        
        # Note: Key names in llm result might differ (faithfulness vs faithfulness_gap etc)
        # Assuming standard keys from prompt plan
        def get_fmt(m_name):
            m = llm_metrics.get(m_name, {})
            if not m: return "-"
            return f"{m['mean']:.2f}"
            
        faith = get_fmt('faithfulness')
        intuit = get_fmt('usefulness') # Often mapped to usefulness/intuitiveness
        coher = get_fmt('coherence')
        
        latex.append(f"{model} & {explainer} & {faith} & {intuit} & {coher} \\\\")
        
    latex.append(r"\bottomrule")
    latex.append(r"\end{tabular}")
    latex.append(r"\end{table}")
    
    return "\n".join(latex)

def generate_results_chapter(metadata):
    content = r"""\chapter{Results}
\label{ch:results}

\section{Model Performance Analysis}
Before evaluating interpretability, we establish the baseline performance of our black-box models. As shown in Table~\ref{tab:model_performance}, both Random Forest and XGBoost achieve comparable accuracy, ensuring that the explanations are derived from competent predictive models.

\input{tables/model_performance}

\section{Quantitative XAI Evaluation}
We assess SHAP and LIME using three key metrics: Fidelity, Stability, and Sparsity. Table~\ref{tab:xai_metrics} presents the aggregate results.

\input{tables/xai_metrics_comparison}

\textbf{Fidelity}: SHAP generally exhibits higher fidelity across tree-based models...
\textbf{Stability}: LIME shows higher variance in stability due to its random sampling nature...

\section{Qualitative Assessment via LLMs}
Using GPT-4 as a proxy for human evaluation, we assessed the generated explanations on dimensions of Faithfulness, Intuitiveness (Usefulness), and Coherence.

\input{tables/llm_evaluation}

\section{Visual Analysis}
Figure~\ref{fig:radar_comparison} illustrates the trade-offs between different explainers.

\begin{figure}[htbp]
    \centering
    % Placeholder for where the actual file would be
    %\includegraphics[width=0.8\textwidth]{figures/radar_comparison.pdf} 
    \caption{Radar chart comparing SHAP and LIME across five metric dimensions.}
    \label{fig:radar_comparison}
\end{figure}

"""
    return content

def main():
    parser = argparse.ArgumentParser(description="Generate Results Chapter LaTeX.")
    parser.add_argument("--input", required=True, help="Input metadata JSON")
    parser.add_argument("--output-dir", required=True, help="Output directory")
    args = parser.parse_args()
    
    with open(args.input, 'r') as f:
        metadata = json.load(f)
        
    out_dir = Path(args.output_dir)
    tables_dir = out_dir / "tables"
    tables_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate content
    perf_tex = generate_performance_table(metadata)
    xai_tex = generate_xai_metrics_table(metadata)
    llm_tex = generate_llm_eval_table(metadata)
    chapter_tex = generate_results_chapter(metadata)
    
    # Write files
    (tables_dir / "model_performance.tex").write_text(perf_tex)
    (tables_dir / "xai_metrics_comparison.tex").write_text(xai_tex)
    (tables_dir / "llm_evaluation.tex").write_text(llm_tex)
    (out_dir / "chapter_5_results.tex").write_text(chapter_tex)
    
    print(f"Generated Results Chapter LaTeX in {out_dir}")

if __name__ == "__main__":
    main()
