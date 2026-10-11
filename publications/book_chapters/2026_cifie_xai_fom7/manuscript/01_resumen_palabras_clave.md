# Resumen y palabras clave

## Resumen

Comprender *por qué* un modelo de aprendizaje automático emite un veredicto crítico es un imperativo ético, técnico y regulatorio en finanzas, medicina y justicia. La ingeniería de datos tradicional asegura observabilidad mediante esquemas deterministas, linaje y pruebas unitarias. No obstante, al incorporar modelos de caja negra no lineales (ensambles o redes neuronales), la telemetría convencional queda ciega ante la lógica interna que determina la predicción.

Para resolver esta opacidad surge la Inteligencia Artificial Explicable (*Explainable Artificial Intelligence*, XAI). Sin embargo, herramientas como LIME, SHAP, Anchors y DiCE exhiben con frecuencia discrepancias, inestabilidad o latencias excesivas ante una misma instancia, revelando la ausencia de un estándar formal de validación.

Este capítulo examina rigurosamente los métodos agnósticos de XAI y formaliza el protocolo **FOM-7** (*Framework for Operational Metrics in 7 Gates*), un marco metrológico de siete puertas para certificar explicadores. Mediante un banco de pruebas sobre *UCI Adult Income*, evaluamos cuatro explicadores en cinco familias de clasificadores (Regresión Logística, Árbol de Decisión, Bosque Aleatorio, XGBoost y Perceptrón Multicapa). Los hallazgos delinean la frontera de Pareto entre la fidelidad axiomática de KernelSHAP y la eficiencia de LIME, junto al valor prescriptivo de Anchors y DiCE. Se concluye con una matriz de decisión y un flujo de auditoría alineado con la Ley de IA europea y NIST AI RMF.

## Palabras clave

Inteligencia artificial explicable; explicabilidad agnóstica; ingeniería de datos; observabilidad algorítmica; benchmarking reproducible; protocolo FOM-7; evaluación multi-métrica; explicaciones post-hoc.

