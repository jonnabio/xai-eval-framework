# Resultados principales: frontera calidad-costo

Fuente inicial: `thesis/capitulo-4-resultados.qmd`, `tables/table_results_summary.md`, `tables/table_metrics.md` y `figures/figure_registry.md`.

## Alcance de los resultados

Los resultados proceden del benchmark EXP2 sobre UCI Adult Income. El diseño planificado comprendía 300 celdas, resultantes de cinco modelos, cuatro métodos XAI, cinco semillas y tres tamaños de muestra. Tras la auditoría de artefactos de FOM-7, se obtuvieron 275 celdas calificadas. Las celdas no calificadas fueron excluidas antes de la inferencia confirmativa.

La cobertura fue completa para SHAP y LIME, con 75 de 75 celdas cada uno. DiCE alcanzó 68 de 75 celdas y Anchors 57 de 75. Esta diferencia de cobertura no debe ocultarse: forma parte de la evidencia sobre viabilidad operativa de los métodos y condiciona la precisión de las conclusiones para Anchors y DiCE.

## Diferencias globales entre métodos

El análisis global muestra diferencias estadísticamente significativas entre métodos en fidelidad y estabilidad. Para fidelidad, la prueba de Friedman produjo $\chi^2_F = 42.12$ sobre 15 bloques completos, con $p_{\mathrm{Holm}} = 1.51 \times 10^{-8}$ y $W = 0.936$. Este resultado rechaza la hipótesis nula de igualdad global entre métodos y muestra un patrón consistente: SHAP ocupa la primera posición de rango, seguido por LIME, Anchors y DiCE.

Para estabilidad, la prueba de Friedman produjo $\chi^2_F = 40.68$, con $p_{\mathrm{Holm}} = 2.29 \times 10^{-8}$ y $W = 0.904$. El patrón no replica simplemente el orden de fidelidad: SHAP mantiene el perfil más fuerte, pero DiCE aparece como método relativamente estable en comparación con LIME y Anchors. Esta diferencia confirma que fidelidad y estabilidad no son constructos equivalentes.

La implicación central es metodológica: una evaluación centrada en una única métrica habría perdido parte del fenómeno. Los métodos no se distinguen solo por cuánto se alinean con el comportamiento local del modelo, sino también por cuánto varían sus explicaciones bajo perturbaciones y por qué tipo de objeto explicativo producen.

## Comparación pareada SHAP-LIME

El contraste pareado SHAP-LIME se realizó sobre 75 celdas coincidentes $(g,s,n)$. Los resultados muestran una ventaja sistemática de SHAP en métricas de calidad explicativa, acompañada de una penalización de coste en la mayoría de contextos.

En fidelidad, SHAP supera a LIME en las 75 celdas, con diferencia media de +0.2479 y tamaño de efecto $d_z = +4.820$. En estabilidad, la ventaja también aparece en las 75 celdas, con diferencia media de +0.7176 y $d_z = +3.002$. Estos tamaños de efecto son muy grandes y respaldan la afirmación de que SHAP ofrece un perfil más fuerte cuando el objetivo principal es fidelidad y consistencia explicativa.

La parsimonia muestra el patrón inverso: SHAP es más denso y LIME más conciso. En coste, SHAP es en promedio más costoso, con diferencia media de +8047.6 ms, aunque el efecto es heterogéneo por modelo. Esto define la frontera calidad-costo: SHAP aporta mayor calidad explicativa bajo las métricas evaluadas, mientras LIME conserva atractivo operativo cuando la latencia y la concisión son prioritarias.

## Perfil de SHAP

SHAP presenta el perfil global más equilibrado en el benchmark. Sus valores consolidados reportados en la tesis son fidelidad = 0.810, estabilidad = 0.724, parsimonia = 0.234, brecha de fidelidad = 0.431 y coste = 24,804 ms sobre bloques calificados.

Este perfil lo posiciona como método fuerte para auditoría técnica cuando se requiere fidelidad y estabilidad. Sin embargo, su coste es heterogéneo: TreeSHAP puede ser eficiente en modelos de árboles, mientras que KernelSHAP puede ser costoso en modelos como SVM o MLP. Por tanto, la recomendación no debe formularse como superioridad universal, sino como preferencia condicionada por el modelo base y las restricciones operativas.

