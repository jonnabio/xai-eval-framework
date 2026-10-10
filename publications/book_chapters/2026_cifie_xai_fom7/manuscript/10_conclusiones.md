# Conclusiones

## Síntesis de aportaciones

Este capítulo ha demostrado que la explicabilidad algorítmica representa la **capa de observabilidad indispensable** para auditar y gobernar modelos complejos en entornos de alta responsabilidad.

A través del protocolo **FOM-7** y de su validación empírica en *UCI Adult Income*, este trabajo aporta:
1. **Un marco conceptual desmitificado:** Se establecieron fronteras operacionales nítidas entre transparencia, interpretabilidad intrínseca y explicabilidad post-hoc, deslindando la atribución estadística de la causalidad real en bases de datos.
2. **Un benchmark multi-métrica y reproducible:** Se caracterizaron cuantitativamente las fortalezas y compromisos de LIME, KernelSHAP, Anchors y DiCE sobre cinco familias de clasificadores, demostrando estadísticamente la superioridad de KernelSHAP en fidelidad y caracterizando la frontera de Pareto entre estabilidad y costo computacional.
3. **Una guía de ingeniería aplicada:** Se formalizaron umbrales numéricos de aprobación, una matriz de decisión para la selección de explicadores y un flujo de auditoría en tres fases alineado con la Ley de IA de la UE y el marco NIST AI RMF.

## Alcance, limitaciones y agenda futura

Reconociendo el alcance acotado de todo estudio experimental riguroso, identificamos las principales limitaciones del presente trabajo y las líneas de desarrollo prioritarias:

* **Extensión a datos no estructurados y Modelos de Lenguaje (LLMs):** El benchmark se focalizó en datos tabulares estructurados. Las investigaciones futuras adaptarán las ecuaciones de FOM-7 a visión por computadora y a modelos masivos de lenguaje (*Large Language Models*, LLMs), donde las perturbaciones semánticas en incrustaciones (*embeddings*) y los mecanismos de atención plantean nuevos desafíos de estabilidad y latencia.
* **Integración con estudios de cognición humana (Niveles 1 y 2):** Tras consolidar la evaluación funcionalmente fundamentada de Nivel 3 en la jerarquía de Doshi-Velez y Kim (2017), los trabajos siguientes vincularán las métricas de FOM-7 con pruebas de usabilidad y comprensión cognitiva con operadores humanos en entornos clínicos y financieros.

## Reflexión final

La explicabilidad algorítmica no es un fin en sí misma: es el instrumento técnico para asegurar que el poder analítico del aprendizaje automático opere bajo supervisión transparente, defendible y centrada en el ser humano. Al dotar a los equipos de ingeniería de un protocolo computable y fundamentado como **FOM-7**, este capítulo aporta una base práctica para transitar desde la opacidad de los algoritmos hacia una supervisión verdaderamente responsable.
