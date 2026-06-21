# Resumen de resultados empíricos

Fuente inicial: `thesis/capitulo-4-resultados.qmd`.

Este resumen identifica los hallazgos que pueden alimentar la sección `08_resultados.md`. Las cifras deben conservar su alcance inferencial: benchmark EXP2 sobre UCI Adult Income, métodos LIME, SHAP, Anchors y DiCE, cinco familias de modelos, semillas y tamaños de muestra definidos en la tesis.

## Cobertura analítica EXP2

| Elemento | Resultado reportado | Alcance / nota |
| -------- | ------------------- | -------------- |
| Diseño planificado | 300 celdas, $5 \times 4 \times 5 \times 3$ | Cinco modelos, cuatro métodos, cinco semillas, tres tamaños de muestra. |
| Artefactos calificados | 275 celdas | Las 25 celdas faltantes fueron excluidas por la puerta 3 de FOM-7. |
| SHAP | 75/75 celdas, 100% | Incluye superposición de recuperación documentada para evitar sesgo por truncamiento. |
| LIME | 75/75 celdas, 100% | Cobertura completa. |
| DiCE | 68/75 celdas, 90.7% | Faltantes distribuidos entre varias combinaciones con semillas específicas. |
| Anchors | 57/75 celdas, 76.0% | Faltantes concentrados en `logreg_anchors` y `mlp_anchors`, con celdas adicionales en `xgb_anchors`. |
| Análisis Friedman H1-H2 | 15 bloques completos $(g,n)$ | Bloques con los cuatro métodos disponibles. |
| Análisis pareado SHAP-LIME H3 | 75 celdas coincidentes $(g,s,n)$ | No generaliza fuera de Adult/tabular sin validación adicional. |

## Resumen de hipótesis y decisiones

| Claim | Test | Unidad / n | Estadístico | p ajustado | Efecto | Decisión |
| ----- | ---- | ---------- | ----------- | ---------- | ------ | -------- |
| H1: existen diferencias de fidelidad entre métodos | Friedman + Nemenyi | 15 bloques $(g,n)$ | $\chi^2_F = 42.12$ | $p_{\mathrm{Holm}} = 1.51 \times 10^{-8}$ | $W = 0.936$ | Rechazar $H_{0,1}$; SHAP supera a Anchors/DiCE y LIME supera a DiCE. |
| H2: existen diferencias de estabilidad entre métodos | Friedman + Nemenyi | 15 bloques $(g,n)$ | $\chi^2_F = 40.68$ | $p_{\mathrm{Holm}} = 2.29 \times 10^{-8}$ | $W = 0.904$ | Rechazar $H_{0,2}$; SHAP/DiCE forman el grupo más estable. |
| H3: SHAP y LIME difieren en calidad-costo | Wilcoxon pareado bilateral | 75 celdas $(g,s,n)$ | $W = 0$ a $205$ | $\leq 2.64 \times 10^{-13}$ para calidad; $1.18 \times 10^{-10}$ para coste | $d_z = 0.451$ a $4.820$ | Rechazar $H_{0,3}$; SHAP mejora calidad y aumenta coste medio. |
| P1: el protocolo es reproducible bajo semillas | CV sobre EXP1 | 5 semillas RF, $N=100$ | CV por métrica | No aplica | CV < 3% en señales principales | Confirmación parcial; LIME-estabilidad queda fuera por media cercana a cero. |

## Rangos y medias por fidelidad

| Método | Suma de rangos | Rango medio | Posición | Media bruta reportada |
| ------ | -------------- | ----------- | -------- | --------------------- |
| SHAP | 15 | 1.000 | 1.ª | $0.808 \pm 0.093$ |
| LIME | 30 | 2.000 | 2.ª | $0.560 \pm 0.068$ |
| Anchors | 48 | 3.200 | 3.ª | $0.389 \pm 0.100$ |
| DiCE | 57 | 3.800 | 4.ª | $0.170 \pm 0.103$ |

## Diferencias pareadas SHAP-LIME

