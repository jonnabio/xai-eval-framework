# Paper G — pre-submission review (2026-11-17)

Session `claude-2026-11-17`, Windows documentation laptop, branch `paper/g-metric-agreement`.
Object: `paper_g_draft.md` / `paper_g.md` and `submission/paper_g_blind.docx` (13 pages) at `26ef7106f` + `main`.
Nothing in the manuscript was changed by this review. Each item marked **[Author]** is the author's decision.

## A. Integrity checks (all pass)

| Check | Result |
|---|---|
| `verify_claims.py` | 2,083 claims re-derived, 2,500 sites, 66 retired-value guards clear |
| `register_paper_g.py --check` | 185 Paper G claims OK |
| `verify_sync.py` | OK |
| `verify_equations.py` | 480 checks, 0 disagreements |
| `paper_g_analyze.py --validate-only` | OK (160 full blocks, 147 degenerate M4 rows) |
| Paper G tests (Windows) | 131 passed, 3 skipped (fork-only S1 driver tests; they run on Linux) |
| Independent recomputation of H1 from `raw/full` and `raw/roar` (own script, not the pipeline) | 0.723 [0.645, 0.802], identical to the manuscript |
| References (`REFERENCE_VERIFICATION.md`) | 50/50 verified; 84% from 2024+; 92% scholarly; all cited |

## B. Venue and template compliance (*Informática y Sistemas*, template `ISRTIC_Plantilla_Articulo-EN.docx`)

The repository's `venue/template/IyS_article_template.docx` is byte-identical to `ISRTIC_Plantilla_Articulo-EN.docx`; the build uses its styles, page size, margins and running header.

| Requirement (source) | Status |
|---|---|
| English, journal template (checklist) | Pass |
| Abstract 150–250 words, one paragraph (template, checklist) | Pass: 220 words |
| 3–5 keywords, semicolon-separated (template) | Pass: 5 |
| Length 8–16 pages incl. references (guidelines, recommended) | Pass: 13 |
| Numbered headings 1–4, first letter capitalised; back matter unnumbered in the template order (template B) | Pass |
| **Title: "capitalize only the first letter and proper nouns" (template)** | **Fail**: title is in Title Case. Fix: *Do faithfulness metrics agree? Metric-dependent rankings of post-hoc explanations on tabular data* |
| APA 7, (Surname, Year) citations, DOI when available, ≥10 refs, ≥90% scientific articles, no web pages (template, checklist) | Pass (6 entries without DOI because none exists: NeurIPS 2017/2019, TMLR, ICLR, and 3 anonymised own manuscripts; 1 arXiv preprint, shanklin2026) |
| Figures as separate files, named `Figure_n`, ≥300 dpi (site) / 600 dpi for charts (template) | Pass: PNG at 600 dpi plus SVG |
| Tables: caption above, source below, horizontal rules only, repeated header row (template) | Pass on header repeat; rules and centring come from the template styles: confirm in Word |
| Equations numbered on the right in parentheses, separated by a blank line (template) | **Check in Word**: the number is typed inside the equation object, not right-aligned by a tab |
| Five declaration sections, completed "even when the answer is none" (checklist) | **Fail until completed**: Funding, Author contributions, Conflicts of interest and the AI declaration still hold bracketed placeholders **[Author]** |
| Double-blind: no names, affiliations, emails or acknowledgements (checklist) | Pass in the file. Risk: repository public under the author's name since 2026-11-13 **[Author]** |
| Similarity ≤10% and AI-generated content ≤30% (Compilatio); over either limit the paper is returned unreviewed | **Highest administrative risk.** The AI declaration states that Claude drafted the text of all sections; unless the author rewrites substantially, the 30% limit is likely exceeded **[Author]** |
| Ethics statement if human data (checklist) | Pass: public de-identified tables, stated in 2.2 |
| OJS: metadata, ORCID, Supporting Agencies ("None" if none), keywords entered one by one, licence CC BY-NC-ND 4.0, no fees | At submission **[Author]** |

## C. Reviewer simulation (CLEIej rubric)

**Pass 1 — claim in one sentence.** Across seven faithfulness metrics, eight tabular datasets and three explainers, metric agreement on explainer rankings is broad only when one explainer's output is mis-represented; with LIME represented as contributions agreement is moderate, falls further under a second masking baseline, and instance-level agreement is weak throughout. Category: experimental work (correctly declared as research article).

**Pass 2 — evidence markers.** Every quantitative claim maps to Table 4, Figures 1–5 or Section 3 and is registered (185 claims). Hypotheses, statistic, unit of inference, permutation test, Holm correction and decision rule are stated before the method; dispersion and intervals accompany every estimate.

**Pass 3 — provenance.** 50 verified references; closest works: Duan et al. 2024, Edin et al. 2025, Miró-Nicolau et al. 2025, Shanklin et al. 2026, Ababneh et al. 2026. Code and data released (identifier withheld for review).

### Ratings a careful reviewer would give now

