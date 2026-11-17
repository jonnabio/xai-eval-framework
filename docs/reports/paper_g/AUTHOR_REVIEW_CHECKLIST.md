# Paper G — author review checklist

**For:** the author, before submission. **Date:** 2026-11-16 (Task 21). Nothing on this list can
be automated: each item needs the author's own judgement, knowledge or signature. Items the build
checks automatically are in `JOURNAL_COMPLIANCE.md`, part A.

## 1. Ownership of the scientific argument

- [ ] I can state, without the manuscript, the question, the design, the original H1 and H2 results,
      and why the H1 classification stands although S1 is lower.
- [ ] I agree with the reporting hierarchy: the original analysis (Section 3.1) carries the only
      decision; S3 and S1 are supplementary; the diagnostics are exploratory.
- [ ] I have checked the methods against the code I authorised, in particular Equations (1) to (5),
      and accept the evidence classes of Table 1 (what was fixed before the run, what after the run
      but before unblinding, and what after the review of the results).
- [ ] I accept each interpretation in Section 3.8 at the strength it is stated (property of the
      computation, observed association, or possible mechanism not isolated), and the limitations.
- [ ] I accept or replace the title, which keeps the plan's wording.
- [ ] I have read every cited work that supports a claim I rely on (`REFERENCE_VERIFICATION.md`
      lists the claim each reference supports), and I accept the reference exceptions listed there
      (five peer-reviewed papers without a DOI, one preprint, three anonymised own manuscripts, one
      article assigned to an issue dated 2027).

## 2. Editorial policy of *Informática y Sistemas*

- [ ] **AI-generated content (at most 30%, Compilatio).** The text was drafted by an AI assistant.
      Whether and how much to rewrite is the author's decision; the limit must not be approached by
      paraphrasing to evade detection. After any rewriting, rebuild (numbers are re-inserted and
      re-verified).
- [ ] **Similarity (at most 10%).** The methods reuse wording of this project's own unpublished
      plan documents, which are public on GitHub; check whether Compilatio will match them.
- [ ] **Originality.** The manuscript is not under review elsewhere, and it restates no result of
      Papers B, E or F.
- [ ] **Double blind.** The source and history of this manuscript are public on GitHub under the
      author's name since 2026-11-13 (see `JOURNAL_COMPLIANCE.md`, part C). Decide what to do, and
      whether to tell the editor. Removing files now would not remove them from the history or
      from copies.
- [ ] **Ethics.** Only public, de-identified benchmark data were used and no human participants
      were involved (COMPAS on OpenML holds sex, age, counts, race and charge degree, no
      identifiers). Confirm that the institution requires no ethics approval.

## 3. Declarations (personal; never filled in by the assistant)

- [ ] Funding: state the funding, or "This research received no external funding"; enter the same
      in the OJS "Supporting Agencies" field ("None" if no funding).
- [ ] Conflicts of interest: state them, or "The author declares no conflicts of interest."
- [ ] Declaration of generative AI use: confirm the extent of your own review and rewriting, and
      add any other generative AI tool used, with name, version, provider, purpose and sections.
      The repository contains `CHATGPT_ADVISOR_PROMPT.md`; if ChatGPT (or another assistant) was
      used as a methodological advisor, it must be declared.
- [ ] Author contributions (CRediT), at acceptance.
- [ ] Data availability: create the Zenodo version of the code and results at acceptance and
      replace the withheld identifier.

## 4. Submission (OJS, author only)

- [ ] Register, link ORCID; enter full author metadata; manuscript type "Research article".
- [ ] Upload `submission/paper_g_blind.docx` after opening it in Word once (pagination, equations,
      repeated table header rows), and `submission/Figure_1` … `Figure_5` as separate files.
- [ ] Keywords entered one at a time; language English; Supporting Agencies completed.
- [ ] Accept the submission checklist and the copyright notice (CC BY-NC-ND 4.0); there is no
      separate signed agreement or checklist file.
- [ ] Optional supplementary material (code, data) only if it does not reveal identity.
