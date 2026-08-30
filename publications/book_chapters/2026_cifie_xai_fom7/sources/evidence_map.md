# Mapa de evidencia y extracción por sección

Este mapa orienta la conversión de materiales de tesis y artículos en un capítulo CIFIE independiente. Su función es prevenir sobreafirmaciones, mantener trazabilidad y separar con claridad evidencia fuente, interpretación y redacción editorial.

## Matriz sección-fuente

| Sección del capítulo | Función argumental | Fuentes base | Evidencia/afirmación a extraer | Dependencias | Estado |
| -------------------- | ------------------ | ------------ | ------------------------- | ------------ | ------ |
| `01_resumen_palabras_clave.md` | Sintetizar problema, contribución FOM-7, benchmark y resultados principales. | `pub/fragments/thesis_resumen_es.qmd`, `pub/claims.toml`, `manuscript/chapter_outline.md` | FOM-7 como protocolo reproducible; benchmark sobre LIME, SHAP, Anchors y DiCE; SHAP fuerte en fidelidad/estabilidad; LIME de bajo coste; DiCE/Anchors con objetivos distintos. | Referencias y resultados verificados. | Borrador inicial completo |
| `02_introduccion.md` | Presentar la transición desde opacidad predictiva hacia evidencia auditable y formular FOM-7 como respuesta metodológica. | `thesis/introduccion.qmd`, `thesis/capitulo-1-marco-teorico.qmd`, `pub/claims.toml`, literatura XAI y evaluación verificada: Adadi y Berrada, Arrieta et al., Ali et al., Lipton, Rudin et al., Doshi-Velez y Kim, Nauta et al., Pawlicki et al., Bhattacharya y Verbert, Hedström et al., Agarwal et al., Canha et al. | La evaluación fragmentada de XAI exige protocolos reproducibles, multi-métricos y trazables; FOM-7 gobierna el paso desde artefactos y métricas hacia afirmaciones admisibles. | Citas sobre opacidad, métodos post-hoc, crisis de evaluación, benchmarking funcional y gobernanza de evidencia. | Revisado para prosa académica, citas en texto y alineación FOM-7 |
| `03_fundamentos_xai.md` | Definir los fundamentos técnicos que hacen admisible la evaluación FOM-7: objeto explicativo, interpretabilidad, explicabilidad, transparencia, escala local/global, plausibilidad, fidelidad, estabilidad, robustez y métricas como proxies. | `thesis/capitulo-2-fundamentos.qmd`, `thesis/references.bib`, literatura XAI verificada: Lipton, Murdoch et al., Miller, Marcinkevičs y Vogt, Schwalbe y Finzel, Rudin et al., Doshi-Velez y Kim, Nauta et al., Pawlicki et al., Canha et al., Bhattacharya y Verbert, Hedström et al., Zheng et al. | Los métodos post-hoc agnósticos producen artefactos heterogéneos condicionados por supuestos de método, datos, escala, métrica y protocolo; FOM-7 convierte esos artefactos en evidencia admisible solo cuando objeto, constructo, unidad de análisis y afirmación están alineados. | Tabla de métricas, citas fundacionales, auditoría OA 2026-07-04 y pasada fundamentos XAI 2026-07-04. | Revisado mediante loop de enriquecimiento bibliográfico, prosa académica y alineación FOM-7 |
| `04_metodos_lime_shap_anchors_dice.md` | Explicar los cuatro métodos con base matemática, salida, fortalezas y límites. | `thesis/capitulo-2-fundamentos.qmd`, `tables/table_methods_comparison.md`, `thesis/references.bib` | LIME: sustituto local; SHAP: Shapley/aditividad; Anchors: reglas de alta precisión; DiCE: contrafactuales diversos. | Entradas BibTeX y tabla comparativa revisadas. | Borrador inicial completo |
| `05_crisis_evaluacion_xai.md` | Argumentar la crisis de evaluación: fragmentación, métricas aisladas y trazabilidad insuficiente. | `thesis/capitulo-1-marco-teorico.qmd`, `thesis/capitulo-2-fundamentos.qmd`, `pub/fragments/paper_c_abstract_en.tex` | La fidelidad aislada no basta; la evaluación debe integrar estabilidad, parsimonia, coste, contexto y fuente de evidencia. | Citas sobre evaluación XAI, Quantus/OpenXAI y taxonomías. | Borrador inicial completo |
| `06_protocolo_fom7.md` | Presentar FOM-7 como secuencia operativa de siete puertas. | `thesis/capitulo-1-marco-teorico.qmd`, `thesis/capitulo-2-fundamentos.qmd`, `thesis/capitulo-3-diseno-experimental.qmd`, `tables/table_fom7_gates.md` | FOM-7 regula el paso desde diseño experimental hasta afirmaciones trazables a evidencia fuente. | Tabla FOM-7 revisada contra tesis. | Borrador inicial completo |
| `07_diseno_empirico.md` | Describir conjunto de datos, modelos, métodos, métricas, celdas y pruebas estadísticas. | `thesis/capitulo-3-diseno-experimental.qmd`, `configs/experiments/exp2_comparative/`, `configs/experiments/exp2_scaled/manifest.yaml` | UCI Adult Income; 5 familias de modelos; LIME, SHAP, Anchors, DiCE; métricas primarias; diseño pareado; pruebas no paramétricas. | Inventario detallado de artefactos de resultados. | Borrador inicial completo |
| `08_aplicacion_empirica_perfiles_fom7.md` | Presentar resultados centrales y frontera calidad-coste. | `thesis/capitulo-4-resultados.qmd`, `thesis/capitulo-6-conclusiones.qmd`, `pub/fragments/paper_a_abstract_en.tex`, `pub/fragments/paper_b_abstract_en.tex` | Friedman significativo para fidelidad, estabilidad, parsimonia, brecha de fidelidad y tiempo de ejecución; SHAP domina fidelidad/estabilidad; DiCE lidera parsimonia; LIME rápido pero inestable; 75 celdas SHAP-LIME. | Tablas de resultados, figuras y auditoría de citas. | Borrador inicial completo |
| `09_implicaciones_evaluacion_auditable_xai.md` | Interpretar implicaciones para auditoría, gobernanza y selección de métodos. | `thesis/capitulo-5-taxonomia.qmd`, `thesis/capitulo-6-conclusiones.qmd`, `pub/claims.toml`, literatura OA verificada: OpenXAI, Quantus, Nauta et al., Pawlicki et al., Canha et al. | No existe método universalmente dominante; la selección debe depender del objetivo operativo y del tipo de evidencia requerido; las herramientas y revisiones recientes amplían métricas, pero no sustituyen criterios de admisibilidad, alcance inferencial y trazabilidad. | Matriz de afirmaciones defendibles; auditoría OA 2026-07-04. | Borrador enriquecido con literatura OA |
| `10_limitaciones_trabajo_futuro.md` | Delimitar alcance y líneas futuras mediante límites de evidencia compatibles con FOM-7. | `thesis/capitulo-6-conclusiones.qmd`, `thesis/apendices.qmd`, literatura OA verificada: Doshi-Velez y Kim, Nauta et al., Bhattacharya y Verbert, Pawlicki et al., Canha et al.; referencias de método y recourse: Ribeiro et al., Lundberg y Lee, Van den Broeck et al., Mothilal et al., Karimi et al., Wachter et al., Laugel et al., Poyiadzi et al. | Limitaciones: datos tabulares, UCI Adult, métricas específicas, validez de constructo, sensibilidad de configuración, ausencia de evaluación directa con usuarios, cobertura incompleta y transferencia limitada de FOM-7. Futuro: nuevas modalidades, estudios con usuarios, sensibilidad de hiperparámetros, réplicas en dominios de alto impacto y comprensibilidad. | Verificación de límites exactos en tesis; auditoría OA 2026-07-04; revisión editorial 2026-07-04. | Revisado para prosa académica, citas en texto y alineación FOM-7 |
| `11_conclusiones.md` | Cerrar con una tesis fuerte sobre evidencia auditable. | `thesis/capitulo-6-conclusiones.qmd`, `manuscript/00_hoja_diseno_editorial.md` | La explicabilidad útil exige evaluar cuándo una explicación es fiel, estable, comparable, reproducible y defendible. | Resultados y límites ya consolidados. | Borrador inicial completo |

