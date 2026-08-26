# Claude Cowork loop prompt — retrieve the Paper B+C corpus PDFs

Copy everything between the `---` markers into Claude Cowork. It is self-contained:
the paper list is embedded, so it does not depend on reading this repo first.

Run it with `/loop` (no interval — let it self-pace), or paste it as a normal
prompt and it will still work, just in one pass.

---

You are retrieving open-access PDFs for a systematic review corpus. Work through
the list below in batches, keeping a ledger so each run continues where the last
stopped. Stop when every paper is either `DONE` or `FAILED`.

## Repository

`c:\Users\jonna\Github\xai-eval-framework`

## Where files go

Save every PDF to:

```
docs/reports/paper_bc/corpus_pdfs/<citation_key>.pdf
```

Named by the **citation key exactly as given below**, lowercase, `.pdf` extension.
For example `adebayo2018sanity.pdf`, `zheng2023judging.pdf`.

Do not use the paper title as a filename. The citation key is the join between
the PDF, the bibliography entry in `docs/reports/paper_bc/paper_bc_jmlr.tex`, and
the `record_slug` column of the corpus CSV. A wrong filename silently breaks that
link.

Create the directory if it does not exist. Do not touch `thesis/papers/` — that is
a different collection and must be left exactly as it is.

## Ledger — read this first, write it every batch

`docs/reports/paper_bc/corpus_pdfs/RETRIEVAL_LOG.md`

One line per paper:

```
| citation_key | STATUS | source_url | note |
```

`STATUS` is `DONE`, `FAILED`, or `PENDING`. On the first run, create it with every
key set to `PENDING`. On each later run, read it first and skip anything already
`DONE` or `FAILED`.

## Procedure, per paper

1. If a link is given, try it first. Prefer the publisher's open-access PDF, then
   arXiv, then the ACM/ACL/PMLR/NeurIPS open proceedings version.
2. If no link is given, search by the exact title. All of these are indexed
   conference or journal papers.
3. Verify before saving: the file must be a real PDF (starts with `%PDF`), larger
   than 50 KB, and its first page title must match the paper you were asked for.
   A landing page, a cookie wall, or an HTML error saved as `.pdf` is a FAILED,
   not a DONE.
4. Save to the path above and mark `DONE` with the URL you actually used.
5. If the paper is paywalled with no open-access version, mark `FAILED` with the
   reason. **Do not substitute a different paper, a preprint of a different
   study, a slide deck, or a summary.** A missing entry is fine; a wrong entry
   corrupts the corpus.

Work in batches of about 6, updating the ledger after each batch so progress
survives an interruption.

## Checking progress

After each batch:

```bash
cd c:\Users\jonna\Github\xai-eval-framework
python scripts/pubs/check_corpus_pdfs.py
```

It prints how many of the tracked papers now have a PDF and lists what is left.
It is non-strict, so it is safe to run mid-task.

## Stop condition

Stop when `check_corpus_pdfs.py` reports no remaining papers from the list below,
or when every line in the ledger is `DONE` or `FAILED`. Then post a summary:
count DONE, count FAILED, and the failed keys with reasons.

Do not commit anything to git. Leave that to the repository owner.

## The 27 papers

### Group 1 — confirmed corpus members (10)

| citation_key | year | title | link |
|---|---|---|---|
| `adebayo2018sanity` | 2018 | Sanity checks for saliency maps | search by title (NeurIPS 2018) |
| `alvarezmelis2018robustness` | 2018 | On the robustness of interpretability methods | https://arxiv.org/abs/1806.08049 |
| `bucinca2020proxy` | 2020 | Proxy tasks and subjective measures can be misleading in evaluating explainable AI systems | search by title (IUI 2020) |
| `gu2024llmjudge` | 2024 | A survey on LLM-as-a-Judge | https://doi.org/10.48550/arXiv.2411.15594 |
| `hase2020evaluating` | 2020 | Evaluating explainable AI: Which algorithmic explanations help users predict model behavior? | https://doi.org/10.18653/v1/2020.acl-main.491 |
| `kaur2020interpreting` | 2020 | Interpreting interpretability: Understanding data scientists' use of interpretability tools for machine learning | https://doi.org/10.1145/3313831.3376219 |
| `nauta2023anecdotal` | 2023 | From anecdotal evidence to quantitative evaluation methods: A systematic review on evaluating explainability | https://doi.org/10.1145/3583558 |
| `rong2022consistent` | 2022 | A consistent and efficient evaluation strategy for attribution methods | search by title (ICML 2022) |
| `yeh2019infidelity` | 2019 | On the (in)fidelity and sensitivity of explanations | https://arxiv.org/abs/1901.09392 |
| `zheng2023judging` | 2023 | Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena | https://doi.org/10.48550/arXiv.2306.05685 |

