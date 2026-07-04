# Aplicación empírica: perfiles explicativos bajo FOM-7

Fuente inicial: `thesis/capitulo-4-resultados.qmd`, `tables/table_results_summary.md`, `tables/table_metrics.md` y `figures/figure_registry.md`.

## De resultados estadísticos a evidencia de capítulo

En un artículo empírico, esta sección podría presentarse como un bloque de resultados separado de la discusión. En este capítulo, su función es distinta: mostrar cómo FOM-7 transforma salidas de benchmarking en perfiles explicativos interpretables, trazables y metodológicamente delimitados. Por ello, las cifras se presentan junto con su lectura sustantiva. La pregunta no es solo qué método obtuvo el mejor valor en una métrica, sino qué enseña cada patrón sobre la evaluación auditable de explicaciones post-hoc.

Los resultados proceden del benchmark EXP2 sobre UCI Adult Income. El diseño planificado comprendía 300 celdas, resultantes de cinco modelos, cuatro métodos XAI, cinco semillas y tres tamaños de muestra. Tras la auditoría de artefactos de FOM-7, se obtuvieron 275 celdas calificadas. Las celdas no calificadas fueron excluidas antes de la inferencia confirmativa. Esta primera cifra ya es una conclusión metodológica: un benchmark auditable no empieza con la prueba estadística, sino con la calificación de qué evidencia puede entrar a la prueba.

La cobertura fue completa para SHAP y LIME, con 75 de 75 celdas cada uno. DiCE alcanzó 68 de 75 celdas y Anchors 57 de 75. Esta diferencia de cobertura no debe ocultarse ni tratarse como un pie de página técnico: forma parte de la evidencia sobre viabilidad operativa de los métodos y condiciona la precisión de las conclusiones para reglas y contrafactuales. La Figura 1 documenta visualmente la cobertura analítica de EXP2 y debe leerse junto con la auditoría de artefactos de FOM-7.

## Evidencia global: diferencias reales, no ranking universal

El análisis global muestra diferencias estadísticamente significativas entre métodos en fidelidad y estabilidad. Para fidelidad, la prueba de Friedman produjo $\chi^2_F = 42.12$ sobre 15 bloques completos, con $p_{\mathrm{Holm}} = 1.51 \times 10^{-8}$ y $W = 0.936$. Este resultado rechaza la hipótesis nula de igualdad global entre métodos y muestra un patrón consistente: SHAP ocupa la primera posición de rango, seguido por LIME, Anchors y DiCE. La lectura inmediata es que, bajo esta operacionalización de fidelidad, las atribuciones SHAP se alinean mejor con los cambios observados en la salida del modelo.

Para estabilidad, la prueba de Friedman produjo $\chi^2_F = 40.68$, con $p_{\mathrm{Holm}} = 2.29 \times 10^{-8}$ y $W = 0.904$. El patrón no replica simplemente el orden de fidelidad: SHAP mantiene el perfil más fuerte, pero DiCE aparece como método relativamente estable en comparación con LIME y Anchors. Esta diferencia confirma que fidelidad y estabilidad no son constructos equivalentes. Una evaluación centrada en una única métrica habría perdido parte del fenómeno: los métodos no se distinguen solo por cuánto se alinean con el comportamiento local del modelo, sino también por cuánto varían sus explicaciones bajo perturbaciones y por qué tipo de objeto explicativo producen.

La implicación para un capítulo de libro es conceptual. El resultado estadístico no debe convertirse en la frase "SHAP gana". Debe convertirse en una lección sobre evaluación: cuando los métodos producen artefactos heterogéneos, las diferencias globales son útiles solo si se interpretan como perfiles condicionados por métrica, objeto explicativo y alcance experimental.

![Figura 2. Diagrama de diferencia crítica de Nemenyi para fidelidad y estabilidad. Fuente: figura derivada de `thesis/assets/figures/fig_cd_diagram_es.png`.](../figures/exported/fig_cd_diagram_es.png)

![Figura 3. Distribución de fidelidad y estabilidad por método. Fuente: figura derivada de `thesis/assets/figures/fig_boxplots_metricas_es.png`.](../figures/exported/fig_boxplots_metricas_es.png)

## SHAP y LIME: frontera calidad-coste

El contraste pareado SHAP-LIME se realizó sobre 75 celdas coincidentes $(g,s,n)$. Esta comparación es especialmente informativa porque ambos métodos alcanzaron cobertura completa y se evaluaron en las mismas coordenadas experimentales. Los resultados muestran una ventaja sistemática de SHAP en métricas de calidad explicativa, acompañada de una penalización de coste en la mayoría de contextos.

En fidelidad, SHAP supera a LIME en las 75 celdas, con diferencia media de +0.2479 y tamaño de efecto $d_z = +4.820$. En estabilidad, la ventaja también aparece en las 75 celdas, con diferencia media de +0.7176 y $d_z = +3.002$. Estos tamaños de efecto son muy grandes y respaldan la afirmación de que SHAP ofrece un perfil más fuerte cuando el objetivo principal es fidelidad y consistencia explicativa. En términos de auditoría técnica, esta regularidad importa más que una diferencia puntual de promedio: muestra que la ventaja aparece de forma sistemática a través de modelos, semillas y tamaños de muestra.

La parsimonia muestra el patrón inverso: SHAP es más denso y LIME más conciso. En coste, SHAP es en promedio más costoso, con diferencia media de +8047.6 ms, aunque el efecto es heterogéneo por modelo. Esto define la frontera calidad-coste: SHAP aporta mayor calidad explicativa bajo las métricas evaluadas, mientras LIME conserva atractivo operativo cuando la latencia y la concisión son prioritarias. La consecuencia no es descartar LIME, sino delimitar su uso. LIME puede ser adecuado para exploración rápida o interfaces de baja latencia, pero su estabilidad casi nula bajo las condiciones evaluadas impide tratar sus salidas como evidencia robusta de auditoría.

