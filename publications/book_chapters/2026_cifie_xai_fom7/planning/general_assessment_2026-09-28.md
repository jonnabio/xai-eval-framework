# First-Pass General Assessment of the CIFIE XAI Book Chapter

**Date:** 2026-09-28

**Lane:** `chapter/cifie-sync-2026-09`

**Role:** Architect

**Scope:** General idea, scientific positioning, literature coverage, readability,
and fitness for a book chapter. No manuscript prose was edited in this pass.

## Executive assessment

The current manuscript is scientifically promising and unusually strong in evidence
governance. Its distinctive contribution is clear: FOM-7 turns heterogeneous XAI
outputs into traceable, reproducible, and appropriately bounded scientific claims.
The empirical case is also protected by a mature claim registry, coverage checks,
and the exclusion of unpublished Paper B+C results.

The manuscript is not yet fully aligned with the broader book-chapter objective now
defined by the author. At present it reads primarily as a technical methodological
chapter about FOM-7 and a benchmark of LIME, SHAP, Anchors, and DiCE. It does not yet
give a sufficiently developed general account of:

- what XAI is, for readers outside the immediate benchmarking literature;
- why XAI matters across the AI lifecycle and to different stakeholders;
- where XAI is likely to be consequential in the coming years;
- concrete, domain-grounded examples of appropriate and inappropriate use; and
- the field's open technical, human, causal, operational, and governance gaps.

The recommended direction is therefore **repositioning, not replacement**. The
chapter should retain FOM-7 and the Adult Income benchmark as its original scientific
contribution, but present them as the methodological answer to a broader problem:
how XAI can move from plausible narratives to evidence that is useful, testable,
auditable, and fit for a declared purpose.

**Readiness judgment:** strong basis for revision; not ready for final editorial
submission under the newly clarified objective.

## Author requirements now fixed

- There is no publisher template.
- The target style is a highly scientific but readable book chapter.
- In-text citations and the reference list use APA 7.
- The deliverable is a Word document with formatting broadly aligned with the thesis.
- Claims must remain science-based, traceable, and no stronger than their evidence.

These decisions resolve the previous blocker concerning template, citation style, and
output format. A publisher word limit remains unnecessary unless one is later imposed.

## What is already strong

### Scientific identity

- The chapter has a defensible central problem: explanation generation is not the
  same as explanation validation.
- It distinguishes plausibility, fidelity, stability, human usefulness, and causal
  validity instead of treating them as synonyms.
- It avoids a universal method ranking and interprets LIME, SHAP, Anchors, and DiCE
  as different explanatory objects with different evaluation needs.
- FOM-7 provides an original organizing contribution rather than another catalogue
  of explanation methods.

### Evidence discipline

- The empirical material is under claim coverage and exclusivity controls.
- The chapter excludes unpublished Paper B+C results under ADR-0018.
- The reference list currently contains 41 cited works, and the 2026-09-27 audit
  reports that all 35 listed DOIs resolve.
- The manuscript repeatedly states the limits of the Adult/tabular benchmark and
  separates functional evaluation from human- and application-grounded evaluation.

### Existing literature base

The chapter already includes many of the right foundations: Lipton; Miller;
Doshi-Velez and Kim; Rudin and colleagues; the original LIME, SHAP, Anchors, and DiCE
papers; Nauta et al.; Quantus; OpenXAI; recent multi-metric reviews; and work on
counterfactual recourse and explanation robustness. This is a credible foundation
for the methodological core.

## Main gaps against the revised objective

### 1. Scope mismatch: technical case study before general orientation

The title, abstract, outline, and most sections foreground reproducible benchmarking.
The introduction names health, credit, education, employment, security, and public
services, but the manuscript does not return to those domains in a substantive way.
Applications appear mainly as a list in the introduction and as future replication
targets in the limitations section.

**Consequence:** a reader can understand FOM-7 without receiving the requested
general map of XAI's importance, uses, and future trajectory.

### 2. No dedicated account of why XAI matters

The manuscript strongly explains why XAI evaluation matters, but less fully explains
the functions XAI itself can serve:

- model debugging and scientific diagnosis;
- safety assurance and failure analysis;
- support for human decision-making;
- contestability and communication to affected people;
- audit, governance, and regulatory oversight; and
- organizational learning and monitoring after deployment.

