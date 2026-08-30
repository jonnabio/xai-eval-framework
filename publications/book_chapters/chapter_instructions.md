You are working inside my existing research/development repository:

`C:\Users\jonna\Github\xai-eval-framework`

This repository supports my doctoral thesis and related papers about model-agnostic evaluation frameworks for Explainable AI, including FOM-7, benchmarking of LIME, SHAP, Anchors, and DiCE, and empirical evaluation of XAI methods.

I now need to incorporate a new publication workstream into this same repository: a Spanish, highly technical book chapter for the CIFIE collective book. The chapter is derived from my doctoral dissertation and symposium presentation. It will have Jonathan Herrera-Vásquez as first author and Miguel Herrero-Uceda as second author, both affiliated with Universidad Americana de Europa (UNADE). Jonathan Herrera-Vásquez has ORCID `0000-0002-7149-6635`.

The book chapter must be treated as a formal publication artifact connected to the thesis, but not as part of the thesis manuscript itself. It should be organized as a distinct publication output under a `publications/book_chapters/` structure.

Please inspect the existing repository structure first. Then create a clean folder structure for the CIFIE book chapter using this preferred path:

`publications/book_chapters/2026_cifie_xai_fom7/`

Create the following directories:

```text
publications/book_chapters/2026_cifie_xai_fom7/
├── README.md
├── manuscript/
├── editorial/
├── sources/
├── figures/
│   ├── editable/
│   └── exported/
├── tables/
├── references/
├── compliance/
├── drafts/
│   ├── v0_planning/
│   ├── v1_structural_draft/
│   ├── v2_technical_draft/
│   ├── v3_editorial_review/
│   └── v4_submission/
└── final/
    └── submission_package/
```

Inside `manuscript/`, create the following Markdown files:

```text
00_hoja_diseno_editorial.md
01_resumen_palabras_clave.md
02_introduccion.md
03_fundamentos_xai.md
04_metodos_lime_shap_anchors_dice.md
05_crisis_evaluacion_xai.md
06_protocolo_fom7.md
07_diseno_empirico.md
08_resultados.md
09_discusion.md
10_limitaciones_trabajo_futuro.md
11_conclusiones.md
chapter_outline.md
chapter_full.md
```

Inside `tables/`, create these placeholder files:

```text
table_methods_comparison.md
table_metrics.md
table_fom7_gates.md
table_results_summary.md
```

Inside `references/`, create:

```text
references.bib
references_apa7.md
citation_audit.md
```

Inside `compliance/`, create:

```text
author_checklist_working.md
ai_use_declaration.md
rubric_self_assessment.md
submission_packet.md
```

Inside `figures/`, create:

```text
figure_registry.md
```

The `README.md` must explain that this folder contains the planning, source materials, manuscript drafts, figures, tables, references, compliance artifacts, and final submission package for the CIFIE collective book chapter derived from the doctoral research project on model-agnostic evaluation frameworks for Explainable AI.

Use the following content direction for the README:

- Chapter language: Spanish.
- Writing style: impersonal academic style.
- Technical level: high.
- Central contribution: FOM-7 as a reproducible protocol for multi-metric benchmarking of post-hoc, model-agnostic explanation methods.
- Methods discussed: LIME, SHAP, Anchors, and DiCE.
- Empirical results: to be incorporated directly from the dissertation and related paper material.
- Relationship to thesis: derived from and connected to the doctoral dissertation, but managed as an independent publication artifact.
- Authors:
  - Jonathan Herrera-Vásquez, Universidad Americana de Europa, ORCID: 0000-0002-7149-6635.
  - Miguel Herrero-Uceda, Universidad Americana de Europa.

Create `manuscript/00_hoja_diseno_editorial.md` with the following sections in Spanish:

