# Resumen y palabras clave

## Resumen

A medida que los sistemas de inteligencia artificial asumen decisiones críticas en la salud, las finanzas y la sociedad, entender *por qué* un modelo toma una determinación ya no es solo una curiosidad técnica: es una necesidad ética, legal y operativa. Sin embargo, generar una explicación no garantiza que esta sea confiable. Herramientas populares como LIME, SHAP, Anchors o DiCE a menudo ofrecen respuestas divergentes ante un mismo problema, lo que plantea una pregunta crucial: ¿cómo evaluar si la explicación misma es digna de confianza?

Este capítulo ofrece una visión introductoria y rigurosa sobre la Inteligencia Artificial Explicable (XAI) a través de **FOM-7**, un protocolo operativo de siete puertas diseñado para auditar, comparar y validar explicaciones algorítmicas de manera reproducible. A partir de un benchmark empírico sobre el conjunto de datos *UCI Adult Income*, el texto analiza cómo responden LIME, SHAP, Anchors y DiCE al evaluar cinco familias de modelos predictivos. El análisis revela el perfil de cada método —mostrando la solidez de SHAP para auditorías de alta exigencia frente a la velocidad pero menor estabilidad de LIME, así como el valor práctico de las reglas de Anchors y los escenarios contrafactuales de DiCE.

Más que un listado de métricas, este capítulo proporciona al lector una hoja de ruta clara para transitar desde la confianza ciega en los algoritmos hacia una supervisión transparente, defendible y centrada en el ser humano.

## Palabras clave

Inteligencia artificial explicable; explicabilidad agnóstica al modelo; benchmarking reproducible; protocolo FOM-7; evaluación multi-métrica; explicaciones post-hoc.
