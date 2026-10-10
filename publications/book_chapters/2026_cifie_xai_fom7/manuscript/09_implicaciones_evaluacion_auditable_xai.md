# Implicaciones para la evaluación auditable de XAI

## De la medición aislada al perfil de desempeño multi-dimensional

Los resultados cuantitativos obtenidos en el benchmark de **FOM-7** demuestran de manera irrefutable que evaluar la explicabilidad de un sistema de IA mediante una única métrica aislada constituye un fallo de diseño metodológico. Ningún explicador agnóstico dominante supera a sus competidores en todas las puertas del protocolo de forma simultánea. Por consiguiente, la gobernanza institucional de la IA debe evolucionar desde la búsqueda ilusoria de "el explicador perfecto" hacia la caracterización de **perfiles de desempeño multi-dimensionales** adaptados al contexto operativo específico de cada aplicación.

Para un organismo regulador o un auditor de sistemas de alto riesgo (según la clasificación de la Ley de IA de la UE), una explicación solo puede considerarse éticamente defendible si se acompañan sus métricas de fidelidad local (G1) y estabilidad (G2). Presentar un gráfico de atribución generado por LIME sin advertir que su estabilidad bajo perturbaciones es de apenas $0.724$ expone a la organización a severos riesgos de impugnación legal y pérdida de confianza pública.

## Protocolo de Auditoría en Tres Fases para Cumplimiento Normativo

Para operacionalizar el protocolo FOM-7 dentro de los marcos de gobernanza contemporáneos, se recomienda un flujo estructurado de auditoría en tres fases:

1. **Fase 1: Pre-certificación Estática (G1, G2, G3):** Antes de autorizar el pase a producción, se audita una muestra estratificada del conjunto de prueba. El modelo y su explicador asociado deben superar los umbrales mínimos de fidelidad ($\ge 0.85$), estabilidad ($\ge 0.80$) y parsimonia.
2. **Fase 2: Validación de Eficiencia y Accionabilidad (G4, G5):** Se certifica que la latencia media cumpla los Acuerdos de Nivel de Servicio (SLA) de la infraestructura operativa y que, en caso de denegación de servicios, se generen contrafactuales con variables legalmente accionables y restricciones de mutabilidad respetadas (DiCE).
3. **Fase 3: Auditoría Cruzada y No Discriminación (G6, G7):** Se ejecuta periódicamente una prueba de consistencia inter-método y se verifica que la fidelidad de las explicaciones no sufra degradación sistemática en subgrupos protegidos por motivos de género, raza o edad.

## Alineamiento con la Ley de IA de la Unión Europea y el Marco NIST AI RMF

La adopción de un protocolo computable como FOM-7 cobra relevancia inmediata ante las exigencias de los marcos normativos globales para inteligencia artificial:

* **Ley de IA de la Unión Europea (Reglamento UE 2024/1689):** El Artículo 13 impone la obligación de transparencia para sistemas de alto riesgo, exigiendo que las operaciones sean interpretables por los usuarios. Asimismo, el Artículo 14 exige mecanismos de supervisión humana efectiva (*Human-in-the-Loop*), mientras que el Artículo 86 consagra el derecho fundamental a recibir explicaciones claras y significativas sobre decisiones adversas. El protocolo FOM-7 aporta la base numérica requerida: la Puerta G1 verifica que la explicación represente con fidelidad el comportamiento del modelo (Art. 13), la Puerta G2 asegura la consistencia de las explicaciones evitando divergencias estocásticas arbitrarias (Art. 14), y la Puerta G7 garantiza la equidad explicativa entre subgrupos demográficos protegidos.
* **Marco de Gestión de Riesgos de IA del NIST (NIST AI RMF 1.0):** La subcategoría *Measure 1.3* exige métricas rigurosas y verificables para cuantificar la explicabilidad y confiabilidad de los componentes algorítmicos, mientras que *Govern 1.2* mandata procesos documentados de rendición de cuentas. Al formular umbrales numéricos reproducibles y verificables en código abierto, FOM-7 transforma directrices normativas abstractas en controles técnicos auditables.

## Recomendaciones prácticas para desarrolladores y auditores

Con base en la evidencia empírica acumulada en este capítulo, se proponen tres directrices de ingeniería para el despliegue responsable de XAI:
1. **Establecer un umbral mínimo de fidelidad (G1 > 0.85):** No autorizar el despliegue en producción de ningún explicador agnóstico cuya fidelidad reconstruida caiga por debajo del $85\%$ para el modelo predictivo en uso.
2. **Publicar la latencia computacional en la documentación técnica (G5):** Incluir la latencia media por explicación en la tarjeta de modelo (*Model Card*) o en la documentación de auditoría para evitar cuellos de botella en entornos operativos en tiempo real.
3. **Adoptar un enfoque híbrido de atribución y prescripción:** Combinar explicaciones de atribución continua de características (SHAP) para auditores técnicos con explicaciones contrafactuales diversas (DiCE) para usuarios finales afectados por la decisión algorítmica.
