# Puertas del protocolo FOM-7

Fuente inicial: `thesis/capitulo-3-diseno-experimental.qmd`, Tabla `@tbl-fom7-gates`.

| Puerta FOM-7 | Propósito | Artefacto de entrada | Artefacto de salida | Fallo controlado | Evidencia / fuente |
| ------------ | --------- | -------------------- | ------------------- | ---------------- | ------------------ |
| 1. Congelación | Fijar diseño, versiones, configuraciones, factores, métodos, métricas y plan inferencial antes de EXP2. | `configs/experiments/exp2_scaled/manifest.yaml`, código versionado. | Diseño factorial declarado y protocolo congelado. | Deriva de protocolo; cambio post-hoc de hipótesis, métricas o criterios. | `manifest.yaml`, commit de tesis. |
| 2. Ejecución | Ejecutar celdas desde configuración declarativa, con semillas fijas y registro del contexto de ejecución. | YAML por celda, modelos congelados. | Árbol `experiments/exp2_scaled/results/`. | Ejecuciones ad-hoc; semillas no registradas; cambios de configuración durante la corrida. | `results.json` por celda. |
| 3. Auditoría | Calificar integridad de resultados mediante inspección determinista de artefactos. | `results.json` crudos. | Inventario de celdas analizables. | Archivos vacíos; esquemas incompatibles; valores inválidos; reconstrucciones sintéticas no documentadas. | `outputs/analysis/paper_a_exp2_stats/exp2_run_inventory.csv`. |
| 4. Armonización | Convertir resultados heterogéneos en tablas comparables para análisis. | Artefactos calificados y `outputs/batch_results.csv`. | Métricas a nivel de ejecución y bloque. | Campos no comparables; mezclas de esquema; errores de agregación. | `exp2_run_level_metrics.csv`, `exp2_block_method_summary.csv`. |
| 5. Exportación | Generar tablas inferenciales deterministas desde entradas calificadas. | Tablas armonizadas. | Resultados Friedman, Nemenyi y Wilcoxon exportados. | Cálculos manuales; doble conteo; pseudorreplicación; uso de artefactos no calificados. | `friedman_results.csv`, `nemenyi_*.csv`, `wilcoxon_*.csv`. |
| 6. Perfilado | Cuantificar reproducibilidad bajo semillas y variabilidad residual. | Réplicas EXP1 y métricas primarias. | CV por método/métrica y rango esperado de variación. | Confundir variación de semilla con efecto de método o fallo de protocolo. | `experiments/exp1_adult/reproducibility/reproducibility_report.csv`. |
| 7. Reporte | Vincular cada afirmación con evidencia identificable y límites de interpretación. | Resultados, tablas, scripts, configuraciones y limitaciones. | Afirmaciones trazables y delimitadas. | Sobreafirmación; afirmaciones no auditables; conclusiones sin fuente verificable. | Tablas de resumen de resultados y trazabilidad de afirmaciones. |

## Regla de elegibilidad

Una afirmación inferencial solo es elegible si las puertas anteriores están satisfechas y si puede trazarse a evidencia fuente. Si no cumple esta regla, debe formularse como observación descriptiva o como hipótesis pendiente de validación.
