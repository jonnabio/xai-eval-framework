# Auditoría de citas

## Estado de extracción inicial

- Fuente base: `thesis/references.bib`.
- Alcance de esta pasada: referencias fundacionales para LIME, SHAP, Anchors, DiCE, evaluación XAI, benchmarking reproducible, robustez/fidelidad, taxonomías y pruebas estadísticas.
- Estado: entradas copiadas a `references/references.bib`; falta validación editorial APA 7 completa antes de envío.

## Citas pendientes de verificar

- `@ribeiro2016` — LIME / modelos sustitutos locales.
- `@adadi2018` — revisión XAI y problema de caja negra.
- `@ali2023` — estado de XAI y requisitos de IA confiable.
- `@arrieta2019` — conceptos, taxonomías y retos de XAI responsable.
- `@belle2021` — principios y práctica de aprendizaje automático explicable.
- `@carvalho2019` — revisión de métodos y métricas de interpretabilidad.
- `@breiman2001` — bosque aleatorio como familia de modelo predictivo.
- `@guidotti2018` — revisión de métodos para explicar modelos de caja negra.
- `@karimi2022` — recourse algorítmico, recomendaciones consecuenciales y contrafactuales.
- `@kohavi1996` — conjunto UCI Adult Income.
- `@lakens2013` — reporte e interpretación de tamaños de efecto.
- `@laugel2019` — riesgos de contrafactuales post-hoc injustificados.
- `@lundberg2017` — SHAP / valores de Shapley.
- `@lipton2018` — crítica conceptual a la interpretabilidad.
- `@marcinkevics2023` — panorama metodológico de interpretabilidad y explicabilidad.
- `@ribeiro2018` — Anchors / reglas locales de alta precisión.
- `@mothilal2020` — DiCE / explicaciones contrafactuales diversas.
- `@murdoch2019` — definiciones, métodos y aplicaciones de aprendizaje interpretable.
- `@miller2019` — explicación como fenómeno contrastivo y social; verificada en pasada fundamentos XAI 2026-07-04 mediante Semantic Scholar, OpenAlex, Crossref y arXiv.
- `@poyiadzi2020` — FACE y contrafactuales factibles/accionables.
- `@slack2020` — ataques adversariales a explicaciones post-hoc LIME/SHAP.
- `@vandenbroeck2022` — tractabilidad de explicaciones SHAP.
- `@wachter2017` — contrafactuales y decisiones automatizadas.
- `@doshi-velez2017` — evaluación rigurosa de interpretabilidad; verificada en pasada OA 2026-07-04 mediante OpenAlex/arXiv.
- `@alvarezmelis2018` — robustez de métodos de interpretabilidad.
- `@canha2025` — benchmark functionally-grounded para XAI; verificada en pasada OA 2026-07-04 mediante OpenAlex y Crossref.
- `@abdulkadir2023` — revisión/taxonomía de métricas XAI.
- `@hedstrom2023` — Quantus y evaluación responsable de explicaciones; verificada en pasada OA 2026-07-04 mediante Semantic Scholar, OpenAlex/arXiv y JMLR.
- `@agarwal2022` — OpenXAI y evaluación transparente; verificada en pasada OA 2026-07-04 mediante Semantic Scholar y OpenAlex/arXiv.
- `@zheng2025` — F-FIDELITY y evaluación de fidelidad.
- `@nauta2023` — revisión sistemática de evaluación cuantitativa XAI; verificada en pasada OA 2026-07-04 mediante Semantic Scholar, OpenAlex y Crossref.
- `@rudin2022` — principios y retos de aprendizaje automático interpretable.
- `@friedman1937` — prueba de Friedman para comparación por rangos.
- `@demsar2006` — comparación estadística no paramétrica de clasificadores/métodos.
- `@nemenyi1963` — comparaciones múltiples post-hoc de Nemenyi.
- `@wilcoxon1945` — prueba pareada de rangos con signo.
- `@altukhi2025` — revisión reciente de avances XAI.
- `@schwalbe2023` — taxonomía de conceptos y métodos XAI.
- `@pawlicki2024` — necesidad de múltiples métricas en evaluación XAI; verificada en pasada OA 2026-07-04 mediante Semantic Scholar, OpenAlex y Crossref.
- `@bhattacharya2024` — evaluación multidimensional de explicaciones; verificada en pasada OA 2026-07-04 mediante OpenAlex y Crossref.
- `@burger2023` — estabilidad de LIME.

## Pasada de enriquecimiento OA: 2026-07-04

Objetivo: reforzar afirmaciones sobre evaluación multidimensional, límites de transferencia de métricas, distinción entre evaluación funcional y estudios con usuarios, y necesidad de benchmarks trazables.

### Bases consultadas