## Perfil de LIME

LIME aparece como método eficiente y parsimonioso. Su coste medio reportado es 226 ms y su fidelidad media 0.560, con parsimonia de 0.085. Estos valores sostienen su utilidad en escenarios donde se requiere explicación rápida, legible y de bajo coste.

La limitación crítica es su estabilidad casi nula bajo las condiciones evaluadas. La tesis reporta estabilidad media cercana a 0.014 y CV de estabilidad de 86.2% bajo semillas. Esto restringe su uso en auditoría, comparación entre instancias o escenarios donde dos ejecuciones razonables deberían producir explicaciones consistentes.

## Perfil de Anchors

Anchors produce reglas locales de alta precisión, cualitativamente distintas a las atribuciones numéricas de LIME y SHAP. Su fortaleza está en la legibilidad condicional: una regla puede comunicar bajo qué condiciones se mantiene una predicción.

En el benchmark, Anchors presenta cobertura incompleta, coste alto y variable, fidelidad media de 0.386 y estabilidad de 0.052. Esta lectura debe ser prudente. No implica que Anchors sea inútil, sino que sus reglas requieren criterios propios de precisión, cobertura y aplicabilidad. Su comparación directa mediante métricas diseñadas para atribuciones debe conservar esta advertencia.

## Perfil de DiCE

DiCE genera contrafactuales, no atribuciones de importancia. Por ello, su baja fidelidad bajo métricas de atribución no debe interpretarse como fallo absoluto. En la tesis, DiCE presenta fidelidad de 0.172, estabilidad intermedia de 0.366, parsimonia muy baja de 0.017 y coste moderado de 2,056 ms.

Este perfil sugiere que DiCE es más pertinente cuando el objetivo explicativo es explorar alternativas de acción o corrección, no cuando se busca auditar importancias locales. Su presencia en el benchmark ayuda a mostrar por qué FOM-7 evalúa perfiles y no rankings universales.

## Reproducibilidad del protocolo

La proposición de reproducibilidad se confirma parcialmente. En configuraciones replicadas de EXP1, SHAP-fidelidad, SHAP-estabilidad y LIME-fidelidad muestran CV inferiores al umbral del 15%, con valores principales por debajo de 3%. La excepción es LIME-estabilidad, con CV de 86.2%, explicable por una media cercana a cero.

Esta excepción no invalida el protocolo. Más bien, revela una propiedad estructural del método bajo la configuración evaluada: cuando la estabilidad media es casi nula, pequeñas variaciones absolutas producen un CV relativo alto. FOM-7 permite distinguir entre irreproducibilidad del protocolo e inestabilidad sustantiva del explicador.

## Lectura integrada

Los resultados sostienen tres conclusiones de alcance delimitado. Primero, existen diferencias globales significativas entre métodos bajo el diseño EXP2. Segundo, SHAP ofrece el perfil más fuerte en fidelidad y estabilidad, especialmente cuando el objetivo es auditoría técnica. Tercero, no existe un método universalmente dominante: LIME conserva ventajas de coste y parsimonia; Anchors produce reglas condicionales con límites de cobertura; DiCE aporta contrafactualidad y acción correctiva.

La frontera calidad-costo es, por tanto, el resultado interpretativo central. La selección de un método XAI debe depender del objetivo operativo: auditoría de alta fidelidad, explicación rápida, regla condicional o exploración contrafactual. FOM-7 permite que esa selección se base en evidencia trazable y no en preferencias anecdóticas.

## Figuras candidatas

Las visualizaciones registradas en `figures/figure_registry.md` deben usarse como apoyo, no como sustituto de las pruebas estadísticas. Las figuras candidatas incluyen la relación estabilidad-coste, la correlación entre métricas, la cobertura EXP2, el diagrama de diferencia crítica, boxplots de fidelidad/estabilidad, diferencias pareadas SHAP-LIME y perfil radar por método. Antes de incorporarlas al manuscrito final, deben copiarse o exportarse al paquete del capítulo y registrarse con fuente exacta.