### Group 2 — candidate corpus members (17)

| citation_key | year | title | link |
|---|---|---|---|
| `ali2023trustworthy` | 2023 | Explainable Artificial Intelligence (XAI): What we know and what is left to attain Trustworthy Artificial Intelligence | https://doi.org/10.1016/j.inffus.2023.101805 |
| `bansal2021whole` | 2021 | Does the whole exceed its parts? The effect of AI explanations on complementary team performance | search by title (CHI 2021) |
| `burkart2021survey` | 2021 | A survey on the explainability of supervised machine learning | https://doi.org/10.1613/jair.1.12228 |
| `canha2025benchmark` | 2025 | A functionally-grounded benchmark framework for XAI methods: Insights and foundations from a systematic literature review | https://doi.org/10.1145/3737445 |
| `fok2023verifiability` | 2023 | In search of verifiability: Explanations rarely enable complementary performance in AI-advised decision making | search by title (AI Magazine 2023) |
| `haufe2026formalization` | 2026 | Explainable AI needs formalization | https://doi.org/10.1038/s44387-026-00095-1 |
| `hooker2019benchmark` | 2019 | A benchmark for interpretability methods in deep neural networks | search by title (NeurIPS 2019, ROAR) |
| `jacovi2020faithfulness` | 2020 | Towards faithfully interpretable NLP systems: How should we define and evaluate faithfulness? | search by title (ACL 2020) |
| `kumar2020problems` | 2020 | Problems with Shapley-value-based explanations as feature importance measures | https://arxiv.org/abs/2002.11097 |
| `mohseni2021survey` | 2021 | A multidisciplinary survey and framework for design and evaluation of explainable AI systems | https://doi.org/10.1145/3387166 |
| `retzlaff2024posthoc` | 2024 | Post-hoc vs ante-hoc explanations: xAI design guidelines for data scientists | https://doi.org/10.1016/j.cogsys.2024.101243 |
| `slack2020fooling` | 2020 | Fooling LIME and SHAP: Adversarial attacks on post hoc explanation methods | https://doi.org/10.1145/3375627.3375830 |
| `sokol2020factsheets` | 2020 | Explainability fact sheets: A framework for systematic assessment of explainable approaches | search by title (FAccT 2020) |
| `wilming2022scrutinizing` | 2022 | Scrutinizing XAI using linear ground-truth data with suppressor variables | search by title (Machine Learning journal 2022) |
| `wilming2023theoretical` | 2023 | Theoretical behavior of XAI methods in the presence of suppressor variables | search by title (ICML 2023) |
| `wu2025userperceptions` | 2025 | User perceptions vs. proxy LLM judges: Privacy and helpfulness in LLM responses to privacy-sensitive scenarios | https://doi.org/10.48550/arXiv.2510.20721 |
| `zhou2025medthink` | 2025 | Automating expert-level medical reasoning evaluation of large language models | https://doi.org/10.1038/s41746-025-02208-7 |

---

## After the loop finishes

Back in this repo:

```bash
# 1. copy the 17 already-held PDFs in under their citation keys
python scripts/pubs/check_corpus_pdfs.py      # prints the source filename for each

# 2. build the corpus CSV -- 16 rows arrive pre-coded from the audit record
python scripts/pubs/seed_corpus_from_audit.py

# 3. code the remaining rows, then check against the manuscript
python scripts/pubs/check_review_corpus.py \
    --corpus docs/reports/paper_bc/paper_bc_review_corpus.csv --expect paper_bc
```

Any `FAILED` entries are worth keeping in the ledger rather than deleting: a
corpus that documents which sources could not be obtained is more defensible
than one that quietly omits them.
