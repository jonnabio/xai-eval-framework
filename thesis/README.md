# Doctoral Thesis Production Workflow

This directory contains the "Source-First" production pipeline for the PhD thesis. It uses **Quarto** to manage professional academic writing and export it to an institutional Microsoft Word template.

## 📁 Directory Structure

- `index.qmd`: Parent file containing the Abstract and Front Matter.
- `01-06- chapters.qmd`: The individual chapters of the thesis.
- `references.bib`: The BibTeX database for all citations.
- `assets/`: Contains the official university Word template (`Plantilla_Tesis_Doctorado.docx`).
- `render.ps1`: Automation script to compile the thesis.

## 🚀 How to Render

To generate the full thesis draft in Word, run the following command in PowerShell:

```powershell
./render.ps1
```

The output document will be created at: `thesis/_output/index.docx`.

## ✍️ Writing and Citing

## Evidence Integration

Before updating Chapter 4 result narratives, regenerate the integrated evidence
handoff:

```powershell
python3 scripts/integrate_experiment_evidence.py
```

Use the generated thesis fragment as the working source for the EXP1/EXP2/EXP3
integration discussion:

- `outputs/analysis/integrated_evidence/thesis_fragment_es.qmd`

The integration procedure is documented in
`docs/analysis/EXP1_EXP2_EXP3_INTEGRATION_PIPELINE.md`.

### Citations
Do not type references manually. Use the citation keys from `references.bib`:
- Parenthetical: `[@adadi2018]` -> (Adadi & Berrada, 2018)
- Narrative: `@ribeiro2018 said...` -> Ribeiro et al. (2018) said...

### Cross-References
To refer to a specific chapter or section:
- `[See Section @sec-intro]` (requires adding `{#sec-intro}` to a heading).

## 📄 Final Polishing in Word

Because Microsoft Word handles its own internal pagination and Table of Contents, perform these two steps after every render:
1. Open `_output/index.docx`.
2. Right-click the **Table of Contents** and select **Update Field** -> **Update entire table**.
3. Save as your final distribution version.

---
**Standard**: Optimized for PhD submission to university repositories.
