# Enquiry to the TMLR Editors-in-Chief — prior publication overlap

**Purpose.** Ask, before submitting, whether the overlap described below is
compatible with TMLR's policy on reuse of results. Send to the Editors-in-Chief
address listed on the TMLR site.

**Why ask rather than submit.** TMLR's editorial policy prohibits reuse of
written text, figures or results with any paper published at an archival,
peer-reviewed venue, and its carve-out covers only non-archival venues. The
overlap here is confined to results, is partly unavoidable in a paired
analysis, and has already been reduced once. Whether what remains counts as
reuse is an editorial judgement, and it is cheaper to ask than to be told after
review.

---

## Draft message

> **Subject:** Pre-submission question on prior-publication policy — overlap
> with an earlier journal article
>
> Dear Editors-in-Chief,
>
> I am preparing a submission to TMLR and would like to check a
> prior-publication question before I submit, rather than after.
>
> **The prior article.** In September 2026 the *Revista de Investigación
> Multidisciplinaria Iberoamericana* (RIMI), issue 3,
> doi:10.69850/rimi.vi3.307, published "A framework for rigorous evaluation of
> model-agnostic explainability methods: multi-metric statistical benchmarking,
> operational protocol, and reproducibility". It reports a multi-metric
> evaluation protocol and a four-method omnibus comparison — SHAP, LIME,
> Anchors and DiCE — over an execution cohort of 275 analysable runs on the
> UCI Adult benchmark. It is a Spanish-language regional journal; the article
> is in English.
>
> **The submission.** The paper I intend to submit contributes a four-axis
> taxonomy of XAI evaluation metrics, a gap analysis over a 44-paper scoping
> corpus, a multi-rater LLM-judge reliability measurement, a paired run-level
> comparison of LIME and SHAP, and a cross-dataset extension. It uses the same
> execution cohort as the RIMI article.
>
> **What I have already removed.** The submission originally reported thirteen
> numeric results that also appear in the RIMI article. I have removed the two
> tables that carried the prior article's own headline findings — the
> four-method Friedman omnibus, and the four-method block means with Nemenyi
> ranks — and replaced them with a cited paragraph that attributes those
> results to the RIMI article and states that they are context rather than
> evidence for any claim in the submission. Five results are now absent from
> the manuscript entirely.
>
> **What remains, and why.** Eight results still appear in both.
>
> Four are the SHAP and LIME group means for fidelity and stability, in the
> table reporting the paired comparison alongside the differences, adjusted
> p-values and effect sizes. I do not see how to remove them: effect sizes
> without the means they are computed from are uninterpretable. They coincide
> with the block-level means in the RIMI article only because both explainers
> have complete 75/75 coverage, which makes run-level and block-level
> aggregation arithmetically identical for those two methods. The analysis
> itself — paired, cell-matched, at the run level, with directional hypotheses
> — is not in the prior article, which reports an omnibus over four methods at
> the block level.
>
> Four are SHAP fidelity values in a cross-dataset table, where they serve as
> the reference condition for an Anchors comparison that is new. **If you
> would prefer zero overlap, I can replace these with the SHAP−Anchors gaps
> and cite the prior article for the levels.** I am ready to do that.
>
> **What does not overlap.** I checked rather than assumed. Across 405
> sentences of at least twelve words, the two papers share two verbatim
> sentences, both of which are titles in the bibliography. The prior article
> contains no figures; the three in the submission are its own. The taxonomy,
> the scoping corpus and gap analysis, the LLM-judge reliability study and the
> paired analysis have no counterpart in it.
>
> **Two further disclosures.** The prior article has two authors; the
> submission has one, because my co-author on that article has declined
> authorship here on the grounds that this work is not his. And the submission
> currently keeps its account of this overlap in a section that is suppressed
> under double-blind review, because naming the shared cohort identifies me. I
> would restore it at camera-ready, or reword it now if you would rather it be
> visible to reviewers.
>
> I would be grateful to know whether the eight remaining results are
> acceptable as they stand, whether you would prefer the cross-dataset four
> converted to gaps, or whether the shared cohort makes the work unsuitable for
> TMLR. I would rather adjust or withdraw now than have this surface during
> review.
>
> Thank you for your time.
>
> Jonathan Herrera-Vasquez
> Universidad Americana de Europa (UNADE)

---

## Before sending

- Confirm the RIMI journal name and DOI against the published article; the
  journal's own site spells the title "multidisiplinaria", which appears to be
  a typo, and the bibliography entry in the manuscript uses the corrected
  spelling.
- Confirm no other venue currently holds this work under review.
- If the answer permits submission, revisit the `\ifdeanonymised` guard on the
  §Validity subsection "Relationship to Previously Published Work" in light of
  what the editors say.

## Supporting evidence, if they ask for specifics

The eight shared results, by registry id:

    exp2.block.shap.fidelity      exp3.shap.breast_cancer.rf.fidelity
    exp2.block.lime.fidelity      exp3.shap.breast_cancer.xgb.fidelity
    exp2.block.shap.stability     exp3.shap.german_credit.rf.fidelity
    exp2.block.lime.stability     exp3.shap.german_credit.xgb.fidelity

The five removed: the fidelity and stability Friedman statistics, Kendall's W
for fidelity, and the Anchors and DiCE block-level fidelity means.
