# Reference Audit: Paper B+C (TMLR submission)

**Date**: 2026-09-28 | **Reviewer role**: Scientific Advisor | **Skill**: `reference-audit`
**Scope**: the embedded `thebibliography` of `docs/reports/paper_bc/paper_bc_tmlr.tex`, and every
`\citep`/`\citet` in its body. The supplementary cites nothing.
**Plan**: `docs/planning/paper_bc_tmlr_remediation_plan_2026-09-28.md`, Step 0.1. Report-only; no
file was edited.
**Method**:
- Keys were parsed from the source. Every entry with a DOI was resolved through the Crossref API;
  entries without a DOI were queried by title.
- A title query that returned an unrelated work counts as **unverified**, not as a mismatch. Those
  entries were checked against the known venue record; the ones that still could not be confirmed
  are listed as unverified below.

## Summary

| Check | Count |
|---|---|
| Entries | 60 |
| Orphans (cited, no entry) | 0 |
| Unused (entry, never cited) | 8 |
| Duplicates | 0 |
| Metadata errors | 3 |
| Preprint cited where a published version exists | 2 |
| Unverified (no DOI; Crossref could not confirm) | 3 |
| Encoding defects | 1 |

The bibliography is hand-written, so `natbib` prints every entry whether or not the text cites it.
The 8 unused entries therefore appear in the PDF.

## Issues

| # | Key | Problem | Evidence | Proposed fix |
|---|---|---|---|---|
| R01 | `agrawal2025xaieval`, `covert2020sage`, `guidotti2018survey`, `lipton2018mythos`, `samek2017evaluating`, `sithakoul2024beexai`, `wachter2017counterfactual`, `yeh2019infidelity` | Unused: none is cited anywhere in the body | key scan of the body against `\bibitem` keys | Remove all eight (plan default). If any is kept, cite it where it supports a sentence. |
| R02 | `nauta2023anecdotal` | Mojibake `SchlÃ¶tterer` in the `\bibitem[...]` label; the entry text itself is correct (`Schl\"{o}tterer`) | source line 1869 | Replace the label text with `Schl\"{o}tterer`. |
| R03 | `fok2023verifiability` | Year wrong | Crossref `10.1002/aaai.12182`: AI Magazine **2024**, 45(3):317-332 | Year 2024 in the label and the entry; the key can stay. |
| R04 | `wilming2022scrutinizing` | Volume, issue and pages missing ("Machine Learning, 1--21") | Crossref `10.1007/s10994-022-06167-y`: Machine Learning 111(5):1903-1923, 2022 | Fill in the volume, issue and pages, and add the DOI. |
| R05 | `wu2025userperceptions` | Cites the arXiv preprint; now published | Crossref `10.18653/v1/2026.acl-long.1645`: Proceedings of the 64th Annual Meeting of the ACL (Long Papers), 35562-35579, 2026 | Cite the ACL 2026 version. The label year becomes 2026, and the key can stay. |
| R06 | `zheng2023judging` | Cites the arXiv DOI for a NeurIPS paper | Crossref `10.52202/075280-2020`: NeurIPS 36, 46595-46623 | Replace the arXiv DOI with the proceedings DOI and pages. |
| R07 | `gu2024llmjudge` | Unverified: arXiv only; Crossref could not match it | title query returned an unrelated work | Check whether a journal version exists. If so, cite it; if not, keep the arXiv version. |
| R08 | `adebayo2018sanity` | Unverified pages (9525-9536) | no DOI; the title query returned the 2022 follow-up paper | Check against the NeurIPS 2018 proceedings page. |
| R09 | `zheng2025ffidelity`, `proszewska2025bxaic` | Unverified: OpenReview/arXiv, no Crossref record | title query returned unrelated works | Confirm the ICLR 2025 acceptance for F-Fidelity (the OpenReview id is given). Check whether B-XAIC is still a preprint. |
| R10 | `wachter2017counterfactual` | The key says 2017 and the entry says 2018 (HJLT 2018; SSRN 2017) | Crossref SSRN record, 2017 | Cosmetic. It becomes moot if R01 removes the entry. |

## Confirmed correct (by DOI or matched record)

`adadi2018xai`, `agarwal2022openxai`, `ali2023trustworthy`, `arrieta2020xai`, `bansal2021whole`,
`bucinca2020proxy`, `burkart2021survey`, `canha2025benchmark`, `chen2016xgboost`,
`hase2020evaluating`, `haufe2026formalization`, `herrera2026framework`, `jacovi2020faithfulness`,
`kadir2023metrics`, `kaur2020interpreting`, `koo2016guideline`, `lakens2013calculating`,
`longo2024manifesto`, `mohseni2021survey`, `mothilal2020dice`, `nauta2023anecdotal` (entry, not
label), `pawlicki2024metrics`, `retzlaff2024posthoc`, `ribeiro2016why`, `ribeiro2018anchors`,
`rudin2019stop`, `slack2020fooling`, `sokol2020factsheets`, `wilcoxon1945individual`,
`zhou2025medthink` (Crossref: npj Digital Medicine 9(1), 2025; the suspicion in the rigor review is
withdrawn).

These have no DOI and did not return a Crossref match, but agree with the standard venue record:
`breiman2001random`, `demsar2006statistical`, `hedstrom2023quantus`, `holm1979simple`,
`hooker2019benchmark`, `kohavi1996scaling`, `kumar2020problems`, `lundberg2017unified`,
`rong2022consistent`, `wilming2023theoretical`, `agarwal2023gnn_eval`,
`alvarezmelis2018robustness`, `doshivelez2017rigorous`, `dua2019uci`.

## Anonymity

`herrera2026framework` is cited in the third person throughout. No other self-reference was found.

## Citation-claim fit (sample)

- `koo2016guideline` supports the 0.75 threshold as the lower bound of "good" ICC. Correct.
- `wilming2022scrutinizing`, `wilming2023theoretical` and `haufe2026formalization` support the
  suppressor-variable caveat (l.1240-1246). Correct.
- `lundberg2017unified` is cited for the axioms at l.236 and implicitly at l.1307. The paper states
  its properties as local accuracy, missingness and consistency. See rigor review F06.
