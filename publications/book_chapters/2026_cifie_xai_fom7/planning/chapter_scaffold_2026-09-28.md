# Scientific Scaffold for the CIFIE XAI Book Chapter

**Status:** Approved working scaffold; Phase 2 structural rewrite active; enriched
2026-09-29 with the section-level requirements of the Scientific Advisor review
(finding IDs refer to the "Review remediation workstream" of the revision plan)

**Created:** 2026-09-28

**Lane:** `chapter/cifie-sync-2026-09`

**Assessment:** `planning/general_assessment_2026-09-28.md`

**Revision plan:** `planning/science_first_revision_plan_2026-09-28.md`

## 1. Purpose of this scaffold

This document defines the chapter's argument before prose is moved or rewritten. It
maps the existing manuscript into a broader science-first structure, identifies the
claims and evidence required by each section, and protects the verified FOM-7 and
empirical material from being weakened during restructuring.

This is a planning artifact. It does not change the eleven manuscript sections, the
claim registry, the bibliography, or the generated Word file.

## 2. Fixed editorial and scientific requirements

- The chapter is a highly scientific but readable book chapter, not a journal article
  reproduced inside a book.
- The language is Spanish; planning records and commit messages remain in English.
- Citations and references follow APA 7.
- The final artifact is a Word document using the thesis's compatible presentation
  standards.
- The chapter provides a general overview of XAI, explains its importance, presents
  future-facing application areas with clear examples, and identifies the field's
  principal gaps.
- FOM-7 remains the original methodological contribution.
- The Adult Income benchmark becomes the bounded empirical demonstration of FOM-7,
  not the sole reason the chapter exists.
- Every scientific claim is proportional to its evidence.
- Every result-shaped number remains subject to RCA-001 coverage and ADR-0018
  exclusivity.

## 3. Working title and central thesis

### Recommended working title

**De la explicación a la evidencia: fundamentos, aplicaciones y evaluación
auditable de la inteligencia artificial explicable**

### Optional subtitle

**El protocolo FOM-7 como marco operativo para comparaciones reproducibles**

### Central thesis

XAI is not a guarantee that an opaque model has become understandable. It is a family
of socio-technical methods for producing purpose- and audience-specific evidence
about model behavior. The scientific value of an explanation depends on whether it
is faithful to its target, stable under relevant variation, meaningful for its user,
reproducible, and auditable. FOM-7 operationalizes part of that requirement for
comparative, functionally grounded evaluation.

### Reader promise

After reading the chapter, the reader should be able to:

1. explain what XAI is and distinguish it from transparency and inherently
   interpretable modeling;
2. identify why an explanation is needed, for whom, and for what decision;
3. recognize major application areas and domain-specific failure modes;
4. distinguish plausible explanations from technically or humanly validated ones;
5. describe the principal gaps preventing XAI from becoming dependable evidence;
6. understand what FOM-7 controls and what remains outside its scope; and
7. interpret the benchmark as a case study rather than a universal method ranking.

## 4. Argument map

```text
Consequential and complex AI systems
        |
        v
Different stakeholders need different kinds of explanation
        |
        v
XAI offers multiple explanatory objects, not one universal solution
        |
        v
Applications expose technical, human, causal, operational, and governance gaps
        |
        v
An explanation becomes evidence only through explicit evaluation and traceability
        |
        v
FOM-7 governs the functionally grounded part of that evidence chain
        |
        v
The Adult/tabular benchmark demonstrates the protocol under bounded conditions
        |
        v
Future XAI must join technical validity with human and application validation
```

## 5. Working length and balance

There is no publisher word limit. A working range is still useful for readability.
The recommended body target is **14,000-16,000 words**, excluding references, with
flexibility after the literature pass. The current build is approximately 17,500 body
words, so new application content should be funded mainly by consolidation rather
than unrestricted expansion.

| Section | Working range | Share of argument |
| --- | ---: | --- |
| 01. Resumen y palabras clave | 200-250 | Compact synthesis |
| 02. Por qué importa la XAI | 900-1,100 | Motivation and stakes |
| 03. Qué es y qué no es la XAI | 1,100-1,400 | General conceptual overview |
| 04. Ámbitos de aplicación y horizontes próximos | 1,700-2,100 | Domain examples |
| 05. Familias explicativas y problema de evaluación | 1,600-1,900 | Methods without catalogue overload |
| 06. Brechas científicas del campo | 1,400-1,700 | Structured gap analysis |
| 07. FOM-7 como respuesta metodológica | 1,400-1,700 | Original contribution |
| 08. Caso empírico: evaluación auditable | 1,900-2,300 | Design plus findings |
| 09. Implicaciones para investigación y práctica | 800-1,000 | Transfer and governance |
| 10. Limitaciones y agenda de investigación | 1,000-1,300 | Boundaries and future work |
| 11. Conclusiones | 400-600 | Answer to the central thesis |

## 6. Section-by-section scaffold

### 01. Resumen y palabras clave

**Purpose:** summarize the problem, general XAI scope, application relevance,
scientific gaps, FOM-7 contribution, empirical demonstration, and bounded conclusion.

**Draft last.** The present abstract is accurate for the technical version but gives
the benchmark more weight than the revised chapter architecture.

**Required moves:**

- retain the distinction between generating and validating explanations;
- introduce the broader application and gap perspective in one sentence;
- describe the benchmark as a demonstration of the protocol;
- keep only the most decision-relevant empirical result;
- avoid presenting SHAP as a generally preferred method;
- retain six or fewer keywords, including XAI, evaluation, auditability, and FOM-7.

