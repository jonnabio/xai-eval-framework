# Tabla 4. Resumen de resultados empíricos

Fuente inicial: `thesis/capitulo-4-resultados.qmd`.

Este resumen identifica los hallazgos que pueden alimentar la sección `08_aplicacion_empirica_perfiles_fom7.md`. Las cifras deben conservar su alcance inferencial: benchmark EXP2 sobre UCI Adult Income, métodos LIME, SHAP, Anchors y DiCE, cinco familias de modelos, semillas y tamaños de muestra definidos en la tesis.

## Cobertura analítica EXP2

| Elemento | Resultado reportado | Alcance / nota |
| -------- | ------------------- | -------------- |
| Diseño planificado | 300 celdas, $5 \times 4 \times 5 \times 3$ | Cinco modelos, cuatro métodos, cinco semillas, tres tamaños de muestra. |
| Artefactos calificados | 275 celdas | Las 25 celdas faltantes fueron excluidas por la puerta 3 de FOM-7. |
| SHAP | 75/75 celdas, 100% | Incluye superposición de recuperación documentada para evitar sesgo por truncamiento. |
| LIME | 75/75 celdas, 100% | Cobertura completa. |
| DiCE | 68/75 celdas, 90.7% | Faltantes distribuidos entre varias combinaciones con semillas específicas. |
| Anchors | 57/75 celdas | Faltantes concentrados en `logreg_anchors` y `mlp_anchors`, con celdas adicionales en `xgb_anchors`. |
| Análisis Friedman H1-H2 | 15 bloques completos $(g,n)$ | Bloques con los cuatro métodos disponibles. |
| Análisis pareado SHAP-LIME H3 | Celdas coincidentes $(g,s,n)$ | Diseño y resultados en la tesis (Herrera-Vásquez, 2026); no generaliza fuera de Adult/tabular sin validación adicional. |

## Resumen de hipótesis y decisiones

| Claim | Test | Unidad / n | Estadístico | p ajustado | Efecto | Decisión |
| ----- | ---- | ---------- | ----------- | ---------- | ------ | -------- |
| H1: existen diferencias de fidelidad entre métodos | Friedman + Nemenyi | 15 bloques $(g,n)$ | $\chi^2_F = 42.12$ | $p_{\mathrm{Holm}} = 1.51 \times 10^{-8}$ | $W = 0.936$ | Rechazar $H_{0,1}$; SHAP supera a Anchors/DiCE y LIME supera a DiCE. |
| H2: existen diferencias de estabilidad entre métodos | Friedman + Nemenyi | 15 bloques $(g,n)$ | $\chi^2_F = 40.68$ | $p_{\mathrm{Holm}} = 2.29 \times 10^{-8}$ | $W = 0.904$ | Rechazar $H_{0,2}$; SHAP/DiCE forman el grupo más estable. |
| H3: SHAP y LIME difieren en calidad-coste | Wilcoxon pareado bilateral | Celdas $(g,s,n)$ | Véase la tesis | Véase la tesis | Véase la tesis | Rechazar $H_{0,3}$; SHAP mejora calidad y aumenta coste medio (Herrera-Vásquez, 2026). |
| Seguimiento dirigido SHAP-LIME (fidelidad) | Wilcoxon y prueba exacta de signos, motivados por la revisión | 15 bloques $(g,n)$ | 15 de 15 bloques a favor de SHAP | $p_{\mathrm{Holm}} = 3.05 \times 10^{-4}$ | No aplica | Misma dirección con la agregación de Friedman; no reemplaza a H3. |
| P1: el protocolo es reproducible bajo semillas | CV sobre EXP1 | 5 semillas RF, $N=100$ | CV por métrica | No aplica | CV < 3% en señales principales | Confirmación parcial; LIME-estabilidad queda fuera por media cercana a cero. |

## Rangos y medias por fidelidad

| Método | Suma de rangos | Rango medio | Posición | Media bruta reportada |
| ------ | -------------- | ----------- | -------- | --------------------- |
| SHAP | 15 | 1.000 | 1.ª | $0.808 \pm 0.093$ |
| LIME | 30 | 2.000 | 2.ª | $0.560 \pm 0.068$ |
| Anchors | 48 | 3.200 | 3.ª | $0.389 \pm 0.100$ |
| DiCE | 57 | 3.800 | 4.ª | $0.170 \pm 0.103$ |

## Contraste pareado SHAP-LIME

Los estadísticos del contraste pareado SHAP-LIME (diferencias medias, tamaños de efecto y recuentos de signo) no se reproducen en el capítulo. Se remite a la tesis (Herrera-Vásquez, 2026), que los documenta con su unidad de análisis y su corrección de multiplicidad. El capítulo solo informa de la dirección: SHAP supera a LIME en fidelidad y estabilidad, y es más costoso en la mayoría de los contextos.

