# Introducción

## Del pipeline determinista a la opacidad algorítmica

En la práctica habitual de la ingeniería de datos y del desarrollo de software, la confiabilidad de los sistemas se sustenta en el determinismo y la trazabilidad. Cuando un ingeniero diseña una canalización de procesamiento (*pipeline*) en SQL, Spark o dbt, cada transformación obedece a reglas de negocio explícitas (`CASE WHEN ... THEN ...`), validaciones de esquema rigurosas y pruebas de integridad referencial. Si una consulta arroja un resultado inesperado, el profesional examina el plan de ejecución (`EXPLAIN ANALYZE`), inspecciona el linaje de datos (*data lineage*) y depura las funciones paso a paso hasta aislar la causa raíz.

Sin embargo, la adopción masiva del aprendizaje automático (*machine learning*) ha transformado este paradigma. Cuando una canalización culmina en un clasificador no lineal de alta dimensionalidad —como un ensamble de *gradient boosting* (XGBoost) o una red neuronal profunda—, la lógica de decisión deja de residir en un conjunto legible de instrucciones de código para codificarse en millones de hiperplanos o en matrices densas de parámetros matemáticos. Las herramientas estándar de monitorización de infraestructura (tales como Prometheus, Grafana, Evidently o DataDog) permiten rastrear métricas agregadas del sistema: latencia de inferencia, rendimiento (*throughput*), deriva de datos (*data drift*) y métricas macroscópicas de desempeño estadístico como el área bajo la curva ROC (AUC-ROC), la exactitud (*accuracy*) o el F1-score.

El problema fundamental radica en que estas métricas globales son **ciegas a las decisiones individuales**. Indican que el modelo acierta en el $88\%$ de los casos sobre el conjunto de prueba, pero son incapaces de responder a la pregunta que formula el usuario final, el oficial de cumplimiento o el equipo de soporte técnico: *¿Por qué el registro número 45,210 fue rechazado para este crédito hipotecario o clasificado como paciente de alto riesgo?* (Barredo Arrieta *et al.*, 2020; Ali *et al.*, 2023). En este escenario, la Inteligencia Artificial Explicable (*Explainable Artificial Intelligence*, XAI) no es un lujo teórico ni un aditamento cosmético: constituye la **capa de observabilidad y depuración de la lógica interna del modelo**, indispensable para que un sistema en producción sea verdaderamente gobernable y auditable.

Esta exigencia ha cobrado urgencia legal inmediata ante la consolidación de marcos normativos internacionales como el Reglamento General de Protección de Datos de la Unión Europea (GDPR, Artículos 13 a 15 y 22) y la Ley de Inteligencia Artificial de la UE (*EU AI Act*, Reglamento UE 2024/1689, Artículos 13 y 14), los cuales consagran el derecho de los ciudadanos a recibir explicaciones claras, significativas y no discriminatorias ante decisiones automatizadas de alto impacto.

## El dilema de diseño: Modelos interpretables frente a explicaciones post-hoc

Antes de examinar los algoritmos de explicabilidad, cualquier profesional de datos debe enfrentarse a un dilema fundamental formulado con agudeza por Rudin (2019): ¿por qué entrenar un modelo complejo de caja negra y luego intentar adivinar su comportamiento mediante una explicación aproximada, en lugar de utilizar directamente un modelo intrínsecamente interpretable por diseño?

La advertencia de Rudin es de enorme relevancia técnica:
1. Una explicación secundaria post-hoc es, por definición matemática, una **aproximación imperfecta** de la caja negra; si fuese un sustituto idéntico en todo el dominio de datos, no necesitaríamos la caja negra original.
2. En múltiples problemas con datos tabulares estructurados, una cuidadosa ingeniería de características combinada con modelos aditivos generalizados (*Generalized Additive Models*, GAMs) o árboles de decisión restringidos puede alcanzar un desempeño predictivo comparable al de modelos opacos, eliminando por completo la incertidumbre de la explicación.