**Evidence:** no new evidence should appear only in the abstract. Every statement must
be supported in the chapter body.

**Acceptance question:** does the abstract describe the revised chapter rather than
the previous technical draft?

### 02. Por qué importa la inteligencia artificial explicable

**Purpose:** explain why XAI is scientifically and practically important before
introducing individual methods.

**Core questions:**

- What problem does opacity create?
- Who needs an explanation?
- What decisions can explanations support?
- Why is explanation not equivalent to correctness or trustworthiness?

**Planned subsections:**

1. De la predicción a la supervisión humana.
2. Funciones de la explicación en el ciclo de vida de la IA.
3. Audiencias y propósitos diferentes.
4. La promesa y el límite de explicar.
5. Objetivo y contribución del capítulo.

**Required claims:**

- Explanation needs differ among developers, auditors, domain professionals,
  affected people, managers, and regulators.
- XAI can support debugging, monitoring, scientific diagnosis, oversight,
  contestability, and communication.
- Explainability is one component of trustworthy AI and cannot substitute for
  validity, safety, fairness, security, or accountability.
- A persuasive explanation can increase confidence without increasing correctness.

**Current material to reuse:**

- `02_introduccion.md`: the first two paragraphs on opacity and the distinction
  between plausible and technically adequate explanations.
- `02_introduccion.md`: the objective, scope, and contribution paragraphs, rewritten
  after the new architecture stabilizes.
- `09_implicaciones_evaluacion_auditable_xai.md`: the idea that selection must be
  conditional on purpose and evidence.

**Current material to compress or relocate:**

- The detailed LIME/SHAP/Anchors/DiCE paragraph moves to section 05.
- The detailed crisis-of-metrics discussion moves to section 06.
- Repeated FOM-7 descriptions move to section 07.

**Evidence base:**

- Existing: Adadi and Berrada; Arrieta et al.; Lipton; Miller; Rudin et al.;
  Doshi-Velez and Kim.
- Candidate: Phillips et al. (2021), NISTIR 8312.
- Candidate: NIST AI RMF 1.0.
- Candidate: Regulation (EU) 2024/1689, Article 13, used narrowly for the transparency
  requirement applied to high-risk-system deployers.

**Acceptance question:** can a scientifically literate reader explain at least four
distinct reasons XAI matters without yet knowing FOM-7?

### 03. Qué es y qué no es la XAI

**Purpose:** provide the general conceptual overview requested by the author.

**Planned subsections:**

1. Interpretabilidad, explicabilidad y transparencia.
2. Modelos interpretables y explicaciones post-hoc.
3. Explicaciones locales, globales y agregadas.
4. Objetos explicativos: atribuciones, reglas, ejemplos y contrafactuales.
5. Plausibilidad, fidelidad, estabilidad y utilidad humana.
6. Lo que una explicación no demuestra.

**Required claims:**

- XAI is a plural field with competing definitions and different explanatory goals.
- Transparency is a property of a system or process; a post-hoc explanation is an
  artifact about selected behavior under assumptions.
- Local explanations cannot be aggregated into global understanding without further
  methodological choices.
- Plausibility to a person is distinct from faithfulness to a model.
- Feature attribution is not causal explanation, and a valid model counterfactual is
  not automatically feasible recourse.
- In high-impact settings, an interpretable model should be considered when it can
  meet the task requirements.

**Current material to reuse:**

- `03_fundamentos_xai.md`: definitions, artifact framing, local/global distinction,
  plausibility versus fidelity, and functionally grounded scope.
- `04_metodos_lime_shap_anchors_dice.md`: concise descriptions of the four kinds of
  explanatory output.

**Current material to compress:**

- Repeated statements that FOM-7 aligns object, construct, metric, and claim.
- Repeated closing summaries of what later sections will do.
- Detailed benchmark values, which move to section 08.

**Evidence base:**

- Existing: Lipton; Miller; Murdoch et al.; Marcinkevičs and Vogt; Schwalbe and
  Finzel; Rudin et al.; Nauta et al.; Karimi et al.
- Candidate: Phillips et al. for audience-appropriate and accurate explanations.

**Acceptance question:** does the section establish a usable vocabulary without
implying that all explanation methods solve the same problem?

### 04. Ámbitos de aplicación y horizontes próximos

**Purpose:** show where XAI matters through clear, evidence-grounded examples and
identify why future applications require different forms of explanation.

**Editorial pattern for each domain:**

1. decision or task;
2. principal stakeholder;
3. bounded example;
4. plausible benefit of explanation;
5. failure mode or risk;
6. evidence required before deployment.

#### 04.1 Salud y biomedicina

**Example:** a clinician investigates whether a diagnostic-risk model relies on
clinically meaningful evidence or a spurious acquisition artifact.

**Stakeholders:** clinicians, patients, developers, hospital governance, regulators.

**Scientific boundary:** a saliency map or feature attribution does not validate an
individual diagnosis and may not improve clinical performance or reliance.

**Candidate evidence:** WHO (2021); Ghassemi, Oakden-Rayner, and Beam (2021); a recent
systematic review selected after quality appraisal.

#### 04.2 Finanzas y decisiones de asignación

**Example:** a credit analyst needs model-level diagnostic evidence, while an
applicant needs an understandable reason and a realistic path to contest or change an
outcome.

