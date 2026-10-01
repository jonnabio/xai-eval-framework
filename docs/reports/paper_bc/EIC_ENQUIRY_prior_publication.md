# Note to the TMLR Editors-in-Chief — shared experimental cohort

**Status of this document.** Rewritten 2026-09-06 after the overlap it
originally described was eliminated; revised 2026-09-14 for sending *after*
submission; shortened and filled in 2026-09-30 for submission 12779, filed that
day. It is a disclosure, not a request for permission, sent so the editors
learn of the shared cohort from the author rather than from a reviewer.

**Why send it at all.** TMLR prohibits reuse of written text, figures or
results with work published at an archival venue. No result is now reported in
both documents. But the two studies rest on the same executions, and that is a
fact an editor should have. Volunteering it costs nothing; having it surface
during review costs a great deal.

**When and where.** Author's decision (2026-09-08): with the submission, not
ahead of it. Send by **email to tmlr-editors@jmlr.org**, from the address
registered on the OpenReview profile. Do not post it as a forum comment: the
note is signed and names the earlier article's authors, so any comment a
reviewer can read would break double-blind review.

---

## Message

**To:** tmlr-editors@jmlr.org

**Subject:** TMLR submission 12779: disclosure of a shared experimental cohort
with an earlier publication

```
Dear Editors-in-Chief,

I have submitted "From Fidelity to Semantics: A Taxonomy of XAI Evaluation Metrics and Paired Empirical Comparison of LIME versus SHAP" to TMLR (submission 12779) and wish to disclose one fact at the outset of review.

Its empirical cohort was released with an earlier article: "A framework for rigorous evaluation of model-agnostic explainability methods: multi-metric statistical benchmarking, operational protocol, and reproducibility", Revista de Investigación Multidisciplinaria Iberoamericana (RIMI), issue 3, 2026, doi:10.69850/rimi.vi3.307. The two studies share raw executions, preprocessing and model controls.

Following your policy on reuse of text, figures and results, I audited the submission against that article. It originally re-reported fifteen numeric results. All fifteen have been removed:

- The four-method Friedman omnibus and the block means with Nemenyi ranks, that article's headline findings, are replaced by a citation.
- The paired comparison table and its figure report the paired differences, with 95% confidence intervals, adjusted p-values and effect sizes, instead of per-method levels. The SHAP and LIME mean runtimes are cited, not stated.
- The cross-dataset table and its figure report the Anchors levels and the SHAP-Anchors gaps instead of SHAP fidelity levels.

Text and figures never overlapped. Of 405 sentences of twelve or more words, the two papers share two, both bibliography titles, and the earlier article has no figures.

The submission states this provenance in its validity section: where the cohort came from, that its levels are cited rather than restated, and that, because both analyses rest on the same executions, neither is an independent replication of the other.

The earlier article has two authors. I am the sole author of this submission: my co-author declined authorship, as this work is not his. He is also my doctoral tutor, and is declared as a conflict of interest on my OpenReview profile.

If you consider the shared cohort disqualifying despite the removals, I would prefer to know early. As this message identifies me, I would be grateful if it were not forwarded to reviewers.

Kind regards,

Jonathan Herrera-Vásquez
Universidad Americana de Europa (UNADE)
```

---

## Before sending

- Copy the text inside the box. The subject line is above it.
- Send from the address registered on the OpenReview profile, so the editors
  can match the note to the submission.
- Confirmed 2026-09-14: the RIMI DOI resolves in Crossref to this article
  (issue 3, published 2026-09-01), and Crossref spells the journal
  "multidisciplinaria" correctly. The "multidisiplinaria" seen on the journal's
  site is the site's own typo.

## Supporting detail, if asked

Removed outright: the fidelity and stability Friedman statistics, Kendall's W
for fidelity, the Anchors and DiCE block-level fidelity means, the SHAP and
LIME fidelity and stability means, and the four cross-dataset SHAP fidelity
levels. The SHAP and LIME mean runtimes were found by a second audit on
2026-09-27 and are now cited rather than stated.

The audit is mechanical and repeatable. Each published number is registered in
`pub/claim_registry.toml` against the manuscripts that carry it, so a shared
result is a claim whose entry names both documents:

```python
import tomllib
d = tomllib.load(open('pub/claim_registry.toml','rb'))
for c in d['claim']:
    files = {s['file'] for s in c.get('appears_in', [])}
    if any('paper_a' in f for f in files) and any('paper_bc' in f for f in files):
        print(c['id'])
```

This now returns nothing. It returned thirteen entries on 2026-09-06 before
the removals. `scripts/pubs/scan_shared_literals.py --strict`, which compares
the printed numbers of both papers without the registry, also finds no
unexplained match.
