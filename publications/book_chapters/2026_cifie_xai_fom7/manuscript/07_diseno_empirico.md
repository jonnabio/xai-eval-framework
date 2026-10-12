# Métodos evaluados y diseño del benchmark

Fuente inicial: `thesis/capitulo-2-fundamentos.qmd`, `tables/table_methods_comparison.md`, `tables/table_metrics.md` y `tables/table_results_summary.md`; `thesis/capitulo-1-marco-teorico.qmd` y `pub/fragments/paper_c_abstract_en.tex`.

## Métodos y objetos explicativos

Los cuatro métodos producen objetos diferentes: LIME, sustitutos locales; SHAP, atribuciones; Anchors, reglas; y DiCE, contrafactuales. Una comparación válida alinea método, objeto, métrica y propósito, en vez de tratar todas las salidas como respuestas a una misma pregunta (Guidotti et al., 2018; Carvalho et al., 2019; Marcinkevičs & Vogt, 2023). Las Figuras 2 y 3 fijan ese vocabulario; FOM-7 conserva la relación entre objeto, contexto experimental y alcance de cada afirmación. La sección 08 presenta perfiles condicionados por las métricas del benchmark, no una jerarquía universal.


**LIME.** LIME (*Local Interpretable Model-agnostic Explanations*) aproxima la predicción de una instancia ajustando un sustituto interpretable, habitualmente lineal, a perturbaciones ponderadas del modelo de caja negra (Ribeiro et al., 2016). Su flexibilidad facilita explicaciones locales legibles, pero el resultado depende del vecindario, el kernel, el muestreo, la selección de características y el sustituto. Usar un modelo lineal no demuestra fidelidad: deben documentarse los parámetros y evaluarse la aproximación local (Ribeiro et al., 2016; Guidotti et al., 2018). Una explicación plausible también puede ser inestable ante perturbaciones o vulnerable a manipulación (Burger et al., 2023; Slack et al., 2020). FOM-7 exige parámetros trazables, controles de estabilidad y afirmaciones limitadas al vecindario evaluado.

**SHAP.** SHAP (*SHapley Additive exPlanations*) representa una predicción mediante atribuciones aditivas basadas en valores de Shapley (Lundberg & Lee, 2017). Su significado depende de los datos de referencia, los supuestos sobre características ausentes, la dependencia entre variables y la variante utilizada. KernelSHAP es general, pero puede requerir numerosas consultas; TreeSHAP aprovecha la estructura de árboles, mientras que el cálculo exacto puede ser intratable para clases amplias de modelos (Van den Broeck et al., 2022). Para reproducirlo deben especificarse variante, modelo, referencia, aproximación y coste. Las atribuciones describen la salida bajo esos supuestos, no establecen causalidad real; las afirmaciones se limitan al benchmark.

**Anchors.** Anchors explica una predicción mediante reglas locales si-entonces: condiciones destinadas a conservarla con alta probabilidad (Ribeiro et al., 2018). A diferencia de LIME o SHAP, produce reglas, no pesos de características. La precisión debe interpretarse junto con cobertura, complejidad y reproducibilidad: una regla específica puede ser precisa y aplicarse a pocos casos (Ribeiro et al., 2018; Guidotti et al., 2018). Como reglas, atribuciones y contrafactuales son objetos distintos, FOM-7 trata la evidencia de Anchors como condicional y advierte contra evaluarla solo con métricas diseñadas para atribuciones continuas.

**DiCE.** DiCE (*Diverse Counterfactual Explanations*) genera instancias alternativas para cambiar una predicción y responder preguntas de recourse, no de atribución retrospectiva (Mothilal et al., 2020; Wachter et al., 2017; Karimi et al., 2022). Los contrafactuales requieren evaluar validez respecto al modelo, proximidad, diversidad, plausibilidad y factibilidad; la cercanía matemática no garantiza una acción realista. FACE enfatiza trayectorias factibles entre datos observados, mientras otros trabajos advierten que un contrafactual post-hoc puede cumplir un objetivo formal sin ser utilizable (Poyiadzi et al., 2020; Laugel et al., 2019). FOM-7 trata DiCE como un objeto explicativo distinto de la atribución.