**Stakeholders:** analysts, applicants, compliance teams, auditors, regulators.

**Scientific boundary:** an attribution may expose model dependence but does not prove
fairness; a mathematically close counterfactual may be infeasible or discriminatory.

**Candidate evidence:** Weber, Carl, and Hinz (2024); Karimi et al. (2022); Wachter et
al. (2017); official governance sources where a legal claim is made.

#### 04.3 Ciberseguridad e infraestructura crítica

**Example:** a security analyst receives an anomaly alert and an explanation of the
traffic patterns that drove it, using the evidence to prioritize investigation.

**Stakeholders:** security operations teams, system owners, incident responders,
auditors.

**Scientific boundary:** explanations must be timely and robust to adversaries; they
can themselves be manipulated or reveal system behavior to attackers.

**Candidate evidence:** Rjoub et al. (2023); Slack et al. (2020); additional primary
evidence for human analyst performance if a performance claim is made.

#### 04.4 Sistemas autónomos e industriales

**Example:** an engineer uses explanations to determine why an autonomous system
selected an action or why a predictive-maintenance model signaled a failure.

**Stakeholders:** operators, engineers, safety assessors, regulators, affected users.

**Scientific boundary:** an intelligible rationale is not a safety case. It must
connect to validation, monitoring, edge cases, and fail-safe behavior.

**Candidate evidence:** Kuznietsov et al. (2024); an industrial fault-diagnosis or
predictive-maintenance systematic review selected after appraisal.

#### 04.5 Modelos fundacionales, lenguaje y sistemas multimodales

**Example:** a team investigates whether an LLM answer is grounded in supplied
evidence, reflects a memorized association, or presents a fluent but unsupported
rationale.

**Stakeholders:** users, developers, evaluators, content owners, organizations
deploying AI assistants or agents.

**Scientific boundary:** a generated chain of reasoning or natural-language rationale
is not automatically a faithful account of internal computation. Scale, emergent
behavior, multilingual variation, and multimodal representations complicate both
local and global explanation.

**Candidate evidence:** Zhao et al. (2024); later peer-reviewed surveys only after
scope and publication status are verified.

#### 04.6 Optional cross-cutting case: educación y servicios públicos

Include only if it contributes a distinct issue such as developmental impact,
procedural contestability, or differentiated explanations for professionals and
affected people. Do not add it merely to lengthen the domain list.

**Current material to reuse:**

- The domain list in `02_introduccion.md` as a transition, not as sufficient coverage.
- The high-impact replication paragraph in `10_limitaciones_trabajo_futuro.md`.
- The human-validation and recourse cautions in sections 03, 04, and 10.

**New material required:** almost the whole section. No empirical performance claims
should be invented from examples.

**Additions from the 2026-09-29 review:**

- This section closes review finding C2 together with section 06: the title,
  the section 02 roadmap and section 03's closing paragraph already promise it.
- Each domain ends with a short "horizonte próximo" paragraph: the expected use of
  XAI in that domain over the coming years, phrased as an evidence-supported
  trajectory or research need, never as a forecast. This answers the requirement on
  expected future uses of XAI at field level, not only as future work for the
  benchmark.
- Introduce here the running credit applicant (revision plan R4.6) if the finance
  example is used; sections 05 and 08 return to it.
- A stakeholder-purpose-evidence table (scaffold section 11, "Consider adding") can
  close the section instead of a prose recap.

**Acceptance question:** does every domain example identify a decision, stakeholder,
benefit, failure mode, and evidentiary requirement?

### 05. Familias explicativas y el problema de evaluarlas

**Purpose:** introduce representative explanation families while showing why their
outputs cannot be ranked on one universal scale.

**Planned subsections:**

1. Atribuciones locales: LIME y SHAP.
2. Reglas locales: Anchors.
3. Contrafactuales y recourse: DiCE.
4. Comparación por pregunta y objeto, no solo por nombre.
5. De la salida explicativa a la evaluación multidimensional.

**Standard template per method:**

- question answered;
- output produced;
- main assumptions;
- useful context;
- characteristic failure mode;
- relevant evaluation dimensions.

**Current material to reuse:**

- `04_metodos_lime_shap_anchors_dice.md`: method definitions, assumptions, and
  method-specific limitations.
- `tables/table_methods_comparison.md`: retained as the primary synthesis device.
- `05_crisis_evaluacion_xai.md`: the sections on fidelity and the gap between metric,
  construct, and claim.

**Current material to move to section 08:**

- all benchmark means, costs, coverage counts, and method performance conclusions;
- statements derived specifically from Adult Income or EXP2.

**Current material to remove or consolidate:**

- repeated end-of-method FOM-7 summaries;
- repeated warnings that the methods are not interchangeable;
- method descriptions duplicated between sections 02, 03, and 04.

**Evidence base:** current foundational method papers and existing reviews. No broad
performance claim should rely only on this chapter's benchmark.

**Additions from the 2026-09-29 review:**

- **Worked example (R4.1):** one Adult instance explained by the four methods side by
  side: LIME weights, SHAP attribution, the Anchors rule with its precision and
  coverage, and one DiCE counterfactual with a note on feasibility. Produce it with a
  committed script from the frozen models, or label it as illustrative. This is the
  section's main teaching device; it shows "different questions, different objects"
  instead of asserting it.
