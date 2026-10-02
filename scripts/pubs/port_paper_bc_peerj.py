"""ONE-TIME port record (2026-10-02). Do not re-run once the PeerJ files have been
edited by hand: it regenerates them from the TMLR source and overwrites the edits.

Assemble paper_bc_peerjcs.tex from the filed TMLR source (tag tmlr-submission-12779).

Text is moved, not rewritten: every block below is a verbatim line range of
paper_bc_tmlr.tex, re-headed to PeerJ's standard sections. New prose is limited
to the PeerJ-required items (infrastructure, AI disclosure, EXP4 judge IDs,
host-heterogeneity limitation, bridging sentences) and is marked NEW below.
"""
import re
from pathlib import Path

D = Path(__file__).resolve().parents[2] / 'docs' / 'reports' / 'paper_bc'
src = (D / 'paper_bc_tmlr.tex').read_text(encoding='utf-8').replace('\r\n', '\n').split('\n')


def L(a, b):
    """Lines a..b of the TMLR source, 1-based inclusive."""
    return '\n'.join(src[a - 1:b])


def demote(text, levels=1):
    for _ in range(levels):
        text = text.replace('\\subsubsection{', '\\paragraph{')
        text = text.replace('\\subsection{', '\\subsubsection{')
        text = text.replace('\\section{', '\\subsection{')
    return text


def must(text, old, new):
    assert old in text, old[:80]
    return text.replace(old, new, 1)


RULE = '% ' + '-' * 71

pre = r"""%% PeerJ Computer Science submission (Research Article).
%% Ported 2026-10-02 from paper_bc_tmlr.tex at tag tmlr-submission-12779 after
%% TMLR desk-rejected submission 12779. Results, tables and figures are
%% unchanged; see docs/planning/paper_bc_peerj_retarget_plan_2026-10-02.md.
%% Review build keeps `lineno`; remove it for camera-ready.
\documentclass[fleqn,10pt,lineno]{wlpeerj}

\usepackage{natbib}
\setcitestyle{authoryear,round}
\usepackage{tabularx}
\usepackage{array}
\usepackage{url}
\usepackage[hidelinks]{hyperref}
\usepackage{tikz}
\usetikzlibrary{positioning,calc,arrows.meta}

% wlpeerj loads Type 1 Times/Helvetica for pdflatex. The local build uses
% Tectonic (XeTeX), which cannot use them, so map to the TeX Gyre clones there.
% Under pdflatex (PeerJ, Overleaf) this block does nothing.
\usepackage{iftex}
\ifXeTeX
  \usepackage{fontspec}
  \setmainfont{texgyretermes}[Extension=.otf, UprightFont=*-regular,
    BoldFont=*-bold, ItalicFont=*-italic, BoldItalicFont=*-bolditalic]
  \setsansfont{texgyreheros}[Extension=.otf, UprightFont=*-regular,
    BoldFont=*-bold, ItalicFont=*-italic, BoldItalicFont=*-bolditalic]
  \setmonofont{texgyrecursor}[Extension=.otf, UprightFont=*-regular,
    BoldFont=*-bold, ItalicFont=*-italic, BoldItalicFont=*-bolditalic]
\fi

% The PeerJ text block is narrower than TMLR's; let long \texttt tokens break.
\setlength{\emergencystretch}{3em}

% Version DOI of the Zenodo release that archives exactly this study
% (docs/reports/paper_bc/ZENODO_RELEASE.md). PENDING until the author publishes it;
% the submission gate fails while this placeholder is present.
\newcommand{\zenodoversiondoi}{\textbf{[ZENODO VERSION DOI PENDING]}}

\title{From Fidelity to Semantics: A Taxonomy of Explainable AI Evaluation
Metrics and a Paired Empirical Comparison of LIME and SHAP}

\author[1]{Jonathan Herrera-V\'asquez}
\affil[1]{Department of Computer Science, Universidad Americana de Europa
(UNADE), Canc\'un, Quintana Roo, Mexico}
\corrauthor[1]{Jonathan Herrera-V\'asquez}{jonnabio@gmail.com}

% Keywords are entered in the PeerJ submission form (wlpeerj prints none);
% the include stays so scripts/pubs/verify_sync.py sees the SSOT wiring.
\newcommand{\pjkeywords}[1]{}
\pjkeywords{\input{../../../pub/fragments/paper_bc_peerj_keywords_en.tex}}

\begin{abstract}
\input{../../../pub/fragments/paper_bc_peerj_abstract_en.tex}
\end{abstract}

\begin{document}

\flushbottom
\maketitle
\thispagestyle{empty}
"""