![Figura 4. Diferencias pareadas SHAP-LIME para fidelidad y estabilidad. Fuente: figura derivada de `thesis/assets/figures/fig_diferencias_pareadas_es.png`.](../figures/exported/fig_diferencias_pareadas_es.png)

![Figura 5. Relación entre estabilidad y coste por método. Fuente: figura derivada de `thesis/assets/figures/fig_estabilidad_coste_es.png`.](../figures/exported/fig_estabilidad_coste_es.png)

## Cuatro perfiles explicativos

SHAP presenta el perfil global más equilibrado en el benchmark. Sus valores consolidados reportados en la tesis son fidelidad = 0.810, estabilidad = 0.724, parsimonia = 0.234, brecha de fidelidad = 0.431 y coste = 24,804 ms sobre bloques calificados. Este perfil lo posiciona como método fuerte para auditoría técnica cuando se requiere fidelidad y estabilidad. Sin embargo, su coste es heterogéneo: TreeSHAP puede ser eficiente en modelos de árboles, mientras que KernelSHAP puede ser costoso en modelos como SVM o MLP. Por tanto, la recomendación no debe formularse como superioridad universal, sino como preferencia condicionada por el modelo base y las restricciones operativas.

LIME aparece como método eficiente y parsimonioso. Su coste medio reportado es 226 ms y su fidelidad media 0.560, con parsimonia de 0.085. Estos valores sostienen su utilidad en escenarios donde se requiere explicación rápida, legible y de bajo coste. La limitación crítica es su estabilidad casi nula bajo las condiciones evaluadas: estabilidad media cercana a 0.014 y CV de estabilidad de 86.2% bajo semillas. El valor de LIME dentro del capítulo es mostrar que una explicación plausible y barata no necesariamente es una explicación reproducible.

Anchors produce reglas locales de alta precisión, cualitativamente distintas a las atribuciones numéricas de LIME y SHAP. Su fortaleza está en la legibilidad condicional: una regla puede comunicar bajo qué condiciones se mantiene una predicción. En el benchmark, Anchors presenta cobertura incompleta, coste alto y variable, fidelidad media de 0.386 y estabilidad de 0.052. Esta lectura debe ser prudente. No implica que Anchors sea inútil, sino que sus reglas requieren criterios propios de precisión, cobertura y aplicabilidad. Su comparación directa mediante métricas diseñadas para atribuciones debe conservar esta advertencia.

DiCE genera contrafactuales, no atribuciones de importancia. Por ello, su baja fidelidad bajo métricas de atribución no debe interpretarse como fallo absoluto. En la tesis, DiCE presenta fidelidad de 0.172, estabilidad intermedia de 0.366, parsimonia muy baja de 0.017 y coste moderado de 2,056 ms. Este perfil sugiere que DiCE es más pertinente cuando el objetivo explicativo es explorar alternativas de acción o corrección, no cuando se busca auditar importancias locales. Su presencia en el benchmark ayuda a mostrar por qué FOM-7 evalúa perfiles y no rankings universales.

![Figura 6. Correlación entre métricas del benchmark. Fuente: figura derivada de `thesis/assets/figures/fig_correlacion_metricas_es.png`.](../figures/exported/fig_correlacion_metricas_es.png)

![Figura 7. Perfil multidimensional normalizado por método. Fuente: figura derivada de `thesis/assets/figures/fig_radar_metodos_es.png`.](../figures/exported/fig_radar_metodos_es.png)

## Reproducibilidad como hallazgo, no solo control

La proposición de reproducibilidad se confirma parcialmente. En configuraciones replicadas de EXP1, SHAP-fidelidad, SHAP-estabilidad y LIME-fidelidad muestran CV inferiores al umbral del 15%, con valores principales por debajo de 3%. La excepción es LIME-estabilidad, con CV de 86.2%, explicable por una media cercana a cero. Esta excepción no invalida el protocolo. Más bien, revela una propiedad estructural del método bajo la configuración evaluada: cuando la estabilidad media es casi nula, pequeñas variaciones absolutas producen un CV relativo alto.

Este punto es importante para el argumento del capítulo. FOM-7 no solo confirma resultados; también ayuda a distinguir entre fallas del protocolo y propiedades problemáticas del método. Si una métrica varía porque el pipeline es inestable, el estudio pierde confiabilidad. Si una métrica varía porque el explicador produce salidas intrínsecamente inestables bajo condiciones controladas, el hallazgo es sustantivo. En este caso, la reproducibilidad funciona como lente interpretativa y no solo como requisito técnico.

## Síntesis del bloque empírico

Los resultados, resumidos en la Tabla 4, sostienen tres conclusiones de alcance delimitado. Primero, existen diferencias globales significativas entre métodos bajo el diseño EXP2. Segundo, SHAP ofrece el perfil más fuerte en fidelidad y estabilidad, especialmente cuando el objetivo es auditoría técnica. Tercero, no existe un método universalmente dominante: LIME conserva ventajas de coste y parsimonia; Anchors produce reglas condicionales con límites de cobertura; DiCE aporta contrafactualidad y acción correctiva.

La frontera calidad-coste es el resultado interpretativo central. La selección de un método XAI debe depender del objetivo operativo: auditoría de alta fidelidad, explicación rápida, regla condicional o exploración contrafactual. FOM-7 permite que esa selección se base en evidencia trazable y no en preferencias anecdóticas. Para un capítulo de libro, esta es la contribución más relevante del bloque empírico: mostrar que el valor de los resultados no reside en una tabla aislada, sino en la manera en que el protocolo convierte diferencias métricas en criterios de uso.
