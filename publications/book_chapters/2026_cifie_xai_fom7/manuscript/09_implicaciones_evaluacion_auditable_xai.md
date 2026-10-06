# Implicaciones para la evaluación auditable de XAI

## De la medición aislada al perfil de desempeño multi-dimensional

Los resultados cuantitativos obtenidos en el benchmark de **FOM-7** demuestran de manera irrefutable que evaluar la explicabilidad de un sistema de IA mediante una única métrica aislada constituye un fallo de diseño metodológico. Ningún explicador agnóstico dominante supera a sus competidores en todas las puertas del protocolo de forma simultánea. Por consiguiente, la gobernanza institucional de la IA debe evolucionar desde la búsqueda ilusoria de "el explicador perfecto" hacia la caracterización de **perfiles de desempeño multi-dimensionales** adaptados al contexto operativo específico de cada aplicación.

Para un organismo regulador o un auditor de sistemas de alto riesgo (según la clasificación de la Ley de IA de la UE), una explicación solo puede considerarse éticamente defendible si se acompañan sus métricas de fidelidad local (G1) y estabilidad (G2). Presentar un gráfico de atribución generado por LIME sin advertir que su estabilidad bajo perturbaciones es de apenas $0.724$ expone a la organización a severos riesgos de impugnación legal y pérdida de confianza pública.

## Recomendaciones prácticas para desarrolladores y auditores

Con base en la evidencia empírica acumulada en este capítulo, se proponen tres recomendaciones metodológicas para la práctica profesional en ingeniería de XAI:

1. **Establecer un umbral mínimo de fidelidad (G1 > 0.85):** No autorizar el despliegue en producción de ningún explicador agnóstico cuya fidelidad reconstruida caiga por debajo del $85\%$ para el modelo predictivo en uso.
2. **Publicar la latencia computacional en la documentación técnica (G5):** Incluir la latencia media por explicación en la tarjeta de modelo (*Model Card*) o en la documentación de auditoría para evitar cuellos de botella en entornos operativos en tiempo real.
3. **Adoptar un enfoque híbrido de atribución y prescripción:** Combinar explicaciones de atribución continua de características (SHAP) para auditores técnicos con explicaciones contrafactuales diversas (DiCE) para usuarios finales afectados por la decisión algorítmica.

## Integración con marcos normativos e internacionales

El protocolo FOM-7 proporciona una implementación computacional concreta que responde directamente a las directrices del Marco de Gestión de Riesgos de IA del NIST (*NIST AI RMF 1.0*) y a los mandatos de auditabilidad previstos en los artículos 13 y 14 de la Ley de IA de la Unión Europea. Al estructurar la auditoría en siete puertas cuantificables, FOM-7 ofrece una evidencia objetiva, trazable y reproducible que permite a las organizaciones certificar el cumplimiento normativo de sus desarrollos algorítmicos.