intro = L(70, 172)
background = must(L(173, 266), '\\section{Background and Definitions}', '\\section{Background}')

# ---- Materials and Methods ---------------------------------------------------
scoping = L(413, 525)
bench_intro = L(760, 779)
bench_intro = must(bench_intro,
    'Section~\\ref{sec:synthesis} established that proxy metrics dominate the\n'
    'current evidence base while human-grounded constructs remain underspecified.\n'
    'The present section fills',
    'As the gap analysis (Section~\\ref{sec:synthesis}) discusses, proxy metrics\n'
    'dominate the current evidence base while human-grounded constructs remain\n'
    'underspecified. The benchmark fills')
bench_intro = bench_intro.replace('The runs analysed in this section', 'The runs analysed here')
bench_intro = bench_intro.replace('whereas the present section is', 'whereas the present analysis is')
bench_design = demote(L(781, 931))

infra = r"""\subsubsection{Computing Infrastructure}
\label{sec:infrastructure}

% NEW (PeerJ AI Application checklist). Facts from environment.yml,
% requirements-frozen.txt and the worker manifests under
% experiments/exp2_scaled/worker_manifests/.
All experiments ran on CPU; no GPU acceleration was configured. The
reference software environment is Python~3.11 with scikit-learn~1.7.1,
XGBoost~3.1.2, SHAP~0.50.0, LIME~0.2.0.1, NumPy~2.2.6, pandas~2.3.3 and
SciPy~1.16.3, pinned in the repository's \texttt{environment.yml} and
\texttt{requirements-frozen.txt}. Runs were executed on several commodity
workstations under macOS, Windows and Linux (native and under the Windows
Subsystem for Linux), distributed by a claim-based work queue in which each
host commits its runs to its own results branch. Each run artifact records
its configuration, seed, timestamps and duration; processor and memory
specifications were not recorded, and the executing host is recorded only for
runs launched through the work queue. The consequence for the cost endpoint
is discussed in Section~\ref{sec:validity}."""

exp4_design = L(580, 593)
exp4_design = must(exp4_design, 'To empirically ground this concern, we conducted',
                   'To test whether LLM judges can serve as semantic evaluators (Gap~3,\n'
                   'Section~\\ref{sec:synthesis}), we conducted')
exp4_methods = ('\\subsection{LLM-Judge Reliability Study (EXP4)}\n\\label{sec:exp4_methods}\n\n'
                + exp4_design + '\n\n' + r"""% NEW (PeerJ AI policy: tool, version and complete prompts for AI used as a
% research component). Model IDs and settings are those of the supplement.
The original-cohort judges were \texttt{gpt-4o-mini} (OpenAI),
\texttt{claude-3-haiku-20240307} (Anthropic) and \texttt{gemini-1.5-flash}
(Google), with temperature~0.0 and a 512-token output limit. The replication
panel (Section~\ref{sec:exp4}) was \texttt{openai/gpt-5.4-mini},
\texttt{anthropic/claude-haiku-4.5} and \texttt{google/gemini-3.8-flash},
accessed through OpenRouter with temperature~0.0 and a 4000-token output
limit. The complete system instruction, per-instance user prompt and rubric
are given in Table~S1 of Supplemental Article~S1; the replication's rendered
prompts and raw responses are archived with the code (Section~\ref{sec:artifacts}).""")

methods = '\n\n'.join([
    RULE, '\\section{Materials and Methods}\n\\label{sec:methods}', RULE,
    '\\subsection{Scoping Review Protocol and Corpus Profile}\n\\label{sec:scoping}',
    scoping,
    '\\subsection{Paired Benchmark Design}\n\\label{sec:empirical}',
    bench_intro, bench_design, infra, exp4_methods,
])

# ---- Results ----------------------------------------------------------------
taxonomy = demote(L(268, 405))
taxonomy = must(taxonomy, '\\subsection{Taxonomy of XAI Evaluation Metrics}',
                '\\subsection{Taxonomy of Explainable AI Evaluation Metrics}')
