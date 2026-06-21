# Métodos post-hoc evaluados: LIME, SHAP, Anchors y DiCE

Fuente inicial: `thesis/capitulo-2-fundamentos.qmd`, `tables/table_methods_comparison.md`, `tables/table_metrics.md` y `tables/table_results_summary.md`.

## Panorama comparativo

Los cuatro métodos analizados representan familias distintas de explicación post-hoc agnóstica o parcialmente agnóstica al modelo. LIME produce sustitutos locales; SHAP genera atribuciones aditivas de características; Anchors formula reglas locales de alta precisión; DiCE construye ejemplos contrafactuales diversos. Esta heterogeneidad es metodológicamente importante porque cada método produce un objeto explicativo diferente y, por tanto, no debe evaluarse como si todos respondieran exactamente la misma pregunta.

La comparación del capítulo debe leerse como evaluación de perfiles, no como ranking universal. FOM-7 exige que cada conclusión conserve unido el método, el objeto explicativo, la métrica, el contexto experimental y el alcance de la afirmación.

## LIME: sustitutos locales e inestabilidad potencial

LIME (*Local Interpretable Model-agnostic Explanations*) explica predicciones individuales mediante una aproximación local del modelo de caja negra. El procedimiento genera perturbaciones alrededor de una instancia, consulta el modelo original y ajusta un modelo interpretable, usualmente lineal, ponderando las observaciones según su proximidad a la instancia explicada [@ribeiro2016].

Su base metodológica puede resumirse como una regresión local ponderada sobre un vecindario artificial. La explicación resultante identifica características con pesos positivos o negativos que aproximan la influencia local en la predicción. Esta salida es relativamente sencilla de comunicar y suele tener bajo coste computacional frente a alternativas más complejas.

La principal fortaleza de LIME es su flexibilidad: puede aplicarse a distintos clasificadores sin acceder a su estructura interna. Sin embargo, esa misma flexibilidad introduce sensibilidad al muestreo, al kernel de proximidad, al tamaño del vecindario, al número de perturbaciones y a la selección de características. Por ello, una explicación LIME no debe evaluarse solo por su legibilidad. Debe comprobarse si es fiel al modelo local y si permanece estable ante perturbaciones razonables.

En el benchmark de la tesis, LIME aparece como una alternativa de bajo coste y alta parsimonia, pero con estabilidad casi nula en las condiciones evaluadas. Esta combinación lo vuelve útil para escenarios de latencia o comunicación rápida, pero problemático en auditoría, comparación entre instancias o decisiones de alto riesgo cuando se requiere consistencia explicativa.

## SHAP: atribución aditiva basada en valores de Shapley

SHAP (*SHapley Additive exPlanations*) interpreta una predicción como suma de contribuciones atribuibles a las características. Su fundamento proviene del valor de Shapley en teoría de juegos cooperativos, adaptado al problema de distribuir la salida de un modelo entre variables explicativas [@lundberg2017].

La salida típica de SHAP es un vector de atribuciones, local para una instancia y agregable para análisis globales. Su fortaleza reside en un marco formal unificado para explicaciones aditivas, con propiedades axiomáticas que facilitan la interpretación comparativa. Esta base lo convierte en un referente para análisis de fidelidad y estabilidad en datos tabulares.

No obstante, SHAP requiere decisiones operativas relevantes. El conjunto de referencia, la forma de simular ausencia de características, la dependencia entre variables y la variante concreta del explicador condicionan el significado de las atribuciones. KernelSHAP conserva mayor generalidad, pero puede ser costoso; TreeSHAP aprovecha modelos de árbol y puede ser mucho más eficiente. Por ello, "usar SHAP" no describe por sí solo una configuración experimental completa.

En los resultados extraídos de la tesis, SHAP presenta el perfil global más fuerte en fidelidad y estabilidad dentro del benchmark, aunque con costes heterogéneos por familia de modelo. Su uso dentro del capítulo debe enfatizar esta frontera calidad-costo: SHAP es especialmente defendible cuando la prioridad es evidencia explicativa de alta calidad, pero su viabilidad práctica depende del modelo base y de las restricciones de latencia.

