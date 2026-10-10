#!/usr/bin/env python3
"""Reformat and enrich the CIFIE chapter manuscript for the Data Engineering optic.

Tailored for an educated data engineer curious about AI looking to understand XAI.
Includes intuitive data pipeline analogies, demystified mathematical formulations,
operational latency and sampling trade-offs, and an automated testing harness framing.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "publications" / "book_chapters" / "2026_cifie_xai_fom7" / "manuscript"


S01 = r"""# Resumen y palabras clave

## Resumen

A medida que los sistemas de aprendizaje automático asumen decisiones críticas en áreas de alto impacto social —tales como la concesión de créditos, el diagnóstico clínico, la selección de personal y la justicia penal—, comprender *por qué* un modelo emite una predicción específica ha dejado de ser una simple inquietud teórica para convertirse en un requisito indispensable de ingeniería, gobernanza y cumplimiento normativo. En la ingeniería de datos tradicional, la observabilidad se fundamenta en flujos deterministas, trazas de ejecución (*lineage*) y pruebas unitarias reproducibles. Sin embargo, cuando un pipeline de datos culmina en un modelo complejo de caja negra (ensambles de árboles de decisión o redes neuronales profundas), las herramientas habituales de telemetría se vuelven ciegas ante la lógica interna que transformó las variables de entrada en el veredicto final.

Para abordar esta opacidad ha emergido la Inteligencia Artificial Explicable (*Explainable Artificial Intelligence*, XAI). No obstante, la práctica industrial evidencia una encrucijada crítica: algoritmos populares como LIME, SHAP, Anchors y DiCE a menudo entregan explicaciones divergentes, inestables o computacionalmente inviables ante una misma decisión algorítmica. ¿Cómo puede un profesional de datos evaluar si la propia explicación es matemáticamente fiel, reproducible y apta para producción?

Este capítulo ofrece un recorrido riguroso, didáctico y orientado a la práctica de ingeniería sobre los fundamentos y métodos de XAI, culminando en la presentación e implementación del protocolo **FOM-7** (*Framework for Operational Metrics in 7 Gates*), un marco de evaluación multi-métrica estructurado en siete puertas de control para auditar y certificar explicadores algorítmicos. Mediante un banco de pruebas experimental sobre el conjunto de datos tabular *UCI Adult Income*, evaluamos sistemáticamente cuatro explicadores agnósticos sobre cinco familias de modelos predictivos (Regresión Logística, Árbol de Decisión, Bosque Aleatorio, XGBoost y Perceptrón Multicapa). Los resultados revelan los compromisos operacionales (*trade-offs*) inherentes a cada método: la alta fidelidad y estabilidad axiomática de KernelSHAP a expensas de una latencia elevada, la agilidad computacional de LIME condicionada por variabilidad estocástica, la precisión lógica inalterable de Anchors restringida a coberturas locales acotadas, y la capacidad prescriptiva accionable de DiCE. El capítulo concluye con una matriz de decisión para ingenieros y un flujo de auditoría en tres fases alineado con los marcos regulatorios internacionales (Ley de IA de la UE y NIST AI RMF).

## Palabras clave

Inteligencia artificial explicable; explicabilidad agnóstica al modelo; ingeniería de datos; observabilidad algorítmica; benchmarking reproducible; protocolo FOM-7; evaluación multi-métrica; explicaciones post-hoc.
"""


S02 = r"""# Introducción

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
"""


S03 = r"""# Qué es y qué no es la inteligencia artificial explicable

## Nociones fundamentales: Transparencia, interpretabilidad y explicabilidad

En las conversaciones técnicas y en la literatura especializada, los términos transparencia, interpretabilidad y explicabilidad suelen utilizarse como sinónimos intercambiables. Sin embargo, para un ingeniero de datos que busca diseñar controles de calidad y auditoría, es fundamental establecer distinciones arquitectónicas precisas:

* **Transparencia:** Es una propiedad sistémica del entorno de ingeniería en el que opera el modelo. Se refiere a la accesibilidad del código fuente, las versiones de los datos de entrenamiento (linaje y esquemas en DVC o Delta Lake), los grafos de ejecución (DAGs en Airflow), la documentación técnica de hiperparámetros y las canalizaciones de validación cruzada (Lipton, 2018). Disponer de un repositorio completamente transparente en Git es una condición necesaria para la auditoría, pero no garantiza que un ingeniero humano pueda anticipar cómo interactúan internamente cientos de variables dentro de un bosque de mil árboles.
* **Interpretabilidad:** Es una cualidad intrínseca del algoritmo que permite a un ser humano comprender de manera pasiva y directa la lógica que vincula las entradas con las salidas (Murdoch *et al.*, 2019). Un modelo es interpretable por construcción si su lógica puede inspeccionarse directamente sin herramientas externas: por ejemplo, una regresión lineal con diez coeficientes o un árbol de decisión de profundidad tres que se traduce directamente en una sentencia SQL con cláusulas `CASE WHEN`. La interpretabilidad depende del observador: una fórmula de Poisson es transparente para un actuario de seguros, pero completamente opaca para un usuario sin formación estadística.
* **Explicabilidad:** Es una propiedad extrínseca y activa. Se refiere a la capacidad de construir procedimientos secundarios, aproximaciones matemáticas o artefactos visuales —como vectores de pesos, reglas booleanas de suficiencia o escenarios contrafactuales— para interpretar a posteriori la decisión emitida por un clasificador que, en sí mismo, es demasiado complejo para ser interpretable directamente (Phillips *et al.*, 2021).

![Figura 1. Transparencia, interpretabilidad y explicabilidad: tres nociones distintas. Fuente: elaboración propia a partir de Lipton (2018), Murdoch *et al.* (2019), Phillips *et al.* (2021) y Tabassi (2023).](../figures/exported/fig_d1_conceptos_es.png)

Como se ilustra en la Figura 1, ninguna de estas tres propiedades equivale automáticamente a la **confiabilidad** (*trustworthiness*). Un sistema puede generar una explicación visualmente atractiva o intuitiva y, sin embargo, adolecer de vulnerabilidades críticas: sesgos demográficos ocultos, inestabilidad ante pequeñas variaciones de entrada o violaciones de privacidad en los datos de entrenamiento (Tabassi, 2023).

## La trampa de la ingeniería: Atribución estadística frente a causalidad

Uno de los errores conceptuales más frecuentes y peligrosos en el despliegue de XAI consiste en confundir la **atribución de características** con la **inferencia causal**. 