taxonomy = taxonomy.replace('The central contribution of this section is', 'The central result of the taxonomy is')
bench_results = L(935, 1105)
exp3 = L(1106, 1204)
exp4_results = ('\\subsection{LLM-Judge Reliability (EXP4)}\n\\label{sec:exp4}\n\n'
                + L(594, 671))
results = '\n\n'.join([
    RULE, '\\section{Results}\n\\label{sec:results_all}', RULE,
    taxonomy,
    '\\subsection{Paired Benchmark Results}\n\\label{sec:results}',
    bench_results, exp3, exp4_results,
])

# ---- Discussion -------------------------------------------------------------
gap3 = L(566, 578).rstrip() + '\n' + (
    'The EXP4 reliability study (Section~\\ref{sec:exp4}) tests this concern\n'
    'directly.\n')
gaps = demote(L(526, 565) + '\n' + gap3)
architecture = L(673, 753)
architecture = architecture.replace('the EXP4 reliability result (Section~\\ref{sec:synthesis})',
                                    'the EXP4 reliability result (Section~\\ref{sec:exp4})')
recommendations = demote(L(1206, 1262))
validity = demote(L(1264, 1484))
host_limit = r"""
% NEW (2026-10-02): disclosed while porting, from the worker manifests.
\paragraph{Execution hosts and the cost endpoint.} Cost is per-instance
wall-clock time, and the runs were executed on several workstations whose
processor and memory specifications were not recorded
(Section~\ref{sec:infrastructure}). The two members of a paired cell are
matched on model, seed and $N$, but are not guaranteed to have run on the
same host. Absolute latencies, and the medians reported here, therefore
include between-host variance and should be read as indicative of this
environment rather than as hardware-normalized measurements. The quality
endpoints (fidelity, stability, sparsity, faithfulness gap) do not depend on
the host.
"""
future = demote(L(1486, 1522))
broader = L(1602, 1629)
discussion = '\n\n'.join([
    RULE, '\\section{Discussion}\n\\label{sec:discussion}', RULE,
    '\\subsection{Open Gaps in the Evaluation Literature}\n\\label{sec:synthesis}',
    gaps, architecture, recommendations, validity + '\n' + host_limit, future,
    '\\subsection{Broader Impact}\n\\label{sec:broader_impact}', broader,
])

conclusion = must(L(1631, 1666), '\\section{Conclusion}', '\\section{Conclusions}')

acks = r"""\section*{Acknowledgments}

% NEW (PeerJ: funders go in the Funding Statement of the submission form, not
% here; AI-use disclosure required by PeerJ Author Policies).
The author designed and directed this research. Generative AI tools
(Anthropic Claude, used through Claude Code) served as assistants under the
author's direction for language editing (grammar, spelling and wording),
programming support for the evaluation framework, and checking the
manuscript's numbers against the committed artifacts. The research
questions, study design, experimental protocol, choice of methods and
metrics, interpretation of the results and all conclusions are the
author's. The author reviewed every AI-assisted change, accepted or rejected
it, and takes full responsibility for the content. No AI tool generated
research data, figures or the reference list. Large language models were also
objects of study in EXP4, as described in Section~\ref{sec:exp4_methods}.
"""

# Availability: keep only the de-anonymised branch of the TMLR source.
avail = L(1524, 1561)
avail = must(avail, '\\ifdeanon{in the public repository\n\\url{https://github.com/jonnabio/xai-eval-framework}}%\n'
             '{in the anonymised artifact bundle supplied as supplementary material with\nthis submission}',
             'in the public repository\n\\url{https://github.com/jonnabio/xai-eval-framework}')
avail = must(avail, '\\ifdeanonymised\n', '')
avail = must(avail, '\\section{Code and Artifact Availability}', '\\section*{Data and Code Availability}')
avail = must(avail, '\\url{https://doi.org/10.5281/zenodo.21538180}', '\\zenodoversiondoi{}')
avail += ('\nThe artifact bundle from which every reported value re-derives is\n'
          'provided as Supplemental Data~S1.')

refs = L(1678, 2085)

body = '\n\n'.join([pre, intro, background, methods, results, discussion,
                    conclusion, acks, avail, refs, '\\end{document}\n'])