| Métrica | Diferencia media SHAP-LIME | Desv. típica | $d_z$ | Positivas | Negativas | n | Interpretación |
| ------- | -------------------------- | ------------ | ----- | --------- | --------- | - | -------------- |
| Fidelidad | +0.2479 | 0.0514 | +4.820 | 75 | 0 | 75 | Ventaja muy grande de SHAP. |
| Estabilidad | +0.7176 | 0.2390 | +3.002 | 75 | 0 | 75 | Ventaja muy grande de SHAP; LIME presenta estabilidad casi nula. |
| Parsimonia | +0.1418 | 0.1690 | +0.839 | 75 | 0 | 75 | SHAP es más denso; LIME es más parsimonioso. |
| Brecha de fidelidad | +0.0453 | 0.0173 | +2.626 | 74 | 1 | 75 | SHAP identifica características con mayor efecto al enmascararse. |
| Coste (ms) | +8047.6 | 17856.6 | +0.451 | 59 | 16 | 75 | SHAP suele ser más costoso, con heterogeneidad por modelo. |

## Perfil multidimensional por método

| Método | Perfil de resultados | Limitación principal | Uso argumental en el capítulo |
| ------ | -------------------- | -------------------- | ----------------------------- |
| SHAP | Perfil global más equilibrado: fidelidad = 0.810, estabilidad = 0.724, parsimonia = 0.234, brecha de fidelidad = 0.431, coste = 24,804 ms sobre bloques calificados. | Coste alto y heterogéneo; KernelSHAP puede ser inviable en baja latencia para SVM/MLP. | Método fuerte para auditoría y calidad explicativa cuando la fidelidad/estabilidad son prioritarias. |
| LIME | Método más económico: coste medio 226 ms, fidelidad moderada 0.560 y parsimonia 0.085. | Estabilidad casi nula: media 0.014 y CV de estabilidad 86.2% bajo semillas. | Alternativa de bajo coste para contextos de latencia, con advertencia fuerte sobre consistencia. |
| Anchors | Reglas locales cualitativamente interpretables; parsimonia comparable a LIME. | Cobertura incompleta y coste alto/variable; fidelidad media 0.386 y estabilidad 0.052. | Útil para explicar condiciones locales, pero no comparable de forma directa con atribuciones numéricas. |
| DiCE | Estabilidad intermedia 0.366, parsimonia muy baja 0.017 y coste moderado 2,056 ms. | Fidelidad baja 0.172 porque su objetivo es contrafactual, no atribucional. | Método orientado a recourse/contrafactualidad; no debe juzgarse solo como método de atribución. |

## Trazabilidad de claims principales

| Claim | Evidencia en tesis | Artefacto fuente | Script / proceso | Alcance |
| ----- | ------------------ | ---------------- | ---------------- | ------- |
| Existen diferencias globales entre métodos en fidelidad. | Tablas `@tbl-friedman-fidelity` y `@tbl-nemenyi-fidelity`. | `outputs/analysis/paper_a_exp2_stats/friedman_results.csv`, `nemenyi_fidelity.csv`. | `scripts/run_exp2_statistical_analysis.py` | 15 bloques Adult Income, cuatro métodos, cinco modelos. |
| Existen diferencias globales entre métodos en estabilidad. | Tabla `@tbl-friedman-stability` y localización Nemenyi en texto. | `friedman_results.csv`, `nemenyi_stability.csv`. | `scripts/run_exp2_statistical_analysis.py` | Mismo diseño de bloques; estabilidad como similitud coseno. |
| SHAP supera a LIME en fidelidad y estabilidad pero aumenta el coste medio. | Tabla `@tbl-paired-shap-lime`. | `wilcoxon_shap_lime_all_models.csv`, `paired_cells_shap_lime_all_models.csv`. | `scripts/run_exp2_statistical_analysis.py` | 75 celdas pareadas $(g,s,n)$; no generaliza fuera de Adult/tabular. |
| FOM-7 produce señales reproducibles para métricas principales. | Tabla `@tbl-cv-p1`. | `experiments/exp1_adult/reproducibility/reproducibility_report.csv`. | Ejecuciones EXP1 por semilla. | Confirmación parcial; LIME-estabilidad queda limitada por media cercana a cero. |
| La cobertura faltante no invalida las pruebas confirmativas principales. | Capítulo 3, tablas de cobertura. | `exp2_run_inventory.csv`, árbol `experiments/exp2_scaled/results/`. | Auditoría FOM-7 puerta 3. | Afecta precisión de Anchors/DiCE; no afecta SHAP-LIME pareado. |

## Restricciones de uso

- No presentar los resultados como universales fuera del contexto Adult/tabular sin validación adicional.
- No convertir fidelidad baja de DiCE o Anchors en fallo absoluto: sus objetos explicativos son distintos a la atribución de características.
- No presentar la cobertura incompleta de Anchors/DiCE como irrelevante; debe mantenerse como límite de precisión y generalización.
- Toda cifra que pase al manuscrito debe conservar fuente, unidad de análisis y alcance.