## Diseño y análisis experimental

**Fases experimentales.** EXP1 calibra el pipeline, congela los modelos compartidos con EXP2 y estima la variación entre semillas; no sustenta las afirmaciones confirmativas. En la tesis, sus métricas de calidad muestran coeficientes de variación inferiores al 9%, mientras que el coste varía más, en especial con KernelSHAP. EXP2 es el benchmark primario: sus artefactos calificados alimentan los perfiles y las pruebas. Esta separación limita la contaminación post hoc; conforme a FOM-7, la calibración informa el diseño, pero la inferencia se apoya en EXP2.

**Datos y modelos.** EXP2 usa UCI Adult Income, un conjunto tabular mixto para clasificación binaria del ingreso superior a 50,000 dólares (Becker & Kohavi, 1996). La partición estratificada, imputación, codificación y escalado se ajustan de forma determinista solo con entrenamiento; el preprocesador congelado se comparte entre métodos para evitar fuga de datos o diferencias de representación.

Se comparan cinco familias predictivas: regresión logística, bosque aleatorio, XGBoost, SVM y MLP. Cubren modelos lineales, de árboles, con kernel y neuronales; el objetivo es evaluar la variación de los perfiles explicativos, no la superioridad predictiva. El bosque aleatorio sigue la tradición de ensamblados de Breiman (2001).

**Diseño factorial.** EXP2 cruza cinco modelos, cuatro métodos (SHAP, LIME, Anchors y DiCE), cinco semillas (42, 123, 456, 789, 999) y tres tamaños por estrato (50, 100 y 200), para 300 celdas planificadas. La auditoría FOM-7 calificó 275; los artefactos faltantes o no armonizables no se imputan ni se ocultan. SHAP y LIME cubren 75 de 75 celdas; DiCE, 68 de 75; Anchors, 57 de 75. La Figura 8 muestra esta cobertura.

**Muestreo.** Se estratifica por cuadrante de error (verdaderos y falsos positivos y negativos), para incluir aciertos y errores. Las ejecuciones contienen entre 27 y 800 instancias (mediana: 400); esa variación se conserva y la inferencia se realiza sobre agregados, no sobre instancias independientes.

![Figura 8. Cobertura analítica EXP2 por modelo y método. Fuente: elaboración propia a partir del inventario de celdas calificadas de EXP2.](../figures/exported/fig_cobertura_exp2_es.png)

**Configuración de explicadores.** Las configuraciones se congelan por ejecución: TreeSHAP para bosque aleatorio y XGBoost, KernelSHAP para los demás; LIME tabular con parámetros fijos; Anchors con umbral de precisión de 0.95; DiCE genera contrafactuales de la clase opuesta. Se comparan estas implementaciones registradas, no etiquetas abstractas; las conclusiones conservan sus límites.

**Métricas primarias.** La Tabla 1 define fidelidad, estabilidad, parsimonia, brecha de fidelidad y coste computacional.

<!-- TABLA: table_metrics.md -->

Las métricas se calculan por instancia y se promedian por ejecución; la inferencia respeta los bloques experimentales para evitar pseudorreplicación.

**Unidad de análisis.** La jerarquía distingue métricas por instancia, medias por ejecución (modelo, método, semilla y tamaño) y bloques modelo-tamaño $(g,n)$. Las pruebas globales usan 15 bloques completos y promedian las semillas calificadas dentro de cada bloque; ni instancias ni semillas se tratan como bloques independientes.

**Plan inferencial.** Las diferencias globales se evalúan con Friedman y, tras rechazar la hipótesis nula, con comparaciones post hoc de Nemenyi sobre bloques completos (Friedman, 1937; Demšar, 2006; Nemenyi, 1963). Los coeficientes de variación describen la reproducibilidad entre semillas. El objetivo es identificar diferencias defendibles bajo este diseño de Adult Income, no establecer un ranking universal.