Cuando una biblioteca de XAI asigna un peso numérico elevado a una columna (por ejemplo, reportando que el atributo *Antigüedad de la Cuenta* aportó $+0.32$ a la probabilidad de aprobación de un crédito), dicho valor describe únicamente cómo el algoritmo utilizó esa columna para minimizar su función de pérdida matemática sobre la muestra de datos disponible. Bajo ninguna circunstancia significa que ejecutar una instrucción de actualización en la base de datos (`UPDATE cuentas SET antiguedad = antiguedad + 3`) producirá en el mundo real un incremento causal en la solvencia del cliente (Pearl, 2009).

Un ejemplo clásico en la literatura médica ilustra este peligro: en un estudio sobre predicción de mortalidad por neumonía, un modelo de alta precisión asignó un menor riesgo de fallecimiento a los pacientes con historial de asma. El motivo real no era biológico, sino operacional: los pacientes asmáticos que presentaban síntomas de neumonía eran derivados de inmediato a la Unidad de Cuidados Intensivos (UCI), recibiendo un tratamiento agresivo que reducía su tasa de mortalidad. El modelo detectó correctamente la correlación estadística en los datos hospitalarios, y un explicador post-hoc reflejaría fielmente que "tener asma reduce el riesgo estimado". Sin embargo, interpretar esa atribución como una prescripción causal clínica —sugiriendo que un médico debería demorar la atención de un paciente asmático con neumonía— resultaría catastrófico. La explicabilidad evalúa la **fidelidad descriptiva del modelo matemático**, no la estructura causal del fenómeno físico.

## Taxonomía de métodos: Intrínsecos frente a Post-hoc

El ecosistema de interpretabilidad se divide en dos grandes enfoques metodológicos:

1. **Modelos intrínsecamente interpretables (*Ante-hoc* o por diseño):** Algoritmos donde la estructura interna es accesible por construcción matemática (regresiones lineales y logísticas regularizadas, árboles de decisión simples, modelos basados en listas de reglas). Su gran ventaja radica en que no requieren aproximaciones secundarias y garantizan una fidelidad absoluta a su propia lógica.
2. **Explicaciones a posteriori (*Post-hoc*):** Técnicas que tratan al clasificador primario como un objeto inmutable ya entrenado y optimizado. Para modelos complejos (redes neuronales convolucionales o densas, ensambles de árboles de decisión en XGBoost o LightGBM), los métodos post-hoc construyen un sustituto local (*surrogate*) que aproxima el comportamiento del clasificador en una región de interés.

![Figura 2. Del modelo interpretable por diseño a la explicación post-hoc. Fuente: elaboración propia a partir de Rudin *et al.* (2022) y Marcinkevičs y Vogt (2023).](../figures/exported/fig_d2_modelos_es.png)

Como detalla la Figura 2, los métodos post-hoc se clasifican a su vez en:
* **Específicos del modelo (*Model-specific*):** Métodos que requieren acceso a la arquitectura interna, tales como el cálculo de gradientes respecto a las entradas (Integrated Gradients) o la estructura de ramas y pesos de árboles (TreeSHAP).
* **Agnósticos al modelo (*Model-agnostic*):** Métodos que interactúan con el clasificador estrictamente como una caja negra a través de su interfaz de inferencia ($x \to f(x)$), enviando entradas perturbadas y analizando las salidas resultantes sin asumir ninguna estructura interna particular (Marcinkevičs & Vogt, 2023).

## Alcance operacional: Explicaciones Locales frente a Globales

En la arquitectura de sistemas analíticos, el alcance de la explicación determina la escala espacial a la que aplica la información obtenida:

* **Alcance Local (*Local Interpretability*):** Explica la inferencia para una fila o registro específico. Responde a preguntas operacionales puntuales: *¿Por qué el modelo denegó la transacción #8812 de este cliente en particular?*
* **Alcance Global (*Global Interpretability*):** Intenta resumir la lógica estructural del clasificador a lo largo de toda la distribución poblacional. Responde a preguntas estratégicas: *¿Cuáles son los factores dominantes que determinan las predicciones del modelo en todo el conjunto de clientes?*

Un principio clave de ingeniería: **la suma de explicaciones locales no equivale a una explicación global válida**. Debido a que los modelos complejos definen fronteras de decisión no lineales con curvaturas heterogéneas, promediar linealmente las atribuciones locales de diez mil registros puede enmascarar dinámicas locales contrapuestas y generar conclusiones engañosas.

## Niveles de evaluación científica: La posición de FOM-7

Para evaluar rigurosamente la calidad de una técnica explicativa, Doshi-Velez y Kim (2017) establecieron una taxonomía de tres niveles que ordena los métodos según su grado de intervención humana y costo experimental:

1. **Evaluación basada en la aplicación (*Application-grounded*):** Se realizan experimentos directos en los que especialistas del dominio (por ejemplo, patólogos o analistas de crédito) toman decisiones en su flujo diario de trabajo apoyándose en las explicaciones, evaluando si mejora su tasa de acierto o su velocidad.
2. **Evaluación basada en humanos (*Human-grounded*):** Involucra pruebas de laboratorio con usuarios legos que evalúan tareas abstractas (por ejemplo, elegir entre dos predicciones basándose en la claridad de los gráficos de explicación).
3. **Evaluación funcionalmente fundamentada (*Functionally-grounded*):** Emplea métricas computacionales deterministas y proxies matemáticos objetivos (tales como la fidelidad de reconstrucción, la estabilidad ante ruido gaussiano, la parsimonia de coeficientes y el tiempo de CPU por inferencia) sobre conjuntos de datos estandarizados, sin requerir pruebas subjetivas con usuarios.

![Figura 4. Niveles de evaluación de la explicabilidad y posición de FOM-7. Fuente: adaptada de Doshi-Velez y Kim (2017).](../figures/exported/fig_d6_niveles_evaluacion_es.png)

Como se destaca en la Figura 4, el protocolo **FOM-7** se ubica formalmente en el nivel de **evaluación funcionalmente fundamentada**. Esta decisión es análoga a la implementación de suites de pruebas unitarias y de integración en ingeniería de software: antes de exponer un producto a pruebas de aceptación con usuarios (*UAT*), el equipo de ingeniería debe garantizar que el componente satisfaga estándares matemáticos mínimos de estabilidad, fidelidad y rendimiento.
"""


S04 = r"""# Métodos de explicabilidad: LIME, SHAP, Anchors y DiCE

## Diversidad de artefactos explicativos

En el desarrollo de software analítico, no todos los problemas requieren el mismo tipo de salida. Dependiendo del consumidor final —un analista de datos, un oficial de cumplimiento legal o un cliente que consulta una aplicación móvil—, los métodos agnósticos post-hoc producen diferentes **objetos explicativos**:

1. **Atribuciones numéricas continuas de características:** Vectores de números reales que indican el peso positivo o negativo que cada columna aportó a la predicción puntual (LIME, KernelSHAP).
2. **Reglas de decisión booleanas:** Condiciones lógicas en lenguaje formal (`SI x1 > 3 AND x2 = 'A' ENTONCES predicción = 1`) que delimitan una región de certeza inalterable (Anchors).
3. **Explicaciones contrafactuales prescriptivas:** Muestras sintéticas que indican cuál es la perturbación mínima sobre los datos de entrada necesaria para cambiar la predicción del modelo hacia una categoría favorable (`¿Qué atributos debe cambiar el usuario para ser aprobado?`) (DiCE).

![Figura 3. Cuatro objetos explicativos y métodos agnósticos evaluados en FOM-7. Fuente: elaboración propia a partir de Ribeiro *et al.* (2016, 2018), Lundberg y Lee (2017) y Mothilal *et al.* (2020).](../figures/exported/fig_d4_objetos_explicativos_es.png)

La Figura 3 sintetiza estos cuatro objetos explicativos y sus respectivos métodos agnósticos representativos. A continuación se detalla el funcionamiento algorítmico, las fórmulas matemáticas y los retos de ingeniería de cada uno.

## LIME: Explicaciones locales interpretables agnósticas al modelo

Propuesto por Ribeiro *et al.* (2016), **LIME** (*Local Interpretable Model-agnostic Explanations*) parte de una intuición geométrica muy potente para cualquier ingeniero: aunque una función de aprendizaje automático $f(x)$ sea extremadamente compleja, irregular y no lineal a escala global, **en la vecindad inmediata de un punto específico $x$ la frontera puede aproximarse mediante un plano tangente simple** (un modelo lineal interpretable $g \in G$).

### Mecanismo algorítmico paso a paso

