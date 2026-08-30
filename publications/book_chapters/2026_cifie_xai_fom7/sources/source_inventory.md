# Inventario de fuentes para el capítulo CIFIE

Este inventario identifica materiales fuente que pueden alimentar el capítulo sin copiar ni sobrescribir artefactos de tesis o artículos. Todo uso de contenido debe pasar por verificación de citas, trazabilidad de resultados y adaptación editorial al formato CIFIE.

## Fuentes primarias de tesis

| Fuente | Uso previsto en el capítulo | Estado |
| ------ | --------------------------- | ------ |
| `thesis/index.qmd` | Título, resumen, palabras clave y formulación general del marco multinivel. | Localizada |
| `thesis/introduccion.qmd` | Planteamiento de la investigación, motivación, alcance y problema general. | Localizada |
| `thesis/capitulo-1-marco-teorico.qmd` | Problema de investigación, objetivos, hipótesis, justificación de FOM-7 y diseño general. | Localizada |
| `thesis/capitulo-2-fundamentos.qmd` | Fundamentos XAI, métodos agnósticos, crisis de evaluación, reproducibilidad y trazabilidad. | Localizada |
| `thesis/capitulo-3-diseno-experimental.qmd` | Diseño empírico, dataset, modelos, celdas experimentales, métricas, pruebas estadísticas y protocolo. | Localizada |
| `thesis/capitulo-4-resultados.qmd` | Resultados principales, pruebas estadísticas, comparación de métodos y frontera calidad-costo. | Localizada |
| `thesis/capitulo-5-taxonomia.qmd` | Taxonomía de métricas, discusión de evaluación semántica y marco conceptual complementario. | Localizada |
| `thesis/capitulo-6-conclusiones.qmd` | Conclusiones, contribuciones, limitaciones, fronteras de generalización y recomendaciones de selección de métodos. | Localizada |
| `thesis/apendices.qmd` | Evidencia suplementaria, análisis de sensibilidad y detalles reproducibles. | Pendiente de revisar |
| `thesis/references.bib` | Base bibliográfica principal para referencias verificadas. | Localizada |
| `thesis/referencias.qmd` | Integración Quarto de referencias. | Localizada |

## Fuentes de publicación y claims

| Fuente | Uso previsto en el capítulo | Estado |
| ------ | --------------------------- | ------ |
| `pub/claims.toml` | Resumen consolidado de tesis, claims centrales y abstracts de artículos relacionados. | Localizada |
| `pub/fragments/thesis_resumen_es.qmd` | Base para resumen del capítulo, adaptada a extensión CIFIE. | Localizada |
| `pub/fragments/thesis_palabras_clave_es.qmd` | Palabras clave iniciales. | Localizada |
| `pub/fragments/paper_a_abstract_en.tex` | Evidencia sobre benchmark multimétrico, cobertura de artefactos y pruebas Friedman. | Localizada |
| `pub/fragments/paper_b_abstract_en.tex` | Evidencia sobre comparación pareada SHAP-LIME y trade-off calidad-costo. | Localizada |
| `pub/fragments/paper_c_abstract_en.tex` | Evidencia sobre crisis de evaluación, taxonomía y evaluación semántica. | Localizada |

## Fuentes experimentales y reproducibilidad

| Fuente | Uso previsto en el capítulo | Estado |
| ------ | --------------------------- | ------ |
| `configs/experiments/exp1_adult_*` | Configuraciones de calibración/reproducibilidad inicial. | Localizada |
| `configs/experiments/exp2_comparative/` | Configuraciones del benchmark comparativo principal por modelo y método. | Localizada |
| `configs/experiments/exp2_scaled/` | Configuraciones con semillas y tamaños de muestra para análisis de estabilidad/escala. | Localizada |
| `configs/experiments/exp2_scaled/manifest.yaml` | Manifiesto de ejecución EXP2 escalado. | Localizada |
| `experiments/`, `results/`, `reports/` | Artefactos de corrida, resultados y reportes si están disponibles localmente. | Pendiente de inventario detallado |

## Figuras candidatas

| Fuente | Uso previsto en el capítulo | Estado |
| ------ | --------------------------- | ------ |
| `thesis/assets/figures/fig_boxplots_metricas_es.png` | Resultados distribucionales por métrica. | Candidata |
| `thesis/assets/figures/fig_cd_diagram_es.png` | Comparación crítica/ranking de métodos. | Candidata |
| `thesis/assets/figures/fig_cobertura_exp2_es.png` | Cobertura experimental y completitud de artefactos. | Candidata |
| `thesis/assets/figures/fig_correlacion_metricas_es.png` | Relaciones entre métricas. | Candidata |
| `thesis/assets/figures/fig_diferencias_pareadas_es.png` | Comparaciones pareadas, especialmente SHAP-LIME. | Candidata |
| `thesis/assets/figures/fig_estabilidad_coste_es.png` | Frontera estabilidad/coste. | Candidata |
| `thesis/assets/figures/fig_radar_metodos_es.png` | Perfil comparativo por método. | Candidata |

## Bibliografía candidata inicial

| Tema | Fuente/referencia esperada | Estado |
| ---- | -------------------------- | ------ |
| LIME | Ribeiro et al. (2016), clave probable `ribeiro2016` en `thesis/references.bib`. | Pendiente de copiar y verificar |
| Anchors | Ribeiro et al. (2018), clave probable `ribeiro2018` en `thesis/references.bib`. | Pendiente de copiar y verificar |
| SHAP | Lundberg y Lee (2017), clave probable `lundberg2017` en `thesis/references.bib`. | Pendiente de copiar y verificar |
| DiCE | Mothilal et al. (2020) y Wachter et al. (2017), claves probables `mothilal2020`, `wachter2017`. | Pendiente de copiar y verificar |
| Evaluación XAI | Doshi-Velez y Kim (2017), Quantus, OpenXAI, Canha et al. | Pendiente de copiar y verificar |

## Reglas de uso

- No editar fuentes originales de `thesis/`, `pub/`, `configs/`, `experiments/`, `results/` o `reports/` durante la redacción del capítulo.
- Copiar o resumir evidencia solo dentro de `publications/book_chapters/2026_cifie_xai_fom7/`.
- Registrar toda afirmación empírica en `evidence_map.md` antes de incorporarla al manuscrito.
- Registrar toda cita en `references/citation_audit.md` hasta que exista entrada bibliográfica verificada.