- Semantic Scholar Graph API:
  - Búsquedas temáticas intentadas: evaluación XAI, OpenXAI, Quantus, evaluación human-grounded y benchmark functionally-grounded.
  - Resultado: la búsqueda general devolvió HTTP 429 por límite del *shared rate pool* sin API key.
  - Consultas por identificador con resultado parcial:
    - `DOI:10.1145/3583558` → `@nauta2023`, Semantic Scholar paperId `7caaafd5a3ee033c98e792c7ea5b699d005753d5`, OA confirmado, PDF ACM registrado.
    - `DOI:10.1016/j.neucom.2024.128282` → `@pawlicki2024`, Semantic Scholar paperId `c44d4ef36b44e4d40861c900881e7153a2cbf958`, OA confirmado.
    - `ARXIV:2202.06861` → `@hedstrom2023`, Semantic Scholar paperId `30e776268268e84becd2863b0632247da61238b9`, identificado como Quantus/JMLR/arXiv.
    - `ARXIV:2206.11104` → `@agarwal2022`, Semantic Scholar paperId `868e35374cb9c0fc6e4cfb17f96835aefcf520cc`, identificado como OpenXAI/arXiv.
- OpenAlex:
  - `@nauta2023` → OpenAlex `W4321786089`, DOI `10.1145/3583558`, OA híbrido, ACM Computing Surveys.
  - `@canha2025` → OpenAlex `W4410705990`, DOI `10.1145/3737445`, OA verde, ACM Computing Surveys.
  - `@pawlicki2024` → OpenAlex `W4401009060`, DOI `10.1016/j.neucom.2024.128282`, OA híbrido, Neurocomputing.
  - `@bhattacharya2024` → OpenAlex `W4400106588`, DOI `10.1145/3631700.3664911`, OA verde, UMAP Adjunct.
  - `@doshi-velez2017` → OpenAlex `W2594475271`, DOI `10.48550/arXiv.1702.08608`, OA verde, arXiv.
- Crossref:
  - DOI metadata verified for `@nauta2023`, `@canha2025`, `@pawlicki2024`, and `@bhattacharya2024`.
  - Crossref returned 404 for arXiv DOI lookups `10.48550/arXiv.1702.08608`, `10.48550/arXiv.2202.06861`, and `10.48550/arXiv.2206.11104`; these remain verified through OpenAlex/Semantic Scholar/arXiv/JMLR URLs rather than Crossref.

### Fuentes aceptadas para esta pasada

- `@nauta2023` — aceptada para respaldar que la evaluación XAI requiere métodos cuantitativos, multidimensionales y dependientes del tipo de explicación.
- `@canha2025` — aceptada para respaldar el encuadre *functionally-grounded* y los límites de generalización de benchmarks funcionales.
- `@pawlicki2024` — aceptada para respaldar la necesidad de múltiples métricas en evaluación XAI.
- `@bhattacharya2024` — aceptada para respaldar la evaluación multidimensional y la estandarización de criterios para métodos XAI diversos.
- `@doshi-velez2017` — aceptada para respaldar la distinción entre evaluación funcional, *human-grounded* y *application-grounded*.
- `@hedstrom2023` y `@agarwal2022` — conservadas como soporte de herramientas/benchmarks de evaluación; se añadieron URLs OA a las referencias de trabajo.

### Fuentes no aceptadas o no usadas

- Búsquedas generales de Semantic Scholar no produjeron candidatos adicionales por HTTP 429.
- No se añadieron fuentes nuevas solo por actualidad; las fuentes aceptadas ya tenían correspondencia directa con afirmaciones presentes en las secciones 09 y 10.

## Pasada de enriquecimiento fundamentos XAI: 2026-07-04

Objetivo: fortalecer `03_fundamentos_xai.md` con distinciones verificadas sobre interpretabilidad, explicabilidad, transparencia, artefactos post-hoc, alcance local/global, plausibilidad, fidelidad, estabilidad, robustez y evaluación funcional bajo FOM-7.

### Bases consultadas

- Semantic Scholar Graph API:
  - Consulta por DOI con resultado aceptado:
    - `DOI:10.1073/pnas.1900654116` → `@murdoch2019`, Semantic Scholar paperId `b9518627db25f05930e931f56497602363a75491`, CorpusId `204755862`, OA confirmado, PDF PNAS registrado.
    - `DOI:10.1002/widm.1493` → `@marcinkevics2023`, Semantic Scholar paperId `7297439e3d43ac95080c9a572b2a925cdc8f9765`, CorpusId `257290340`, OA confirmado, PDF Wiley registrado.
    - `DOI:10.1016/j.artint.2018.07.007` → `@miller2019`, Semantic Scholar paperId `e89dfa306723e8ef031765e9c44e5f6f94fd8fda`, CorpusId `36024272`, OA confirmado, PDF arXiv `1706.07269` registrado.
  - Consultas por DOI con HTTP 429 en el *shared rate pool*: `@lipton2018`, `@nauta2023`, `@schwalbe2023`, `@rudin2022`.
  - Búsqueda temática `explainable AI evaluation fidelity stability robustness metrics` devolvió HTTP 429; se usaron OpenAlex y Crossref para cross-check de candidatos ya identificados por DOI.