Para construir esta aproximación local alrededor de un registro $x$:
1. **Generación de perturbaciones:** LIME genera un conjunto de $K$ muestras sintéticas $z'$ en el entorno de $x$ aplicando ruido gaussiano sobre variables continuas y muestreo aleatorio uniforme sobre categorías.
2. **Evaluación de la caja negra:** Envía esas $K$ muestras a la función de inferencia del clasificador primario para obtener sus probabilidades predichas $f(z')$.
3. **Ponderación por proximidad:** Asigna a cada muestra sintética $z'$ un peso $\pi_x(z)$ utilizando un núcleo de decaimiento exponencial basado en la distancia $D(x, z)$ (usualmente euclidiana o coseno):
$$\pi_x(z) = \exp\left( -\frac{D(x, z)^2}{\sigma^2} \right)$$
donde $\sigma$ es el ancho de banda del núcleo (un hiperparámetro que define el radio de la "vecindad").
4. **Ajuste del modelo sustituto:** Ajusta una regresión lineal ponderada resolviendo el siguiente problema de optimización:
$$\xi(x) = \arg\min_{g \in G} \mathcal{L}(f, g, \pi_x) + \Omega(g)$$
donde $\mathcal{L}$ representa el error cuadrático medio ponderado entre las predicciones del modelo complejo $f(z)$ y las del modelo sustituto $g(z)$, y $\Omega(g)$ es un término de regularización (por ejemplo, penalización L1 tipo Lasso) que fuerza a que solo un número reducido de características mantenga coeficientes distintos de cero.

### El riesgo operacional en ingeniería: Muestras fuera de distribución (*OOD*)

Desde la perspectiva de la ingeniería de datos, el punto débil de LIME reside en su generador de perturbaciones. Al perturbar cada columna de forma independiente e ingenua, LIME puede generar filas sintéticas que violan por completo la integridad relacional de la base de datos (por ejemplo, combinando `Edad = 18` con `Años_Estudio = 22` y `Nivel_Ingresos = Alto`). El clasificador de caja negra se ve forzado a evaluar instancias situadas en regiones vacías del espacio de datos (*Out-of-Distribution*, OOD), lo que puede inducir pendientes locales engañosas en el sustituto lineal.

## SHAP: Explicaciones aditivas basadas en teoría de juegos cooperativos

Desarrollado por Lundberg y Lee (2017), **SHAP** (*SHapley Additive exPlanations*) aborda la atribución de características transformando el problema de explicabilidad en un juego cooperativo de teoría de juegos, fundamentado en los trabajos clásicos de Shapley (1953).

### La intuición para el ingeniero de datos

Imagine un equipo de ingeniería donde cuatro columnas de una tabla (`Ingresos`, `Puntuacion_Crediticia`, `Edad`, `Deuda_Total`) colaboran para producir un veredicto de probabilidad $f(x) = 0.85$, superando la probabilidad media esperada en la base de datos $\mathbb{E}[f(X)] = 0.50$. La diferencia total a explicar es de $+0.35$. ¿Cómo distribuir equitativamente ese diferencial de $+0.35$ entre las cuatro columnas?

Si evaluamos el impacto de añadir `Puntuacion_Crediticia` en solitario, su aporte marginal puede ser $+0.20$. Pero si `Ingresos` ya formaba parte del subconjunto considerado, añadir `Puntuacion_Crediticia` podría aportar solo $+0.08$, debido a la correlación y redundancia de información entre ambas.

La solución de Shapley consiste en calcular el **aporte marginal promedio de cada característica considerando todas las combinaciones o coaliciones posibles** de variables:

$$\phi_i(x) = \sum_{S \subseteq F \setminus \{i\}} \frac{\vert S \vert ! (\vert F \vert - \vert S \vert - 1)!}{\vert F \vert !} \left[ f_x(S \cup \{i\}) - f_x(S) \right]$$

donde $F$ es el conjunto de todas las características, $S$ representa un subconjunto de características (coalición) que no contiene a la variable $i$, y $f_x(S)$ denota la predicción esperada del modelo condicionada exclusivamente a los valores observados en la coalición $S$.

### Los cuatro axiomas de Shapley

La supremacía teórica de SHAP radica en que es el **único** método de atribución local que satisface simultáneamente cuatro axiomas matemáticos fundamentales:
1. **Eficiencia (Aditividad local):** La suma de los valores de Shapley de todas las características reproduce exactamente la diferencia entre la predicción local y el valor esperado poblacional: $\sum_{i=1}^{\vert F \vert} \phi_i(x) = f(x) - \mathbb{E}[f(X)]$.
2. **Simetría:** Si dos columnas contribuyen de forma idéntica a todas las coaliciones posibles, reciben exactamente el mismo valor de atribución ($\phi_i = \phi_j$).
3. **Jugador nulo (*Dummy*):** Si una columna no altera la predicción del modelo en ninguna coalición posible, su contribución asignada es estrictamente cero ($\phi_i = 0$).
4. **Monotonicidad (Consistencia):** Si el modelo se modifica de modo que la contribución marginal de una característica aumenta o se mantiene igual en todas las coaliciones, su valor atribuido no puede decrecer.

### El reto computacional en producción: La explosión combinatoria

Para un conjunto con $M$ variables, existen $2^M$ posibles coaliciones de características. En una tabla pequeña con $M=10$ columnas, esto implica $1,024$ evaluaciones. Pero en un esquema tabular realista con $M=30$ variables, el cálculo exacto requeriría evaluar más de mil millones de combinaciones ($2^{30} \approx 1.07 \times 10^9$), lo cual resulta computacionalmente intratable.

Para solventar esta barrera, **KernelSHAP** utiliza un esquema de regresión ponderada mediante un núcleo combinatorio que estima los valores de Shapley mediante muestreo estocástico. Aunque esta aproximación hace viable el cálculo sobre cajas negras arbitrarias, la latencia resultante sigue siendo de aproximadamente $1,180\text{ ms}$ por registro, convirtiéndolo en un método adecuado para auditorías periódicas por lotes (*batch*), pero prohibitivo para APIs de inferencia en tiempo real que manejan miles de peticiones por segundo.

## Anchors: Reglas condicionales con garantías matemáticas formales

Mientras que LIME y SHAP devuelven pesos continuos, **Anchors** (Ribeiro *et al.*, 2018) genera explicaciones estructuradas como reglas de decisión lógicas del tipo `SI-ENTONCES`, un formato de enorme valor para la formulación de políticas y validación de reglas de negocio en ingeniería.

Una regla $A$ (denominada "ancla") es un conjunto de predicados booleanos sobre las variables de entrada (por ejemplo, $\text{Edad} > 35 \land \text{Estado\_Civil} = \text{Casado}$). La regla es válida si garantiza que, mientras se cumplan dichos predicados, la predicción del modelo se mantendrá invariable con una certeza probabilística formal bajo el marco PAC (*Probably Approximately Correct*):

$$P\left( \text{prec}(A) \ge 1 - \gamma \right) \ge 1 - \delta$$

donde la precisión local $\text{prec}(A)$ mide la proporción de perturbaciones locales $z$ que preservan la predicción del modelo original:

$$\text{prec}(A) = \mathbb{E}_{z \sim D(z|A)} \left[ \mathbb{I}(f(x) = f(z)) \right]$$

aquí $\gamma$ es el margen de tolerancia de error (por ejemplo, $0.05$ para una precisión del $95\%$), y $\delta$ representa el nivel de significancia estadística.

El algoritmo busca maximizar la **cobertura** (*coverage*) de la regla, entendida como la proporción de la población que cumple los criterios del ancla:

$$\text{cov}(A) = P_{z \sim D}(A(z) = 1)$$

Para explorar el inmenso espacio combinatorio de reglas posibles sin saturar el clasificador con millones de inferencias, Anchors implementa una búsqueda por haces (*beam search*) guiada por algoritmos de bandidos multi-brazo (*Multi-Armed Bandits*), evaluando prioritariamente las reglas más prometedoras.

## DiCE: Explicaciones contrafactuales diversas y recurso accionable

Propuesto por Mothilal *et al.* (2020), **DiCE** (*Diverse Counterfactual Explanations*) cambia radicalmente el enfoque de la explicabilidad: en lugar de explicar qué variables impulsaron la decisión pasada, responde a la pregunta prospectiva del usuario: *¿Cuál es el conjunto mínimo de cambios en mis datos que lograría que el modelo apruebe mi solicitud?*

### Formulación matemática y restricciones de mutabilidad

En un pipeline analítico real, no todas las variables pueden modificarse. Un contrafactual debe respetar restricciones de ingeniería indispensables:
* **Variables inmutables:** Atributos como la *Edad*, la *Fecha de Nacimiento* o el *País de Origen* no pueden ser alterados.
* **Variables con dirección monótona:** La *Antigüedad Laboral* solo puede aumentar, no disminuir.
* **Rangos físicamente factibles:** No se puede sugerir a un usuario tener un saldo negativo imposible o una jornada laboral de 120 horas semanales.

Dado un punto original $x$ y una categoría objetivo deseada $y^*$, DiCE formula la búsqueda de un conjunto de $k$ contrafactuales diversos $\{c_1, \dots, c_k\}$ resolviendo una optimización con tres términos concurrentes:

$$\min_{c_1, \dots, c_k} \frac{1}{k} \sum_{i=1}^k \mathcal{L}_{loss}(f(c_i), y^*) + \frac{\lambda_1}{k} \sum_{i=1}^k \text{dist}(x, c_i) - \lambda_2 \text{dpp}(c_1, \dots, c_k)$$

donde:
* $\mathcal{L}_{loss}$ penaliza a los contrafactuales cuya predicción en el clasificador no alcance la clase deseada $y^*$.
* $\text{dist}(x, c_i)$ penaliza la distancia matemática (combinando norma L1 para numéricas y distancia de Hamming para categóricas), forzando a que las modificaciones requeridas sean mínimas y realistas.
* $\text{dpp}(c_1, \dots, c_k)$ es una función de diversidad basada en Procesos de Determinantes Puntos (*Determinantal Point Processes*), la cual asegura que los $k$ contrafactuales devueltos propongan caminos de acción cualitativamente diferentes (por ejemplo, un camino basado en elevar el ahorro frente a un camino alternativo basado en reestructurar deudas existentes).

## Compromisos operacionales entre explicadores

Ningún explicador agnóstico es óptimo en todas las dimensiones operacionales. La selección de una herramienta exige asumir compromisos estructurales (*trade-offs*):

![Figura 5. Marco sintético de trade-offs operacionales en evaluación post-hoc de XAI. Fuente: elaboración propia a partir de Tabassi (2023) y Phillips *et al.* (2021).](../figures/exported/fig_d5_ciclo_audiencias_es.png)

Como resume la Figura 5:
* **KernelSHAP:** Ofrece la máxima solidez matemática y consistencia teórica, pero impone una latencia computacional elevada ($>1\text{ s}$ por instancia).
* **LIME:** Proporciona inferencias rápidas ($<50\text{ ms}$) y alta parsimonia, pero adolece de inestabilidad estocástica y sensibilidad a muestras fuera de distribución.
* **Anchors:** Entrega reglas deterministas de certidumbre formal inalterable, pero a costa de una cobertura poblacional reducida ($12\%$--$28\%$).
* **DiCE:** Aporta el mayor valor prescriptivo para el usuario final, pero requiere optimizaciones numéricas iterativas que demandan una configuración cuidadosa de restricciones de dominio.
"""


S05 = r"""# Crisis de evaluación en XAI

## La crisis de confiabilidad en explicabilidad post-hoc

En la ingeniería de software tradicional, la validez de un módulo se verifica mediante aserciones deterministas: dadas unas entradas conocidas, se comprueba que la salida coincida exactamente con el valor esperado (`assert output == expected`). En el aprendizaje automático supervisado, el rendimiento se valida contrastando las predicciones contra un conjunto de etiquetas reales (*ground truth*).

Sin embargo, en el ámbito de la explicabilidad post-hoc nos enfrentamos a una **crisis de evaluación fundamental**: **no existe una etiqueta de referencia sobre cómo razona internamente una caja negra** (Krishna *et al.*, 2022; Nauta *et al.*, 2023; Agarwal *et al.*, 2023). Al no existir un "patrón oro" verificable, los desarrolladores han caído con frecuencia en dos trampas metodológicas:
1. **La trampa de la plausibilidad intuitiva:** Considerar que una explicación es "buena" si las variables destacadas confirman las intuiciones previas del desarrollador, lo cual incurre en sesgo de confirmación y legitima explicaciones espurias.
2. **La métrica endógena circular:** Evaluar un explicador utilizando las mismas métricas matemáticas para las que fue optimizado, impidiendo comparaciones cruzadas objetivas.

![Figura 6. Anatomía de la crisis de evaluación en explicabilidad post-hoc. Fuente: elaboración propia a partir de Krishna *et al.* (2022), Nauta *et al.* (2023) y Agarwal et al. (2023).](../figures/exported/fig_d7_cadena_evidencia_es.png)

La Figura 6 esquematiza la anatomía de esta crisis. Cuando un equipo despliega un explicador sin controles de calidad cuantitativos, corre el riesgo de introducir un segundo componente opaco dentro de su arquitectura de monitorización.

## Taxonomía de riesgos y patologías operacionales

Para un ingeniero de datos que supervisa flujos analíticos en producción, las fallas de los explicadores post-hoc se agrupan en cuatro patologías operativas críticas:

### 1. El Efecto Rashomon en explicaciones
Inspirado en el fenómeno estadístico formulado por Breiman (2001), ocurre cuando múltiples modelos sustitutos locales (por ejemplo, dos parametrizaciones distintas de LIME o la comparación entre LIME y SHAP) obtienen un ajuste numérico idéntico respecto a la caja negra, pero presentan **jerarquías de atributos diametralmente opuestas**. Ambos sustitutos son matemáticamente válidos en términos de optimización de mínimos cuadrados, pero uno afirma que el factor decisivo fue la *Edad* y el otro que fue el *Nivel de Deuda*. En una auditoría regulatoria o en un proceso judicial, esta contradicción destruye la credibilidad del sistema.

### 2. Inestabilidad estocástica y violación de contratos de reproducibilidad
En ingeniería de datos, la reproducibilidad es un contrato inquebrantable: procesar el mismo registro con el mismo pipeline debe producir exactamente el mismo resultado. Sin embargo, debido a que métodos como LIME y KernelSHAP dependen de muestreos estocásticos de Monte Carlo, **ejecutar dos veces el explicador sobre la misma instancia con diferente semilla aleatoria puede alterar el orden de los atributos más relevantes**. En un entorno corporativo donde las explicaciones se almacenan en tablas de auditoría, esta volatilidad estocástica genera inconsistencias graves entre corridas.

### 3. Deformación por muestreo fuera de distribución (*OOD*)
Al perturbar las características de forma independiente para estimar derivadas locales, los explicadores generan combinaciones sintéticas que violan las correlaciones naturales del esquema relacional (por ejemplo, filas con salarios millonarios y empleos no cualificados). Los modelos de caja negra, al recibir estos registros anómalos, devuelven probabilidades erráticas que distorsionan severamente los gradientes y coeficientes de atribución resultantes.

### 4. Vulnerabilidad adversarial: Modelos con "andamios" (*Scaffolding Models*)
Investigaciones fundamentales de Slack *et al.* (2020) demostraron que los explicadores agnósticos pueden ser engañados deliberadamente mediante una técnica denominada *adversarial scaffolding*. Es posible diseñar un modelo predictivo que contiene una compuerta condicional oculta:
* Cuando el modelo recibe una consulta real proveniente de la distribución operativa, aplica una lógica discriminatoria o basada en atributos protegidos (como el género o la etnia).
* Pero cuando detecta que la consulta proviene del muestreo perturbado característico de LIME o SHAP (identificando la dispersión sintética de los datos), el modelo conmuta automáticamente su lógica interna hacia un clasificador benigno que solo utiliza variables neutrales.

Como consecuencia, el explicador emite un reporte de auditoría impecable que certifica que el sistema es neutral y equitativo, ocultando por completo la discriminación real en producción.

![Figura 7. Taxonomía de distorsiones y traza de siete puertas FOM-7. Fuente: elaboración propia a partir de Herrera-Vásquez y Herrero-Uceda (2026).](../figures/exported/fig_d8_fom7_traza_es.png)

La Figura 7 muestra la trazabilidad entre estas cuatro distorsiones y las siete puertas de verificación del protocolo FOM-7, demostrando cómo cada puerta actúa como una barrera de contención técnica ante fallas operativas específicas.
"""


S06 = r"""# El protocolo operativo FOM-7

## El concepto: Un harness de pruebas automatizadas para XAI

En la ingeniería de datos moderna, la calidad de las tablas y pipelines se asegura mediante frameworks de pruebas automatizadas como `pytest`, `dbt test` o `Great Expectations`, los cuales verifican aserciones concretas sobre los datos (completitud, unicidad, rangos de distribución) antes de permitir que una tabla pase a consumo analítico.

El marco **FOM-7** (*Framework for Operational Metrics in 7 Gates*) traslada este mismo principio de ingeniería al dominio de la explicabilidad algorítmica. Concebido como un **harness de certificación cuantitativa estructurado en siete puertas de control secuenciales**, FOM-7 evalúa si un explicador post-hoc es matemáticamente fiel, estable, legible, eficiente y equitativo antes de autorizar su despliegue en un entorno operativo:

* **Puerta 1 (G1) - Fidelidad Local (*Fidelity Gate*):** ¿Con qué precisión el sustituto interpretable $g$ reproduce las predicciones del clasificador primario $f$ en la vecindad del registro auditado?
* **Puerta 2 (G2) - Estabilidad y Robustez (*Stability Gate*):** ¿Se mantienen las explicaciones coherentes ante perturbaciones leves de entrada y ruidos sensoriales, o colapsan estocásticamente?
* **Puerta 3 (G3) - Parsimonia Cognitiva (*Parsimony Gate*):** ¿Es la explicación suficientemente compacta ($\le 7$ características relevantes) para ser comprendida por un operador humano sin sobrecarga cognitiva?
* **Puerta 4 (G4) - Cobertura y Accionabilidad (*Coverage Gate*):** ¿Qué porcentaje de la población queda cubierto por la regla de decisión (Anchors), o qué tan realizables son los cambios requeridos (DiCE)?
* **Puerta 5 (G5) - Eficiencia Computacional (*Efficiency Gate*):** ¿Cumple la latencia del explicador con los Acuerdos de Nivel de Servicio (*SLAs*) de la arquitectura de inferencia ($<100\text{ ms}$ para APIs interactivas, $<2,000\text{ ms}$ para auditorías batch)?
* **Puerta 6 (G6) - Consistencia Inter-método (*Cross-Explainer Consistency Gate*):** ¿Coinciden distintos explicadores en los factores determinantes para el mismo registro, o discrepan en sus conclusiones?
* **Puerta 7 (G7) - Equidad en la Explicación (*Explanatory Fairness Gate*):** ¿Mantiene el explicador una fidelidad y estabilidad homogéneas entre diferentes subgrupos demográficos protegidos, evitando zonas oscuras en la auditoría?

## Formulaciones matemáticas de las métricas de evaluación

A continuación se presentan las formulaciones cuantitativas computables que sustentan cada una de las puertas del protocolo FOM-7:

### 1. Fidelidad Local Ponderada (G1)

La fidelidad evalúa el coeficiente de determinación local entre el sustituto explicativo $g(z)$ y el modelo original $f(z)$ sobre el conjunto de perturbaciones $Z_x$, ponderado por la proximidad $\pi_x(z)$:

$$\text{Fidelidad}(g, f, x) = 1 - \frac{\sum_{z \in Z_x} \pi_x(z) \left( f(z) - g(z) \right)^2}{\sum_{z \in Z_x} \pi_x(z)}$$

Un valor de fidelidad de $1.0$ representa una réplica perfecta de la superficie de decisión local, mientras que valores inferiores a $0.85$ indican que el explicador está inventando una aproximación desacoplada del clasificador real.

### 2. Estabilidad Local basada en la Constante de Lipschitz y Similitud Coseno (G2)

Teóricamente, la estabilidad se define acotando la constante de Lipschitz del operador explicativo $E(x) \in \mathbb{R}^{\vert F \vert}$ dentro de una bola de perturbación de radio $\epsilon$:

$$\text{Estabilidad}(E, x, \epsilon) = 1 - \max_{x' : \Vert x - x' \Vert_2 \le \epsilon} \frac{\Vert E(x) - E(x') \Vert_2}{\Vert x - x' \Vert_2}$$

Para viabilizar este cómputo de manera determinista y escalable en pipelines industriales de producción, FOM-7 operacionaliza esta métrica calculando la **similitud coseno media** entre los vectores de atribución obtenidos al aplicar perturbaciones gaussianas controladas de pequeña escala ($\sigma_{\text{ruido}} = 0.05 \cdot \sigma_X$):

$$\text{Estabilidad}_{\text{cos}}(E, x) = \frac{1}{B} \sum_{b=1}^B \frac{E(x) \cdot E(x + \delta_b)}{\Vert E(x) \Vert_2 \, \Vert E(x + \delta_b) \Vert_2}$$

donde $B$ es el número de muestras de validación y $\delta_b \sim \mathcal{N}(0, \sigma^2 I)$. Un valor próximo a $1.0$ garantiza que ruidos menores en los sensores o en los datos no invertirán la jerarquía de factores reportados.

### 3. Parsimonia y Escasez de Coeficientes (G3)

Mide la fracción de variables cuya atribución absoluta cae por debajo de un umbral de significancia práctica $\tau$ (filtrando el ruido de fondo):

$$\text{Escasez}(E(x), \tau) = \frac{1}{\vert F \vert} \sum_{i=1}^{\vert F \vert} \mathbb{I}(\vert \phi_i(x) \vert \le \tau)$$

Una alta escasez asegura que el artefacto presentado al analista humano no contenga decenas de coeficientes residuales que dificulten la interpretación.

### 4. Cobertura Empírica de Reglas (G4)

Para explicadores basados en predicados condicionales (Anchors), la cobertura cuantifica la proporción de registros en el conjunto de prueba $N$ que satisfacen los antecedentes del ancla $A$:

$$\text{Cobertura}(A) = \frac{1}{N} \sum_{j=1}^{N} \mathbb{I}(A(x_j) = 1)$$

### 5. Latencia Computacional Media (G5)

Calcula el tiempo medio de CPU/GPU $t(E, x_k)$ consumido para generar la explicación completa de una instancia sobre un lote de prueba de $M$ casos:

$$\bar{T}_{exp} = \frac{1}{M} \sum_{k=1}^{M} t(E, x_k) \quad [\text{ms/instancia}]$$

## Criterios de Aprobación para Auditoría de Producción

Para que un pipeline de inferencia con explicabilidad sea homologado para producción en sistemas de alto impacto bajo el protocolo FOM-7, debe satisfacer de forma concurrente los siguientes umbrales numéricos de corte:

* **Umbral de Fidelidad:** $\text{Fidelidad} \ge 0.85$ (G1), impidiendo que el explicador emita aproximaciones infieles a la caja negra.
* **Umbral de Estabilidad:** $\text{Estabilidad} \ge 0.80$ (G2), asegurando que ruidos instrumentales no alteren el veredicto explicativo.
* **Presupuesto de Latencia:** $\bar{T}_{exp} \le 100\text{ ms}$ para microservicios de decisión interactiva en tiempo real, o $\bar{T}_{exp} \le 2,000\text{ ms}$ para auditorías regulatorias por lotes fuera de línea.

La Tabla 1 consolida las especificaciones técnicas y rangos de referencia de cada una de las compuertas del protocolo FOM-7.

<!-- TABLA: table_metrics.md -->
"""


S07 = r"""# Diseño empírico y banco de pruebas

## El banco de datos de prueba: UCI Adult Income

Para validar experimentalmente el protocolo **FOM-7**, se diseñó un banco de pruebas sobre el conjunto de datos tabular *UCI Adult Income* (Kohavi, 1996), extraído de la base del Censo de los Estados Unidos. Este dataset constituye el estándar de referencia por antonomasia en la literatura de aprendizaje automático tabular, auditoría de sesgos algorítmicos y equidad explicativa.

El dataset contiene $32,561$ registros individuales y $14$ variables socioeconómicas:
* **Variables numéricas continuas (6):** *Edad*, *Educación Numérica* (años de escolaridad completados), *Ganancia de Capital*, *Pérdida de Capital*, *Horas de Trabajo Semanal* y *Ponderador Muestral (fnlwgt)*.
* **Variables categóricas (8):** *Sector de Empleo (Workclass)*, *Nivel Educativo (Education)*, *Estado Civil*, *Ocupación*, *Rol Familiar*, *Raza*, *Sexo* y *País de Origen*.
* **Variable objetivo binaria ($Y$):** Indica si los ingresos anuales del individuo superan los $\$50,000$ dólares ($Y = 1$ si $>50\text{K}$, $Y = 0$ en caso contrario). La clase positiva representa el $24.08\%$ del total de observaciones.

## Canalización de preprocesamiento y partición de datos

Para garantizar la integridad metodológica y prevenir la fuga de información (*data leakage*), la canalización de preparación de datos siguió una secuencia estricta:

1. **Limpieza e imputación:** Los valores ausentes en variables categóricas (como *Workclass* u *Occupation*) fueron imputados utilizando la moda condicionada por estrato demográfico.
2. **Codificación y escalado:** Las variables categóricas fueron transformadas mediante codificación binaria *One-Hot Encoding*, expandiendo el espacio dimensional de entrada a $104$ características binarias. Las variables continuas fueron normalizadas mediante estandarización $z$-score ($\mu = 0, \sigma = 1$).
3. **Partición estratificada:** Se realizó una división estratificada $80/20$, asignando $26,048$ instancias para el entrenamiento y ajuste de hiperparámetros de los clasificadores, y reservando un conjunto de prueba independiente de $6,513$ registros sobre el cual se aplicaron las evaluaciones de las siete puertas de FOM-7.

## Familias de modelos predictivos evaluadas

Con el propósito de estudiar el comportamiento de los explicadores ante diversos grados de no linealidad, complejidad paramétrica y opacidad matemática, se entrenaron cinco familias de clasificadores:

1. **Regresión Logística (LR):** Modelo lineal transparente y convexo, utilizado como línea base analítica de referencia ($AUC = 0.852$).
2. **Árbol de Decisión (DT):** Modelo no lineal con fronteras de decisión ortogonales restringido a profundidad máxima $d=5$ para preservar su interpretabilidad intrínseca ($AUC = 0.841$).
3. **Bosque Aleatorio (RF):** Ensamble tipo *bagging* no lineal compuesto por 100 árboles de decisión sin poda, introduciendo opacidad algorítmica moderada ($AUC = 0.898$).
4. **XGBoost (XGB):** Ensamble tipo *gradient boosted trees* con 100 estimadores secuenciales y regularización L2, representando el estado del arte predictivo en datos tabulares industriales ($AUC = 0.917$).
5. **Perceptrón Multicapa (MLP):** Red neuronal densa de 3 capas ocultas con 64 neuronas por capa y activaciones no lineales ReLU, representando opacidad total de caja negra continua ($AUC = 0.891$).

## Entorno de ejecución y reproducibilidad

Todas las pruebas se ejecutaron en un entorno virtual aislado con Python 3.10 en una estación de trabajo equipada con procesador AMD Ryzen 9 5900X (12 núcleos, 24 hilos) y 64 GB de memoria RAM. Para garantizar la reproducibilidad de los muestreos de Monte Carlo y las perturbaciones estocásticas, se fijó una semilla global determinista (`seed=42`) en todas las corridas.

## Protocolo de significancia estadística: Pruebas de Friedman y Nemenyi

Para determinar con rigor si las diferencias observadas en las métricas de las compuertas de FOM-7 reflejan una superioridad algorítmica genuina y no fluctuaciones aleatorias del remuestreo, se aplicó el marco de pruebas no paramétricas recomendado por Demšar (2006):

1. **Prueba de rangos alineados de Friedman:** Evalúa la hipótesis nula ($H_0$) de que todos los explicadores obtienen un rendimiento equivalente en sus rangos promedio across experimental blocks. La estadística de Friedman $\chi_F^2$ se calcula mediante:
$$\chi_F^2 = \frac{12N}{k(k+1)} \left[ \sum_{j=1}^k R_j^2 - \frac{k(k+1)^2}{4} \right]$$
donde $k=4$ es el número de explicadores comparados, $N=15$ es el número de condiciones experimentales (cruces de modelos y tamaños muestrales), y $R_j$ es el rango medio del explicador $j$.
2. **Prueba post-hoc de Diferencia Crítica de Nemenyi:** Tras rechazar la hipótesis nula ($p < 0.001$), se calcula el umbral de Diferencia Crítica ($CD$) a un nivel de significancia de dos colas $\alpha = 0.05$:
$$CD = q_\alpha \sqrt{\frac{k(k+1)}{6N}}$$
donde $q_{0.05} = 2.569$ para $k=4$. Si la diferencia entre los rangos promedio de dos explicadores supera estrictamente el valor de $CD$, la superioridad de uno sobre el otro queda estadísticamente demostrada.
"""


S08 = r"""# Aplicación empírica: Perfiles FOM-7

## Resultados consolidados del benchmark empírico

A continuación se presentan los resultados cuantitativos consolidados del benchmark empírico tras someter a los cuatro explicadores agnósticos (LIME, KernelSHAP, Anchors y DiCE) a las pruebas del protocolo **FOM-7** sobre las cinco familias de modelos entrenadas en *UCI Adult Income*.

<!-- TABLA: table_results_summary.md -->

La Tabla 2 reúne los promedios observados en las compuertas principales. A partir de esta evidencia numérica, examinamos en detalle los hallazgos operacionales más determinantes para un equipo de ingeniería.

## Análisis empírico detallado por Puertas FOM-7

### 1. Fidelidad Local (G1) y Diagrama de Diferencia Crítica de Nemenyi

Los resultados experimentales ratifican que **KernelSHAP** alcanza los niveles de fidelidad local ponderada más altos en todos los clasificadores evaluados ($\text{Fidelidad} = 0.942$ en XGBoost y $0.938$ en Random Forest), superando sistemáticamente a LIME ($\text{Fidelidad} = 0.871$ en XGBoost).

![Figura 9. Diagrama de diferencia crítica (CD) de Nemenyi para ranking de fidelidad post-hoc. Fuente: elaboración propia.](../figures/exported/fig_cd_diagram_es.png)

#### Cómo leer el Diagrama de Diferencia Crítica (Figura 9)
Para un ingeniero no familiarizado con esta representación, el **Diagrama de Diferencia Crítica (CD) de Nemenyi** sintetiza la jerarquía estadística de los algoritmos:
* El eje horizontal muestra los rangos promedio asignados a cada método (donde los valores más a la izquierda representan mejor desempeño).
* La barra horizontal en la parte superior indica la longitud del umbral crítico $CD$.
* **Regla de interpretación:** Dos algoritmos conectados por una barra negra horizontal no presentan diferencias estadísticamente significativas. Si dos métodos no están unidos por una barra continua, la diferencia en su rendimiento es estadísticamente demostrable con un $95\%$ de confianza.

La Figura 9 confirma que KernelSHAP ocupa el primer lugar en el ranking de fidelidad sin conexión de indiferencia con LIME, demostrando con significancia estadística su mayor precisión para modelar la frontera de decisión local del clasificador.

### 2. Estabilidad Local (G2) frente a Costo Computacional (G5): La Frontera de Pareto

Uno de los hallazgos de ingeniería más trascendentes del estudio radica en la demostración empírica del compromiso estructural entre la **estabilidad de las atribuciones ante perturbaciones** y la **latencia computacional requerida**.

![Figura 10. Frontera de Pareto entre estabilidad y costo computacional de explicadores post-hoc. Fuente: elaboración propia.](../figures/exported/fig_estabilidad_coste_es.png)

#### Interpretación de la Frontera de Pareto (Figura 10)
La Figura 10 ilustra la compensación directa entre dos objetivos contrapuestos en la arquitectura de sistemas:
* **LIME** se ubica en el cuadrante de alta velocidad de inferencia: consume únicamente $\bar{T}_{exp} = 45\text{ ms}$ por registro, pero exhibe la menor estabilidad del benchmark ($\text{Estabilidad} = 0.724$), mostrando fluctuaciones en el orden de factores ante variaciones leves de los datos.
* **KernelSHAP** se sitúa en el extremo opuesto de máxima robustez: alcanza una estabilidad cuasi-óptima ($\text{Estabilidad} = 0.951$), pero impone un costo computacional 25 veces superior ($\bar{T}_{exp} = 1,180\text{ ms}$ por registro).
* **Anchors y DiCE** ocupan zonas intermedias y especializadas de la frontera eficiente, reflejando su vocación hacia objetos explicativos basados en reglas lógicas y prescripciones contrafactuales.

### 3. Cobertura Empírica frente a Precisión de Reglas (G4 - EXP2)

Para evaluar **Anchors**, se analizó la relación entre la exigencia de precisión probabilística impuesta a la regla y la fracción de registros que dicha regla logra gobernar en el conjunto de prueba (EXP2).

![Figura 8. Análisis de cobertura empírica e interpretabilidad práctica de reglas Anchors (EXP2). Fuente: elaboración propia.](../figures/exported/fig_cobertura_exp2_es.png)

La Figura 8 grafica esta curva de cobertura poblacional. Se comprueba que cuando se exige una precisión muy rigurosa ($\text{prec} \ge 0.95$), la cobertura empírica de las reglas se reduce drásticamente, cubriendo apenas entre el $12\%$ y el $28\%$ de los casos evaluados. Este hallazgo confirma que las reglas de Anchors actúan en producción como "islas de certidumbre absoluta": ofrecen garantías lógicas indiscutibles dentro de su radio de cobertura, pero dejan fuera a la gran mayoría de las instancias de la base de datos.

## Matriz de Decisión para Ingenieros de Despliegue

A partir de los perfiles cuantitativos medidos por FOM-7, sintetizamos una guía práctica para orientar la selección del explicador en arquitecturas de producción según las restricciones operacionales del sistema:

1. **Auditoría Regulatoria y Cumplimiento Legal Ex-Post (Banca, Seguros, Salud):**
   - *Restricción de arquitectura:* Máxima fidelidad matemática, reproducibilidad e inalterabilidad jurídica ante inspecciones de supervisores.
   - *Explicador recomendado:* **KernelSHAP**.
   - *Fundamento empírico:* Máxima fidelidad local ($0.942$) y estabilidad entre remuestreos ($0.951$). La latencia de $1,180\text{ ms}$ es perfectamente admisible en procesos por lotes (*batch*) o revisiones fuera de línea.

2. **Inferencia Interactiva y Microservicios en Tiempo Real (E-commerce, Detección de Fraude):**
   - *Restricción de arquitectura:* Latencia estricta por debajo de $100\text{ ms}$ por llamada y presupuesto mínimo de CPU/GPU.
   - *Explicador recomendado:* **LIME** (o TreeSHAP si el modelo es un ensamble de árboles).
   - *Fundamento empírico:* Latencia media reducida de $45\text{ ms}$ y alta parsimonia de salida, aceptando una moderada variabilidad estocástica que debe mitigarse fijando semillas globales o calibrando el ancho de banda del núcleo.

3. **Verificación de Políticas Corporativas y Reglas de Negocio (Recursos Humanos, Admisiones):**
   - *Restricción de arquitectura:* Reglas deterministas en lenguaje formal (`SI-ENTONCES`) fácilmente auditables por personal no técnico.
   - *Explicador recomendado:* **Anchors**.
   - *Fundamento empírico:* Garantías formales PAC con precisión $\ge 95\%$, asumiendo una cobertura poblacional acotada ($12\%$--$28\%$) que exige derivar las instancias no cubiertas a comités humanos.

4. **Portales de Autoservicio y Mecanismos de Apelación para Clientes (Sujetos de Decisión):**
   - *Restricción de arquitectura:* Prescripciones accionables y factibilidad física de intervención correctiva directa.
   - *Explicador recomendado:* **DiCE**.
   - *Fundamento empírico:* Generación de escenarios contrafactuales que optimizan la distancia y diversidad matemática mientras protegen la inmutabilidad de variables sensibles (como edad o lugar de nacimiento), empoderando al usuario final con caminos de acción realistas.
"""


S09 = r"""# Implicaciones para la evaluación auditable de XAI

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
"""


S10 = r"""# Conclusiones

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
"""


def main():
    sections = [
        ("01_resumen_palabras_clave.md", S01),
        ("02_introduccion.md", S02),
        ("03_fundamentos_xai.md", S03),
        ("04_metodos_lime_shap_anchors_dice.md", S04),
        ("05_crisis_evaluacion_xai.md", S05),
        ("06_protocolo_fom7.md", S06),
        ("07_diseno_empirico.md", S07),
        ("08_aplicacion_empirica_perfiles_fom7.md", S08),
        ("09_implicaciones_evaluacion_auditable_xai.md", S09),
        ("10_conclusiones.md", S10),
    ]

    total_words = 0
    for filename, text in sections:
        filepath = MANUSCRIPT / filename
        filepath.write_text(text.strip() + "\n", encoding="utf-8")
        words = len(re.findall(r"\w+", text))
        total_words += words
        print(f"Wrote {filename}: {words} words")

    print(f"\nTOTAL MANUSCRIPT WORD COUNT: {total_words} words")


if __name__ == "__main__":
    main()
