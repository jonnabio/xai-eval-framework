# Introducción

## De la opacidad predictiva a la exigencia de evidencia

El avance de los modelos de aprendizaje automático ha incrementado la capacidad predictiva en dominios donde las decisiones automatizadas afectan oportunidades, recursos y riesgos. Sin embargo, la mejora de rendimiento suele venir acompañada de opacidad. Modelos basados en ensambles, kernels o arquitecturas neuronales pueden producir predicciones precisas sin ofrecer una descripción inmediata de las razones que las sustentan. Esta tensión convierte la explicabilidad en una condición técnica, metodológica y de gobernanza para el uso responsable de sistemas de IA.

La inteligencia artificial explicable (XAI) responde a esta tensión mediante métodos que generan artefactos interpretables: atribuciones de características, reglas locales, sustitutos lineales, ejemplos contrafactuales o resúmenes globales. En particular, los métodos post-hoc agnósticos al modelo permiten explicar sistemas ya entrenados sin modificar su arquitectura interna. LIME, SHAP, Anchors y DiCE representan cuatro familias ampliamente utilizadas: sustitutos locales, atribuciones aditivas, reglas condicionales y contrafactuales diversos [@ribeiro2016; @lundberg2017; @ribeiro2018; @mothilal2020; @wachter2017].

No obstante, la disponibilidad de explicadores no resuelve por sí sola el problema de evaluación. Una explicación puede ser plausible para un usuario y, aun así, ser poco fiel al modelo; puede ser fiel en una instancia y variar de forma sustantiva ante perturbaciones menores; puede ser breve pero omitir variables relevantes; puede ser útil para acción correctiva y no funcionar como atribución de importancia. Por tanto, la pregunta central ya no es solo cómo generar explicaciones, sino cuándo esas explicaciones merecen ser tratadas como evidencia.

## La crisis de evaluación en XAI

La literatura reciente describe una crisis de evaluación en XAI: proliferan métricas, herramientas y taxonomías, pero persisten dificultades para comparar resultados entre estudios, acumular evidencia y separar observaciones descriptivas de afirmaciones inferenciales [@doshi-velez2017; @abdulkadir2023; @canha2025; @nauta2023]. Parte del problema surge porque la interpretabilidad no es un constructo unitario. Fidelidad, estabilidad, parsimonia, coste, comprensibilidad, robustez y utilidad decisional capturan dimensiones distintas.

Los marcos y bibliotecas de evaluación han contribuido a ordenar el campo. Quantus ofrece una infraestructura amplia para métricas de explicación, y OpenXAI promueve comparaciones transparentes entre explicadores [@hedstrom2023; @agarwal2022]. Sin embargo, calcular métricas no equivale a gobernar un proceso de evidencia. Antes de aceptar un resultado como defendible, deben declararse las configuraciones, las semillas, los artefactos válidos, las reglas de exclusión, la unidad de análisis, el plan inferencial y los límites de interpretación.

Este capítulo parte de esa brecha. La evaluación XAI necesita métricas, pero también necesita protocolo. Sin un control secuencial, un benchmark puede mezclar artefactos incompletos, configuraciones heterogéneas, comparaciones no pareadas y conclusiones que exceden su base empírica. La consecuencia es una literatura rica en salidas explicativas, pero a menudo débil en trazabilidad de afirmaciones.

## Objetivo y contribución del capítulo

El objetivo del capítulo es presentar FOM-7 como protocolo reproducible para la evaluación multi-métrica de métodos post-hoc agnósticos al modelo, y mostrar su utilidad mediante un benchmark empírico sobre LIME, SHAP, Anchors y DiCE. La contribución no consiste en proponer un nuevo explicador, sino en ordenar el ciclo que permite transformar ejecuciones experimentales en evidencia auditable.

FOM-7 se organiza en siete puertas: congelación del protocolo, ejecución controlada, auditoría de artefactos, armonización analítica, exportación inferencial, perfilado de reproducibilidad y reporte trazable. La regla central es simple: ninguna afirmación inferencial debe formularse si las puertas previas no están satisfechas o si la afirmación no puede vincularse con evidencia fuente verificable.

El capítulo también aporta una lectura empírica de perfiles explicativos. Bajo las condiciones evaluadas, SHAP muestra un perfil fuerte en fidelidad y estabilidad; LIME conserva ventajas de coste y concisión, con una limitación crítica de estabilidad; Anchors aporta reglas locales con límites de cobertura; DiCE responde a una lógica contrafactual que no debe evaluarse solo como atribución de características. La selección de métodos se interpreta así como una decisión condicionada por objetivo operativo, métrica, coste y riesgo.

## Alcance empírico

El benchmark se acota al conjunto UCI Adult Income, un problema tabular de clasificación binaria. El diseño compara cuatro métodos XAI sobre cinco familias de modelos, cinco semillas y tres tamaños de muestra. Las métricas primarias son fidelidad, estabilidad, parsimonia, brecha de fidelidad y coste computacional, descritas en `tables/table_metrics.md`.

El alcance de los resultados es deliberadamente limitado. Las conclusiones no se presentan como superioridad universal de un método, sino como evidencia bajo condiciones experimentales controladas. Las figuras candidatas registradas en `figures/figure_registry.md` y las tablas de trabajo del capítulo funcionan como controles de trazabilidad para evitar sobreafirmaciones.

## Marco del capítulo

La exposición avanza en cinco movimientos. Primero, se establecen los fundamentos técnicos de la explicabilidad agnóstica al modelo y se diferencia entre plausibilidad, fidelidad, estabilidad y utilidad humana. Segundo, se describen LIME, SHAP, Anchors y DiCE como métodos con objetos explicativos heterogéneos. Tercero, se formula la crisis de evaluación y se presenta FOM-7 como respuesta metodológica. Cuarto, se reporta el diseño empírico y los resultados principales del benchmark. Finalmente, se discuten implicaciones, límites y líneas futuras.

Esta estructura busca sostener una tesis principal: la explicabilidad útil no depende únicamente de producir explicaciones plausibles, sino de evaluar cuándo esas explicaciones son fieles, estables, comparables, reproducibles y defendibles.
