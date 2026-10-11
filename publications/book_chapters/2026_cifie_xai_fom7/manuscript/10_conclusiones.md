# Conclusiones

## Síntesis de aportaciones

Este capítulo demuestra que la explicabilidad algorítmica constituye la **capa de observabilidad indispensable** para auditar modelos complejos en entornos de alta responsabilidad.

A través del protocolo **FOM-7** y su validación empírica en *UCI Adult Income*, este trabajo aporta:

1. **Un marco conceptual desmitificado:** Delimita operativamente transparencia, interpretabilidad intrínseca y explicabilidad post-hoc, distinguiendo la atribución estadística de la causalidad real.
2. **Un benchmark multi-métrica reproducible:** Evalúa LIME, KernelSHAP, Anchors y DiCE sobre cinco familias de clasificadores. Demuestra la superioridad estadística de KernelSHAP en fidelidad y caracteriza la frontera de Pareto entre estabilidad y costo computacional.
3. **Una guía de ingeniería aplicada:** Formaliza umbrales cuantitativos, una matriz de decisión para despliegue y un flujo de auditoría en tres fases alineado con la Ley de IA de la UE y NIST AI RMF.

## Alcance, limitaciones y agenda futura

Reconociendo el alcance acotado del estudio experimental, se identifican dos líneas prioritarias de investigación:

* **Extensión a datos no estructurados y Modelos de Lenguaje (LLMs):** El benchmark se concentró en datos tabulares. Futuras investigaciones adaptarán FOM-7 a visión artificial y a modelos masivos de lenguaje (*Large Language Models*, LLMs), donde las perturbaciones en representaciones densas (*embeddings*) y los mecanismos de atención plantean nuevos retos de estabilidad.
* **Integración con estudios cognitivos (Niveles 1 y 2):** Este trabajo consolida la evaluación funcionalmente fundamentada de Nivel 3 (Doshi-Velez & Kim, 2017). Investigaciones posteriores vincularán las métricas de FOM-7 con pruebas de usabilidad y rendimiento con usuarios humanos en entornos clínicos y financieros.

## Reflexión final

La explicabilidad algorítmica no es un fin en sí misma. Es el instrumento técnico para asegurar que el aprendizaje automático opere bajo supervisión transparente, defendible y centrada en el ser humano. Al dotar a los equipos de ingeniería de un protocolo cuantitativo como **FOM-7**, este trabajo aporta una base sólida para transitar desde la opacidad algorítmica hacia una gobernanza verdaderamente responsable.