| Dimension | Score | Main reason |
|---|---|---|
| Originality | 4 | Clear delta (paired multi-metric agreement on tabular data, stability benchmark, representation finding); no positioning table |
| Presentation | 3 | Dense; notation clash; long Table 4 caption; abstract hard to parse |
| Relevance | 4 | Practical recommendations; the reason for this journal's readership is implicit |
| Technical soundness | 3 | Strong pre-specification, but the headline now rests on post-hoc S1, and one alternative explanation is not addressed (M1 below) |
| Related work | 4 | Current and verified; benchmark-library tradition missing |
| Likely recommendation | — | **Major revision** as it stands; **minor revision** if M1–M4 are done before submission |

### Major concerns a reviewer is likely to raise (fix before submission)

- **M1 (R14, soundness). Lower stability as an alternative explanation for the S1 drop.** With S1-B the within-metric stability benchmark also falls (0.873 → 0.797, Table 4). Part of the fall in between-metric agreement (0.723 → 0.529) may therefore come from LIME-contribution rankings being noisier, not from metrics disagreeing more. The ratio between and within is 0.83 originally and 0.66 with S1-B, so a drop remains, but the paper does not say so. Action: one sentence in 3.4 and 3.8 (and a registered value for the ratio, or a per-dataset comparison against the benchmark, which Figure 3 already shows).
- **M2 (R3, soundness). Framing of the pre-specified result.** The abstract reports the decision ("broadly agreed") and then states it was obtained under a mis-represented explainer. A reviewer can read this as "the confirmatory result is an artefact; the conclusions rest on unconfirmed analyses". The paper is honest about this, but the sentence "LIME had been stored as local slopes rather than contributions" sounds like an implementation error. Action: describe it as a configuration choice whose output semantics (slopes) differ from what the metrics assume, which is what Section 2.3 says, and state in the abstract that S1 is supplementary and carries no test decision.
- **M3 (R34, presentation). Notation clash.** *b* is the masking baseline (2.4) and also the block index (Eq. 4, *D*~*b*~, ρ̄~*b*~). Action: rename the block index to an unused symbol (*k*, *ℓ* and *j* are already taken; *u* is free). Also define ρ~*s*~ as "Spearman correlation (Pearson correlation of rank vectors)".
- **M4 (R22, reproducibility). Parameter table.** Model hyperparameters ("one configuration ... recorded before training") are not reported. Action: add an appendix table (model settings, SHAP background size and algorithm, LIME parameters, occlusion baseline, M5 *R*, M7 shares, seeds, package versions), or a supplementary file referenced from 2.7.

### Minor concerns

- R26/R31: a short positioning table (5 closest works, one differentiator each) would settle originality in one place.
- R27: the benchmark-library tradition is absent: Quantus (Hedström et al., 2023, JMLR) and OpenXAI (Agarwal et al., 2022, NeurIPS Datasets and Benchmarks), both of which bundle faithfulness metrics for tabular data. Both are pre-2024; adding them keeps the 2024+ share at 42/52 = 81% (still ≥80%). Verify against the source before adding.
- Relevance: one sentence in the introduction on why this matters to the journal's readership (practitioners in Latin America using SHAP/LIME on tabular data).
- Table 4 caption: replace "the first, second, sixth and seventh rows" with a column or row marker.
- *p*-value style is mixed (".05" in Table 3, "0.00001" in text); APA 7 omits the leading zero for *p*.
- Section 3.8 marks every statement as *Observed / Property / Mechanism*. This is rigorous but reads as mechanical; a reviewer may ask to simplify.
- The random control was last under all seven metrics in only 15/160 blocks originally (3.7); state in 3.1 that this was already a signal of the representation problem, since a reviewer will notice it.
- Section "Source: Authors." with a single author: kept, as the template prescribes this wording.

### What a reviewer will value (keep)

Pre-specification with a dated evidence-class table (Table 1); dataset as the unit of inference with a permutation test justified by a simulation; within-metric stability benchmark; random control; the synthetic ground-truth check (S3); transparent reporting of the deviation (omitted variance shares) and of the post-hoc status of S1.

## Applied on 2026-11-17 (author's instruction)

Title in sentence case; M1 (stability benchmark as an alternative explanation, Sections 3.4 and 3.8);
M2 (abstract describes LIME's slope output as a configuration property and states that S1 is
supplementary with no test decision); M3 (block index renamed *u*; ρ~*s*~ defined as Spearman);
M4 (Appendix A, parameter table from `experiments/exp_g/config.toml` and `host.json`, cited in 2.7);
the AI-use declaration replaced with the author's text. `paper_g.md` rebuilt; claims and
`verify_claims` pass; abstract 229 words. The `.docx` and `.pdf` were **not** rebuilt (no pandoc or
LibreOffice on this laptop). Minor items and items 2–4 below remain open.

## D. Remaining author actions before submission

1. Decide M1–M4 and the minor items (the assistant can draft each change).
2. Fix the title case.
3. Complete the four declarations; in the AI declaration, state the extent of the author's own review and any other assistant used.
4. Address the 30% AI-content limit (substantive rewriting by the author) and the double-blind risk.
5. Rebuild the `.docx` (pandoc and LibreOffice are not installed on this laptop: rebuild on the Linux host, or install them here) and check equations, tables and pagination in Word.
6. Re-run `register_paper_g.py` and `verify_claims.py` after any edit.