```markdown
# Hoja de diseño editorial

## Título provisional

Del modelo de caja negra a la evidencia auditable: evaluación reproducible de métodos agnósticos de explicabilidad mediante el protocolo FOM-7

## Autoría

- Jonathan Herrera-Vásquez
- Miguel Herrero-Uceda

## Afiliación institucional

Universidad Americana de Europa (UNADE)

## ORCID

- Jonathan Herrera-Vásquez: https://orcid.org/0000-0002-7149-6635
- Miguel Herrero-Uceda: Pendiente / no disponible

## Tema central

Evaluación reproducible, multi-métrica y auditable de métodos de inteligencia artificial explicable agnósticos al modelo.

## Problema que aborda

La evaluación de métodos de explicabilidad en inteligencia artificial suele realizarse de manera fragmentada, con énfasis excesivo en métricas aisladas de fidelidad, sin suficiente trazabilidad de artefactos, control de variabilidad, comparación estadística o separación clara entre evidencia exploratoria y confirmatoria.

## Objetivo del capítulo

Analizar y demostrar la necesidad de protocolos reproducibles para la evaluación de métodos agnósticos de explicabilidad en inteligencia artificial, tomando como base el protocolo FOM-7 y un benchmark empírico sobre métodos post-hoc como LIME, SHAP, Anchors y DiCE.

## Tipo de capítulo

Investigación empírica de orientación metodológica derivada de tesis doctoral.

## Público al que se dirige

Investigadores en inteligencia artificial, ciencia de datos, explicabilidad algorítmica, auditoría de modelos, gobernanza de IA, evaluación tecnológica y metodologías de investigación aplicada.

## Principal aportación

El capítulo propone y contextualiza FOM-7 como un protocolo operativo para transformar la evaluación de explicaciones post-hoc en un proceso reproducible, multi-métrico y auditable.

## Mensaje principal que debe recordar el lector

La explicabilidad útil no depende únicamente de generar explicaciones plausibles, sino de evaluar cuándo dichas explicaciones merecen ser consideradas fieles, estables, comparables, reproducibles y técnicamente defendibles.

## Palabras clave

- Inteligencia artificial explicable
- Explicabilidad agnóstica al modelo
- Benchmarking de XAI
- FOM-7
- Evaluación reproducible
```

Create `manuscript/chapter_outline.md` with a detailed Spanish outline using this structure:

```markdown
# Esquema del capítulo

## Título provisional

Del modelo de caja negra a la evidencia auditable: evaluación reproducible de métodos agnósticos de explicabilidad mediante el protocolo FOM-7

## Extensión recomendada

7,000 a 8,500 palabras, salvo que la editorial indique posteriormente un límite diferente.

## Estructura propuesta

### 1. Resumen

Síntesis de 150 a 250 palabras. Debe redactarse al final.

### 2. Palabras clave

Tres a cinco palabras clave según la guía editorial.

### 3. Introducción

Plantear el problema de los modelos de caja negra y la necesidad de evaluar rigurosamente las explicaciones generadas por métodos XAI.

### 4. Fundamentos técnicos de la explicabilidad agnóstica al modelo

Definir caja negra, interpretabilidad, explicabilidad, métodos post-hoc, métodos agnósticos al modelo, explicaciones locales y globales, y diferencia entre plausibilidad y fidelidad.

### 5. Métodos post-hoc evaluados: LIME, SHAP, Anchors y DiCE

Presentar cada método con base matemática, tipo de explicación, fortaleza principal y limitación técnica.

### 6. La crisis de evaluación en XAI

Analizar la fragmentación metodológica, el exceso de evaluación centrada en fidelidad, la falta de trazabilidad y la necesidad de protocolos reproducibles.

### 7. Protocolo FOM-7 para benchmarking auditable

Desarrollar las siete etapas de FOM-7:

1. Congelamiento del protocolo.
2. Ejecución controlada por lotes.
3. Auditoría de artefactos.
4. Armonización inferencial.
5. Exportación determinista de artefactos pareados.
6. Perfilado de dispersión entre ejecuciones.
7. Reporte de afirmaciones trazables a evidencia fuente.

### 8. Diseño empírico del benchmark

Describir dataset, modelos, métodos XAI, celdas experimentales, artefactos, métricas y pruebas estadísticas.

### 9. Resultados principales: frontera calidad-costo

Presentar los hallazgos centrales: diferencias globales significativas, SHAP como método fuerte en calidad explicativa, LIME como alternativa de bajo costo, DiCE como opción destacada en concisión/contrafactualidad y ausencia de un método universalmente dominante.

### 10. Discusión

Interpretar las implicaciones para IA confiable, auditoría técnica, gobernanza de modelos, investigación doctoral y reproducibilidad científica.

### 11. Limitaciones y trabajo futuro

Reconocer límites del estudio y líneas futuras: visión, texto, series temporales, evaluación con usuarios, causalidad, robustez adversarial, sensibilidad contrafactual y escalabilidad.

### 12. Conclusiones

Cerrar con una interpretación fuerte sobre la necesidad de pasar de explicaciones plausibles a evidencia auditable.
```

