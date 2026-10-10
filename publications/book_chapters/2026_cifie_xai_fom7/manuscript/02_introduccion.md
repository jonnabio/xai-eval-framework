# Introducción

## Del pipeline determinista a la opacidad algorítmica

En la ingeniería de datos y el desarrollo de software, la confiabilidad de los sistemas descansa en el determinismo y la trazabilidad. Al diseñar una canalización de procesamiento (*pipeline*) en SQL, Spark o dbt, cada transformación responde a reglas de negocio explícitas (`CASE WHEN ... THEN ...`), contratos de esquema rigurosos y pruebas de integridad referencial. Si una consulta devuelve un resultado anómalo, el equipo inspecciona el plan de ejecución (`EXPLAIN ANALYZE`), audita el linaje de datos y depura el código hasta aislar la causa raíz.

La integración de modelos de aprendizaje automático altera radicalmente este paradigma. Cuando una canalización culmina en un clasificador no lineal de alta dimensionalidad —como un ensamble de *gradient boosting* (XGBoost) o una red neuronal profunda—, la lógica de decisión deja de residir en instrucciones de código legibles para distribuirse en millones de hiperplanos o matrices densas de parámetros. Las herramientas habituales de telemetría (Prometheus, Grafana, Evidently o DataDog) monitorizan métricas macroscópicas: latencia de inferencia, rendimiento (*throughput*), deriva de datos (*data drift*) y métricas estadísticas agregadas como exactitud (*accuracy*) o AUC-ROC.

El problema fundamental es que estos indicadores globales son **ciegos a las decisiones individuales**. Indican que el modelo acierta en el $88\%$ de los casos, pero no responden al interrogante que formula un cliente, un analista o un oficial de cumplimiento: *¿Por qué el registro número 45,210 fue rechazado para este crédito o catalogado como paciente de alto riesgo?* (Barredo Arrieta *et al.*, 2020; Ali *et al.*, 2023). En este contexto, la Inteligencia Artificial Explicable (*Explainable Artificial Intelligence*, XAI) constituye la **capa de observabilidad y depuración de la lógica interna del modelo**, necesaria para hacer gobernable y auditable un sistema en producción.

Esta necesidad se ha consolidado en mandatos jurídicos vinculantes, tales como el Reglamento General de Protección de Datos de la Unión Europea (GDPR, Artículos 13 a 15 y 22) y la Ley de Inteligencia Artificial de la UE (*EU AI Act*, Reglamento UE 2024/1689, Artículos 13 y 14), que exigen explicaciones claras, significativas y no discriminatorias ante decisiones automatizadas de alto impacto.

## El dilema de diseño: Modelos interpretables frente a explicaciones post-hoc

Antes de examinar los algoritmos de explicabilidad, es indispensable confrontar el dilema epistemológico formulado por Rudin (2019): ¿por qué entrenar un modelo complejo de caja negra y aproximar su comportamiento mediante una explicación secundaria, en lugar de utilizar directamente un modelo intrínsecamente interpretable por diseño?

La advertencia de Rudin es de gran relevancia para la ingeniería:
1. Una explicación post-hoc es, por definición matemática, una **aproximación imperfecta** de la caja negra; si fuese idéntica en todo el dominio de datos, la caja negra original resultaría superflua.
2. En múltiples problemas con datos tabulares estructurados, una cuidadosa ingeniería de características combinada con modelos aditivos generalizados (GAMs) o árboles de baja profundidad alcanza un desempeño predictivo equiparable al de modelos opacos, eliminando la incertidumbre de la explicación.

No obstante, en entornos industriales complejos, prescindir de modelos no lineales avanzados no siempre es factible. En presencia de interacciones de muy alto orden, grandes volúmenes de datos o arquitecturas preentrenadas, las organizaciones despliegan ensambles complejos para maximizar la generalización. En ese escenario, la explicabilidad post-hoc opera como una **herramienta de auditoría y reducción de daños**. El reto de ingeniería no radica en confiar ciegamente en estas explicaciones, sino en someterlas a pruebas cuantitativas rigurosas para certificar si la aproximación es suficientemente fiel, estable y reproducible (Phillips *et al.*, 2021; Tabassi, 2023).

## El problema científico: La divergencia entre explicadores

El núcleo del desafío radica en la ausencia histórica de un protocolo estandarizado de prueba para las explicaciones. Cuando un ingeniero aplica dos de las bibliotecas más consolidadas —como LIME y KernelSHAP— sobre la misma instancia de un modelo XGBoost, con frecuencia obtiene jerarquías de importancia contradictorias: LIME puede atribuir el veredicto a la *Edad*, mientras que KernelSHAP señala al *Nivel Educativo*, asignando a la *Edad* un peso residual.

Ante esta discrepancia, surge la pregunta central: ¿cuál de los explicadores reproduce con mayor fidelidad la frontera de decisión del clasificador? ¿Cómo medir la calidad de un artefacto explicativo sin depender de intuiciones subjetivas?

La hipótesis de este trabajo sostiene que la confiabilidad de una explicación post-hoc requiere una **evaluación multi-métrica concurrente** que pondere su fidelidad local respecto al modelo, su estabilidad ante ruido y variaciones de semillas, su parsimonia cognitiva, su cobertura poblacional y su viabilidad computacional para su despliegue en producción.

## Hoja de ruta del capítulo

Para acompañar al lector técnico desde los fundamentos conceptuales hasta la implementación de pruebas operativas, este capítulo se estructura en seis etapas:

1. **Fundamentos conceptuales (Sección 03):** Se delimitan los conceptos de transparencia, interpretabilidad y explicabilidad, y se distingue la atribución estadística de la inferencia causal en datos tabulares.
2. **Métodos agnósticos principales (Sección 04):** Se exponen la lógica algorítmica, las formulaciones matemáticas y las restricciones computacionales de LIME, SHAP, Anchors y DiCE.
3. **La crisis de evaluación en XAI (Sección 05):** Se analizan las fallas operacionales de los explicadores: el efecto Rashomon, la inestabilidad por muestreo aleatorio y la deformación por datos fuera de distribución (*OOD*).
4. **El protocolo operativo FOM-7 (Sección 06):** Se introduce formalmente el marco de siete puertas (*Framework for Operational Metrics in 7 Gates*), con sus ecuaciones cuantitativas y umbrales de pase/fallo para auditoría industrial.
5. **Diseño empírico y benchmark (Secciones 07 y 08):** Se detalla la evaluación experimental sobre el dataset *UCI Adult Income* comparando cinco familias de clasificadores mediante 10 figuras y 2 tablas normalizadas APA 7.
6. **Implicaciones operacionales y gobernanza (Secciones 09 y 10):** Se propone una matriz de decisión para ingenieros, un flujo de auditoría en tres fases alineado con la Ley de IA de la UE y se sintetiza la agenda de trabajo futuro.