These functions should be separated because each has a different audience and a
different standard for a successful explanation.

### 3. Application areas lack concrete examples

The future-facing application landscape is not developed. At minimum, the chapter
needs evidence-grounded examples in:

- health and biomedical decision support;
- finance, credit, fraud, and other consequential allocation decisions;
- cybersecurity and critical-infrastructure monitoring;
- autonomous and industrial systems; and
- foundation models, LLMs, and multimodal systems.

Education and public administration can be included as a cross-cutting human-services
case if space permits. Examples must be illustrative and bounded; they must not imply
that an explanation proves a decision correct.

### 4. The gap analysis is too concentrated on metric fragmentation

The current crisis section is good but narrower than the field-level assessment now
required. It should retain metric fragmentation and add a structured gap taxonomy:

1. **Technical validity:** faithfulness, robustness, sensitivity, dependence, and
   vulnerability to manipulation.
2. **Construct validity:** whether a metric measures the property its label implies.
3. **Human validity:** usefulness, cognitive fit, calibrated reliance, and the risk
   that persuasive explanations create unjustified trust.
4. **Causal and action validity:** whether attributions or counterfactuals support
   interventions, feasible recourse, or causal claims.
5. **Operational validity:** distribution shift, monitoring, latency, scale,
   reproducibility, and lifecycle change.
6. **Socio-technical governance:** audience-specific explanation, contestability,
   documentation, accountability, and domain-specific oversight.
7. **Emerging-model coverage:** generative, foundation, agentic, and multimodal AI,
   where fluent rationales can be mistaken for faithful mechanisms.

### 5. Readability is limited by repetition and density

The assembled chapter is approximately 17,500 body words. The same core claims recur
across the introduction, foundations, crisis, FOM-7, implications, limitations, and
conclusion: no universal winner; plausibility is not fidelity; metrics require
context; and claims must be traceable. These repetitions are individually sound but
collectively slow the argument.

**Recommended editorial principle:** explain each major distinction once in full,
then refer back to it. Use short domain examples, synthesis tables, and transition
paragraphs to make the science more readable without simplifying the evidence.

### 6. The empirical material occupies too much of the conceptual center

The design and results are scientifically useful, but they currently determine the
identity of the whole chapter. For the revised objective, the benchmark should become
a rigorous case study demonstrating how weakly governed explanations can be turned
into auditable evidence. That preserves every protected result while giving the
chapter broader relevance.

### 7. The literature is strong but thematically unbalanced

The existing bibliography is concentrated in definitions, methods, metrics, and the
chapter's benchmark. It needs a controlled extension in four directions:

- authoritative trustworthiness and transparency frameworks;
- domain-specific systematic reviews;
- human-centered evaluation and calibrated reliance;
- emerging-model explainability, especially LLMs and multimodal systems.

The purpose is not to maximize citation count. Each new source must support a named
claim in the evidence map.

### 8. Word rendering does not yet match the stated standard

`scripts/build_cifie_chapter.py` currently assembles the Markdown with Pandoc and
adds a hanging indent to the bibliography. It does not yet use the thesis reference
document or the thesis post-render formatting rules. The future build should adapt
the compatible thesis conventions: justified body text, 1.5 line spacing, coherent
heading hierarchy, centered captions and figures, APA-style tables, hanging
references, and decimal page numbering. Thesis-only elements such as its cover and
front matter should not be copied automatically.

### 9. Some planning artifacts are stale

The evidence map and source inventory still mark several empirical tables and claims
as pending even though the 2026-09-27 synchronization and coverage work completed
them. Before a new literature pass, these records should be reconciled so the plan
does not confuse old extraction tasks with new work.

## Recommended scientific thesis

> XAI is not a guarantee that a complex model has become understandable. It is a
> family of socio-technical methods for producing purpose- and audience-specific
> evidence about model behavior. Its value depends on whether that evidence is
> faithful, stable, useful, reproducible, and auditable. FOM-7 operationalizes those
> requirements for comparative evaluation.

This thesis is broad enough for a book chapter and precise enough to preserve the
project's empirical contribution.

## Recommended narrative arc

1. **The problem:** increasingly consequential AI systems can be difficult to inspect.
2. **The promise and limit of XAI:** explanations can support understanding and
   oversight, but can also be unstable, misleading, or merely persuasive.
