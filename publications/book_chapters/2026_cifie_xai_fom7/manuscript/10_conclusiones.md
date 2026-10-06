# Conclusiones

## Síntesis de hallazgos y contribuciones principales

Este capítulo ha desarrollado un marco riguroso, pedagógico y empíricamente fundamentado para abordar la evaluación de la Inteligencia Artificial Explicable. A lo largo del documento, se ha construido una narrativa progresiva que parte desde la clarificación conceptual de los fundamentos de la XAI hasta la formulación e implementación del protocolo operativo **FOM-7**.

Las contribuciones centrales de este trabajo se sintetizan en tres aportes clave:
1. **Unificación pedagógica y conceptual:** Se ha proporcionado un marco analítico accesible que distingue la transparencia de la explicabilidad y expone de forma clara la formulación intuitiva y matemática de LIME, SHAP, Anchors y DiCE.
2. **El protocolo operativo FOM-7:** Se ha presentado un estándar de auditoría estructurado en siete puertas cuantitativas que resuelve la crisis de evaluación en XAI al medir de manera independiente la fidelidad, estabilidad, parsimonia, cobertura, eficiencia, consistencia y equidad.
3. **Evidencia empírica y perfiles de uso:** Mediante un benchmark riguroso sobre *UCI Adult Income* evaluando cinco familias de modelos, se ha caracterizado empíricamente la Frontera de Pareto entre estabilidad y costo computacional, entregando una guía de selección orientada al riesgo.

## Alcance y compromisos de trabajo futuro

Reconociendo el alcance acotado de todo estudio científico, se resumen a continuación las principales limitaciones del presente trabajo y los compromisos de investigación futura:

* **Ampliación a modalidades de datos no estructurados:** El benchmark presentado se restringió a datos tabulares estructurados. Las investigaciones futuras extenderán las ecuaciones de las siete puertas de FOM-7 hacia arquitecturas de visión por computador (imágenes médicas y de diagnóstico) y modelos de lenguaje de gran escala (LLMs), donde las perturbaciones espaciales y semánticas plantean nuevos desafíos analíticos.
* **Integración con estudios de interpretabilidad humana:** Aunque FOM-7 proporciona una evaluación funcionalmente fundamentada de Nivel 3 en la taxonomía de Doshi-Velez y Kim (2017), el trabajo futuro integrará las métricas computacionales con experimentos de laboratorio con usuarios de Nivel 2 y Nivel 1, midiendo la comprensión cognitiva efectiva de operadores humanos ante explicaciones auditadas por FOM-7.

## Reflexión final

La explicabilidad no puede continuar tratándose como un parche cosmetico o un módulo accesorio que se añade a posteriori sobre una caja negra predictiva. La explicabilidad representa una dimensión estructural de la seguridad, la gobernanza y la justicia algorítmica. Al dotar a la comunidad académica e industrial de un protocolo computable y auditable como **FOM-7**, este capítulo busca aportar una guía sólida para transitar desde la confianza ciega en las decisiones automatizadas hacia una supervisión transparente, defendible y verdaderamente centrada en el ser humano.
