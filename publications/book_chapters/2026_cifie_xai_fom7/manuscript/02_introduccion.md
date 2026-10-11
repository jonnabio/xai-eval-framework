# Introducción

## Del pipeline determinista a la opacidad algorítmica

En la ingeniería de datos clásica, la confiabilidad descansa en el determinismo y la trazabilidad. Al estructurar una canalización (*pipeline*) en SQL, Spark o dbt, cada transformación responde a reglas explícitas, contratos de esquema y pruebas de integridad referencial. Si una consulta falla, el equipo examina el plan de ejecución (`EXPLAIN ANALYZE`), audita el linaje de datos y aísla la causa raíz.

El aprendizaje automático altera este paradigma. Cuando el flujo culmina en un clasificador no lineal de alta dimensionalidad —como un ensamble XGBoost o una red neuronal densa—, la lógica predictiva se dispersa en millones de hiperplanos o matrices numéricas. La telemetría estándar rastrea indicadores agregados: latencia, deriva (*drift*) y métricas globales (AUC-ROC o exactitud).

Indican que el modelo acierta en el $88\%$ de los casos globales. Sin embargo, no aclaran el caso puntual: *¿por qué el registro 45,210 fue rechazado para un crédito o clasificado en alto riesgo médico?* (Barredo Arrieta *et al.*, 2020; Ali *et al.*, 2023). En este marco, la Inteligencia Artificial Explicable (*Explainable Artificial Intelligence*, XAI) aporta la **capa de observabilidad y depuración interna** indispensable para gobernar el sistema en producción.

Esta exigencia cobra fuerza legal bajo marcos como el GDPR europeo (Artículos 13–15 y 22) y la Ley de Inteligencia Artificial de la UE (*EU AI Act*, Reglamento UE 2024/1689, Artículos 13 y 14). Ambas normas exigen explicaciones comprensibles, reproducibles y no discriminatorias en decisiones automatizadas de alto impacto.

## El dilema de diseño: Modelos interpretables frente a explicaciones post-hoc

Antes de desplegar algoritmos de explicabilidad, conviene evaluar la advertencia epistemológica de Rudin (2019): ¿por qué entrenar un modelo opaco y aproximar su conducta con un método secundario, en vez de adoptar directamente un modelo intrínsecamente interpretable?

La objeción de Rudin plantea dos realidades técnicas:

1. Una explicación post-hoc constituye una **aproximación imperfecta** de la caja negra; de ser idéntica globalmente, el modelo original sería redundante.
2. En múltiples problemas con datos tabulares estructurados, una depurada ingeniería de características con modelos aditivos generalizados (GAMs) o árboles de decisión alcanza un rendimiento predictivo equivalente al de modelos opacos, eliminando la incertidumbre interpretativa.

Pese a ello, prescindir de modelos no lineales complejos no siempre resulta viable en la industria. Ante interacciones complejas de alto orden o grandes volúmenes de datos, los equipos optan por ensambles para maximizar la generalización. En ese contexto, la explicabilidad post-hoc opera como una **estrategia de auditoría y mitigación de riesgos**. El desafío de ingeniería radica en someter estas herramientas a pruebas cuantitativas rigurosas que certifiquen su fidelidad, estabilidad y reproducibilidad (Phillips *et al.*, 2021; Tabassi, 2023).

## El problema científico: La divergencia entre explicadores

La principal dificultad práctica surge de la falta de un protocolo formal para validar explicaciones. Al aplicar dos bibliotecas estándar —como LIME y KernelSHAP— sobre la misma instancia de un clasificador XGBoost, emergen con frecuencia jerarquías contradictorias. LIME puede atribuir el veredicto a la *Edad*, mientras que KernelSHAP prioriza el *Nivel Educativo* y relega la edad a un plano marginal.

Esta disparidad suscita preguntas fundamentales: ¿cuál aproximación refleja fielmente la frontera de decisión? ¿Cómo cuantificar la solidez de una explicación sin depender de inspecciones subjetivas?

La hipótesis de este trabajo sostiene que evaluar una explicación post-hoc requiere un **marco métrico concurrente**. Este marco debe ponderar su fidelidad local, su estabilidad ante perturbaciones estocásticas, su parsimonia cognitiva, su cobertura poblacional y su viabilidad computacional en producción.

## Hoja de ruta del capítulo

Para acompañar al lector técnico desde los fundamentos conceptuales hasta la certificación práctica, el capítulo se estructura en seis etapas:

1. **Fundamentos conceptuales (Sección 03):** Delimitación de transparencia, interpretabilidad y explicabilidad, distinguiendo atribución estadística de inferencia causal.
2. **Métodos agnósticos principales (Sección 04):** Lógica matemática, formulaciones y costo computacional de LIME, SHAP, Anchors y DiCE.
3. **La crisis de evaluación en XAI (Sección 05):** Efecto Rashomon, inestabilidad por muestreo y deformaciones fuera de distribución (*OOD*).
4. **El protocolo operativo FOM-7 (Sección 06):** Marco de siete puertas con métricas formales y umbrales de pase/fallo para auditoría técnica.
5. **Diseño empírico y benchmark (Secciones 07 y 08):** Evaluación empírica en *UCI Adult Income* comparando cinco clasificadores con 14 figuras y 2 tablas APA 7.
6. **Gobernanza e implicaciones (Secciones 09 y 10):** Matriz de decisión técnica, flujo de auditoría para la Ley de IA de la UE y agenda de investigación futura.