- **Terminology fixed here and reused everywhere:**
  - *parsimonia* is measured as the proportion of active features, so lower means
    more concise. Either rename the measure (for example "densidad de la
    explicación") or state the inversion once, prominently, at this point.
  - *brecha de fidelidad* (the Δk metric) collides with *brechas* (the field gaps of
    section 06). Rename the metric (for example "caída por enmascaramiento") or
    qualify it every time.
  - one definition of fidelity; sections 07-08 and Table 3 refer back to it.
- **SHAP variants:** state here that TreeSHAP is model-specific and KernelSHAP is
  model-agnostic, so section 08 can disclose the variant confound (review M3)
  without a new definition.
- **Remove:** the self-directed sentence "El capítulo debe cuidar especialmente el
  lenguaje al interpretar DiCE"; the "no se dice X, sino Y" closing (keep the device
  at most once in the chapter, preferably in section 07); code identifiers such as
  `logreg_anchors`.

**Acceptance question:** can the reader choose an explanation family based on the
question being asked without mistaking that choice for evidence that the method is
valid?

### 06. Brechas científicas de la XAI

**Purpose:** provide the requested field-level gap analysis and create the necessity
for a governed evaluation protocol.

**Gap taxonomy:**

| Gap | Core question | Existing material | Evidence need |
| --- | --- | --- | --- |
| Technical validity | Is the explanation faithful, stable, robust, and resistant to manipulation? | Sections 03, 05, and 10 | Nauta et al.; Alvarez-Melis and Jaakkola; Slack et al.; metric reviews |
| Construct validity | Does the metric measure the property its label implies? | Sections 03, 05, and 10 | Nauta et al.; Canha et al.; Pawlicki et al.; Bhattacharya and Verbert |
| Human validity | Does the explanation improve understanding, decisions, and calibrated reliance for the intended user? | Section 10 | Kim, Maathuis, and Sent (2024); selected primary user studies |
| Causal/action validity | Do attributions or counterfactuals support interventions and feasible recourse? | Sections 04 and 10 | Karimi et al.; Laugel et al.; Poyiadzi et al.; causal-XAI literature if used |
| Operational validity | Does the explanation remain useful under scale, latency, drift, and lifecycle change? | Sections 05 and 10 | Domain reviews and lifecycle evaluation literature |
| Governance validity | Can explanations support documentation, contestability, accountability, and oversight? | Sections 02 and 09 | NIST; EU AI Act; WHO; OECD where appropriate |
| Emerging-model validity | How should XAI evaluate generative, agentic, multilingual, or multimodal systems? | Minimal current coverage | Zhao et al. and verified peer-reviewed follow-up literature |

**Required conclusion:** the field's problem is not a lack of explanation methods. It
is the lack of evidence connecting an explanatory artifact to its intended construct,
user, task, and decision.

**Current material to reuse:** most of `05_crisis_evaluacion_xai.md`, reorganized by
gap rather than by repeated descriptions of metric fragmentation; selected parts of
`10_limitaciones_trabajo_futuro.md`.

**Additions from the 2026-09-29 review:**

- Each gap receives one concrete illustration drawn from section 04 or from a cited
  primary study; old section 05 contained six pages without an example.
