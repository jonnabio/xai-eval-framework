# Paper B+C corpus — PDFs to retrieve

> **Status 2026-08-26: collection complete — 44/44.**
> 25 retrieved automatically by `scripts/pubs/fetch_corpus_pdfs.py`, 17 copied
> from `thesis/papers/`, and 2 (`kaur2020interpreting`, `retzlaff2024posthoc`)
> supplied manually by the author from institutional access and verified on
> arrival. Per-paper provenance is in `corpus_pdfs/RETRIEVAL_LOG.md`.
> The list below is retained as the record of what was needed.

Generated from `corpus_pdf_manifest.csv`. Resolves the retrieval half of finding A14.

| | count |
|---|---|
| Corpus papers tracked | 44 |
| Already in `thesis/papers/` | 17 |
| **To retrieve** | **27** |

Of the 48 the manuscript claims, 44 are identifiable from the citation record;
the remaining ~4 were coded but never cited, and cannot be recovered from the
paper. See `REVIEW_CORPUS.md`.

## Where to put them

```
thesis/papers/                     <- existing library, leave as is
docs/reports/paper_bc/corpus_pdfs/ <- NEW: put retrieved PDFs here
```

A separate folder, for three reasons: `thesis/papers/` is the thesis reading
library and mixing the two loses the distinction; it already carries 92
`- Copy` duplicates that would confuse any automated count; and the corpus
needs a one-to-one file-per-coded-paper mapping that the library does not have.

**Filename convention — use the citation key exactly:**

```
docs/reports/paper_bc/corpus_pdfs/<citation_key>.pdf

e.g. adebayo2018sanity.pdf
     zheng2023judging.pdf
```

This is what makes the rest automatable: the key is the join between the PDF,
the bibliography entry, and the `record_slug` column of the corpus CSV. Do not
use paper titles as filenames.

For the 17 already present, either copy them in under the citation-key name or
symlink them; the checker only cares that `<key>.pdf` resolves.

## To retrieve (27)

`link` comes from the bibliography where the entry carries a DOI or arXiv id.
Where it is blank the reference had no identifier, so search by exact title —
all are well-indexed venue papers.

| # | citation key | year | title | link |
|---|---|---|---|---|
| 1 | `adebayo2018sanity` | 2018 | Sanity checks for saliency maps | _search by title_ |
| 2 | `alvarezmelis2018robustness` | 2018 | On the robustness of interpretability methods | https://arxiv.org/abs/1806.08049 |
| 3 | `bucinca2020proxy` | 2020 | Proxy tasks and subjective measures can be misleading in evaluating explainable AI systems | _search by title_ |
| 4 | `gu2024llmjudge` | 2024 | A survey on LLM-as-a-Judge | https://doi.org/10.48550/arXiv.2411.15594 |
| 5 | `hase2020evaluating` | 2020 | Evaluating explainable AI: Which algorithmic explanations help users predict model behavior? | https://doi.org/10.18653/v1/2020.acl-main.491 |
| 6 | `kaur2020interpreting` | 2020 | Interpreting interpretability: Understanding data scientists' use of interpretability tools for machine learning | https://doi.org/10.1145/3313831.3376219 |
| 7 | `nauta2023anecdotal` | 2023 | From anecdotal evidence to quantitative evaluation methods: A systematic review on evaluating explainability | https://doi.org/10.1145/3583558 |
| 8 | `rong2022consistent` | 2022 | A consistent and efficient evaluation strategy for attribution methods | _search by title_ |
| 9 | `yeh2019infidelity` | 2019 | On the infidelity and sensitivity of explanations | https://arxiv.org/abs/1901.09392 |
| 10 | `zheng2023judging` | 2023 | Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena | https://doi.org/10.48550/arXiv.2306.05685 |
| 11 | `ali2023trustworthy` | 2023 | Explainable Artificial Intelligence (XAI): What we know and what is left to attain Trustworthy Artificial Intelligence | https://doi.org/10.1016/j.inffus.2023.101805 |
| 12 | `bansal2021whole` | 2021 | Does the whole exceed its parts? | _search by title_ |
| 13 | `burkart2021survey` | 2021 | A survey on the explainability of supervised machine learning | https://doi.org/10.1613/jair.1.12228 |
| 14 | `canha2025benchmark` | 2025 | A functionally-grounded benchmark framework for XAI methods: Insights and foundations from a systematic literature review | https://doi.org/10.1145/3737445 |
| 15 | `fok2023verifiability` | 2023 | In search of verifiability: Explanations rarely enable complementary performance in AI-advised decision making | _search by title_ |
| 16 | `haufe2026formalization` | 2026 | Explainable AI needs formalization | https://doi.org/10.1038/s44387-026-00095-1 |
| 17 | `hooker2019benchmark` | 2019 | A benchmark for interpretability methods in deep neural networks | _search by title_ |
| 18 | `jacovi2020faithfulness` | 2020 | Towards faithfully interpretable NLP systems: How should we define and evaluate faithfulness? | _search by title_ |
| 19 | `kumar2020problems` | 2020 | Problems with Shapley-value-based explanations as feature importance measures | https://arxiv.org/abs/2002.11097 |
| 20 | `mohseni2021survey` | 2021 | A multidisciplinary survey and framework for design and evaluation of explainable AI systems | https://doi.org/10.1145/3387166 |
| 21 | `retzlaff2024posthoc` | 2024 | Post-hoc vs ante-hoc explanations: xAI design guidelines for data scientists | https://doi.org/10.1016/j.cogsys.2024.101243 |
| 22 | `slack2020fooling` | 2020 | Fooling LIME and SHAP: Adversarial attacks on post hoc explanation methods | https://doi.org/10.1145/3375627.3375830 |
| 23 | `sokol2020factsheets` | 2020 | Explainability fact sheets: A framework for systematic assessment of explainable approaches | _search by title_ |
| 24 | `wilming2022scrutinizing` | 2022 | Scrutinizing XAI using linear ground-truth data with suppressor variables | _search by title_ |
| 25 | `wilming2023theoretical` | 2023 | Theoretical behavior of XAI methods in the presence of suppressor variables | _search by title_ |
| 26 | `wu2025userperceptions` | 2025 | User perceptions vs.\ proxy LLM judges: Privacy and helpfulness in LLM responses to privacy-sensitive scenarios | https://doi.org/10.48550/arXiv.2510.20721 |
| 27 | `zhou2025medthink` | 2025 | Automating expert-level medical reasoning evaluation of large language models | https://doi.org/10.1038/s41746-025-02208-7 |

