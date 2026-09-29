# Inventario de fuentes para el capítulo CIFIE

**Estado:** reconciliado el 2026-09-28 con la sincronización empírica del
2026-09-27 y la nueva arquitectura científica.

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
| `thesis/apendices.qmd` | Evidencia suplementaria, análisis de sensibilidad y detalles reproducibles. | Localizada; consultar solo para límites o trazabilidad específicos |
| `thesis/references.bib` | Base bibliográfica principal para referencias verificadas. | Localizada |
| `thesis/referencias.qmd` | Integración Quarto de referencias. | Localizada |

## Fuentes de publicación y claims

| Fuente | Uso previsto en el capítulo | Estado |
| ------ | --------------------------- | ------ |
| `pub/claims.toml` | Resumen consolidado de tesis, claims centrales y abstracts de artículos relacionados. | Localizada |
| `pub/fragments/thesis_resumen_es.qmd` | Base para resumen del capítulo, adaptada a extensión CIFIE. | Localizada |
| `pub/fragments/thesis_palabras_clave_es.qmd` | Palabras clave iniciales. | Localizada |
| `pub/fragments/paper_a_abstract_en.tex` | Evidencia sobre benchmark multimétrico, cobertura de artefactos y pruebas Friedman. | Localizada |
| `pub/fragments/paper_b_abstract_en.tex` | Material de publicación no admisible como fuente de resultados para el capítulo. | Excluida por ADR-0018 `[exclusivity]` |
| `pub/fragments/paper_c_abstract_en.tex` | Material de publicación no admisible como fuente de resultados para el capítulo. | Excluida por ADR-0018 `[exclusivity]` |

## Fuentes experimentales y reproducibilidad

| Fuente | Uso previsto en el capítulo | Estado |
| ------ | --------------------------- | ------ |
| `configs/experiments/exp1_adult_*` | Configuraciones de calibración/reproducibilidad inicial. | Localizada |
| `configs/experiments/exp2_comparative/` | Configuraciones del benchmark comparativo principal por modelo y método. | Localizada |
| `configs/experiments/exp2_scaled/` | Configuraciones con semillas y tamaños de muestra para análisis de estabilidad/escala. | Localizada |
| `configs/experiments/exp2_scaled/manifest.yaml` | Manifiesto de ejecución EXP2 escalado. | Localizada |
| `experiments/`, `results/`, `reports/` | Artefactos de corrida, resultados y reportes para trazabilidad del caso. | Evidencia del capítulo sincronizada mediante claims, RIMI y guards; inventario directo solo si una revisión numérica lo exige |

## Figuras candidatas

| Fuente | Uso previsto en el capítulo | Estado |
| ------ | --------------------------- | ------ |
| `thesis/assets/figures/fig_boxplots_metricas_es.png` | Resultados distribucionales por métrica. | Copiada y registrada; revisar redundancia antes de la versión final |
| `thesis/assets/figures/fig_cd_diagram_es.png` | Comparación crítica/ranking de métodos. | Copiada y registrada; mantener límites inferenciales |
| `thesis/assets/figures/fig_cobertura_exp2_es.png` | Cobertura experimental y completitud de artefactos. | Copiada y registrada; candidata prioritaria para el caso empírico |
| `thesis/assets/figures/fig_correlacion_metricas_es.png` | Relaciones entre métricas. | Copiada y registrada; revisar redundancia antes de la versión final |
| `thesis/assets/figures/fig_diferencias_pareadas_es.png` | Comparaciones pareadas SHAP-LIME. | Retirada el 2026-09-27 por ADR-0018 `[exclusivity]` |
| `thesis/assets/figures/fig_estabilidad_coste_es.png` | Frontera estabilidad/coste. | Copiada y registrada; candidata para el perfil calidad-coste |
| `thesis/assets/figures/fig_radar_metodos_es.png` | Perfil comparativo por método. | Copiada y registrada; revisar redundancia antes de la versión final |

## Bibliografía candidata inicial

| Tema | Fuente/referencia esperada | Estado |
| ---- | -------------------------- | ------ |
| LIME | Ribeiro et al. (2016), clave `ribeiro2016`. | Presente, citada y auditada en la base actual |
| Anchors | Ribeiro et al. (2018), clave `ribeiro2018`. | Presente, citada y auditada en la base actual |
| SHAP | Lundberg y Lee (2017), clave `lundberg2017`. | Presente, citada y auditada en la base actual |
| DiCE y recourse | Mothilal et al. (2020), Wachter et al. (2017) y Karimi et al. (2022). | Presentes, citadas y auditadas en la base actual |
| Evaluación XAI | Doshi-Velez y Kim, Quantus, OpenXAI, Nauta et al., Pawlicki et al., Bhattacharya y Verbert, Canha et al. | Presentes, citadas y auditadas en la base actual |

## Literatura externa para la ampliación científica

La primera pasada y su ampliación dirigida verificaron diecisiete candidatos sin
incorporarlos todavía a la lista final.
El detalle de metadata, claim admisible, límite y registro APA 7 se conserva en
`references/candidate_literature_2026-09-28.md`.

| Paquete | Candidatos verificados | Uso previsto | Estado |
| --- | --- | --- | --- |
| Principios y gobernanza | Phillips et al. (2021); Tabassi (2023); Reglamento (UE) 2024/1689 | Audiencias, funciones de explicación, límites de conocimiento y transparencia para despliegue | Verificados; transferir solo al citar |
| Salud | WHO (2021); Ghassemi et al. (2021) | Gobernanza de IA en salud y límite de las explicaciones post-hoc | Verificados; fuente primaria adicional solo para efectos clínicos concretos |
| Evaluación humana | Kim et al. (2024); Alufaisan et al. (2021); Poursabzi-Sangdeh et al. (2021) | Estandarización, desempeño de decisiones, confianza y corrección de errores | Verificados con límites de tarea |
| Finanzas | Weber et al. (2024) | Mapa sistemático de áreas de uso y brechas | Verificada |
| Robustez y cambio de distribución | Lakkaraju et al. (2020) | Fidelidad y estabilidad de explicaciones bajo conjuntos declarados de cambio | Estudio primario verificado; no extrapolar a todo cambio en producción |
| Ciberseguridad | Rjoub et al. (2023); Roch et al. (2026) | Taxonomía de uso y estudio humano sobre confianza y desempeño | Verificadas; resultado humano limitado a la tarea estudiada |
| Sistemas autónomos | Kuznietsov et al. (2024); Kaufman et al. (2025) | Taxonomía de monitoreo/validación y efecto de errores explicativos | Verificadas; no equivalen a evidencia directa de seguridad operacional |
| LLM y multimodal | Zhao et al. (2024); Turpin et al. (2023); Zaman y Srivastava (2026) | Taxonomía, prueba de racionalización no fiel y counterevidence metodológico | Verificadas; claim limitado a LLM y dependiente de métrica |

## Reglas de uso

- No editar fuentes originales de `thesis/`, `pub/`, `configs/`, `experiments/`, `results/` o `reports/` durante la redacción del capítulo.
- Copiar o resumir evidencia solo dentro de `publications/book_chapters/2026_cifie_xai_fom7/`.
- Registrar toda afirmación empírica en `evidence_map.md` antes de incorporarla al manuscrito.
- Registrar toda cita en `references/citation_audit.md` hasta que exista entrada bibliográfica verificada.
- No añadir una fuente candidata a las bibliografías de producción hasta que exista
  una cita correspondiente en la prosa revisada.
- No usar resultados no publicados de Paper B+C, aunque el artefacto fuente exista en
  el repositorio.