## Afirmaciones empíricas prioritarias

| Afirmación prioritaria | Fuente inicial | Evidencia requerida antes de redacción final | Estado |
| --------------- | -------------- | -------------------------------------------- | ------ |
| El benchmark EXP2 produjo diferencias globales significativas entre métodos en fidelidad. | `pub/fragments/paper_a_abstract_en.tex`, `thesis/capitulo-4-resultados.qmd`, `thesis/capitulo-6-conclusiones.qmd` | Estadístico Friedman, p-valor, diseño de bloques, tamaño de muestra analizable. | Pendiente de verificar |
| SHAP presentó el perfil más fuerte en fidelidad y estabilidad en los contextos evaluados. | `pub/claims.toml`, `thesis/capitulo-4-resultados.qmd`, `thesis/capitulo-6-conclusiones.qmd` | Tabla/figura de resultados, alcance por modelo/conjunto de datos, límites inferenciales. | Verificado en extracción |
| LIME fue competitivo cuando el coste computacional fue crítico, pero con inestabilidad estructural. | `pub/fragments/paper_b_abstract_en.tex`, `thesis/capitulo-6-conclusiones.qmd` | Resultados pareados SHAP-LIME, métricas de coste, CV/similitud de estabilidad, análisis de sensibilidad. | Pendiente de verificar |
| DiCE destacó en parsimonia/contrafactualidad, pero no debe compararse como atribución de características pura. | `pub/fragments/paper_a_abstract_en.tex`, `thesis/capitulo-2-fundamentos.qmd`, `thesis/capitulo-6-conclusiones.qmd` | Definición de salida contrafactual, métricas de parsimonia/validez, límites del constructo. | Pendiente de verificar |
| Anchors aporta reglas locales de alta precisión, con límites de cobertura y coste según configuración. | `thesis/capitulo-2-fundamentos.qmd`, `thesis/capitulo-4-resultados.qmd` | Resultados de precisión/cobertura si se reportan, costes por modelo, citas fundacionales. | Pendiente de verificar |
| FOM-7 convierte resultados numéricos en afirmaciones trazables mediante siete puertas. | `thesis/capitulo-1-marco-teorico.qmd`, `thesis/capitulo-2-fundamentos.qmd`, `thesis/capitulo-3-diseno-experimental.qmd` | Descripción exacta de puertas, criterios de admisibilidad y artefactos esperados. | Verificado en extracción |

