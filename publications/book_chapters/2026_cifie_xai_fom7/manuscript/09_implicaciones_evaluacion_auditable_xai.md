# Implicaciones para la evaluación auditable de XAI

## Del indicador aislado al perfil multi-dimensional

El principal aprendizaje del benchmark de **FOM-7** para la ingeniería de datos es que **evaluar la explicabilidad mediante una sola métrica aislada constituye un fallo de diseño de sistemas**. Ningún algoritmo post-hoc supera a sus alternativas en todas las dimensiones de forma concurrente. La gobernanza de la IA debe avanzar hacia la definición de **perfiles operacionales de desempeño** adaptados a cada caso de uso.

Para un oficial de cumplimiento o un auditor de sistemas de alto riesgo (según la Ley de IA de la UE), una explicación carece de validez legal si no se acreditan conjuntamente su fidelidad local (G1) y su estabilidad ante perturbaciones (G2). Entregar un reporte de atribución sin verificar estabilidad suficiente ($\ge 0.80$) expone a la organización a severos riesgos de impugnación legal.

## Flujo de Auditoría en Tres Fases para Pipelines de Producción

Para incorporar el protocolo FOM-7 dentro de las prácticas de MLOps y gobierno del dato, se recomienda un flujo estructurado de auditoría en tres fases:

1. **Fase 1: Pre-certificación Estática en CI/CD (G1, G2, G3):**
   En la fase de pruebas automatizadas previas al despliegue, el modelo y su explicador deben superar los umbrales de fidelidad ($\text{Fidelidad} \ge 0.85$), estabilidad ($\text{Estabilidad} \ge 0.80$) y parsimonia cognitiva ($\le 7$ variables dominantes) sobre un conjunto de validación reservado.
2. **Fase 2: Validación de Eficiencia y Restricciones Operativas (G4, G5):**
   Se certifica que la latencia media $\bar{T}_{exp}$ cumpla con los SLAs de la infraestructura (por ejemplo, $<100\text{ ms}$ para servicios síncronos). En explicaciones contrafactuales (DiCE), se verifica que las modificaciones prescritas respeten estrictamente las máscaras de inmutabilidad (impidiendo alteraciones en variables protegidas o no modificables).
3. **Fase 3: Auditoría Cruzada y No Discriminación en Producción (G6, G7):**
   Se ejecutan tareas periódicas por lotes que comparan las salidas de dos explicadores para detectar divergencias de Rashomon (G6), y se comprueba que la fidelidad y la estabilidad de las explicaciones no sufran degradaciones sistemáticas en subgrupos demográficos protegidos (G7).

## Alineamiento con la Ley de IA de la UE y el Marco NIST AI RMF

El protocolo FOM-7 aporta la base técnica auditable requerida por los marcos regulatorios internacionales:

* **Ley de Inteligencia Artificial de la UE (Reglamento UE 2024/1689):**
  - *Artículo 13 (Transparencia):* Exige que los sistemas de alto riesgo permitan a los usuarios interpretar sus salidas. La Puerta G1 valida matemáticamente que la explicación refleje con fidelidad las decisiones del modelo.
  - *Artículo 14 (Supervisión humana):* Demanda mecanismos de supervisión efectiva (*Human-in-the-Loop*). Las Puertas G2 y G3 aseguran que las explicaciones sean consistentes entre consultas y presenten una carga cognitiva manejable.
  - *Artículo 86 (Derecho a explicación):* Consagra el derecho a recibir justificaciones claras sobre decisiones automatizadas adversas. La Puerta G7 garantiza que este derecho se cumpla sin sesgos demográficos en la calidad de la respuesta.
* **Marco de Gestión de Riesgos de IA de NIST (NIST AI RMF 1.0):**
  - Directriz *Measure 1.3*: Exige métricas formales y verificables para cuantificar la explicabilidad y confiabilidad algorítmica.
  - Directriz *Govern 1.2*: Mandata procesos documentados y reproducibles de supervisión técnica. Al formular aserciones numéricas en código abierto, FOM-7 transforma directrices normativas cualitativas en controles de ingeniería auditables.

## Recomendaciones prácticas para arquitectos de datos

1. **Establecer un umbral mínimo de fidelidad local (G1 > 0.85):** No desplegar ningún explicador agnóstico en producción cuya fidelidad reconstruida respecto al clasificador caiga por debajo del $85\%$.
2. **Documentar la latencia de explicación en el Model Card (G5):** Registrar la latencia media por inferencia y el consumo de memoria en la ficha técnica del modelo para dimensionar adecuadamente la infraestructura de servicio.
3. **Adoptar una arquitectura híbrida de explicación:** Desplegar explicaciones de atribución (KernelSHAP) para ciencia de datos y auditoría interna, combinadas con explicaciones prescriptivas contrafactuales (DiCE) en las interfaces orientadas al usuario final.