- OpenAlex:
  - `@murdoch2019` → OpenAlex `W2910705748`, DOI `10.1073/pnas.1900654116`, OA bronce, PNAS.
  - `@marcinkevics2023` → OpenAlex `W4322621694`, DOI `10.1002/widm.1493`, OA híbrido, WIREs Data Mining and Knowledge Discovery.
  - `@nauta2023` → OpenAlex `W4321786089`, DOI `10.1145/3583558`, OA híbrido, ACM Computing Surveys.
  - `@schwalbe2023` → OpenAlex `W4313650676`, DOI `10.1007/s10618-022-00867-8`, OA híbrido, Data Mining and Knowledge Discovery.
  - `@rudin2022` → OpenAlex `W3137125108`, DOI `10.1214/21-SS133`, OA diamante, Statistics Surveys.
  - `@miller2019` → OpenAlex `W2670253439`, DOI `10.1016/j.artint.2018.07.007`, OA verde, arXiv PDF `1706.07269`.
- Crossref:
  - DOI metadata verified for `@lipton2018`, `@murdoch2019`, `@marcinkevics2023`, `@nauta2023`, `@schwalbe2023`, `@rudin2022`, and `@miller2019`.
  - Crossref confirmed `@miller2019` as journal article in *Artificial Intelligence*, published 2019-02.

### Fuentes aceptadas para esta pasada

- `@miller2019` — añadida para respaldar que las explicaciones tienen una dimensión contrastiva y social, sin convertir plausibilidad para una audiencia en fidelidad técnica.
- `@murdoch2019` — reutilizada para respaldar definiciones y métodos de aprendizaje interpretable.
- `@marcinkevics2023` y `@schwalbe2023` — reutilizadas para respaldar distinciones entre familias de métodos, conceptos y salidas explicativas.
- `@nauta2023`, `@canha2025`, `@pawlicki2024`, `@bhattacharya2024`, `@hedstrom2023` y `@zheng2025` — reutilizadas para sostener evaluación cuantitativa, multidimensional, proxy-based y dependiente del constructo.
- `@lipton2018`, `@rudin2022`, `@doshi-velez2017` y `@alvarezmelis2018` — reutilizadas para sostener ambigüedad conceptual, preferencia por modelos interpretables cuando corresponde, alcance de evaluación funcional y límites de robustez.

### Fuentes no aceptadas o no usadas

- No se aceptaron candidatos nuevos a partir de búsqueda temática porque Semantic Scholar devolvió HTTP 429.
- No se añadieron fuentes adicionales sobre explicabilidad human-centered más allá de `@miller2019`, ya que el capítulo no evalúa usuarios ni comprensión subjetiva.

## Referencias sin cita en texto

Tras las pasadas de redacción controlada, las referencias fundacionales y de evaluación más relevantes ya se citan en el manuscrito. Antes del envío debe ejecutarse una revisión final para detectar entradas remanentes en `references/references.bib` que no aparezcan en `manuscript/*.md`.

## Citas sin entrada bibliográfica

- Ninguna detectada en esta pasada. Las futuras citas del manuscrito deben cotejarse contra `references/references.bib`.

## DOI pendientes

- `@alvarezmelis2018`: entrada arXiv con URL; sin DOI en la fuente de tesis.
- `@hedstrom2023`: sin DOI JMLR registrado en la entrada de trabajo; URL oficial JMLR y arXiv `2202.06861` añadidos.
- `@agarwal2022`: sin DOI NeurIPS registrado en la entrada de trabajo; URL arXiv `2206.11104` añadida.
- `@zheng2025`: entrada fuente usa URL del proyecto; verificar DOI/publicación final si existe.

## URL pendientes de validación

- `https://arxiv.org/abs/1806.08049` (`@alvarezmelis2018`).
- `https://trustai4s-lab.github.io/ffidelity` (`@zheng2025`).
- Página oficial de Quantus/JMLR para `@hedstrom2023` registrada en la pasada OA de 2026-07-04.
- Página arXiv/OpenXAI para `@agarwal2022` registrada en la pasada OA de 2026-07-04.

## Figuras/tablas que requieren fuente

- `tables/table_metrics.md`: derivada de `thesis/capitulo-1-marco-teorico.qmd` y `thesis/capitulo-3-diseno-experimental.qmd`.
- `tables/table_methods_comparison.md`: debe cotejarse con `thesis/capitulo-2-fundamentos.qmd` y las referencias fundacionales de cada método.
- Futuras figuras copiadas desde `thesis/assets/figures/` deberán registrarse en `figures/figure_registry.md` con fuente exacta.
