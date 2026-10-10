# Conclusiones

## Síntesis de aportaciones

El desarrollo de este capítulo ha demostrado que la explicabilidad algorítmica no puede seguir considerándose un módulo cosmético ni una caja de herramientas de uso ciego. Para un ingeniero de datos o un profesional de la tecnología, XAI representa la **capa de observabilidad indispensable** para auditar y gobernar modelos opacos en entornos de alta responsabilidad.

A través del protocolo **FOM-7** y de su validación empírica en el conjunto de datos *UCI Adult Income*, este trabajo aporta:
1. **Un marco conceptual desmitificado:** Se establecieron fronteras nítidas entre transparencia de código, interpretabilidad intrínseca y explicabilidad post-hoc, deslindando la atribución estadística de la causalidad real en bases de datos.
2. **Un banco de pruebas multi-métrica y reproducible:** Se demostraron las fortalezas y debilidades de LIME, KernelSHAP, Anchors y DiCE sobre cinco familias de modelos, probando estadísticamente la superioridad de KernelSHAP en fidelidad y caracterizando la frontera de Pareto entre estabilidad y costo computacional.
3. **Una guía de ingeniería aplicada:** Se formalizaron umbrales de validez numérica, una matriz de decisión para la selección de explicadores y un flujo de auditoría en tres fases alineado con los marcos regulatorios internacionales (Ley de IA de la UE y NIST AI RMF).

## Alcance, limitaciones y agenda de investigación futura

Reconociendo el alcance acotado de todo estudio experimental riguroso, identificamos las principales limitaciones del trabajo actual y las líneas de desarrollo prioritarias:

* **Extensión a datos no estructurados y Modelos de Lenguaje (LLMs):** El benchmark presentado se concentró en datos tabulares estructurados. La agenda futura adaptará las ecuaciones de las siete puertas de FOM-7 a modalidades de visión por computadora y a modelos masivos de lenguaje (*Large Language Models*, LLMs), donde las perturbaciones semánticas en incrustaciones (*embeddings*) y los mecanismos de atención plantean nuevos desafíos de estabilidad y costo de inferencia.
* **Integración con estudios de cognición humana (Niveles 1 y 2):** Habiendo consolidado la evaluación funcionalmente fundamentada de Nivel 3 en la jerarquía de Doshi-Velez y Kim (2017), los trabajos siguientes vincularán las métricas matemáticas de FOM-7 con pruebas de usabilidad y comprensión cognitiva real con operadores humanos en entornos de decisión clínica y financiera.

## Reflexión final

La explicabilidad algorítmica no es un fin en sí misma: es un medio técnico para garantizar que el inmenso poder analítico del aprendizaje automático permanezca al servicio de decisiones transparentes, justas y auditables. Al dotar a la comunidad de ingeniería de un protocolo computable, riguroso y fundamentado como **FOM-7**, este capítulo busca facilitar el tránsito desde la opacidad de los algoritmos hacia una supervisión verdaderamente defendible y centrada en el ser humano.
