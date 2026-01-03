import json
import argparse
from pathlib import Path

def generate_hyperparameter_table(experiments):
    """Generates a LaTeX table for model hyperparameters."""
    latex = []
    latex.append(r"\begin{table}[htbp]")
    latex.append(r"\centering")
    latex.append(r"\caption{Model Hyperparameters}")
    latex.append(r"\label{tab:hyperparameters}")
    latex.append(r"\begin{tabular}{lll}")
    latex.append(r"\toprule")
    latex.append(r"Model & Parameter & Value \\")
    latex.append(r"\midrule")

    for exp in experiments:
        model_name = exp['model']
        params = exp['hyperparameters']
        # Also include explainer params if desired, or make a separate table
        
        for param, value in params.items():
            # Escape key latex chars if needed
            safe_param = str(param).replace("_", r"\_")
            safe_value = str(value).replace("_", r"\_")
            latex.append(f"{model_name} & {safe_param} & {safe_value} \\\\")
            
    latex.append(r"\bottomrule")
    latex.append(r"\end{tabular}")
    latex.append(r"\end{table}")
    
    return "\n".join(latex)

def generate_metrics_table(metrics):
    """Generates a LaTeX table for metric definitions."""
    latex = []
    latex.append(r"\begin{table}[htbp]")
    latex.append(r"\centering")
    latex.append(r"\caption{Evaluation Metrics Summary}")
    latex.append(r"\label{tab:metrics}")
    latex.append(r"\begin{tabular}{lp{10cm}}")
    latex.append(r"\toprule")
    latex.append(r"Metric & Description \\")
    latex.append(r"\midrule")
    
    for name, info in metrics.items():
        desc = info['description']
        latex.append(f"{name} & {desc} \\\\")
        
    latex.append(r"\bottomrule")
    latex.append(r"\end{tabular}")
    latex.append(r"\end{table}")
    
    return "\n".join(latex)

def generate_chapter_template(metadata):
    """Generates the main chapter LaTeX file with placeholders."""
    ds = metadata.get('dataset', {})
    env = metadata.get('environment', {})
    
    content = r"""\chapter{Methodology}
\label{ch:methodology}

\section{Introduction}
This chapter details the experimental methodology used to evaluate specific XAI techniques on tabular data. We focus on the Adult Income dataset and employ two popular explainability methods: SHAP and LIME.

\section{Experimental Design}

\subsection{Dataset}
We utilize the UCI Adult Income dataset~\cite{kohavi1996adult}.
\begin{itemize}
    \item \textbf{Total Samples}: """ + str(ds.get('n_total', 'N/A')) + r"""
    \item \textbf{Training Samples}: """ + str(ds.get('n_train', 'N/A')) + r"""
    \item \textbf{Test Samples}: """ + str(ds.get('n_test', 'N/A')) + r"""
    \item \textbf{Features}: """ + str(ds.get('n_features', 'N/A')) + r"""
    \item \textbf{Positive Class Ratio}: """ + f"{ds.get('class_balance_pos_ratio', 0):.2f}" + r"""
\end{itemize}

\subsection{Preprocessing}
[Describe imputation, encoding, and scaling steps here]

\section{Model Architectures}
We evaluate two primary black-box models: Random Forest~\cite{breiman2001random} and XGBoost~\cite{chen2016xgboost}. The specific hyperparameters used are detailed in Table~\ref{tab:hyperparameters}.

\input{tables/hyperparameters}

\section{Explainability Techniques}
We evaluate the following local explanation methods:
\begin{itemize}
    \item \textbf{SHAP}~\cite{lundberg2017shap}: Using TreeExplainer.
    \item \textbf{LIME}~\cite{ribeiro2016lime}: Using LimeTabularExplainer.
\end{itemize}

\section{Evaluation Metrics Framework}
We employ a diverse set of quantitative metrics to assess explanation quality. A summary is provided in Table~\ref{tab:metrics}.

\input{tables/metrics_summary}

\subsection{Statistical Analysis}
To validate our findings, we apply the Friedman test and Wilcoxon signed-rank test~\cite{demsar2006statistical}.

\section{Reproducibility}
All experiments were conducted using the following environment:
\begin{itemize}
    \item Python: """ + env.get('python', 'N/A') + r"""
    \item Scikit-learn: """ + env.get('scikit-learn', 'N/A') + r"""
    \item SHAP: """ + env.get('shap', 'N/A') + r"""
    \item LIME: """ + env.get('lime', 'N/A') + r"""
    \item XGBoost: """ + env.get('xgboost', 'N/A') + r"""
\end{itemize}

"""
    return content

def main():
    parser = argparse.ArgumentParser(description="Generate LaTeX artifacts for Methodology chapter.")
    parser.add_argument("--input", required=True, help="Input JSON metadata file")
    parser.add_argument("--output-dir", required=True, help="Output directory for tex files")
    args = parser.parse_args()
    
    with open(args.input, 'r') as f:
        metadata = json.load(f)
        
    out_dir = Path(args.output_dir)
    table_dir = out_dir / "tables"
    table_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate artifacts
    hp_table_tex = generate_hyperparameter_table(metadata.get('experiments', []))
    metrics_table_tex = generate_metrics_table(metadata.get('metrics', {}))
    chapter_tex = generate_chapter_template(metadata)
    
    # Write files
    (table_dir / "hyperparameters.tex").write_text(hp_table_tex)
    (table_dir / "metrics_summary.tex").write_text(metrics_table_tex)
    (out_dir / "chapter_3_methodology.tex").write_text(chapter_tex)
    
    print(f"Generated LaTeX files in {out_dir}")

if __name__ == "__main__":
    main()
