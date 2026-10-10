# Resumen y palabras clave

## Resumen

A medida que los sistemas de aprendizaje automático asumen decisiones críticas en finanzas, salud, empleo y justicia, comprender *por qué* un modelo emite un veredicto específico se ha convertido en un requisito indispensable de ingeniería, gobernanza y cumplimiento normativo. En la ingeniería de datos tradicional, la observabilidad se fundamenta en flujos deterministas, trazas de linaje (*data lineage*) y pruebas unitarias reproducibles. No obstante, cuando un pipeline culmina en un modelo complejo de caja negra (ensambles de árboles o redes neuronales densas), la telemetría estándar se vuelve ciega ante la lógica interna que transformó las variables de entrada en la predicción final.

Para abordar esta opacidad ha emergido la Inteligencia Artificial Explicable (*Explainable Artificial Intelligence*, XAI). Sin embargo, herramientas populares como LIME, SHAP, Anchors y DiCE a menudo entregan explicaciones divergentes, inestables o de alta latencia ante una misma instancia, evidenciando la falta de un estándar cuantitativo de evaluación.

Este capítulo ofrece un recorrido riguroso y orientado a la ingeniería sobre los métodos agnósticos de XAI, presentando el protocolo **FOM-7** (*Framework for Operational Metrics in 7 Gates*), un marco de siete puertas de control para auditar y certificar explicadores algorítmicos. Mediante un benchmark experimental sobre el conjunto de datos *UCI Adult Income*, evaluamos sistemáticamente cuatro explicadores sobre cinco familias de modelos predictivos (Regresión Logística, Árbol de Decisión, Bosque Aleatorio, XGBoost y Perceptrón Multicapa). Los resultados caracterizan la frontera de Pareto entre la alta fidelidad y estabilidad axiomática de KernelSHAP frente a la agilidad computacional de LIME, así como el valor operacional de las reglas de Anchors y los contrafactuales de DiCE. El capítulo concluye con una matriz de decisión para ingenieros y un flujo de auditoría en tres fases alineado con la Ley de IA de la Unión Europea y el marco NIST AI RMF.

## Palabras clave

Inteligencia artificial explicable; explicabilidad agnóstica; ingeniería de datos; observabilidad algorítmica; benchmarking reproducible; protocolo FOM-7; evaluación multi-métrica; explicaciones post-hoc.
