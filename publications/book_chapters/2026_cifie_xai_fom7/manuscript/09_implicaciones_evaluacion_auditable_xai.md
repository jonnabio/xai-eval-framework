# Implicaciones para la evaluación auditable de XAI

## Del indicador aislado al perfil multi-dimensional

El principal aprendizaje del benchmark **FOM-7** para la ingeniería de datos es claro: **evaluar la explicabilidad mediante una sola métrica aislada constituye un fallo de diseño**. Ningún método post-hoc domina todas las dimensiones simultáneamente. La gobernanza de la IA exige definir **perfiles operacionales de desempeño** adaptados a cada escenario productivo.

Para un auditor bajo la Ley de IA de la UE, una explicación carece de validez legal si no acredita conjuntamente fidelidad (G1) y estabilidad (G2). Emitir atribuciones sin certificar estabilidad suficiente ($\ge 0.80$) expone al sistema a impugnaciones técnicas y legales.

## Flujo de Auditoría en Tres Fases para Pipelines de Producción

Para incorporar FOM-7 en entornos de MLOps y gobierno de datos, se establece un flujo estructurado en tres fases:

1. **Fase 1: Pre-certificación Estática en CI/CD (G1, G2, G3):**
   Durante la integración continua, el clasificador y su explicador deben superar los umbrales mínimos sobre datos de validación independientes. Se exige fidelidad $\ge 0.85$, estabilidad $\ge 0.80$ y parsimonia cognitiva ($\le 7$ variables dominantes).

2. **Fase 2: Eficiencia y Restricciones Operacionales (G4, G5):**
   Se verifica el cumplimiento de los SLAs de infraestructura ($\bar{T}_{exp} < 100\text{ ms}$ en servicios en línea). En contrafactuales (DiCE), se audita el respeto irrestricto a las máscaras de inmutabilidad sobre atributos protegidos.

3. **Fase 3: Auditoría Cruzada y Equidad en Producción (G6, G7):**
   Se programan tareas periódicas por lotes que contrastan pares de explicadores para alertar sobre divergencias de Rashomon (G6). Asimismo, se audita que la calidad explicativa mantenga paridad estadística entre subgrupos demográficos protegidos (G7).

## Alineamiento con la Ley de IA de la UE y el Marco NIST AI RMF

El protocolo FOM-7 aporta la base cuantitativa auditable exigida por la regulación internacional:

* **Ley de Inteligencia Artificial de la UE (Reglamento UE 2024/1689):**
  - *Artículo 13 (Transparencia):* Exige que los sistemas de alto riesgo sean interpretables. La Puerta G1 verifica matemáticamente la fidelidad de la aproximación.
  - *Artículo 14 (Supervisión humana):* Demanda supervisión efectiva (*Human-in-the-Loop*). Las Puertas G2 y G3 garantizan consistencia y parsimonia cognitiva.
  - *Artículo 86 (Derecho a explicación):* Otorga el derecho a justificaciones claras ante decisiones adversas. La Puerta G7 previene sesgos discriminatorios en la auditoría.
* **Marco NIST AI RMF 1.0:**
  - *Directriz Measure 1.3:* Requiere métricas formales y reproducibles de explicabilidad y confiabilidad.
  - *Directriz Govern 1.2:* Exige gobernanza técnica documentada. Mediante aserciones cuantitativas, FOM-7 traduce directrices abstractas en pruebas de software auditables.

## Recomendaciones prácticas para arquitectos de datos

1. **Umbral mínimo de fidelidad local (G1 $\ge 0.85$):** Rechazar en despliegue explicadores cuya fidelidad respecto a la caja negra sea inferior al $85\%$.
2. **Telemetría de explicabilidad en el Model Card (G5):** Registrar latencia media y consumo de memoria en la ficha técnica para dimensionar la infraestructura de inferencia.
3. **Arquitectura de explicación híbrida:** Emplear vectores de atribución (KernelSHAP) para auditoría técnica y ciencia de datos, combinados con contrafactuales prescriptivos (DiCE) en portales orientados al usuario final.