## Figuras y tablas del capítulo

| Artefacto del capítulo | Fuente | Acción requerida | Estado |
| ---------------------- | ---------------- | ---------------- | ------ |
| `tables/table_metrics.md` | `thesis/capitulo-1-marco-teorico.qmd`, `thesis/capitulo-3-diseno-experimental.qmd` | Completar definiciones de fidelidad, estabilidad, parsimonia, brecha de fidelidad y coste. | Pendiente |
| `tables/table_results_summary.md` | `thesis/capitulo-4-resultados.qmd`, `pub/fragments/paper_a_abstract_en.tex`, `pub/fragments/paper_b_abstract_en.tex` | Extraer resultados confirmados y límites de interpretación. | Pendiente |
| `figures/exported/` | `thesis/assets/figures/*_es.png` | Figuras seleccionadas copiadas y registradas en `figures/figure_registry.md`. | Completado |
| `references/references.bib` | `thesis/references.bib` | Copiar solo entradas citadas en el capítulo y auditar DOI/APA 7. | Pendiente |

## Secuencia recomendada de extracción

1. Extraer definiciones y citas fundacionales para `03_fundamentos_xai.md`.
2. Completar `references/references.bib` con LIME, SHAP, Anchors, DiCE y evaluación XAI.
3. Completar `tables/table_metrics.md` y revisar `tables/table_methods_comparison.md`.
4. Extraer protocolo FOM-7 para `06_protocolo_fom7.md` y validar `tables/table_fom7_gates.md`.
5. Extraer diseño empírico para `07_diseno_empirico.md`.
6. Extraer resultados confirmados para `08_aplicacion_empirica_perfiles_fom7.md` y `tables/table_results_summary.md`.
7. Redactar discusión, limitaciones y conclusiones.
8. Redactar introducción, resumen y palabras clave al final.

## Controles de calidad

- Toda cifra debe tener fuente exacta, sección o archivo de origen.
- Toda cita debe existir en `references/references.bib` y pasar por `references/citation_audit.md`.
- Toda figura debe registrarse en `figures/figure_registry.md` antes de ser usada.
- Toda afirmación empírica debe conservar límites de alcance: conjunto de datos, modelos, métricas, semillas, tamaño de muestra y método estadístico.