3. **Where the issue matters:** concrete examples across high-impact and emerging
   domains, each tied to a stakeholder and decision.
4. **Why current evaluation is insufficient:** technical, human, causal,
   operational, and governance gaps.
5. **The methodological response:** FOM-7 as an evidence-governance protocol.
6. **The empirical demonstration:** the existing benchmark as a bounded case study.
7. **The agenda:** what must change for XAI to become scientifically and socially
   useful across future systems.

## Seed literature for the next pass

The current bibliography remains the base. The following sources are priority
candidates for verification and selective addition; inclusion is not automatic.

| Need | Candidate source | Intended use |
| --- | --- | --- |
| General principles | Phillips et al. (2021), NISTIR 8312, `10.6028/NIST.IR.8312` | Distinguish evidence, meaningfulness, explanation accuracy, and knowledge limits. |
| Trustworthy-AI context | NIST AI RMF 1.0 (2023) | Place explainability beside validity, safety, fairness, privacy, transparency, and accountability rather than treating it as sufficient by itself. |
| High-risk transparency | Regulation (EU) 2024/1689, Article 13 | Establish that transparency must enable appropriate interpretation and use of high-risk-system outputs. |
| Health governance | World Health Organization (2021), *Ethics and governance of artificial intelligence for health* | Ground health examples in safety, autonomy, transparency, oversight, and lifecycle evaluation. |
| Health caution | Ghassemi, Oakden-Rayner, and Beam (2021), `10.1016/S2589-7500(21)00208-9` | Show why plausible post-hoc explanations do not by themselves validate clinical decisions. |
| Human-centered evidence | Kim, Maathuis, and Sent (2024), `10.3389/frai.2024.1456486` | Support the lack of standardized user evaluation and the distinction between explanation quality, interaction, and performance. |
| Finance | Weber, Carl, and Hinz (2024), `10.1007/s11301-023-00320-0` | Ground credit, risk, portfolio, and fraud examples in a systematic review. |
| Cybersecurity | Rjoub et al. (2023), `10.1109/TNSM.2023.3282740` | Ground threat detection, analyst triage, and adversarial-use examples. |
| Autonomous systems | Kuznietsov et al. (2024), `10.1109/TITS.2024.3474469` | Ground safety assurance, monitoring, validation, and user-facing explanations in autonomous driving. |
| Foundation models | Zhao et al. (2024), `10.1145/3639372` | Introduce LLM-specific explainability challenges and explain why generated rationales are not automatically mechanistic evidence. |

## Addendum 2026-09-29: review of the formatted build

A Scientific Advisor review of
`drafts/v3_editorial_review/cifie_xai_fom7_2026-09-29_formatted.docx` (Word render,
75 pages) found the new sections 02-03 already at the intended register, and
returned **Not ready** for the build as a whole:

- **Resolved since this assessment:** gap 2 (why XAI matters) is addressed by the
  new section 02; the "Fuente inicial" notes, black ink, justification and 1.5
  spacing of gap 8 are met in the build.
- **Still open:** gap 3 (applications) and gap 4 (field gaps). The title and the
  section 02 roadmap now promise both sections, which makes their absence a
  reader-facing defect rather than a planning gap.
- **Gap 5 is more specific than recorded here:** sentences addressed to the author,
  repository paths in prose, undefined thesis labels (P1, H1-H3), and arguments
  repeated between old section 05 and new sections 02-03.
- **New findings:** the build cannot be reproduced from committed state; a retired
  LIME cost (226 ms) survives in the method section; the reproducibility CVs are
  attributed to EXP1 instead of the EXP2 RF/N=100 subset; two figures are
  illegible in grayscale; several APA metadata errors.

All findings, their order and their exit checks are in the revision plan
("Review remediation workstream") and in the section-level additions of
`chapter_scaffold_2026-09-28.md`.

## Overall conclusion

The chapter should not abandon its technical depth. Its strongest future form is a
scientific synthesis in which readers first understand XAI's purpose and stakes,
then see why the field's evaluation gaps matter, and finally encounter FOM-7 and the
benchmark as a concrete, auditable response. This change will make the chapter more
general, more readable, and more useful without weakening its scientific identity.