No obstante, en la realidad de la ingeniería de software y analítica avanzada, prescindir de modelos complejos no siempre es viable. Existen dominios donde las interacciones no lineales de alto orden entre cientos de variables continuas y categóricas, el volumen masivo de datos o el uso de arquitecturas preentrenadas imponen el despliegue de ensambles avanzados para no degradar la precisión predictiva. Es exactamente en este punto donde la explicabilidad post-hoc se convierte en una **herramienta indispensable de auditoría y reducción de daños**. El objetivo no es asumir que la explicación post-hoc es una verdad absoluta, sino someterla a pruebas empíricas rigurosas para certificar si la aproximación es suficientemente fiel, estable y reproducible para ser defendida ante un regulador o un cliente (Phillips *et al.*, 2021; Tabassi, 2023).

## El problema científico: La divergencia entre explicadores

El núcleo del desafío que enfrenta un equipo de ingeniería radica en la ausencia histórica de estándares de prueba cuantitativos para las explicaciones. Cuando un desarrollador toma una instancia problemática y ejecuta dos de las bibliotecas de explicabilidad más populares de la industria —por ejemplo, LIME y KernelSHAP—, se encuentra con frecuencia ante un resultado desconcertante: LIME señala que la variable más influyente para la decisión fue la *Edad*, mientras que KernelSHAP afirma que fue el *Nivel Educativo*, asignando a la *Edad* un peso marginal.

Frente a esta contradicción directa, surge el problema científico: ¿cuál de los explicadores refleja con mayor fidelidad la frontera de decisión del clasificador? ¿Cómo medir la calidad de un artefacto explicativo sin depender de la apreciación intuitiva o del sesgo de confirmación del analista?

La hipótesis que articula este trabajo sostiene que la calidad de una explicación post-hoc no es una propiedad unidimensional ni reducible a un solo indicador estático. La confiabilidad de una explicación exige una **evaluación multi-métrica y holística** que pondere de manera concurrente:
* La **fidelidad local** de la reconstrucción con respecto al modelo primario.
* La **estabilidad estocástica** ante perturbaciones leves en las entradas y variaciones de semillas.
* La **parsimonia cognitiva** o legibilidad humana del artefacto generado.
* La **cobertura operacional** de las reglas dentro de la población de datos.
* La **eficiencia computacional** (latencia y consumo de memoria) necesaria para su integración en pipelines de inferencia por lotes o en tiempo real.

## Hoja de ruta del capítulo

Para guiar al lector técnico desde los fundamentos conceptuales hasta la implementación de pruebas operativas en producción, el capítulo se organiza de la siguiente manera:

1. **Fundamentos conceptuales (Sección 03):** Se deslindan con rigor los términos transparencia, interpretabilidad y explicabilidad, y se aclara la diferencia fundamental entre atribución estadística y causalidad en datos tabulares.
2. **Métodos agnósticos principales (Sección 04):** Se examinan los mecanismos internos, la intuición algorítmica y los costos computacionales de LIME, SHAP, Anchors y DiCE.
3. **La crisis de evaluación en XAI (Sección 05):** Se analizan las fallas operacionales de los explicadores: el efecto Rashomon, la inestabilidad por muestreo aleatorio y el riesgo de muestras fuera de distribución (*OOD*).
4. **El protocolo operativo FOM-7 (Sección 06):** Se introduce formalmente el marco de siete puertas (*Framework for Operational Metrics in 7 Gates*), con sus ecuaciones formales y umbrales de pase/fallo para auditoría industrial.
5. **Diseño empírico y banco de pruebas (Secciones 07 y 08):** Se detalla el benchmark experimental sobre el dataset *UCI Adult Income* comparando cinco familias de clasificadores mediante 10 figuras descriptivas y 2 tablas normalizadas APA 7.
6. **Implicaciones operacionales y gobernanza (Secciones 09 y 10):** Se propone una matriz de decisión para ingenieros de despliegue, un flujo de auditoría en tres fases alineado con la Ley de IA de la UE y se sintetiza la agenda de trabajo futuro.
