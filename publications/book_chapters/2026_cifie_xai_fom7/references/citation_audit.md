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
- `@lundberg2017` — SHAP / valores de Shapley.
- `@lipton2018` — crítica conceptual a la interpretabilidad.
- `@marcinkevics2023` — panorama metodológico de interpretabilidad y explicabilidad.
- `@ribeiro2018` — Anchors / reglas locales de alta precisión.
- `@mothilal2020` — DiCE / explicaciones contrafactuales diversas.
- `@murdoch2019` — definiciones, métodos y aplicaciones de aprendizaje interpretable.
- `@wachter2017` — contrafactuales y decisiones automatizadas.
- `@doshi-velez2017` — evaluación rigurosa de interpretabilidad.
- `@alvarezmelis2018` — robustez de métodos de interpretabilidad.
- `@canha2025` — benchmark functionally-grounded para XAI.
- `@abdulkadir2023` — revisión/taxonomía de métricas XAI.
- `@hedstrom2023` — Quantus y evaluación responsable de explicaciones.
- `@agarwal2022` — OpenXAI y evaluación transparente.
- `@zheng2025` — F-FIDELITY y evaluación de fidelidad.
- `@nauta2023` — revisión sistemática de evaluación cuantitativa XAI.
- `@rudin2022` — principios y retos de aprendizaje automático interpretable.
- `@friedman1937` — prueba de Friedman para comparación por rangos.
- `@altukhi2025` — revisión reciente de avances XAI.
- `@schwalbe2023` — taxonomía de conceptos y métodos XAI.
- `@pawlicki2024` — necesidad de múltiples métricas en evaluación XAI.
- `@bhattacharya2024` — evaluación multidimensional de explicaciones.
- `@burger2023` — estabilidad de LIME.

## Referencias sin cita en texto

Tras las pasadas de redacción controlada, las referencias fundacionales y de evaluación más relevantes ya se citan en el manuscrito. Antes del envío debe ejecutarse una revisión final para detectar entradas remanentes en `references/references.bib` que no aparezcan en `manuscript/*.md`.

## Citas sin entrada bibliográfica

- Ninguna detectada en esta pasada. Las futuras citas del manuscrito deben cotejarse contra `references/references.bib`.

## DOI pendientes

- `@alvarezmelis2018`: entrada arXiv con URL; sin DOI en la fuente de tesis.
- `@hedstrom2023`: falta DOI en la entrada fuente; verificar si JMLR registra DOI o usar URL oficial.
- `@agarwal2022`: falta DOI en la entrada fuente; verificar registro NeurIPS/OpenReview si aplica.
- `@zheng2025`: entrada fuente usa URL del proyecto; verificar DOI/publicación final si existe.

## URL pendientes de validación

- `https://arxiv.org/abs/1806.08049` (`@alvarezmelis2018`).
- `https://trustai4s-lab.github.io/ffidelity` (`@zheng2025`).
- Página oficial de Quantus/JMLR para `@hedstrom2023`.
- Página oficial NeurIPS/OpenReview para `@agarwal2022`.

## Figuras/tablas que requieren fuente

- `tables/table_metrics.md`: derivada de `thesis/capitulo-1-marco-teorico.qmd` y `thesis/capitulo-3-diseno-experimental.qmd`.
- `tables/table_methods_comparison.md`: debe cotejarse con `thesis/capitulo-2-fundamentos.qmd` y las referencias fundacionales de cada método.
- Futuras figuras copiadas desde `thesis/assets/figures/` deberán registrarse en `figures/figure_registry.md` con fuente exacta.
