# Aplicación empírica: perfiles explicativos bajo FOM-7

Fuente inicial: `thesis/capitulo-3-diseno-experimental.qmd`, `tables/table_metrics.md`, `tables/table_fom7_gates.md` y `tables/table_results_summary.md`; `thesis/capitulo-4-resultados.qmd`, `tables/table_results_summary.md`, `tables/table_metrics.md` y `figures/figure_registry.md`.

## Diseño y evidencia global

Esta sección interpreta el benchmark EXP2 como perfiles de evidencia bajo FOM-7, no como un ranking universal de explicadores.

En UCI Adult Income se planificaron 300 celdas; tras la auditoría FOM-7, 275 fueron calificadas y las restantes se excluyeron antes de la inferencia confirmativa.

SHAP y LIME cubrieron 75 de 75 celdas; DiCE, 68 de 75; Anchors, 57 de 75. La cobertura condiciona la interpretación: las celdas faltantes de Anchors se concentran en regresión logística y MLP, por lo que sus medias descansan en menos semillas. La tesis acota el sesgo mediante sensibilidad al umbral, sin cambiar la posición relativa del método. La Figura 8 presenta esta cobertura junto con la auditoría de artefactos.

Friedman detectó diferencias de fidelidad entre métodos ($\chi^2_F = 42.12$, 15 bloques completos, $p_{\mathrm{Holm}} = 1.51 \times 10^{-8}$, $W = 0.936$). SHAP ocupó el primer rango, seguido por LIME, Anchors y DiCE bajo esta operacionalización. Véase la Figura 9.

En estabilidad, Friedman también fue significativo ($\chi^2_F = 40.68$, $p_{\mathrm{Holm}} = 2.29 \times 10^{-8}$, $W = 0.904$). SHAP mantuvo el perfil más fuerte y DiCE fue relativamente estable frente a LIME y Anchors. El patrón confirma que fidelidad y estabilidad describen propiedades distintas.

Estas diferencias se interpretan como perfiles condicionados por métrica, objeto y diseño, no como una victoria universal.

![Figura 9. Diagrama de diferencia crítica de Nemenyi para fidelidad y estabilidad. Fuente: elaboración propia a partir de las tablas de rangos y comparaciones de Nemenyi de EXP2.](../figures/exported/fig_cd_diagram_es.png)

SHAP y LIME son los únicos métodos con cobertura completa. SHAP ocupó el primer rango en fidelidad y estabilidad; Nemenyi separó ambos métodos en estabilidad, pero no en fidelidad (Herrera-Vásquez & Herrero-Uceda, 2026). Véase la Figura 10.

SHAP es más denso y, en general, más costoso; LIME es más conciso, aunque el coste depende de la familia y variante del explicador. La diferencia define una frontera calidad-coste, no una recomendación universal: LIME puede servir para exploración rápida, pero su estabilidad casi nula limita su uso como evidencia de auditoría.

![Figura 10. Relación entre estabilidad y coste por método. Fuente: elaboración propia a partir de los resultados del benchmark EXP2.](../figures/exported/fig_estabilidad_coste_es.png)

SHAP obtuvo medias por bloque de 0.808 en fidelidad y 0.732 en estabilidad (Herrera-Vásquez & Herrero-Uceda, 2026), y medias por ejecución de 0.226 en parsimonia y 0.380 en brecha de fidelidad (Herrera-Vásquez, 2026). El coste medio por ejecución fue de 21 ms con TreeSHAP sobre XGBoost, 2,820 ms sobre Random Forest y 54,231 ms con KernelSHAP sobre SVM. El rótulo agrupa variantes distintas; el perfil depende del modelo y la implementación.

LIME registró fidelidad media por bloque de 0.560 y parsimonia media por ejecución de 0.085. Su coste medio fue de 52 ms en MLP, 73 ms en regresión logística, 122 ms en XGBoost y 436 ms en bosque aleatorio, frente a 17,620 ms en SVM; TreeSHAP fue más rápido que LIME en XGBoost. Su estabilidad media por bloque fue 0.014. El perfil muestra que bajo coste y plausibilidad no garantizan reproducibilidad.

Anchors produce reglas condicionales y tuvo cobertura incompleta. Sus medias por bloque fueron 0.389 en fidelidad y 0.043 en estabilidad; el coste medio por ejecución fue 38,159 ms. Estos resultados no implican inutilidad: exigen reportar precisión, cobertura y aplicabilidad, y limitan la comparación con métricas de atribución.

DiCE genera contrafactuales, no atribuciones. Sus medias por bloque fueron 0.170 en fidelidad y 0.361 en estabilidad; la parsimonia fue 0.017 y el coste medio por ejecución, 28,209 ms. Su pertinencia depende de si se buscan alternativas de acción, no importancias locales.

## Reproducibilidad, perfiles y selección

La reproducibilidad se evaluó en un subconjunto EXP2 de bosque aleatorio, 100 instancias por estrato y cinco semillas. SHAP-fidelidad, SHAP-estabilidad y LIME-fidelidad tuvieron CV inferiores al umbral del 15%, con valores principales por debajo de 3%. En el conjunto completo, el CV agrupado de fidelidad fue 11.4% para SHAP y 12.0% para LIME. LIME-estabilidad fue la excepción: media 0.018 y desviación típica 0.015 (Herrera-Vásquez, 2026). Su CV relativo alto refleja inestabilidad bajo esta configuración, no una propiedad universal. FOM-7 ayuda a distinguir variación del pipeline de un resultado sustantivo del método.

La Tabla 2 resume diferencias entre métodos bajo EXP2, el perfil de SHAP en fidelidad y estabilidad y la ausencia de un método universalmente dominante. LIME ofrece concisión; Anchors, reglas con cobertura limitada; DiCE, contrafactuales orientados a acción.

<!-- TABLA: table_results_summary.md -->

La selección depende del objetivo: auditoría, explicación rápida, regla o exploración contrafactual. FOM-7 vincula esa decisión con evidencia trazable, no con preferencias anecdóticas.
