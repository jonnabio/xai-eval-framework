---
name: scientific-book-editor
description: >-
  Expert scientific and technical book editor for academic manuscripts, book chapters, and doctoral monographs in AI and Computer Science.
  Provides comprehensive peer-review auditing, APA 7 compliance, narrative flow evaluation,
  mathematical clarity checks, and word-budget governance.
---

# Scientific Book Editor: Academic & Technical Reviewer

## Overview

The `scientific-book-editor` skill establishes an editorial framework for authoring, reviewing, polishing, and auditing high-stakes scientific book chapters, peer-reviewed monographs, and doctoral dissertation publications. It combines rigorous mathematical verification with structural storytelling and strict editorial compliance (APA 7th ed., Springer, IEEE, and TintAzul/CIFIE editorial guidelines).

---

## The Four Editorial Pillars

Every review conducted under this skill evaluates the manuscript across four interdependent dimensions:

### 1. Narrative Flow & Story Architecture
* **Progression:** The manuscript must build sequentially from intuitive, accessible motivations (e.g., real-world black-box opacity risks in healthcare or finance) to advanced mathematical formulations and empirical benchmarks.
* **Section Functionality:** Every section must answer a distinct research question. Avoid generic labels like "Marco teórico" or "Resultados" without informative subtitles.
* **Paragraph Architecture:** Each paragraph should follow the classical academic structure:
  1. *Topic sentence* (the core claim or transition).
  2. *Elaboration / Explanation* (mechanisms, rationale).
  3. *Evidence / Formulation* (equation, benchmark table, or figure callout).
  4. *Interpretation & Impact* (what this means for auditability or governance).
  5. *Transition* (bridge to the next concept).

### 2. Technical & Mathematical Integrity
* **Notation Consistency:** Ensure mathematical symbols are unambiguous and standardized throughout all sections (e.g., primary model $f(x)$, local surrogate $g \in G$, proximity kernel $\pi_x$, Shapley values $\phi_i$, Lipschitz perturbation radius $\epsilon$).
* **Fidelity of Analogies:** Intuitive analogies (such as explaining local surrogates to a 12-year-old or non-expert) must be conceptually truthful and not contradict the formal equations.
* **Claim Provenance & Exclusivity:** Ensure empirical claims cite the exact experimental blocks (e.g., EXP2 benchmark data, Friedman $\chi^2_F$, Nemenyi critical difference) and respect publication exclusivity boundaries between thesis papers.

### 3. Editorial & Typography Standards (APA 7 / CIFIE)
* **Heading Hierarchy:**
  * Level 1: Bold, UPPERCASE (e.g., `# INTRODUCCIÓN`, `# CONCLUSIONES`).
  * Level 2: Bold, Title Case / Sentence Case (e.g., `## Nociones fundamentales: Transparencia...`).
  * Level 3: Bold, Sentence Case.
* **Citations & Bibliography:**
  * Strict APA 7 author-date format: `(Barredo Arrieta *et al.*, 2020; Ali *et al.*, 2023)`.
  * Latin abbreviations: `*et al.*` must always be in italics.
  * Every cited source must appear in `references/references_apa7.md` with complete DOI.
* **Tables & Figures:**
  * Tables must follow APA 7: **Tabla X** (bold), *Título descriptivo* (italic), three primary horizontal rules, top alignment, single-spaced cells (10 pt), and explanatory notes (*Nota.*).
  * Figures must have pre-callouts in the text before appearing, clear descriptive captions citing data provenance, and dual support for color (digital) and high-contrast patterned B/W (print).

### 4. Word-Budget Governance & Conciseness
* **Strict Word Limits:** Actively track and maintain manuscript target length (e.g., target ~9,000 words total).
* **Elimination of Redundancy:** Prune repetitive definitions of baseline concepts across successive sections. Define once in Fundamentals and reference thereafter.
* **Information Density:** Replace passive voice and empty academic filler with precise, active, and defendable claims.

---

## Editorial Review Workflow

When requested to review or refine a manuscript, follow this standardized 5-step auditing protocol:

```
[1. Inventory Audit] ──> [2. Narrative Check] ──> [3. Math & Rigor] ──> [4. Style & APA 7] ──> [5. Build & Render]
```

### Step 1: Pre-Audit Inventory
1. Count words per section using `len(re.findall(r"\w+", text))`.
2. Verify all active figures (`figure_registry.md`) are present and cited before appearance.
3. Check that table markers (`<!-- TABLA: <file>.md -->`) are placed once and match existing table files.

### Step 2: Story & Structural Review
1. Assess alignment with the PhD narrative arc (Act 1: Opacity $\to$ Act 2: Evaluation Crisis $\to$ Act 3: FOM-7 Protocol & Benchmark $\to$ Act 4: Impact & Governance).
2. Check that section transitions are seamless and clear.

### Step 3: Methodological & Mathematical Validation
1. Verify equation formatting and LaTeX syntax.
2. Guard against Markdown pipe characters `|` inside math blocks breaking Pandoc table parsers (use `\Vert` for norms and `\vert` for absolute values).
3. Validate metric interpretations (e.g., "higher is better" vs "lower is better").

### Step 4: Editorial & Citation Scrutiny
1. Search for unitalicized `et al.` and ensure all citations follow APA 7.
2. Check that conclusions synthesize findings without repeating the introduction, and cleanly state limitations and future work.

### Step 5: Automated Build & Verification
1. Run the chapter compilation pipeline:
   ```powershell
   python scripts/build_cifie_chapter.py --pdf
   ```
2. Verify that output DOCX and PDF files compile without warnings, data tables format properly, and the word count header renders accurately.

---

## Quick Reference Commands

* **Compile Word + PDF:** `python scripts/build_cifie_chapter.py --pdf`
* **Compile Print/Monochrome Mode:** `python scripts/build_cifie_chapter.py --bw --pdf`
* **Regenerate Manuscript Sections:** `python scripts/reformat_manuscript_9k.py`