Create `compliance/ai_use_declaration.md` with a Spanish draft stating that AI tools may be used only as auxiliary support for organization of ideas, style improvement, linguistic review, structural coherence, and editorial review. Explicitly state that AI must not be used to fabricate data, generate experimental results, invent references, replace academic judgment, or substitute the intellectual responsibility of the authors.

Create `compliance/rubric_self_assessment.md` with a checklist aligned to the CIFIE rubric:

```markdown
# Autoevaluación frente a la rúbrica editorial CIFIE

## Pertinencia y contribución académica

- [ ] El capítulo se alinea claramente con el eje temático del libro.
- [ ] La contribución metodológica de FOM-7 está claramente identificada.
- [ ] La aportación al conocimiento puede resumirse en una oración.

## Rigor científico

- [ ] Existe coherencia entre problema, objetivo, metodología, resultados y conclusiones.
- [ ] La fundamentación teórica es pertinente y actualizada.
- [ ] Las afirmaciones están sustentadas por evidencia verificable.
- [ ] La metodología empírica está descrita con suficiente precisión.

## Organización del capítulo

- [ ] La estructura facilita la comprensión del lector.
- [ ] Cada sección cumple una función argumental específica.
- [ ] Las conclusiones responden al objetivo.
- [ ] Existe correspondencia entre título, resumen, objetivo, desarrollo y conclusiones.

## Calidad de la escritura

- [ ] El texto utiliza lenguaje académico claro, técnico y preciso.
- [ ] Las citas dialogan con el argumento y no sustituyen la voz de los autores.
- [ ] Las tablas y figuras aportan información relevante.

## Aspectos editoriales

- [ ] El manuscrito sigue la plantilla editorial.
- [ ] Las citas y referencias cumplen APA 7.
- [ ] La versión final está lista para evaluación editorial.
```

Create `references/citation_audit.md` with sections for:

- Citas pendientes de verificar.
- Referencias sin cita en texto.
- Citas sin entrada bibliográfica.
- DOI pendientes.
- URL pendientes de validación.
- Figuras/tablas que requieren fuente.

Create `figures/figure_registry.md` with columns:

- Figure ID.
- Proposed title.
- Source material.
- Editable file.
- Exported file.
- Used in section.
- Citation/source note.
- Status.

Create `tables/table_methods_comparison.md` with an initial Markdown table comparing LIME, SHAP, Anchors, and DiCE across:

- Base matemática.
- Tipo de salida.
- Fortaleza principal.
- Limitación principal.
- Uso dentro del capítulo.

Create `tables/table_fom7_gates.md` with a table listing the seven FOM-7 gates, purpose, expected artifact, and role in claim eligibility.

Do not overwrite existing thesis or paper files. If similar folders already exist, adapt the structure conservatively and avoid duplication. Prefer creating a new branch named:

`publication/cifie-xai-fom7-book-chapter`

After creating the structure, provide a concise summary of:

1. Files and folders created.
2. Any existing structure you reused.
3. Any conflicts or assumptions.
4. Recommended next steps.