# NEW (PeerJ AI Application checklist): third-party datasets cited with DOIs.
# DOIs resolved through doi.org on 2026-10-02 (titles and years match).
body = must(body, r'UCI Adult dataset \citep{kohavi1996scaling}',
            r'UCI Adult dataset \citep{kohavi1996scaling,becker1996adult}')
body = must(body, r'Breast Cancer Wisconsin \citep{dua2019uci}',
            r'Breast Cancer Wisconsin \citep{dua2019uci,wolberg1993breast}')
body = must(body, r'German Credit \citep{dua2019uci}',
            r'German Credit \citep{dua2019uci,hofmann1994statlog}')
body = must(body, r'\bibitem[Bhatt et~al.(2020)', r'''\bibitem[Becker and Kohavi(1996)]{becker1996adult}
Becker, B. and Kohavi, R. (1996).
Adult [dataset].
UCI Machine Learning Repository.
\url{https://doi.org/10.24432/C5XW20}.

\bibitem[Bhatt et~al.(2020)''')
body = must(body, r'\bibitem[Holm(1979)]', r'''\bibitem[Hofmann(1994)]{hofmann1994statlog}
Hofmann, H. (1994).
Statlog ({German} credit data) [dataset].
UCI Machine Learning Repository.
\url{https://doi.org/10.24432/C5NC77}.

\bibitem[Holm(1979)]''')
body = must(body, r'\bibitem[Wu et~al.(2026)', r'''\bibitem[Wolberg et~al.(1993)Wolberg, Mangasarian, Street, and
  Street]{wolberg1993breast}
Wolberg, W., Mangasarian, O., Street, N., and Street, W. (1993).
Breast cancer {Wisconsin} (diagnostic) [dataset].
UCI Machine Learning Repository.
\url{https://doi.org/10.24432/C5DW2B}.

\bibitem[Wu et~al.(2026)''')

# Supplement references, PeerJ style ("Table S1", "Supplemental Article S1").
body = re.sub(r'Supplementary\s+Tables~?\s*S', 'Tables~S', body)
body = re.sub(r'Supplementary\s+Table~?S', 'Table~S', body)

code = '\n'.join(l for l in body.split('\n') if not l.lstrip().startswith('%'))
for bad in ('\\ifdeanon', '\\ifdeanonymised', '\\acks{', 'tmlr', 'TMLR'):
    assert bad not in code, bad
(D / 'paper_bc_peerjcs.tex').write_text(body, encoding='utf-8', newline='\n')
print('lines', body.count('\n'))


# ---- Supplemental Article S1 --------------------------------------------------
sup = (D / 'paper_bc_tmlr_supplementary.tex').read_text(encoding='utf-8').replace('\r\n', '\n').split('\n')
sup_body = '\n'.join(sup[35:435])  # lines 36..435: everything between \maketitle and \end{document}
sup_body = must(sup_body, r'\section*{Supplementary Material}', r'\section*{Supplemental Article S1}')
sup_pre = r"""%% PeerJ Computer Science: Supplemental Article S1 for paper_bc_peerjcs.tex.
%% Body copied verbatim from paper_bc_tmlr_supplementary.tex (tag
%% tmlr-submission-12779); only the preamble and title block differ.
\documentclass[11pt]{article}
\usepackage[letterpaper,margin=25mm]{geometry}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{tabularx}
\usepackage{array}
\usepackage{multirow}
\usepackage{url}
\usepackage{path}
\setlength{\emergencystretch}{3em}

\title{Supplemental Article S1\\[4pt]
\large From Fidelity to Semantics: A Taxonomy of Explainable AI Evaluation
Metrics and a Paired Empirical Comparison of LIME and SHAP}
\author{Jonathan Herrera-V\'asquez\\
\small Department of Computer Science, Universidad Americana de Europa (UNADE),\\
Canc\'un, Quintana Roo, Mexico}
\date{}

\begin{document}
\maketitle
"""
sup_out = sup_pre + sup_body + '\n' + r'\end{document}' + '\n'
code = '\n'.join(l for l in sup_out.split('\n') if not l.lstrip().startswith('%'))
for bad in ('tmlr', 'TMLR', r'\name', r'\addr', r'\openreview'):
    assert bad not in code, bad
(D / 'paper_bc_peerjcs_supplemental_S1.tex').write_text(sup_out, encoding='utf-8', newline='\n')
print('supplement lines', sup_out.count('\n'))