## Already present (17)

| citation key | file in `thesis/papers/` |
|---|---|
| `adadi2018xai` | Peeking_Inside_the_Black-Box_A_Survey_on_Explainable_Artificial_Intelligence_XAI.pdf |
| `agarwal2022openxai` | OpenXAI- Towards a Transparent Evaluation of Post hoc Model Explanations.pdf |
| `agarwal2023gnn_eval` | Evaluating explainability for graph neural networks.pdf |
| `arrieta2020xai` | Explainable Artificial Intelligence (XAI) Concepts, taxonomies, opportunities and challenges toward responsible AI.pdf |
| `doshivelez2017rigorous` | Towards A Rigorous Science of Interpretable Machine Learning.pdf |
| `hedstrom2023quantus` | Quantus- An Explainable AI Toolkit for Responsible Evaluation of Neural Network Explanations and Beyond.pdf |
| `kadir2023metrics` | 14708_XAI_Evaluation_Metrics__Taxonomies__Concepts_and_Applications__INES_2023_-7.pdf |
| `longo2024manifesto` | Explainable Artificial Intelligence (XAI) 2.0  A manifesto of open challenges and interdisciplinary research directions.pdf |
| `lundberg2017unified` | SHAP-a-unified-approach-to-interpreting-model-predictions-Paper.pdf |
| `mothilal2020dice` | Explaining Machine Learning Classifiers through Diverse Counterfactual Explanations.pdf |
| `pawlicki2024metrics` | Evaluating the necessity of the multiple metrics for assessing explainable AI A critical examination.pdf |
| `proszewska2025bxaic` | B-XAIC Dataset Benchmarking Explainable AI for Graph Neural Networks Using Chemical Data.pdf |
| `ribeiro2016why` | LIME_Explaining the Predictions of Any Classifier.pdf |
| `ribeiro2018anchors` | Anchors High-Precision Model-Agnostic Explanations.pdf |
| `rudin2019stop` | Stop Explaining Black Box Machine Learning Models.pdf |
| `wachter2017counterfactual` | Counterfactual Explanations Without Opening the Black BoxAutomated Decisions and the GDPR.pdf |
| `zheng2025ffidelity` | F-FIDELITY A ROBUST FRAMEWORK FOR FAITHFULNESS EVALUATION OF EXPLAINABLE AI.pdf |

## After retrieving

```bash
# 1. confirm every tracked key now has a PDF
python scripts/pubs/check_corpus_pdfs.py

# 2. build the corpus CSV -- 16 rows come free from the audit data
python scripts/pubs/seed_corpus_from_audit.py

# 3. code the remainder, then check against the manuscript
python scripts/pubs/check_review_corpus.py \
    --corpus docs/reports/paper_bc/paper_bc_review_corpus.csv --expect paper_bc
```

Step 2 pre-fills the 16 papers whose original four-axis coding survives in
`second_reviewer_audit_results.csv`, so only the remaining rows need coding.

