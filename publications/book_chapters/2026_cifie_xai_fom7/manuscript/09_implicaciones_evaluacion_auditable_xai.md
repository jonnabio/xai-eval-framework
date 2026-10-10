# Implicaciones para la evaluación auditable de XAI

## Del indicador aislado al perfil multi-dimensional

El principal aprendizaje que arroja el benchmark de **FOM-7** para la práctica de la ingeniería de datos es que **evaluar la explicabilidad mediante una sola métrica aislada constituye un error de diseño de sistemas**. Ningún algoritmo agnóstico post-hoc supera a sus alternativas en todas las dimensiones del protocolo de manera concurrente. La gobernanza de la IA debe abandonar la pretensión de encontrar "el explicador perfecto" y avanzar hacia la definición de **perfiles operacionales de desempeño** alineados con los requerimientos específicos de cada caso de uso.

Para un oficial de cumplimiento o un auditor de sistemas de alto riesgo (según las directrices de la Ley de IA de la UE), una explicación carece de validez legal si no se presentan conjuntamente su fidelidad local (G1) y su estabilidad ante ruido (G2). Entregar un reporte de atribución sin verificar que su estabilidad bajo perturbaciones alcanza al menos $0.80$ expone a la organización a severos riesgos de impugnación y pérdida de confianza pública.

## Flujo de Auditoría en Tres Fases para Pipelines de Producción

Para incorporar el protocolo FOM-7 dentro de las prácticas estándar de MLOps y gobierno del dato, se recomienda un flujo estructurado de auditoría en tres fases:

```
[Fase 1: Pre-certificación Estática] ---> [Fase 2: Validación de SLAs] ---> [Fase 3: Auditoría Cruzada Continua]
   - Test de Fidelidad (G1 >= 0.85)          - Benchmarking de Latencia (G5)   - Consistencia Inter-método (G6)
   - Test de Estabilidad (G2 >= 0.80)        - Validación de Mutabilidad (G4)  - Paridad Demográfica (G7)
```

1. **Fase 1: Pre-certificación Estática en CI/CD (G1, G2, G3):**
   Antes de autorizar el paso a producción de un nuevo modelo o explicador, se ejecuta una suite de pruebas automatizadas sobre una muestra reservada del conjunto de validación. El componente debe superar obligatoriamente los umbrales de fidelidad ($\text{Fidelidad} \ge 0.85$), estabilidad ($\text{Estabilidad} \ge 0.80$) y parsimonia cognitiva ($\le 7$ variables dominantes).
2. **Fase 2: Validación de Eficiencia y Restricciones Operativas (G4, G5):**
   Se certifica en el entorno de pruebas de carga que la latencia media $\bar{T}_{exp}$ cumpla con los SLAs de la infraestructura (por ejemplo, $<100\text{ ms}$ para servicios síncronos). En aplicaciones que requieran explicaciones contrafactuales (DiCE), se verifica que las modificaciones sugeridas respeten estrictamente las máscaras de inmutabilidad (impidiendo cambios en variables no modificables).
3. **Fase 3: Auditoría Cruzada y No Discriminación en Producción (G6, G7):**
   Se programan tareas periódicas de auditoría por lotes que comparan las salidas de dos explicadores distintos para detectar posibles divergencias de Rashomon (G6), y se verifica que la fidelidad y la estabilidad de las explicaciones no sufran degradaciones sistemáticas en subgrupos poblacionales protegidos por motivos de género, etnia o edad (G7).

## Alineamiento con la Ley de IA de la UE y el Marco NIST AI RMF

La formalización de un protocolo computable como FOM-7 adquiere relevancia directa ante los marcos regulatorios internacionales vigentes:

* **Ley de Inteligencia Artificial de la Unión Europea (Reglamento UE 2024/1689):**
  - *Artículo 13 (Transparencia):* Exige que los sistemas de alto riesgo permitan a los usuarios interpretar sus salidas. La Puerta G1 de FOM-7 valida matemáticamente que la explicación represente fielmente la decisión del modelo.
  - *Artículo 14 (Supervisión humana):* Demanda que los sistemas cuenten con interfaces que permitan una supervisión efectiva (*Human-in-the-Loop*). Las Puertas G2 y G3 aseguran que las explicaciones sean consistentes entre consultas y presenten una carga cognitiva manejable.
  - *Artículo 86 (Derecho a explicación):* Reconoce el derecho de los ciudadanos a recibir explicaciones claras sobre decisiones automatizadas adversas. La Puerta G7 garantiza que este derecho se cumpla de forma equitativa y sin sesgos demográficos en la calidad de la respuesta.
* **Marco de Gestión de Riesgos de IA de NIST (NIST AI RMF 1.0):**
  - La directriz *Measure 1.3* exige métricas formales y verificables para medir la explicabilidad y confiabilidad algorítmica.
  - La directriz *Govern 1.2* mandata procesos documentados y reproducibles de supervisión técnica. Al formular aserciones numéricas en código abierto, FOM-7 transforma directrices normativas cualitativas en controles de ingeniería auditables.

## Recomendaciones prácticas para desarrolladores y arquitectos de datos

Con base en la experiencia empírica acumulada en este trabajo, proponemos tres directrices directas para los equipos de ingeniería de datos:
1. **Establecer un umbral mínimo de fidelidad local (G1 > 0.85):** Nunca autorizar el uso de un explicador agnóstico en producción si su fidelidad reconstruida respecto al clasificador cae por debajo del $85\%$.
2. **Documentar la latencia de explicación en el Model Card (G5):** Registrar la latencia media por inferencia y el consumo de memoria en la ficha técnica del modelo para evitar colapsos de concurrencia en producción.
3. **Adoptar una arquitectura híbrida de explicación:** Desplegar explicaciones continuas de atribución (KernelSHAP) para los equipos de ciencia de datos y auditoría interna, combinadas con explicaciones prescriptivas contrafactuales (DiCE) en las interfaces orientadas al cliente o usuario final.