- Remove arguments already made in sections 02-03 ("el nombre del método deja de ser
  una unidad experimental suficiente", "dos excesos simétricos") and the subsection
  "Implicación para el capítulo", which addresses the author.
- The regulatory gap must go beyond the Articles 13-14 summary in section 02: what
  the rules require versus what current methods can demonstrate.
- Close with a gap-to-evaluation table (already proposed in section 11 of this
  scaffold) that section 07 then maps onto the gates.

**Acceptance question:** does the section explain both the gaps FOM-7 addresses and
the gaps it does not address?

### 07. FOM-7 como respuesta metodológica

**Purpose:** present FOM-7 as the chapter's original operational response to the
functionally grounded portion of the gap landscape.

**Planned subsections:**

1. Alcance y función del protocolo.
2. Regla secuencial de admisibilidad.
3. Las siete puertas.
4. Qué brechas controla FOM-7.
5. Qué brechas quedan fuera de FOM-7.

**Gate-to-gap mapping:**

| FOM-7 gate | Primary gap controlled | Boundary |
| --- | --- | --- |
| 1. Protocol freeze | Researcher degrees of freedom and post-hoc drift | Does not prove the chosen construct is correct. |
| 2. Controlled execution | Reproducibility and undocumented configuration variation | Does not guarantee external validity. |
| 3. Artifact audit | Missing, malformed, or inadmissible evidence | Does not repair non-random missingness. |
| 4. Harmonization | Schema and unit incompatibility | Must not erase differences among explanatory objects. |
| 5. Inferential export | Pseudoreplication, unqualified inputs, and test mismatch | Does not make weak proxies meaningful. |
| 6. Reproducibility profiling | Variation across repeated runs | Does not establish human usefulness or causal validity. |
| 7. Traceable reporting | Claim drift and overstatement | Does not replace domain or user validation. |

**Current material to reuse:**

- `06_protocolo_fom7.md` and `tables/table_fom7_gates.md`.

**Current material to compress:**

- repeated descriptions of why tools are insufficient;
- repeated method-specific benchmark interpretations;
- repeated closing limitations already handled in sections 06 and 10.

**Evidence:** FOM-7's definition is project-authored. External literature supports
the problem and design principles, not an unsupported claim that FOM-7 is the first or
only such protocol. Any novelty statement requires a scoped literature check.

**Additions from the 2026-09-29 review:**

- **Gate trace figure (R4.2):** follow one claim, "SHAP supera a LIME en fidelidad",
  from cell artifacts to Table 4, one step per gate. It replaces the ASCII flow block
  ("Congelación -> ... -> Reporte"), which breaks mid-word in Word.
- **Uniform gate template is too mechanical:** give each gate its failure example in
  one or two sentences and move artifact detail (manifest, result files, recovery
  overlay) into a technical box.
- **Remove from prose:** `configs/experiments/exp2_scaled/manifest.yaml`,
  `results.json`, `outputs/batch_results.csv`, `mlp_shap`/`svm_shap`; the
  sentence "Dentro de este capítulo, FOM-7 debe presentarse como protocolo...".
- **Thesis labels:** P1 and H1-H3 must not appear before they are defined; define
  them here in one sentence each or refer only to "la proposición de
  reproducibilidad" and "las hipótesis del caso".
- **Expansion of the acronym:** confirm "Framework Operation Method" is the intended
  expansion and use it consistently with the thesis.
- **Table 2:** widen "Propósito"; see scaffold section 12.
- **Support for Gate 1:** Agarwal et al., Canha et al. and Zheng et al. support
  benchmarking discipline in general, not protocol freezing; cite a
  preregistration or researcher-degrees-of-freedom source, or narrow the sentence.

**Acceptance question:** can the reader state precisely what FOM-7 guarantees, what it
checks, and what it leaves unresolved?

### 08. Caso empírico: de un benchmark a evidencia auditable

**Purpose:** demonstrate FOM-7 through the verified Adult/tabular benchmark while
preserving every evidence boundary.

**Planned subsections:**

1. Pregunta demostrativa y alcance del caso.
2. Datos, modelos, métodos y diseño factorial.
3. Unidad de análisis y plan inferencial.
4. Auditoría y cobertura de artefactos.
5. Perfiles explicativos observados.
6. Lo que el caso demuestra sobre evaluación.
7. Lo que el caso no demuestra sobre XAI en general.

**Current material to reuse:**

- `07_diseno_empirico.md`: design, sampling, units, FOM-7 control, and inferential
  plan, compressed around decisions necessary to interpret the findings.
- `08_aplicacion_empirica_perfiles_fom7.md`: coverage, global differences, method
  profiles, reproducibility, and synthesis.
- empirical passages moved out of the current method section.
- Tables 3 and 4 and the figures selected after an information-value review.

**Compression rules:**

- Keep a statistic only if it supports a methodological lesson or a central finding.
- Do not restate the full profile of each method in more than one place.
- Prefer Table 4 for repeated values and prose for interpretation.
- Consider retaining coverage, one comparison figure, and one multidimensional
  profile figure; every additional figure must add a distinct inference.
- Preserve the distinction between block means and run means.

**Protected constraints:**

- all result-shaped numbers must remain registered;
- chapter coverage and exclusivity must remain green;
- no unpublished Paper B+C result may re-enter the chapter;
- the thesis may be cited for thesis-only results;
- RIMI-published results may remain with the appropriate citation;
- no value may be moved without checking its pinned occurrence count.

**Corrections required from the 2026-09-29 review (see revision plan R1):**

- H1: remove the retired LIME cost "226 ms" (currently in the method section, moving
  here); use registered per-model costs.
- H2: the reproducibility CVs (< 3%) come from the EXP2 RF/N=100 subset, not EXP1;
  add the pooled 11.4% (SHAP) and 12.0% (LIME). Keep section 07's EXP1 CV < 9%.
- M1: label thesis-only results (paired SHAP-LIME contrast, LIME cross-dataset
  stability) as unpublished; no causal wording about the origin of LIME instability.
- M2: qualify LIME's cost and parsimony advantage (DiCE more parsimonious; TreeSHAP
  on XGBoost cheaper; LIME on SVM 17,620 ms).
- M3: disclose that "SHAP" pools TreeExplainer and KernelExplainer.
- M4: disclose non-random Anchors missingness and its bias bound.
- M5: label the 15/15 block follow-up as exploratory and post hoc.

**Reader-experience additions:**

- Follow each key result with one sentence of practical meaning (R4.3).
- Revisit the section 05 worked example to show how the benchmark profiles appear in a
  single case.