## Anchors: reglas locales de alta precisión

Anchors explica una predicción mediante reglas locales tipo si-entonces. La idea central es encontrar condiciones suficientes bajo las cuales el modelo mantiene la misma predicción con alta probabilidad [@ribeiro2018]. A diferencia de LIME o SHAP, Anchors no produce principalmente pesos de características, sino reglas que delimitan una región de decisión.

La fortaleza de Anchors es comunicativa. Una regla local puede resultar más legible que una lista de atribuciones, sobre todo cuando se necesita explicar condiciones que sostienen una decisión. Sin embargo, la precisión de una regla debe interpretarse junto con su cobertura. Una regla muy estrecha puede ser precisa porque aplica a pocos casos; una regla más amplia puede perder precisión.

Esta tensión convierte a Anchors en un método que exige evaluación cuidadosa. Su salida no se alinea naturalmente con todas las métricas de atribución. Si el benchmark lo evalúa solo con fidelidad de importancia, puede penalizarlo por no producir el mismo tipo de artefacto que SHAP o LIME. Por ello, FOM-7 debe presentar Anchors como evidencia condicional: útil cuando precisión y cobertura se reportan juntas, pero limitada cuando se compara directamente contra métodos de atribución.

En los resultados de la tesis, Anchors muestra cobertura incompleta, coste alto y variable, y valores inferiores de fidelidad y estabilidad frente a SHAP y LIME bajo las métricas usadas. Esta lectura no debe interpretarse como fallo absoluto del método, sino como evidencia de que las reglas locales de alta precisión tienen un objeto explicativo distinto y pueden requerir criterios adicionales de evaluación.

## DiCE: contrafactuales diversos y acción correctiva

DiCE (*Diverse Counterfactual Explanations*) genera ejemplos contrafactuales: instancias alternativas que, con cambios mínimos o controlados, producirían una predicción diferente [@mothilal2020]. Su pregunta principal no es qué característica contribuyó más a la predicción actual, sino qué tendría que cambiar para obtener otro resultado.

Esta orientación ubica a DiCE en una familia distinta de explicaciones. Sus criterios naturales incluyen validez del cambio de predicción, proximidad a la instancia original, diversidad entre alternativas, factibilidad y accionabilidad. La tradición de explicaciones contrafactuales también subraya la relación entre explicación, decisiones automatizadas y posibilidad de acción correctiva [@wachter2017].

DiCE no debe evaluarse como si fuera simplemente un método de atribución. Una baja fidelidad en términos de correlación de importancias puede reflejar que el método optimiza otro objetivo: producir alternativas contrafactuales. Por tanto, sus resultados deben interpretarse en relación con concisión, cambios propuestos, proximidad, diversidad y límites de factibilidad.

En la tesis, DiCE aparece con baja fidelidad bajo métricas de atribución, estabilidad intermedia, alta parsimonia contrafactual y coste moderado. Esta combinación lo vuelve relevante para discutir la ausencia de un método universalmente dominante: puede ser menos adecuado para auditar importancias locales, pero más alineado con escenarios donde interesa explorar alternativas de acción.

## Comparación metodológica y uso dentro de FOM-7

Los cuatro métodos no producen evidencia intercambiable. LIME aproxima localmente una frontera; SHAP reparte contribuciones; Anchors identifica condiciones suficientes; DiCE propone alternativas contrafactuales. La evaluación debe respetar esa ontología de salidas.

Dentro de FOM-7, la comparación se vuelve admisible solo cuando el capítulo declara:

- qué objeto explicativo produce cada método;
- qué métrica se aplica y por qué es pertinente;
- qué unidad experimental sostiene el resultado;
- qué artefactos y scripts respaldan la cifra;
- qué límites conserva la afirmación.

Esta regla permite usar los resultados del benchmark sin sobreafirmar. SHAP puede describirse como fuerte en fidelidad y estabilidad bajo las condiciones evaluadas; LIME como eficiente pero inestable; Anchors como regla local con límites de cobertura; DiCE como método contrafactual cuya calidad no se agota en métricas de atribución. Esa lectura por perfiles es la base técnica para la discusión posterior del capítulo.
