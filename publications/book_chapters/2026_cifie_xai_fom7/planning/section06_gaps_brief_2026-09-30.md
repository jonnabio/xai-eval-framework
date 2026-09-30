# Writing Brief: Section 06, "Brechas científicas de la XAI"

**Date:** 2026-09-30

**For:** the author, who writes the section (auxiliary-use decision E-AI, 2026-09-30).
Claude's part after the draft: language editing, citation and bibliography checks,
registry coverage, build, Word render and size report.

**Production file (updated 2026-09-30):** `manuscript/05_crisis_evaluacion_xai.md`.
Under the author's narrative arc the gap taxonomy is the core of section 05, "La crisis
de evaluación en XAI", the final framing of the problem before FOM-7 (section 06). The
section numbers below still say "section 06"; read them as the crisis section. The
existing material is now in file 05, in this order: "Un campo con métodos maduros...",
"La insuficiencia de la fidelidad aislada", "Brecha entre métrica, constructo y
afirmación", "Reproducibilidad y trazabilidad insuficientes", "Herramientas sin
protocolo de gobernanza suficiente", "De la crisis a la admisibilidad de la evidencia".
The method families (LIME, SHAP, Anchors, DiCE) now come after FOM-7, in section 07,
so refer to explanation objects as introduced in section 03, not to the methods'
details.

**Scaffold reference:** `planning/chapter_scaffold_2026-09-28.md`, section "06.
Brechas científicas de la XAI" (gap taxonomy and required conclusion).

## 1. Function in the chapter

Section 05 ends by showing that the four explanation families produce different
objects, that isolated fidelity is insufficient, and that metric, construct and claim
can drift apart. Section 07 then presents FOM-7. Section 06 sits between them and has
two jobs:

1. give the reader the field-level map of what XAI still cannot demonstrate (one of the
   chapter's required contents: "current scientific, technical, human, regulatory and
   evaluation gaps"); and
2. make FOM-7 necessary without making it universal: the section must say which gaps
   FOM-7 addresses and which it leaves open.

**Required conclusion (scaffold):** the field's problem is not a lack of explanation
methods; it is the lack of evidence connecting an explanatory artifact to its intended
construct, user, task and decision.

**Template alignment (TintAzul/CIFIE):** each subsection answers a different question;
each paragraph carries one main idea, its explanation, evidence, interpretation and a
transition; informative subtitles; no overlong paragraphs; citations combine narrative
and parenthetical forms and put authors in dialogue.

## 2. Length

Scaffold range: 1,400-1,700 words. The file now holds 1,172 words of existing material
(listed in section 4), part of which can be reused. Length is under observation (E-SIZE);
a reasonable target is about 1,700-1,900 words including the reused material, offset
later by the section 08 compression in section 6 of this brief.

## 3. Proposed structure

| # | Subsection (working title) | Question it answers | Status of material |
| --- | --- | --- | --- |
| 0 | Opening paragraph (no subtitle) | Why does a field with mature methods still lack evidence? | Reuse the first paragraph of "Un campo con métodos maduros y evaluación fragmentada", shortened |
| 1 | Validez técnica: fidelidad, estabilidad y robustez | Is the explanation faithful to the model and stable under relevant variation, including attack? | New; refer back to section 05 for isolated fidelity |
| 2 | Validez de constructo: métricas que no miden lo que nombran | Does the metric measure the property its label implies? | Reuse paragraphs 2-3 of "Un campo con métodos maduros..." |
| 3 | Validez humana: comprensión, confianza y decisión | Does the explanation help the intended person decide better? | New |
| 4 | Validez causal y de acción | Do attributions or counterfactuals support real interventions and feasible recourse? | New |
| 5 | Validez operativa: reproducibilidad, coste y ciclo de vida | Does the explanation hold across runs, scale, cost and data drift? | Reuse "Reproducibilidad y trazabilidad insuficientes" |
| 6 | Validez de gobernanza: transparencia exigida y evidencia disponible | Can explanations support documentation, oversight and contestability as required? | Reuse "Herramientas sin protocolo de gobernanza suficiente" partly |
| 7 | Modelos fundacionales y de lenguaje: una brecha que se amplía | How should explanations of generative and multimodal systems be evaluated? | New |
| 8 | Qué brechas aborda FOM-7 y cuáles no (bridge) | Where does a governed functional protocol help, and where not? | Reuse "De la crisis a la admisibilidad de la evidencia", adding the scope statement |

A table can replace part of subsection 8 (see section 5).

## 4. Existing material now in the file

| Current subsection in file 06 | Words (approx.) | Suggested use |
| --- | ---: | --- |
| Un campo con métodos maduros y evaluación fragmentada | 380 | Paragraph 1 → opening (0); paragraphs 2-3 → construct validity (2) |
| Reproducibilidad y trazabilidad insuficientes | 330 | Operational validity (5), shortened; keep the Hedström, Agarwal, Canha citation |
| Herramientas sin protocolo de gobernanza suficiente | 280 | Governance (6) or the bridge (8): the toolkit-versus-governance argument |
| De la crisis a la admisibilidad de la evidencia | 180 | Bridge (8); keep the seven-gate summary short, since section 07 lists the gates |

A comment marker at the top of the file (`<!-- PENDIENTE ... -->`) marks where the new
subsections go; pandoc drops it from the Word output.

## 5. Evidence per gap

All sources below are already in the chapter bibliography, with verified metadata and
recorded boundaries (`references/citation_audit.md`,
`references/candidate_literature_2026-09-28.md`). No new source is needed. The
"Boundary" column is what the source does not support.

### Gap 1. Technical validity

| Claim | Source | Boundary |
| --- | --- | --- |
| Local explanations can change substantially under small input perturbations. | Alvarez-Melis and Jaakkola (2018) | Shown for the methods and settings studied; a preprint (arXiv), cite as such. |
| LIME's stability is a documented problem beyond tabular data. | Burger et al. (2023) | Text classifiers; do not generalize the magnitude. |
| Post-hoc explainers such as LIME and SHAP can be manipulated to hide a model's behavior. | Slack et al. (2020) | Adversarial construction; not evidence that deployed systems are manipulated. |
| Fidelity metrics can themselves be unreliable (out-of-distribution masking); robust fidelity evaluation is an active research line. | Zheng et al. (2025) | Conference framework; cite as a proposal, not settled practice. |
| Exact SHAP values are intractable for broad model classes, so practice relies on approximations. | Van den Broeck et al. (2022) | Complexity result; say nothing about approximation quality in the case study. |

Illustration: section 04, cybersecurity (the explanation as attack surface). Refer back
to section 05 ("La insuficiencia de la fidelidad aislada") instead of repeating it.
**FOM-7:** partially; it measures fidelity and stability under declared conditions but
does not test adversarial robustness.

### Gap 2. Construct validity

| Claim | Source | Boundary |
| --- | --- | --- |
| XAI evaluation is multidimensional and depends on the type of explanation; many studies evaluate anecdotally or with a single property. | Nauta et al. (2023) | Systematic review; report scope, not prevalence beyond its corpus. |
| Several metrics are needed because single metrics disagree or miss properties. | Pawlicki et al. (2024) | Critical examination; bounded to the metrics studied. |
| Standardized multi-dimensional evaluation across diverse methods is still missing. | Bhattacharya and Verbert (2024) | Proposal paper. |
| Metric taxonomies show proliferation of names and operationalizations. | Kadir et al. (2023) | Review and taxonomy. |
| Functionally grounded benchmarks need explicit criteria derived from the literature. | Canha et al. (2025) | Framework from a systematic review. |

Reuse the "layers" paragraph (metric proliferation, variable inclusion criteria,
exploratory versus confirmatory, claim discipline) and "the method name is not an
experimental unit". **FOM-7:** partially; it forces the construct and unit to be declared
and harmonized, but cannot prove a proxy measures the intended property.

### Gap 3. Human validity

| Claim | Source | Boundary |
| --- | --- | --- |
| Evaluation levels differ: application-grounded, human-grounded, functionally grounded. | Doshi-Velez and Kim (2017) | Conceptual; already defined in section 03, refer back. |
| Human-centered XAI evaluation lacks consistent, reused frameworks. | Kim et al. (2024) | Systematic review; no counts beyond its corpus. |
| Explanations did not conclusively improve decisions in studied tasks; transparency did not improve appropriate reliance or error correction. | Alufaisan et al. (2021); Poursabzi-Sangdeh et al. (2021) | Already presented in section 02; cite briefly, do not repeat details. |
| Domain-expert users did not gain performance or trust from explanations in a security task; erroneous explanations lowered reliance and confidence in simulated driving. | Roch et al. (2026); Kaufman et al. (2025) | Already presented in section 04; one sentence each at most. |

**FOM-7:** no; it is functionally grounded by design (state this plainly).

### Gap 4. Causal and action validity

| Claim | Source | Boundary |
| --- | --- | --- |
| Counterfactuals must be valid for the model and also feasible, actionable and consequential for the person (algorithmic recourse). | Karimi et al. (2022); Wachter et al. (2017) | Survey and legal-technical proposal. |
| Post-hoc counterfactuals can be unjustified when they rely on regions not connected to observed data. | Laugel et al. (2019) | Method-specific demonstration. |
| Feasibility can be operationalized by paths through observed data. | Poyiadzi et al. (2020) | One approach among several. |
| Diversity and proximity are design objectives of counterfactual generation. | Mothilal et al. (2020) | Method paper. |

Also state (no new source needed, section 03 supports it) that an attribution is not a
causal effect. Illustration: section 04, credit. **FOM-7:** no; the case study measures
counterfactuals with attribution-oriented metrics, which section 05 already qualifies.

### Gap 5. Operational validity

| Claim | Source | Boundary |
| --- | --- | --- |
| An explanation fitted to one data distribution can stop approximating the model after distribution shift. | Lakkaraju et al. (2020) | Declared perturbation sets and explanation families. |
| Explainability belongs to lifecycle risk management, including monitoring. | Tabassi (2023) | Framework, not evidence of effectiveness. |
| In autonomous driving, XAI contributes to monitoring and validation. | Kuznietsov et al. (2024) | Not a safety case. |
| Reproducibility must cover configuration, artifacts, metrics, analysis and reporting. | Hedström et al. (2023); Agarwal et al. (2022); Canha et al. (2025) | Already cited in the reused paragraph. |

Cost and latency can be raised conceptually and pointed forward to the case study
(section 08) without numbers. **FOM-7:** partially; it profiles variation across seeds
and records cost, but does not monitor drift after deployment.

### Gap 6. Governance validity

| Claim | Source | Boundary |
| --- | --- | --- |
| High-risk systems must be transparent enough for deployers to interpret and use outputs; human oversight includes understanding limits and automation bias. | European Parliament & Council of the European Union (2024) | Articles 13-14; narrow reading, no legal advice. |
| Explanation principles include meaningfulness, explanation accuracy and knowledge limits. | Phillips et al. (2021) | Principles, not a test. |
| Trustworthiness characteristics interact and can conflict; explainability does not substitute for the others. | Tabassi (2023) | Framework. |
| In health, governance must span the lifecycle. | World Health Organization (2021) | Guidance. |

The gap itself is an interpretation the author may state as such: the requirements say
what explanations must enable, but the field has no agreed evidence standard for showing
that a given explanation meets them. Reuse the toolkit-versus-governance argument (tools
compute metrics; admissibility rules are a separate layer). **FOM-7:** partially; it
provides an audit trail from artifact to claim, not a compliance test.

### Gap 7. Emerging models

| Claim | Source | Boundary |
| --- | --- | --- |
| LLM explainability needs model- and paradigm-specific methods and faces distinct evaluation problems. | Zhao et al. (2024) | Survey. |
| Chain-of-thought rationales can omit factors that influenced the answer. | Turpin et al. (2023) | Specific models and interventions. |
| Non-verbalization alone may conflate incompleteness with unfaithfulness; conclusions depend on the metric. | Zaman and Srivastava (2026) | Counterpoint; not proof of faithfulness. |

Section 04 already presents these studies: keep this subsection short and focused on
the evaluation gap. Multimodal evidence is limited; say so rather than cite beyond it.
**FOM-7:** no, as applied; transfer requires redesign (section 10).

## 6. Optional table and numbering

A table "Brechas de la XAI y alcance de FOM-7" (gap, core question, what FOM-7 controls,
what remains open) would make subsection 8 compact and prepare the gate mapping in
section 07. It would become Table 2 and renumber the current Tables 2-4 to 3-5; the
renumbering is mechanical and Claude can do it after the draft. It also counts toward
length (about 150-200 words).

## 7. Constraints

- No Paper B+C results and no direct mention of Paper B+C (E-PRIOR); indirect discussion
  is fine.
- No new numbers. If one is needed, it must be registered first.
- Do not redefine terms set in section 03 (interpretability, fidelity, stability,
  robustness, evaluation levels); refer back.
- Do not repeat the details of studies already presented in sections 02 and 04.
- Citations: "y" in narrative form, "&" in parentheses; "et al." from the first
  citation.
- End with a transition that names what section 07 will do (the gate-to-gap mapping).

## 8. Section 08 compression list (P-CASE, for a later pass)

The design and the results now sit together in `08_aplicacion_empirica_perfiles_fom7.md`
(3,850 words). Duplications to remove when that section is revised:

1. "De resultados estadísticos a evidencia de capítulo", paragraph 2, repeats the 300
   planned and 275 qualified cells stated in "Diseño factorial EXP2".
2. The coverage counts (SHAP and LIME 75 of 75, DiCE 68, Anchors 57) appear in the design
   and again in the results; keep one place, next to Figure 1.
3. "Control FOM-7" restates the gate list of section 07; two sentences suffice.
4. "Enfoque general" restates the functionally grounded scope already set in sections 03
   and 07.
5. "Evidencia global" prose repeats the Friedman statistics printed in Table 4; the
   template asks tables not to duplicate text; keep the numbers in one place.
6. Figures 2-6 must be mentioned in the text before they appear (E-FIG).
7. Headings: group the design subsections under one informative heading and the results
   under another, so the section reads as design, then evidence.

Removing items 1-5 should save roughly 600-800 words.