- Put the statistical plan (Friedman, Nemenyi, Kendall's W, Holm, Wilcoxon) in a
  technical box, with a one-sentence plain gloss of each in the main text.
- Present the factorial design as a sentence or small table, not a code block.
- Remove "En un artículo empírico, esta sección podría presentarse..." and "La
  implicación para un capítulo de libro es conceptual".
- State each figure's inference in the text before the figure appears.

**Acceptance question:** does the case demonstrate why evidence governance changes
interpretation, rather than merely repeat a methods leaderboard?

### 09. Implicaciones para investigación, práctica y gobernanza

**Purpose:** translate the conceptual and empirical argument into decisions for
researchers and practitioners.

**Planned subsections:**

1. Elegir la explicación desde la pregunta y el usuario.
2. Separar exploración, auditoría y comunicación.
3. Evaluar durante todo el ciclo de vida.
4. Tratar la trazabilidad como infraestructura científica.
5. Transferir FOM-7 por adaptación, no por copia automática.

**Current material to reuse:** `09_implicaciones_evaluacion_auditable_xai.md`, with
method-specific repetition reduced and application-domain lessons added.

**Required claims:**

- Different audiences can legitimately require different explanations of the same
  system.
- Explanation design must begin with the decision and failure mode, not with a
  preferred visualization or explainer.
- Evaluation should cover pre-deployment validation and post-deployment monitoring.
- Auditability requires preserving the chain from artifact to claim.

**Additions from the 2026-09-29 review:**

- **Decision guide (R4.4):** a table with columns question type (debugging, audit,
  contestation, recourse, monitoring), relevant evidence, explanation family, what
  the Adult case can say, and what it cannot. It replaces the current "Implicaciones
  prácticas" prose, which restates section 08.
- The current section is about 700 words and mostly repeats section 08; its new
  content must come from sections 04 and 06 (domains, lifecycle, gaps).
- Remove "la pregunta editorialmente más valiosa para un capítulo de libro" and the
  third "no dice X; dice Y" passage.

**Acceptance question:** are the recommendations actionable without claiming that
FOM-7 alone establishes trustworthy AI?

### 10. Limitaciones y agenda científica

**Purpose:** separate the limitations of this chapter's evidence from the research
agenda of the broader field.

**Part A: limitations of the empirical demonstration**

- one tabular, binary-classification dataset;
- selected model families and configurations;
- proxy-dependent metrics;
- functionally grounded rather than human- or application-grounded evaluation;
- incomplete coverage for some methods;
- no causal or deployment claim.

**Part B: research agenda**

1. multimodal, text, time-series, and foundation-model evaluation;
2. standardized human-centered studies tied to decision performance;
3. causal explanation and feasible, fair recourse;
4. distribution shift, monitoring, and explanation drift;
5. adversarial robustness and security of explanations;
6. domain-specific validation in health, finance, cyber, autonomy, and public
   decision-making;
7. integration of functional, human-grounded, and application-grounded evidence.

**Current material to reuse:** most of `10_limitaciones_trabajo_futuro.md`, after
moving its general gap material to section 06 and removing duplicated method profiles.

**Acceptance question:** does each future direction follow from an identified gap
rather than from generic speculation?

### 11. Conclusiones

**Purpose:** answer the chapter's central question without introducing new evidence.

**Required sequence:**

1. XAI is necessary because consequential AI requires inspectable evidence and
   meaningful oversight.
2. XAI is insufficient when explanation is treated as persuasion, a single metric,
   or a substitute for validation.
3. Application domains make explanation requirements context- and stakeholder-bound.
4. FOM-7 contributes an operational discipline for reproducible and auditable
   functionally grounded evaluation.
5. The benchmark demonstrates that discipline under bounded conditions.
6. The field's next step is to connect technical validity to human and application
   validity.

**Current material to reuse:** the best formulations in `11_conclusiones.md`, but the
opening and closing must reflect the broader chapter rather than primarily the method
comparison.

**Additions from the 2026-09-29 review:**

- Answer explicitly the guiding question posed in section 02: "¿bajo qué condiciones
  una explicación de un sistema de IA puede considerarse evidencia útil, reproducible
  y defendible para una audiencia y un propósito concretos?"
- Do not list benchmark numbers again; the current draft states the results for the
  third time.
- Close on the field-level agenda (future uses and open gaps), not only on the
  benchmark.
- Carry over the M1 label: the paired SHAP-LIME result is a thesis result, not yet
  published.

**Acceptance question:** can the conclusion be read as the answer to the title and
central thesis?

## 7. Current-content migration map

| Current file or artifact | Disposition | New destination |
| --- | --- | --- |
| `00_hoja_diseno_editorial.md` | Update after scaffold approval | New title, objective, audience, and central message |
| `01_resumen_palabras_clave.md` | Rewrite last | Section 01 |
| `02_introduccion.md` | Retain strong opening; distribute technical detail | Sections 02, 03, 06, 07 |
| `03_fundamentos_xai.md` | Compress and generalize | Section 03, with some limits in 06 |
| `04_metodos_lime_shap_anchors_dice.md` | Keep method science; move all results out | Section 05; empirical passages to 08 |
| `05_crisis_evaluacion_xai.md` | Reorganize by gap taxonomy | Sections 05 and 06 |
| `06_protocolo_fom7.md` | Retain contribution; compress repetition | Section 07 |
| `07_diseno_empirico.md` | Compress to interpretive essentials | Section 08 |
| `08_aplicacion_empirica_perfiles_fom7.md` | Retain protected evidence; synthesize | Section 08 |
| `09_implicaciones_evaluacion_auditable_xai.md` | Retain and broaden | Section 09 |
| `10_limitaciones_trabajo_futuro.md` | Split gaps from agenda | Sections 06 and 10 |
| `11_conclusiones.md` | Rewrite around broad thesis | Section 11 |
| Table 1: methods | Retain and simplify if necessary | Section 05 |
| Table 2: FOM-7 gates | Retain; add gap mapping in prose or note | Section 07 |
| Table 3: metrics | Retain in case-study context | Section 08 |
| Table 4: results | Retain under guards | Section 08 |
| Six current figures | Review for unique information value | Primarily section 08 |

## 8. Claim-evidence matrix for the new material

| ID | Planned claim | Evidence class | Current status |
| --- | --- | --- | --- |
| G01 | XAI includes multiple goals, audiences, and explanatory objects. | Conceptual reviews and taxonomies | Strong existing support |
| G02 | Explainability can support debugging, monitoring, audit, oversight, and contestability. | Authoritative framework plus domain evidence | Candidate set verified: NISTIR 8312, NIST AI RMF, AI Act, WHO |
| G03 | Explainability is not sufficient for trustworthy AI. | NIST/WHO plus critical literature | Candidate set verified: Tabassi (2023), WHO (2021), Ghassemi et al. (2021) |
| G04 | Human-centered XAI evaluation lacks standardization. | Systematic review | Candidate verified: Kim et al. (2024) |
| G05 | Explanations can produce misplaced or uncalibrated reliance. | Human-subject primary studies and reviews | Primary counterevidence verified: Alufaisan et al. (2021); Poursabzi-Sangdeh et al. (2021) |
| A01 | Health XAI can support model interrogation but does not validate a clinical decision. | WHO, critical viewpoint, systematic review | Candidate set verified: WHO (2021); Ghassemi et al. (2021) |
| A02 | Finance uses XAI across credit, risk, markets, and fraud, with distinct stakeholder needs. | Finance systematic review | Candidate verified: Weber et al. (2024) |
| A03 | Cybersecurity explanations must support analyst action and resist adversarial use. | Cybersecurity survey plus primary evidence | Verified: Rjoub et al. (2023) and bounded user counterevidence from Roch et al. (2026) |
| A04 | Autonomous-system explanations contribute to monitoring and validation but are not a safety case. | Systematic review and safety literature | Verified: Kuznietsov et al. (2024) plus explanation-error evidence from Kaufman et al. (2025) |
| A05 | LLM explanations face scale, faithfulness, and rationale-generation problems distinct from conventional tabular XAI. | Peer-reviewed LLM survey plus primary evidence | Verified as a contested claim: Zhao et al. (2024), Turpin et al. (2023), and Zaman and Srivastava (2026) |
| C01 | Feature attribution is not causal explanation. | Conceptual and causal-XAI literature | Partial existing support |
| C02 | Model-valid counterfactuals are not automatically feasible recourse. | Recourse surveys and primary methods | Strong existing support |
| E01 | XAI evaluation is multidimensional and proxy-dependent. | Systematic reviews and tool papers | Strong existing support |
| E02 | Artifact, construct, metric, test, result, and claim must remain aligned. | Existing reviews plus chapter synthesis | Strong existing support; phrase as synthesis |
| F01 | FOM-7 governs the admissibility of functionally grounded comparative evidence. | Project protocol and benchmark record | Existing project evidence |
| F02 | FOM-7 does not establish human usefulness, causal validity, or deployment impact. | Protocol scope plus evaluation taxonomy | Strong existing support |
| B01 | The Adult benchmark demonstrates method differences under declared conditions. | Registered artifacts, RIMI, thesis | Verified and protected |

## 9. Literature acquisition checklist

Before any new source enters prose:

- [x] Verify the title, author list, year, venue, DOI, and publication status for the
      first candidate set.
- [x] Prefer the publisher, DOI record, PubMed, IEEE, ACM, JMLR, institutional
      repository, official standard, or official regulation page.
- [x] Locate an open-access version when available.
- [x] Read enough of the source to confirm it supports the staged claim.
- [x] Record the supported claim and any limitation in `sources/evidence_map.md`.
- [ ] Add the source to both bibliography representations.
- [x] Record acceptance in `references/citation_audit.md`.
- [x] Avoid using a systematic review as proof of a specific empirical effect when the
      original study is available and load-bearing.
- [x] Include critical or null evidence for contested claims about trust and decision
      performance.

The unchecked bibliography item is deliberately deferred until revised prose cites a
candidate, preventing uncited works from entering the final reference list.

## 10. Readability devices

The chapter should use a small number of recurring devices:

- **Domain example boxes:** decision, stakeholder, explanation, risk, evidence.
- **Comparison tables:** explanation families and application requirements.
- **Boundary sentences:** “Esto permite afirmar X; no permite concluir Y.”
- **Short transitions:** explain why the next section is necessary.
- **One definition per term:** later sections refer back instead of redefining.
- **Layered detail:** general explanation first, technical qualification second.

Avoid fictional case outcomes, anthropomorphic language, unexplained acronyms, and
long lists of citations detached from individual claims.

Added after the 2026-09-29 review:

- **Worked examples:** the four-method case (section 05) and the gate trace (section
  07) are the two anchoring examples; section 08 returns to the first.
- **Technical boxes:** implementation and statistical detail that a methods reader
  needs but the argument does not (sections 07-08).
- **Practical-meaning sentence** after each key number.
- **Banned in reader-facing prose:** sentences addressed to the author ("el capítulo
  debe...", "para un capítulo de libro..."); repository paths, file names and code
  identifiers; undefined thesis labels (P1, H1-H3); more than one use of "no se dice
  X, sino Y".
- **Paragraph length:** split paragraphs longer than about eight lines in the Word
  render, and reduce chains of nominalizations in sections 05-07.
- **Roadmap check:** the section 02 roadmap and the section 03 closing paragraph must
  name the sections that actually follow.

## 11. Tables and figures

### Retain

- Table 1: methods, reframed around explanatory question and output.
- Table 2: FOM-7 gates.
- Table 3: benchmark metrics.
- Table 4: verified results summary.

### Consider adding

- One conceptual table mapping stakeholder, purpose, explanation type, and evidence
  requirement across application domains.
- One gap-to-evaluation table derived from section 06.

### Review before retaining all six figures

The empirical section should not carry multiple figures that communicate the same
ranking. Candidate minimum:

- artifact coverage;
- one global comparison figure;
- one multi-metric or quality-cost profile.

Any removed figure remains available in the repository; removal from the chapter does
not delete the asset.

### Figure requirements from the 2026-09-29 review

| Figure (reviewed build) | Defect | Required change |
| --- | --- | --- |
| 1. Coverage heatmap | Black cell labels on near-black cells after grayscale conversion. | Label colour by cell luminance; design in grayscale. |
| 2. Critical-difference diagram | Small, low-contrast method labels. | Larger black labels; keep the non-significance bars. |
| 3. Box plots | Printed values are medians, unregistered, and read as the means in the text. | Remove the labels or mark them as medians and register them. |
| 4. Stability-cost | Legend greys indistinguishable; symmetric SD bars on a log axis run below zero and are clipped. | Marker shapes plus direct labels; IQR or min-max bars. |
| 5-6. Correlation, radar | Candidates for removal under the minimum-figure rule. | Keep only if they support a distinct inference stated in the text. |
| All | Titles and CSV filenames inside the images; captions below, fully italic, with "Fuente:". | APA caption above (bold number, italic title) and *Nota.* below; no text duplicated inside the image. |

Planned additions: the four-method worked example (section 05) and the gate-trace
diagram (section 07). All figures come from `scripts/generate_cifie_chapter_figures.py`,
committed, and each data label is registered or removed.

## 12. Word rendering scaffold

The chapter-specific Word pipeline should eventually apply these compatible thesis
standards:

- justified body paragraphs;
- 1.5 line spacing;
- consistent heading hierarchy;
- decimal page numbering;
- centered figures and captions;
- APA-style table number, italic title, body, and note;
- bibliography with hanging indentation;
- stable page breaks around headings, tables, and figures;
- accessible figure sizing and readable table widths.

Do not automatically copy thesis-only cover, dedication, acknowledgements, chapter
numbering conventions, or front-matter pagination.

Status against the 2026-09-29 reviewed build (Word render, 75 pages):

| Standard | Status | Remaining work |
| --- | --- | --- |
| Black ink | Met for text (all runs explicit black, no theme colours) | Figures must be legible in grayscale (section 11 above). |
| Justified body | Met for body, captions, notes and references | Code blocks must be left-aligned; table cells stay left-aligned by decision. |
| 1.5 line spacing | Met for all 462 paragraphs, including table cells | None. |
| "Fuente inicial" removed | Met in the package | The notes remain in the sources and are stripped only by the build; keep that step committed. |
| Decimal page numbers | Missing | Add a footer page field. |
| Page geometry | Undefined (renders Letter here) | Set page size and margins explicitly. |
| Stable breaks | Not met | Keep-with-next on table number, title and header; keep notes with the table (Tables 2 and 3). |
| Readable tables | Not met for Table 2 | Widen "Propósito" (2.35 cm) so no word breaks. |
| Centered figures and APA captions | Figures centered; captions not APA | See section 11 above. |
| Hanging references | Met | Decide whether justified references (wide gaps near DOIs) are acceptable. |

## 13. Verification plan for later prose changes

After each completed section revision:

1. audit all new citations against the bibliography;
2. run a numerical-literal check before finalizing the section;
3. run `python scripts/pubs/verify_claims.py` for any numeric or protected edit;
4. run the exclusivity check through the same verifier;
5. rebuild the Word output after any completed structural unit;
6. visually inspect the changed pages;
7. update the evidence map and citation audit in the same section-level unit.

At chapter completion, run all three project verifiers, a full Scientific Advisor
rigor review, and a final reference audit.

Added after the 2026-09-29 review:

8. build only from committed state, and record the commit hash with each reviewed
   DOCX;
9. render through Microsoft Word for visual inspection (the 2026-09-29 checkpoint
   recorded 48 pages and readable tables; Word shows 75 pages and three layout
   defects);
10. after widening a retired-value guard, negative-test it by reintroducing the value;
11. run `scripts/pubs/scan_shared_literals.py --strict` for any value moved between
    sections;
12. cross-check cited versus listed references on the rendered DOCX text, not only
    on the sources;
13. re-run the top-level statement sweep (title, Resumen, section 02 roadmap,
    conclusions) whenever a claim is rescoped.

## 14. Baseline recorded for this scaffold

On 2026-09-28, before creating this scaffold:

- `verify_claims.py`: passed; 257 claims re-derived, 429 manuscript sites checked,
  26 retired-value guards clear, 19 files fully registered, and 15 files clear of
  unpublished results;
- `verify_sync.py`: passed;
- `verify_exp4_reconstruction.py`: passed against the 18 source-file hash pins;
- the CIFIE lane had no shared-substrate difference from `origin/main`;
- no manuscript section, table, bibliography, or build script was changed.

## 15. Execution decision recorded

The author's instruction to proceed activates this scaffold as the working baseline.
The following defaults govern the next revision unit:

- retain the working-title direction, subject to refinement after prose review;
- use the five priority domains already defined;
- retain the fourteen-to-sixteen-thousand-word planning range;
- treat the benchmark as a bounded case study; and
- keep education and public services as cross-cutting examples unless later evidence
  justifies a distinct subsection.

The expanded claim-evidence pass is now recorded in `sources/evidence_map.md`,
`sources/source_inventory.md`, `references/citation_audit.md`, and
`references/candidate_literature_2026-09-28.md`. The principal targeted gaps now have
bounded primary evidence or explicit narrowing. The next execution unit is the
structural update to the production outline and editorial design sheet. No section
prose has yet been moved or rewritten.