## Perfil multidimensional por método

Agregación: la fidelidad y la estabilidad son medias por bloque $(g,n)$; la parsimonia, la brecha de fidelidad y el coste son medias por ejecución.

| Método | Perfil de resultados | Limitación principal | Uso argumental en el capítulo |
| ------ | -------------------- | -------------------- | ----------------------------- |
| SHAP | Perfil global más equilibrado: fidelidad 0.808, estabilidad 0.732, parsimonia 0.226, brecha de fidelidad 0.380. | Coste heterogéneo por familia de modelo: 21 ms (XGBoost, TreeSHAP) frente a 54,231 ms (SVM, KernelSHAP). | Método fuerte para auditoría y calidad explicativa cuando la fidelidad/estabilidad son prioritarias. |
| LIME | Método económico en la mayoría de las familias (52 ms en MLP, 73 ms en regresión logística, 122 ms en XGBoost); fidelidad moderada 0.560 y parsimonia 0.085. | Estabilidad casi nula: media 0.014; coste de 17,620 ms sobre SVM. | Alternativa de bajo coste para contextos de latencia, con advertencia fuerte sobre consistencia. |
| Anchors | Reglas locales cualitativamente interpretables; parsimonia comparable a LIME. | Cobertura incompleta; fidelidad 0.389, estabilidad 0.043, coste medio 38,159 ms. | Útil para explicar condiciones locales, pero no comparable de forma directa con atribuciones numéricas. |
| DiCE | Estabilidad intermedia 0.361 y parsimonia muy baja 0.017. | Fidelidad baja 0.170 porque su objetivo es contrafactual, no atribucional; coste medio 28,209 ms. | Método orientado a acción correctiva/contrafactualidad; no debe juzgarse solo como método de atribución. |

## Trazabilidad de afirmaciones principales

| Afirmación | Evidencia en tesis | Artefacto fuente | Script / proceso | Alcance |
| ----- | ------------------ | ---------------- | ---------------- | ------- |
| Existen diferencias globales entre métodos en fidelidad. | Tablas `@tbl-friedman-fidelity` y `@tbl-nemenyi-fidelity`. | `outputs/analysis/paper_a_exp2_stats/friedman_results.csv`, `nemenyi_fidelity.csv`. | `scripts/run_exp2_statistical_analysis.py` | 15 bloques Adult Income, cuatro métodos, cinco modelos. |
| Existen diferencias globales entre métodos en estabilidad. | Tabla `@tbl-friedman-stability` y localización Nemenyi en texto. | `friedman_results.csv`, `nemenyi_stability.csv`. | `scripts/run_exp2_statistical_analysis.py` | Mismo diseño de bloques; estabilidad como similitud coseno. |
| SHAP supera a LIME en fidelidad y estabilidad pero aumenta el coste medio. | Tabla `@tbl-paired-shap-lime` y seguimiento de 15 bloques (Herrera-Vásquez, 2026). | `wilcoxon_shap_lime_all_models.csv`, `wilcoxon_shap_lime_blocks.csv`. | `scripts/run_exp2_statistical_analysis.py`, `scripts/run_exp2_block_paired_analysis.py` | Celdas pareadas $(g,s,n)$ y bloques $(g,n)$; estadísticos solo en la tesis; no generaliza fuera de Adult/tabular. |
| FOM-7 produce señales reproducibles para métricas principales. | Tabla `@tbl-cv-p1`. | `experiments/exp1_adult/reproducibility/reproducibility_report.csv`. | Ejecuciones EXP1 por semilla. | Confirmación parcial; LIME-estabilidad queda limitada por media cercana a cero. |
| La cobertura faltante no invalida las pruebas confirmativas principales. | Capítulo 3, tablas de cobertura. | `exp2_run_inventory.csv`, árbol `experiments/exp2_scaled/results/`. | Auditoría FOM-7 puerta 3. | Afecta precisión de Anchors/DiCE; no afecta SHAP-LIME pareado. |

## Restricciones de uso

- No presentar los resultados como universales fuera del contexto Adult/tabular sin validación adicional.
- No convertir fidelidad baja de DiCE o Anchors en fallo absoluto: sus objetos explicativos son distintos a la atribución de características.
- No presentar la cobertura incompleta de Anchors/DiCE como irrelevante; debe mantenerse como límite de precisión y generalización.
- Toda cifra que pase al manuscrito debe conservar fuente, unidad de análisis y alcance.
