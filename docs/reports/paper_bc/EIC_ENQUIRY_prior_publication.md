# Note to the TMLR Editors-in-Chief — shared experimental cohort

**Status of this document.** Rewritten 2026-09-06 after the overlap it
originally described was eliminated; revised 2026-09-14 for sending *after*
submission. It is a disclosure, not a request for permission, sent so the
editors learn of the shared cohort from the author rather than from a reviewer.

**Why send it at all.** TMLR prohibits reuse of written text, figures or
results with work published at an archival venue. No result is now reported in
both documents. But the two studies rest on the same executions, and that is a
fact an editor should have. Volunteering it costs nothing; having it surface
during review costs a great deal.

**When and where.** Author's decision (2026-09-08): with the submission, not
ahead of it. Send by **email to tmlr-editors@jmlr.org** as soon as the
submission number exists. Do not post it as a forum comment: the note is
signed and names the earlier article's authors, so any comment a reviewer can
read would break double-blind review.

---

## Draft message

> **To:** tmlr-editors@jmlr.org
>
> **Subject:** TMLR submission [NUMBER]: disclosure of a shared experimental
> cohort with an earlier publication
>
> Dear Editors-in-Chief,
>
> I have just submitted "From Fidelity to Semantics: A Taxonomy of XAI
> Evaluation Metrics and Paired Empirical Comparison of LIME versus SHAP"
> to TMLR (submission [NUMBER], [FORUM URL]), and would like to place one fact
> on the record at the outset of review.
>
> The empirical cohort my submission analyses was released with an earlier
> article: "A framework for rigorous evaluation of model-agnostic
> explainability methods: multi-metric statistical benchmarking, operational
> protocol, and reproducibility", *Revista de Investigación Multidisciplinaria
> Iberoamericana* (RIMI), issue 3, 2026, doi:10.69850/rimi.vi3.307. The two
> studies therefore share raw executions, preprocessing and model controls.
>
> Reading your policy on reuse of text, figures and results, I audited the
> submission against that article rather than assuming the overlap was
> immaterial. It originally re-reported thirteen numeric results. All thirteen
> have been removed:
>
> - The four-method Friedman omnibus and the four-method block means with
>   Nemenyi ranks — the earlier article's own headline findings — are gone,
>   replaced by a cited paragraph.
> - The paired comparison table no longer prints per-method mean levels. It
>   reports the mean paired difference with a 95% confidence interval, the
>   adjusted p-values and the effect sizes, which are the quantities the paired
>   analysis contributes.
> - The cross-dataset table no longer prints SHAP fidelity levels. It reports
>   the Anchors levels and the SHAP−Anchors gaps.
> - The corresponding figure was regenerated, because it had been labelling the
>   SHAP levels directly.
>
> Text and figures never overlapped: across 405 sentences of at least twelve
> words the two papers share two, both bibliography titles, and the earlier
> article contains no figures.
>
> The submission states this provenance openly in its validity section rather
> than in a note only you would see. It records that the cohort came from the
> earlier study, that the levels are cited rather than restated, and that
> because both analyses rest on the same executions, agreement between them is
> arithmetic and neither is an independent replication of the other.
>
> One further disclosure: the earlier article has two authors. I am the sole
> author of this submission, my co-author on that article having declined
> authorship here on the grounds that this work is not his. He is also my
> doctoral tutor, and is declared as a conflict of interest on my OpenReview
> profile.
>
> I would rather you heard this from me. If you consider the shared cohort
> disqualifying notwithstanding the removals, I would prefer to know early.
>
> Because this message identifies me, I would be grateful if it were not
> forwarded to reviewers.
>
> Thank you for your time.
>
> Jonathan Herrera-Vasquez
> Universidad Americana de Europa (UNADE)

---

## Before sending

- Fill in `[NUMBER]` (twice) and `[FORUM URL]`.
- Send from the address registered on the OpenReview profile, so the editors
  can match the note to the submission.
- Confirmed 2026-09-14: the RIMI DOI resolves in Crossref to this article
  (issue 3, published 2026-09-01), and Crossref spells the journal
  "multidisciplinaria" correctly. The "multidisiplinaria" seen on the journal's
  site is the site's own typo.
- The only remaining confirmation: the work is under review at no other venue.
  The submission form asks for the same thing.

## Supporting detail, if asked

Removed outright: the fidelity and stability Friedman statistics, Kendall's W
for fidelity, the Anchors and DiCE block-level fidelity means, the SHAP and
LIME fidelity and stability means, and the four cross-dataset SHAP fidelity
levels.

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
the removals.
