# ADR-0020: Paper B+C Targets *Inteligencia Artificial* (IBERAMIA) Instead of PeerJ

> **Status:** Accepted<br>
> **Date:** 2026-10-02<br>
> **Supersedes:** decisions 1, 3 and 5 of
> [ADR-0019](0019-paper-bc-venue-peerj-and-single-working-folder.md) (PeerJ as the venue,
> the PeerJ file names, single-blind review). ADR-0019's working-folder decisions (7, 8)
> stand.<br>
> **Related:** [ADR-0018](0018-cifie-chapter-excludes-unpublished-results.md),
> [RCA-001](../rca/RCA-001-manuscript-artifact-drift.md),
> [RCA-003](../rca/RCA-003-toml-escape-in-abstract.md),
> `docs/reports/paper_bc/IBERAMIA_SUBMISSION.md`

---

## Context

ADR-0019 retargeted Paper B+C to PeerJ Computer Science after TMLR's desk rejection. PeerJ
reviews free of charge but requires payment after acceptance: an Article Processing Charge of
about US$2,155, or an Individual Lifetime Membership from about US$755. Mexico does not
qualify for its automatic waiver. The author cannot pay publication fees (2026-10-02). An
accepted PeerJ paper that is not paid for is not published, so PeerJ is not a viable venue.

The author asked for a credible venue with no fees. *Inteligencia Artificial*, the journal of
the Ibero-American Society of Artificial Intelligence, states that it charges "no fees for
publication nor editing tasks". It is indexed in Scopus, ESCI, DOAJ and Compendex, accepts
English, and its scope covers XAI evaluation. Its submission rules set no page limit for
research articles; only thesis summaries are limited, to 2–4 pages. The single uploaded PDF is
limited to 4 MB.

## Decision

1. **Paper B+C targets *Inteligencia Artificial***, as a research article. The PeerJ edition
   was never submitted.
2. **Refactor, not rewrite.** In `docs/reports/paper_bc/`:
   - `paper_bc_peerjcs.tex` is renamed `paper_bc_iberamia.tex`;
   - the PeerJ supplement becomes `paper_bc_iberamia_appendix.tex`, Appendix A of the same PDF,
     because the journal takes one PDF;
   - `PEERJ_SUBMISSION.md` is renamed `IBERAMIA_SUBMISSION.md`.

   Removed: `wlpeerj.cls`, the PeerJ upload folder and `scripts/pubs/export_peerj_upload.py`.
   The journal's `iberamia.sty` and `logo.png` are added unmodified. Results, tables, figures
   and section structure are unchanged.
3. **Double-blind review returns**, through one switch, `\camerareadyfalse`/`true`. Under
   review, the author block, the GitHub URL and the Zenodo DOI are withheld. The RIMI paper
   is cited in the third person, as the journal's rules require.
4. **A Spanish abstract and keywords are added**, because the journal's template makes the
   Resumen mandatory. They are generated from new `pub/claims.toml` keys (`abstract_es_tex`,
   `keywords_es_tex`) like the English ones. Numbers keep the decimal point, as in the thesis
   Resumen, and the Spanish fragment's numbers are registered.
5. **The abstract is unstructured again.** PeerJ's bold section headings are dropped; the
   sentences and numbers are unchanged.
6. **Citations are numbered** (`natbib`, `numbers`), as in the journal's template.

## Consequences

**Positive**
- No cost to publish.
- The registry still re-derives every number: 321 claims, now at 487 sites (two added for the
  Spanish abstract). Coverage, the shared-literal scan, the regression guards, the sync
  check and the artifact bundle all point at the new files.

**Negative**
- Lower international profile than PeerJ or TMLR.
- The licence is CC BY-NC with copyright transferred to IBERAMIA, where PeerJ was CC BY.
- An arXiv preprint posted before review weakens the double-blind process.

**Unchanged**
- ADR-0018: the CIFIE chapter still prints no Paper B+C result while it is unpublished.
- The Zenodo archive (`10.5281/zenodo.23111684`) remains the code and data release. Its tag
  name mentions PeerJ. The analysis code and data in it are unchanged since; only the figure
  styling (titles removed) and the manuscript files have changed. Before the camera-ready
  version, publish a new Zenodo version so the archive matches the published paper exactly.
