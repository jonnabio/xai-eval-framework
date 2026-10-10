#!/usr/bin/env python3
"""Reformat and condense the CIFIE chapter manuscript to <= 8,800 words.

Applies high-density, crisp, elegant Spanish technical prose tailored for the
Data Engineering perspective. Preserves 100% of mathematical equations, all 10
figures, both APA 7 tables, data pipeline analogies, and audit workflows while
eliminating syntactic redundancies and pleonasms.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "publications" / "book_chapters" / "2026_cifie_xai_fom7" / "manuscript"


S01 = r"""# Resumen y palabras clave

## Resumen

A medida que los sistemas de aprendizaje automático asumen decisiones críticas en finanzas, salud, empleo y justicia, comprender *por qué* un modelo emite un veredicto específico se ha convertido en un requisito indispensable de ingeniería, gobernanza y cumplimiento normativo. En la ingeniería de datos tradicional, la observabilidad se fundamenta en flujos deterministas, trazas de linaje (*data lineage*) y pruebas unitarias reproducibles. No obstante, cuando un pipeline culmina en un modelo complejo de caja negra (ensambles de árboles o redes neuronales densas), la telemetría estándar se vuelve ciega ante la lógica interna que transformó las variables de entrada en la predicción final.

Para abordar esta opacidad ha emergido la Inteligencia Artificial Explicable (*Explainable Artificial Intelligence*, XAI). Sin embargo, herramientas populares como LIME, SHAP, Anchors y DiCE a menudo entregan explicaciones divergentes, inestables o de alta latencia ante una misma instancia, evidenciando la falta de un estándar cuantitativo de evaluación.

Este capítulo ofrece un recorrido riguroso y orientado a la ingeniería sobre los métodos agnósticos de XAI, presentando el protocolo **FOM-7** (*Framework for Operational Metrics in 7 Gates*), un marco de siete puertas de control para auditar y certificar explicadores algorítmicos. Mediante un benchmark experimental sobre el conjunto de datos *UCI Adult Income*, evaluamos sistemáticamente cuatro explicadores sobre cinco familias de modelos predictivos (Regresión Logística, Árbol de Decisión, Bosque Aleatorio, XGBoost y Perceptrón Multicapa). Los resultados caracterizan la frontera de Pareto entre la alta fidelidad y estabilidad axiomática de KernelSHAP frente a la agilidad computacional de LIME, así como el valor operacional de las reglas de Anchors y los contrafactuales de DiCE. El capítulo concluye con una matriz de decisión para ingenieros y un flujo de auditoría en tres fases alineado con la Ley de IA de la Unión Europea y el marco NIST AI RMF.

## Palabras clave

Inteligencia artificial explicable; explicabilidad agnóstica; ingeniería de datos; observabilidad algorítmica; benchmarking reproducible; protocolo FOM-7; evaluación multi-métrica; explicaciones post-hoc.
"""


S02 = r"""# Introducción

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
"""


S03 = r"""# Qué es y qué no es la inteligencia artificial explicable

## Nociones fundamentales: Transparencia, interpretabilidad y explicabilidad

En la práctica técnica, los términos transparencia, interpretabilidad y explicabilidad suelen confundirse. Para diseñar controles de auditoría eficaces, es indispensable establecer distinciones operacionales precisas:

* **Transparencia:** Propiedad sistémica del entorno de ingeniería. Describe la accesibilidad del código fuente, el linaje y versiones de los datos de entrenamiento (en DVC o Delta Lake), los grafos de ejecución (DAGs en Airflow), la documentación técnica de hiperparámetros y las canalizaciones de validación cruzada (Lipton, 2018). Disponer de un repositorio abierto en Git es condición necesaria para la auditoría, pero no garantiza que un ingeniero pueda anticipar la lógica de un bosque de mil árboles.
* **Interpretabilidad:** Cualidad intrínseca de una arquitectura matemática que permite a un observador comprender de forma directa la lógica que vincula entradas y salidas (Murdoch *et al.*, 2019). Un modelo es interpretable por diseño si su estructura equivale a una instrucción SQL simple (`CASE WHEN`) o a una regresión con pocos coeficientes. Depende del dominio: una ecuación actuarial es interpretable para un estadístico, pero opaca para un usuario lego.
* **Explicabilidad:** Propiedad extrínseca y activa. Consiste en construir procedimientos secundarios, aproximaciones matemáticas o artefactos visuales —tales como vectores de pesos, reglas booleanas o escenarios contrafactuales— para interpretar a posteriori la inferencia de un clasificador demasiado complejo para ser inspeccionado directamente (Phillips *et al.*, 2021).

![Figura 1. Transparencia, interpretabilidad y explicabilidad: tres nociones distintas. Fuente: elaboración propia a partir de Lipton (2018), Murdoch *et al.* (2019), Phillips *et al.* (2021) y Tabassi (2023).](../figures/exported/fig_d1_conceptos_es.png)

Como ilustra la Figura 1, ninguna de estas dimensiones equivale automáticamente a la **confiabilidad** (*trustworthiness*). Un sistema puede generar explicaciones legibles y, sin embargo, presentar sesgos demográficos o inestabilidad ante perturbaciones menores (Tabassi, 2023).

## La trampa de la ingeniería: Atribución estadística frente a causalidad

Un error crítico en el despliegue de XAI consiste en equiparar la **atribución de características** con la **inferencia causal**.

Cuando un método post-hoc asigna un peso elevado a una variable (por ejemplo, reportando que *Antigüedad de la Cuenta* aportó $+0.32$ a la aprobación crediticia), dicho valor describe únicamente cómo el algoritmo utilizó esa columna para minimizar su función de pérdida matemática sobre la muestra de entrenamiento. No implica que ejecutar una instrucción de actualización en la base de datos (`UPDATE cuentas SET antiguedad = antiguedad + 3`) producirá en el mundo real un incremento causal en la solvencia del cliente (Pearl, 2009).

El caso clásico de predicción de mortalidad por neumonía ejemplifica este riesgo: un modelo asignó menor riesgo de muerte a pacientes con antecedentes de asma. La causa real era operacional: los pacientes asmáticos con síntomas de neumonía eran ingresados de inmediato en la Unidad de Cuidados Intensivos (UCI), recibiendo un tratamiento intensivo que reducía su letalidad. El algoritmo capturó fielmente la correlación estadística en los datos hospitalarios, y un explicador post-hoc reflejaría que el asma "protege" al paciente. Sin embargo, interpretar esa atribución como una prescripción médica causal —demorando la atención de pacientes asmáticos— sería desastroso. La explicabilidad evalúa la **fidelidad descriptiva del modelo**, no la estructura causal del fenómeno.

## Taxonomía de métodos: Intrínsecos frente a Post-hoc

El ecosistema de XAI se estructura en dos enfoques principales:

1. **Modelos intrínsecamente interpretables (*Ante-hoc* o por diseño):** Algoritmos cuya estructura matemática es transparente por construcción (regresiones lineales regularizadas, árboles de decisión simples, modelos aditivos generalizados). Garantizan fidelidad absoluta a su propia lógica sin requerir aproximaciones accesorias.
2. **Explicaciones a posteriori (*Post-hoc*):** Técnicas que operan sobre el clasificador como un objeto inmutable ya entrenado. Para modelos complejos (ensambles en XGBoost, redes neuronales densas), los métodos post-hoc construyen un sustituto local (*surrogate*) que aproxima el comportamiento del clasificador en una vecindad de interés.

![Figura 2. Del modelo interpretable por diseño a la explicación post-hoc. Fuente: elaboración propia a partir de Rudin *et al.* (2022) y Marcinkevičs y Vogt (2023).](../figures/exported/fig_d2_modelos_es.png)

Como detalla la Figura 2, los métodos post-hoc se dividen a su vez en:
* **Específicos del modelo (*Model-specific*):** Requieren acceso a estructuras internas, como gradientes de una red o topologías de árboles (TreeSHAP).
* **Agnósticos al modelo (*Model-agnostic*):** Tratan al clasificador estrictamente como una caja negra a través de su interfaz de inferencia ($x \to f(x)$), enviando entradas perturbadas y analizando las salidas resultantes sin asumir ninguna estructura interna (Marcinkevičs & Vogt, 2023).

## Alcance operacional: Explicaciones Locales frente a Globales

En la arquitectura de sistemas analíticos, el alcance determina la escala espacial a la que aplica la información obtenida:

* **Alcance Local (*Local Interpretability*):** Explica la inferencia para un registro específico (*¿Por qué el modelo denegó la transacción #8812 de este cliente?*).
* **Alcance Global (*Global Interpretability*):** Resume la lógica estructural del clasificador en toda la población (*¿Cuáles son los atributos dominantes del modelo para toda la cartera?*).

Un principio de ingeniería fundamental: **la suma de explicaciones locales no equivale a una explicación global válida**. Debido a las fronteras de decisión no lineales y a las interacciones complejas, promediar las atribuciones locales de miles de registros puede enmascarar dinámicas locales contrapuestas y generar conclusiones erróneas.

## Niveles de evaluación científica: La posición de FOM-7

Doshi-Velez y Kim (2017) definieron una taxonomía de tres niveles que ordena los métodos según su grado de intervención humana y costo experimental:

1. **Evaluación basada en la aplicación (*Application-grounded*):** Expertos del dominio (como patólogos o analistas de crédito) toman decisiones en su flujo diario de trabajo apoyándose en las explicaciones, evaluando si mejora su rendimiento real.
2. **Evaluación basada en humanos (*Human-grounded*):** Pruebas de laboratorio con usuarios legos evaluando tareas abstractas (por ejemplo, elegir entre dos predicciones según la claridad del gráfico).
3. **Evaluación funcionalmente fundamentada (*Functionally-grounded*):** Métricas computacionales objetivas y proxies matemáticos deterministas (fidelidad de reconstrucción, estabilidad ante ruido gaussiano, parsimonia y tiempo de CPU por inferencia) sobre datasets estandarizados, sin pruebas con usuarios.

![Figura 4. Niveles de evaluación de la explicabilidad y posición de FOM-7. Fuente: adaptada de Doshi-Velez y Kim (2017).](../figures/exported/fig_d6_niveles_evaluacion_es.png)

Como muestra la Figura 4, el protocolo **FOM-7** se ubica en el nivel de **evaluación funcionalmente fundamentada**. Esta decisión equivale a implementar pruebas unitarias y de integración en software: antes de exponer un componente a pruebas de usuario (*UAT*), el equipo de ingeniería debe certificar que cumple estándares cuantitativos mínimos de estabilidad, fidelidad y rendimiento.
"""


S04 = r"""# Métodos de explicabilidad: LIME, SHAP, Anchors y DiCE

## Diversidad de artefactos explicativos

En el desarrollo de software analítico, los métodos agnósticos post-hoc producen diferentes **objetos explicativos** según las necesidades del destinatario:

1. **Atribuciones numéricas continuas de características:** Vectores de números reales que ponderan la contribución positiva o negativa de cada variable a la predicción puntual (LIME, KernelSHAP).
2. **Reglas de decisión booleanas:** Condiciones condicionales (`SI x1 > 3 AND x2 = 'A' ENTONCES predicción = 1`) que delimitan una región de certeza inalterable (Anchors).
3. **Explicaciones contrafactuales prescriptivas:** Muestras sintéticas que indican la alteración mínima en los datos de entrada requerida para conmutar la predicción del modelo hacia una categoría deseada (DiCE).

![Figura 3. Cuatro objetos explicativos y métodos agnósticos evaluados en FOM-7. Fuente: elaboración propia a partir de Ribeiro *et al.* (2016, 2018), Lundberg y Lee (2017) y Mothilal *et al.* (2020).](../figures/exported/fig_d4_objetos_explicativos_es.png)

La Figura 3 sintetiza estos cuatro objetos explicativos y sus algoritmos representativos. A continuación se detallan sus mecanismos, ecuaciones y consideraciones de ingeniería.

## LIME: Explicaciones locales interpretables agnósticas al modelo

Propuesto por Ribeiro *et al.* (2016), **LIME** (*Local Interpretable Model-agnostic Explanations*) asume que, aunque una función de aprendizaje automático $f(x)$ sea no lineal a escala global, **en la vecindad inmediata de un punto $x$ la frontera de decisión puede aproximarse mediante un plano tangente lineal simple** ($g \in G$).

### Mecanismo algorítmico

Para construir la aproximación local alrededor de un registro $x$:
1. **Generación de perturbaciones:** Genera $K$ muestras sintéticas $z'$ en el entorno de $x$ aplicando ruido gaussiano sobre variables continuas y remuestreo sobre categóricas.
2. **Evaluación de la caja negra:** Envía las muestras $z'$ al clasificador primario para obtener sus probabilidades predichas $f(z')$.
3. **Ponderación por proximidad:** Asigna a cada muestra sintética $z'$ un peso $\pi_x(z)$ mediante un núcleo exponencial basado en la distancia $D(x, z)$ (euclidiana o coseno):
$$\pi_x(z) = \exp\left( -\frac{D(x, z)^2}{\sigma^2} \right)$$
donde $\sigma$ es el ancho de banda del núcleo.
4. **Ajuste del modelo sustituto:** Ajusta una regresión lineal resolviendo:
$$\xi(x) = \arg\min_{g \in G} \mathcal{L}(f, g, \pi_x) + \Omega(g)$$
donde $\mathcal{L}$ mide el error cuadrático ponderado entre $f(z)$ y $g(z)$, y $\Omega(g)$ es una penalización L1 (Lasso) que fuerza a que solo un subconjunto reducido de variables conserve coeficientes no nulos.

### Riesgo operacional: Muestras fuera de distribución (*OOD*)

Desde la perspectiva de la ingeniería de datos, el punto débil de LIME reside en perturbar columnas de forma independiente. Este procedimiento genera registros sintéticos que pueden violar la integridad lógica del esquema (por ejemplo, combinando `Edad = 18` con `Años_Estudio = 22`). Al recibir instancias situadas en zonas vacías del espacio de datos (*Out-of-Distribution*, OOD), el clasificador devuelve predicciones atípicas que pueden sesgar los coeficientes del sustituto lineal.

## SHAP: Explicaciones aditivas basadas en teoría de juegos cooperativos

Desarrollado por Lundberg y Lee (2017), **SHAP** (*SHapley Additive exPlanations*) formula la atribución de características transformando el problema en un juego cooperativo de teoría de juegos (Shapley, 1953).

### Intuición para el ingeniero de datos

Imagine que cuatro columnas de una tabla (`Ingresos`, `Puntaje_Crediticio`, `Edad`, `Deuda`) colaboran para emitir una probabilidad $f(x) = 0.85$, superando la media base $\mathbb{E}[f(X)] = 0.50$. La diferencia a explicar es de $+0.35$. El aporte marginal de `Puntaje_Crediticio` en solitario puede ser $+0.20$; pero si `Ingresos` ya forma parte del subconjunto evaluado, su aporte puede reducirse a $+0.08$ debido a la redundancia informacional entre ambas.

Shapley resuelve esta asignación calculando el **aporte marginal promedio de cada variable a través de todas las posibles combinaciones o coaliciones** de características:

$$\phi_i(x) = \sum_{S \subseteq F \setminus \{i\}} \frac{\vert S \vert ! (\vert F \vert - \vert S \vert - 1)!}{\vert F \vert !} \left[ f_x(S \cup \{i\}) - f_x(S) \right]$$

donde $F$ es el conjunto de características, $S$ es una coalición que no contiene a la variable $i$, y $f_x(S)$ es la predicción esperada condicionada a los valores observados en $S$.

### Los cuatro axiomas de Shapley

SHAP es el **único** método de atribución local que satisface cuatro propiedades axiomáticas concurrentes:
1. **Eficiencia (Aditividad local):** La suma de los valores de Shapley reproduce la desviación entre la predicción local y el valor esperado poblacional: $\sum_{i=1}^{\vert F \vert} \phi_i(x) = f(x) - \mathbb{E}[f(X)]$.
2. **Simetría:** Si dos columnas aportan lo mismo a todas las coaliciones, reciben idéntico valor de atribución ($\phi_i = \phi_j$).
3. **Jugador nulo (*Dummy*):** Si una columna no modifica la predicción en ninguna coalición, su contribución es cero ($\phi_i = 0$).
4. **Monotonicidad (Consistencia):** Si la contribución marginal de una variable no disminuye en un modelo alternativo, su valor atribuido no puede decrecer.

### Costo computacional: La explosión combinatoria y KernelSHAP

Para $M$ variables existen $2^M$ posibles coaliciones. Con $M=10$ columnas se requieren $1,024$ evaluaciones; con $M=30$, el cálculo exacto exige más de mil millones de combinaciones ($2^{30} \approx 1.07 \times 10^9$), resultando intratable.

Para cajas negras genéricas, **KernelSHAP** resuelve esta barrera estimando los valores mediante regresión lineal ponderada utilizando un núcleo combinatorio específico $\pi(z')$:

$$\pi(z') = \frac{|F| - 1}{\binom{|F|}{|z'|} |z'| (|F| - |z'|)}$$

donde $|z'|$ es el número de características presentes en la muestra sintética. Este núcleo asigna el peso máximo a coaliciones con muy pocas o casi todas las variables presentes, que es donde el impacto marginal resulta más informativo. Aunque viabiliza el cálculo, su latencia media ronda los $1,180\text{ ms}$ por registro. Resulta idóneo para auditorías periódicas por lotes (*batch*), pero prohibitivo para microservicios en tiempo real con alta concurrencia.

## Anchors: Reglas condicionales con garantías formales

A diferencia de los vectores continuos, **Anchors** (Ribeiro *et al.*, 2018) genera explicaciones estructuradas como reglas de decisión lógicas `SI-ENTONCES`.

Una regla $A$ (el "ancla") es un conjunto de predicados booleanos sobre las variables de entrada (por ejemplo, $\text{Edad} > 35 \land \text{Estado\_Civil} = \text{Casado}$). La regla es válida si garantiza que, mientras se cumplan dichos predicados, la predicción del modelo se mantendrá invariable con una certeza probabilística formal bajo el marco PAC (*Probably Approximately Correct*):

$$P\left( \text{prec}(A) \ge 1 - \gamma \right) \ge 1 - \delta$$

donde la precisión local $\text{prec}(A)$ mide la proporción de perturbaciones locales $z$ que preservan la predicción original:

$$\text{prec}(A) = \mathbb{E}_{z \sim D(z|A)} \left[ \mathbb{I}(f(x) = f(z)) \right]$$

aquí $\gamma$ es la tolerancia de error ($0.05$ para $95\%$ de precisión), y $\delta$ representa el nivel de significancia estadística.

El algoritmo busca maximizar la **cobertura** (*coverage*) de la regla en la población:

$$\text{cov}(A) = P_{z \sim D}(A(z) = 1)$$

Anchors implementa una búsqueda por haces (*beam search*) guiada por bandidos multi-brazo (*Multi-Armed Bandits*), explorando eficientemente el espacio combinatorio de reglas candidatas sin evaluar innecesariamente el clasificador.

## DiCE: Explicaciones contrafactuales diversas y recurso accionable

Propuesto por Mothilal *et al.* (2020), **DiCE** (*Diverse Counterfactual Explanations*) adopta un enfoque prescriptivo: responde a la pregunta del usuario: *¿Cuál es el cambio mínimo en mis variables que lograría que el modelo apruebe la solicitud?*

En producción, un contrafactual debe respetar restricciones de ingeniería indispensables:
* **Variables inmutables:** Atributos como la *Edad* o el *País de Origen* no pueden ser modificados.
* **Dirección monótona:** La *Antigüedad Laboral* solo puede aumentar.
* **Rangos factibles:** Evitar combinaciones imposibles (como jornadas de 120 horas semanales).

Dado un punto $x$ y una clase deseada $y^*$, DiCE optimiza un conjunto de $k$ contrafactuales $\{c_1, \dots, c_k\}$ resolviendo:

$$\min_{c_1, \dots, c_k} \frac{1}{k} \sum_{i=1}^k \mathcal{L}_{loss}(f(c_i), y^*) + \frac{\lambda_1}{k} \sum_{i=1}^k \text{dist}(x, c_i) - \lambda_2 \text{dpp}(c_1, \dots, c_k)$$

donde:
* $\mathcal{L}_{loss}$ penaliza contrafactuales que no alcancen la clase $y^*$.
* $\text{dist}(x, c_i)$ fuerza a que las modificaciones requeridas sean mínimas (distancia L1 para continuas y Hamming para categóricas).
* $\text{dpp}(c_1, \dots, c_k) = \det(\mathbf{K})$ promueve la diversidad mediante Procesos de Determinantes Puntos (*Determinantal Point Processes*), donde $\mathbf{K}$ es una matriz semidefinida positiva cuyas entradas $K_{i,j} = \frac{1}{1 + \text{dist}(c_i, c_j)}$ capturan la proximidad mutua; maximizar el determinante equivale a maximizar el volumen espacial cubierto, garantizando alternativas cualitativamente distintas.

## Compromisos operacionales entre explicadores

La selección de un explicador exige asumir compromisos de diseño (*trade-offs*):

![Figura 5. Marco sintético de trade-offs operacionales en evaluación post-hoc de XAI. Fuente: elaboración propia a partir de Tabassi (2023) y Phillips *et al.* (2021).](../figures/exported/fig_d5_ciclo_audiencias_es.png)

Como resume la Figura 5:
* **KernelSHAP:** Máxima solidez axiomática y fidelidad local, a costa de una latencia computacional elevada ($>1\text{ s}$ por instancia).
* **LIME:** Inferencias veloces ($<50\text{ ms}$) y alta parsimonia, sujeto a inestabilidad estocástica y sensibilidad a muestras OOD.
* **Anchors:** Reglas deterministas de certidumbre formal inalterable, con cobertura poblacional acotada ($12\%$--$28\%$).
* **DiCE:** Alto valor prescriptivo para el usuario final, requiriendo optimizaciones numéricas iterativas con restricciones de dominio.
"""


S05 = r"""# Crisis de evaluación en XAI

## La crisis de confiabilidad en explicabilidad post-hoc

En la ingeniería de software, un módulo se valida mediante aserciones deterministas (`assert output == expected`). En aprendizaje supervisado, el rendimiento se comprueba contrastando predicciones con etiquetas reales (*ground truth*).

En la explicabilidad post-hoc nos encontramos ante una **crisis de evaluación estructural**: **no existe una etiqueta de referencia sobre cómo razona internamente una caja negra** (Krishna *et al.*, 2022; Nauta *et al.*, 2023; Agarwal *et al.*, 2023). Ante la ausencia de un patrón oro, los equipos han incurrido a menudo en dos prácticas metodológicamente vulnerables:
1. **La trampa de la plausibilidad intuitiva:** Asumir que una explicación es correcta si las variables destacadas confirman las expectativas previas del analista (sesgo de confirmación).
2. **La métrica endógena circular:** Evaluar un explicador utilizando las mismas métricas para las que fue optimizado algorítmicamente.

![Figura 6. Anatomía de la crisis de evaluación en explicabilidad post-hoc. Fuente: elaboración propia a partir de Krishna *et al.* (2022), Nauta *et al.* (2023) y Agarwal et al. (2023).](../figures/exported/fig_d7_cadena_evidencia_es.png)

La Figura 6 sintetiza esta crisis: desplegar un explicador sin controles cuantitativos independientes introduce un segundo componente opaco dentro de la arquitectura de supervisión.

## Taxonomía de riesgos y patologías operacionales

Para un ingeniero de datos que gestiona pipelines en producción, las fallas de los explicadores post-hoc se agrupan en cuatro patologías críticas:

### 1. El Efecto Rashomon en explicaciones
Inspirado en el fenómeno formulado por Breiman (2001), ocurre cuando múltiples modelos sustitutos obtienen un ajuste numérico equivalente respecto a la caja negra, pero presentan **jerarquías de atributos contradictorias**. Ambos sustitutos son válidos en términos de optimización cuadrática, pero uno señala a la *Edad* como variable dominante y el otro a la *Deuda*. En una auditoría regulatoria, esta discrepancia invalida la credibilidad técnica del sistema.

### 2. Inestabilidad estocástica y contratos de reproducibilidad
En ingeniería de datos, la reproducibilidad es un requisito ineludible: procesar el mismo registro con el mismo pipeline debe producir idéntico resultado. Sin embargo, al depender de muestreos de Monte Carlo, **ejecutar dos veces LIME o KernelSHAP sobre la misma instancia con diferente semilla aleatoria puede alterar el orden de los factores explicativos**. En entornos corporativos donde las explicaciones se persisten en tablas de auditoría, esta volatilidad estocástica genera inconsistencias operativas graves.

### 3. Deformación por muestreo fuera de distribución (*OOD*)
Al perturbar variables de forma independiente para estimar derivadas locales, los explicadores generan combinaciones sintéticas que violan las correlaciones del esquema relacional (por ejemplo, salarios ejecutivos con empleos no cualificados). Los modelos, al recibir estas filas anómalas, devuelven probabilidades erráticas que distorsionan los coeficientes de atribución resultantes.

### 4. Vulnerabilidad adversarial: Modelos con "andamios" (*Scaffolding Models*)
Slack *et al.* (2020) demostraron que los explicadores agnósticos pueden manipularse deliberadamente. Es posible entrenar un clasificador con una bifurcación lógica oculta:
* Aplica una lógica discriminatoria sobre consultas reales provenientes de la distribución operativa.
* Conmuta hacia un modelo neutral cuando detecta la dispersión sintética característica de las perturbaciones de LIME o SHAP.

Como resultado, el explicador emite un reporte de auditoría impecable certificando equidad, mientras el modelo discrimina activamente en producción.

![Figura 7. Taxonomía de distorsiones y traza de siete puertas FOM-7. Fuente: elaboración propia a partir de Herrera-Vásquez y Herrero-Uceda (2026).](../figures/exported/fig_d8_fom7_traza_es.png)

La Figura 7 muestra cómo cada una de las siete puertas del protocolo FOM-7 actúa como una barrera técnica de contención ante estas fallas operacionales.
"""


S06 = r"""# El protocolo operativo FOM-7

## El concepto: Un harness de pruebas automatizadas para XAI

En la ingeniería de datos moderna, la calidad de los pipelines se asegura mediante frameworks como `pytest`, `dbt test` o `Great Expectations`, que verifican aserciones concretas sobre los datos (completitud, unicidad, rangos de distribución) antes de autorizar su consumo.

El marco **FOM-7** (*Framework for Operational Metrics in 7 Gates*) traslada este principio al ámbito de la explicabilidad algorítmica. Concebido como un **harness de certificación cuantitativa estructurado en siete puertas de control secuenciales**, FOM-7 evalúa si un explicador post-hoc es matemáticamente fiel, estable, legible, eficiente y equitativo:

* **Puerta 1 (G1) - Fidelidad Local (*Fidelity Gate*):** Precisión con la que el sustituto interpretable $g$ reproduce las predicciones del clasificador primario $f$ en la vecindad del registro auditado.
* **Puerta 2 (G2) - Estabilidad y Robustez (*Stability Gate*):** Resistencia del explicador ante perturbaciones leves de entrada y ruidos sensoriales.
* **Puerta 3 (G3) - Parsimonia Cognitiva (*Parsimony Gate*):** Brevedad de la explicación ($\le 7$ características relevantes) para garantizar comprensibilidad humana sin sobrecarga.
* **Puerta 4 (G4) - Cobertura y Accionabilidad (*Coverage Gate*):** Proporción de la población cubierta por la regla (Anchors) o factibilidad física de los cambios prescritos (DiCE).
* **Puerta 5 (G5) - Eficiencia Computacional (*Efficiency Gate*):** Cumplimiento de los SLAs de infraestructura ($<100\text{ ms}$ para APIs interactivas, $<2,000\text{ ms}$ para auditorías batch).
* **Puerta 6 (G6) - Consistencia Inter-método (*Cross-Explainer Consistency Gate*):** Grado de concordancia entre distintos explicadores sobre una misma instancia.
* **Puerta 7 (G7) - Equidad en la Explicación (*Explanatory Fairness Gate*):** Homogeneidad de fidelidad y estabilidad a través de subgrupos demográficos protegidos.

## Formulaciones matemáticas de las métricas de evaluación

A continuación se presentan las formulaciones cuantitativas computables de cada compuerta:

### 1. Fidelidad Local Ponderada (G1)

Evalúa el coeficiente de determinación local entre el sustituto explicativo $g(z)$ y el modelo original $f(z)$ sobre el conjunto de perturbaciones $Z_x$, ponderado por la proximidad $\pi_x(z)$:

$$\text{Fidelidad}(g, f, x) = 1 - \frac{\sum_{z \in Z_x} \pi_x(z) \left( f(z) - g(z) \right)^2}{\sum_{z \in Z_x} \pi_x(z)}$$

Un valor de $1.0$ representa una réplica perfecta de la frontera local; valores inferiores a $0.85$ indican un desacoplamiento inaceptable respecto al clasificador real.

### 2. Estabilidad Local basada en la Constante de Lipschitz y Similitud Coseno (G2)

Teóricamente, la estabilidad se define acotando la constante de Lipschitz del operador explicativo $E(x) \in \mathbb{R}^{\vert F \vert}$ en una bola de radio $\epsilon$:

$$\text{Estabilidad}(E, x, \epsilon) = 1 - \max_{x' : \Vert x - x' \Vert_2 \le \epsilon} \frac{\Vert E(x) - E(x') \Vert_2}{\Vert x - x' \Vert_2}$$

Para viabilizar este cómputo de manera determinista y escalable en producción, FOM-7 calcula la **similitud coseno media** entre vectores de atribución obtenidos bajo perturbaciones gaussianas controladas ($\sigma_{\text{ruido}} = 0.05 \cdot \sigma_X$):

$$\text{Estabilidad}_{\text{cos}}(E, x) = \frac{1}{B} \sum_{b=1}^B \frac{E(x) \cdot E(x + \delta_b)}{\Vert E(x) \Vert_2 \, \Vert E(x + \delta_b) \Vert_2}$$

donde $B$ es el número de muestras de validación y $\delta_b \sim \mathcal{N}(0, \sigma^2 I)$. Un valor próximo a $1.0$ garantiza que ruidos menores no alterarán la jerarquía de factores reportados.

### 3. Parsimonia y Escasez de Coeficientes (G3)

Mide la fracción de variables cuya atribución absoluta cae por debajo de un umbral de significancia práctica $\tau$:

$$\text{Escasez}(E(x), \tau) = \frac{1}{\vert F \vert} \sum_{i=1}^{\vert F \vert} \mathbb{I}(\vert \phi_i(x) \vert \le \tau)$$

### 4. Cobertura Empírica de Reglas (G4)

Para métodos basados en predicados condicionales (Anchors), cuantifica la proporción de registros del conjunto de prueba $N$ que satisfacen los antecedentes del ancla $A$:

$$\text{Cobertura}(A) = \frac{1}{N} \sum_{j=1}^{N} \mathbb{I}(A(x_j) = 1)$$

### 5. Latencia Computacional Media (G5)

Tiempo medio de CPU/GPU $t(E, x_k)$ requerido para generar la explicación de una instancia sobre un lote de $M$ casos:

$$\bar{T}_{exp} = \frac{1}{M} \sum_{k=1}^{M} t(E, x_k) \quad [\text{ms/instancia}]$$

### 6. Consistencia Inter-método (G6)

Mide la correlación de rangos de Spearman entre los vectores de atribución generados por dos explicadores $E_1$ y $E_2$ sobre la misma instancia:

$$\text{Consistencia}(E_1, E_2, x) = 1 - \frac{6 \sum_{i=1}^{|F|} d_i^2}{|F| (|F|^2 - 1)}$$

donde $d_i$ es la diferencia entre los rangos asignados a la característica $i$.

### 7. Equidad en la Explicación (G7)

Evalúa la paridad en la fidelidad local media entre subgrupos demográficos protegidos (como género o etnia), aplicando el criterio regulatorio de la regla de los cuatro quintos:

$$\text{Paridad}(G_1) = \min_{a, b \in \mathcal{A}} \frac{\bar{G}_1(A = a)}{\bar{G}_1(A = b)} \ge 0.80$$

## Criterios de Aprobación para Auditoría de Producción

Para que un pipeline de inferencia sea certificado para producción bajo el protocolo FOM-7, debe satisfacer concurrentemente:

* **Umbral de Fidelidad:** $\text{Fidelidad} \ge 0.85$ (G1), impidiendo que el explicador emita aproximaciones espurias.
* **Umbral de Estabilidad:** $\text{Estabilidad} \ge 0.80$ (G2), asegurando que ruidos instrumentales no alteren el veredicto explicativo.
* **Presupuesto de Latencia:** $\bar{T}_{exp} \le 100\text{ ms}$ para microservicios interactivos, o $\bar{T}_{exp} \le 2,000\text{ ms}$ para auditorías batch.

La Tabla 1 consolida las especificaciones técnicas de cada compuerta del protocolo FOM-7.

<!-- TABLA: table_metrics.md -->
"""


S07 = r"""# Diseño empírico y banco de pruebas

## El banco de datos de prueba: UCI Adult Income

Para validar experimentalmente el protocolo **FOM-7**, se diseñó un banco de pruebas sobre el conjunto de datos tabular *UCI Adult Income* (Kohavi, 1996), estándar de referencia en la literatura de aprendizaje automático tabular y equidad algorítmica.

El dataset contiene $32,561$ registros y $14$ variables socioeconómicas:
* **Variables numéricas continuas (6):** *Edad*, *Educación Numérica* (años completados), *Ganancia de Capital*, *Pérdida de Capital*, *Horas Semanales* y *Ponderador Muestral (fnlwgt)*.
* **Variables categóricas (8):** *Sector de Empleo (Workclass)*, *Nivel Educativo (Education)*, *Estado Civil*, *Ocupación*, *Rol Familiar*, *Raza*, *Sexo* y *País de Origen*.
* **Variable objetivo binaria ($Y$):** Ingresos anuales superiores a $\$50,000$ dólares ($Y = 1$ si $>50\text{K}$, $Y = 0$ en caso contrario), con una prevalencia positiva del $24.08\%$.

## Canalización de preprocesamiento y partición

La preparación de datos siguió una canalización rigurosa para prevenir fuga de información (*data leakage*):
1. **Limpieza e imputación:** Valores ausentes en variables categóricas fueron imputados utilizando la moda condicionada por estrato demográfico.
2. **Codificación y escalado:** Variables categóricas transformadas mediante *One-Hot Encoding*, expandiendo el espacio dimensional a $104$ columnas binarias. Variables continuas estandarizadas mediante $z$-score ($\mu = 0, \sigma = 1$).
3. **Partición estratificada:** División estratificada $80/20$, asignando $26,048$ instancias para entrenamiento y reservando un conjunto de prueba independiente de $6,513$ registros para evaluar las siete puertas de FOM-7 en cinco bloques de tamaño muestral ($n \in \{50, 100, 200, 500, 1000\}$).

## Familias de modelos predictivos evaluadas

Se entrenaron cinco familias de clasificadores con distintos niveles de no linealidad y opacidad:
1. **Regresión Logística (LR):** Modelo lineal convexo con regularización L2 ($C=1.0$), utilizado como línea base interpretable ($AUC = 0.852$).
2. **Árbol de Decisión (DT):** Modelo no lineal ortogonal con criterio Gini restringido a profundidad $d=5$ ($AUC = 0.841$).
3. **Bosque Aleatorio (RF):** Ensamble *bagging* no lineal de 100 árboles de decisión no podados con submuestreo de $\sqrt{p}$ variables ($AUC = 0.898$).
4. **XGBoost (XGB):** Ensamble *gradient boosting* con 100 estimadores secuenciales, profundidad $d=6$, tasa $\eta = 0.1$ y regularización L2 ($AUC = 0.917$).
5. **Perceptrón Multicapa (MLP):** Red neuronal densa de 3 capas ocultas (64 neuronas cada una) con activaciones ReLU y optimizador Adam ($AUC = 0.891$).

## Entorno de ejecución y reproducibilidad

Las pruebas se ejecutaron en Python 3.10 sobre una estación de trabajo AMD Ryzen 9 5900X (12 núcleos, 24 hilos) con 64 GB de RAM, fijando una semilla global determinista (`seed=42`) para garantizar la reproducibilidad exacta de los muestreos.

## Protocolo de significancia estadística: Pruebas de Friedman y Nemenyi

Para determinar si las diferencias observadas en las métricas de FOM-7 reflejan superioridad algorítmica real y no fluctuaciones muestrales, se aplicó el protocolo no paramétrico de Demšar (2006):

1. **Prueba de rangos alineados de Friedman:** Evalúa la hipótesis nula ($H_0$) de rendimiento equivalente en rangos promedio across experimental blocks:
$$\chi_F^2 = \frac{12N}{k(k+1)} \left[ \sum_{j=1}^k R_j^2 - \frac{k(k+1)^2}{4} \right]$$
donde $k=4$ explicadores, $N=15$ condiciones experimentales (cruces de modelos y tamaños de muestra), y $R_j$ es el rango medio del explicador $j$.
2. **Prueba post-hoc de Diferencia Crítica de Nemenyi:** Tras rechazar $H_0$ ($p < 0.001$), se calcula la Diferencia Crítica ($CD$) a nivel $\alpha = 0.05$:
$$CD = q_\alpha \sqrt{\frac{k(k+1)}{6N}}$$
donde el valor crítico de rango studentizado es $q_{0.05} = 2.569$ para $k=4$. Si la distancia entre rangos promedio de dos métodos supera estrictamente $CD$, la superioridad queda estadísticamente demostrada.
"""


S08 = r"""# Aplicación empírica: Perfiles FOM-7

## Resultados consolidados del benchmark empírico

A continuación se presentan los resultados consolidados tras someter a LIME, KernelSHAP, Anchors y DiCE a las pruebas de **FOM-7** sobre las cinco familias de modelos entrenadas en *UCI Adult Income*.

<!-- TABLA: table_results_summary.md -->

La Tabla 2 reúne los promedios observados en las compuertas principales. Se observa que la complejidad arquitectónica del clasificador afecta de manera dispar a cada explicador: mientras que KernelSHAP sostiene niveles elevados de fidelidad en todas las familias ($0.942$ en XGBoost, $0.938$ en Random Forest, $0.929$ en MLP), LIME experimenta una degradación notable al transicionar desde modelos lineales ($0.912$ en LR) hacia redes no lineales ($0.854$ en MLP).

## Análisis empírico detallado por Puertas FOM-7

### 1. Fidelidad Local (G1) y Diagrama de Diferencia Crítica de Nemenyi

**KernelSHAP** alcanza los niveles de fidelidad local ponderada más altos en todos los clasificadores evaluados, superando sistemáticamente a LIME.

![Figura 9. Diagrama de diferencia crítica (CD) de Nemenyi para ranking de fidelidad post-hoc. Fuente: elaboración propia.](../figures/exported/fig_cd_diagram_es.png)

#### Interpretación del Diagrama de Diferencia Crítica (Figura 9)
* El eje horizontal muestra los rangos promedio asignados a cada método (valores más a la izquierda indican mejor desempeño).
* La barra horizontal superior marca la longitud del umbral crítico $CD$.
* **Regla de lectura:** Dos algoritmos conectados por una barra negra horizontal no presentan diferencias estadísticamente significativas. Si no están unidos, la diferencia en su rendimiento es estadísticamente demostrable con un $95\%$ de confianza.

La Figura 9 ratifica que KernelSHAP ocupa el primer lugar en fidelidad sin conexión de indiferencia con LIME, demostrando con significancia estadística su superioridad para reconstruir la frontera de decisión local del clasificador.

### 2. Estabilidad Local (G2) frente a Costo Computacional (G5): La Frontera de Pareto

El estudio demuestra empíricamente el compromiso estructural entre la **estabilidad de las atribuciones** y la **latencia computacional requerida**.

![Figura 10. Frontera de Pareto entre estabilidad y costo computacional de explicadores post-hoc. Fuente: elaboración propia.](../figures/exported/fig_estabilidad_coste_es.png)

#### Interpretación de la Frontera de Pareto (Figura 10)
* **LIME** se ubica en el cuadrante de alta velocidad: consume $\bar{T}_{exp} = 45\text{ ms}$ por registro, pero exhibe la menor estabilidad del benchmark ($\text{Estabilidad} = 0.724$), mostrando fluctuaciones ante ruidos leves.
* **KernelSHAP** se sitúa en el extremo de máxima robustez: alcanza estabilidad cuasi-óptima ($\text{Estabilidad} = 0.951$), pero impone un costo computacional 25 veces superior ($\bar{T}_{exp} = 1,180\text{ ms}$).
* **Anchors y DiCE** ocupan zonas intermedias y especializadas de la frontera eficiente, orientadas a reglas lógicas y contrafactuales.

### 3. Cobertura Empírica frente a Precisión de Reglas (G4 - EXP2)

Para **Anchors**, se analizó la relación entre la exigencia de precisión probabilística y la cobertura de registros en el conjunto de prueba (EXP2).

![Figura 8. Análisis de cobertura empírica e interpretabilidad práctica de reglas Anchors (EXP2). Fuente: elaboración propia.](../figures/exported/fig_cobertura_exp2_es.png)

La Figura 8 grafica esta curva: al exigir precisión rigurosa ($\text{prec} \ge 0.95$), la cobertura empírica de las reglas se contrae, cubriendo entre el $12\%$ y el $28\%$ de los registros. Las reglas de Anchors actúan como "islas de certidumbre absoluta": ofrecen garantías lógicas indiscutibles dentro de su radio, pero dejan sin cobertura a la mayoría de las instancias.

## Matriz de Decisión para Ingenieros de Despliegue

Sintetizamos una guía para orientar la selección del explicador en arquitecturas de producción:

1. **Auditoría Regulatoria Ex-Post (Banca, Seguros, Salud):**
   - *Restricción:* Máxima fidelidad matemática, reproducibilidad e inalterabilidad jurídica.
   - *Recomendación:* **KernelSHAP** (Fidelidad $0.942$, Estabilidad $0.951$). La latencia de $1,180\text{ ms}$ es admisible en procesos por lotes (*batch*).
2. **Inferencia Interactiva y Microservicios en Tiempo Real (E-commerce, Detección de Fraude):**
   - *Restricción:* Latencia $<100\text{ ms}$ por llamada y presupuesto mínimo de CPU/GPU.
   - *Recomendación:* **LIME** (o TreeSHAP si el modelo es un ensamble de árboles). Latencia de $45\text{ ms}$ y alta parsimonia, mitigando su variabilidad con semillas fijas.
3. **Control de Políticas Corporativas y Cumplimiento (Recursos Humanos, Admisiones):**
   - *Restricción:* Reglas deterministas en lenguaje formal (`SI-ENTONCES`) comprensibles por comités no técnicos.
   - *Recomendación:* **Anchors** (Garantías PAC con precisión $\ge 95\%$), derivando los casos fuera de cobertura ($>70\%$) a revisión experta.
4. **Portales de Autoservicio y Apelaciones (Sujetos de Decisión):**
   - *Restricción:* Prescripciones accionables respetando variables inmutables.
   - *Recomendación:* **DiCE** (Contrafactuales diversos con mutabilidad restringida para guiar al usuario final).
"""


S09 = r"""# Implicaciones para la evaluación auditable de XAI

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
"""


S10 = r"""# Conclusiones

## Síntesis de aportaciones

Este capítulo ha demostrado que la explicabilidad algorítmica representa la **capa de observabilidad indispensable** para auditar y gobernar modelos complejos en entornos de alta responsabilidad.

A través del protocolo **FOM-7** y de su validación empírica en *UCI Adult Income*, este trabajo aporta:
1. **Un marco conceptual desmitificado:** Se establecieron fronteras operacionales nítidas entre transparencia, interpretabilidad intrínseca y explicabilidad post-hoc, deslindando la atribución estadística de la causalidad real en bases de datos.
2. **Un benchmark multi-métrica y reproducible:** Se caracterizaron cuantitativamente las fortalezas y compromisos de LIME, KernelSHAP, Anchors y DiCE sobre cinco familias de clasificadores, demostrando estadísticamente la superioridad de KernelSHAP en fidelidad y caracterizando la frontera de Pareto entre estabilidad y costo computacional.
3. **Una guía de ingeniería aplicada:** Se formalizaron umbrales numéricos de aprobación, una matriz de decisión para la selección de explicadores y un flujo de auditoría en tres fases alineado con la Ley de IA de la UE y el marco NIST AI RMF.

## Alcance, limitaciones y agenda futura

Reconociendo el alcance acotado de todo estudio experimental riguroso, identificamos las principales limitaciones del presente trabajo y las líneas de desarrollo prioritarias:

* **Extensión a datos no estructurados y Modelos de Lenguaje (LLMs):** El benchmark se focalizó en datos tabulares estructurados. Las investigaciones futuras adaptarán las ecuaciones de FOM-7 a visión por computadora y a modelos masivos de lenguaje (*Large Language Models*, LLMs), donde las perturbaciones semánticas en incrustaciones (*embeddings*) y los mecanismos de atención plantean nuevos desafíos de estabilidad y latencia.
* **Integración con estudios de cognición humana (Niveles 1 y 2):** Tras consolidar la evaluación funcionalmente fundamentada de Nivel 3 en la jerarquía de Doshi-Velez y Kim (2017), los trabajos siguientes vincularán las métricas de FOM-7 con pruebas de usabilidad y comprensión cognitiva con operadores humanos en entornos clínicos y financieros.

## Reflexión final

La explicabilidad algorítmica no es un fin en sí misma: es el instrumento técnico para asegurar que el poder analítico del aprendizaje automático opere bajo supervisión transparente, defendible y centrada en el ser humano. Al dotar a los equipos de ingeniería de un protocolo computable y fundamentado como **FOM-7**, este capítulo aporta una base práctica para transitar desde la opacidad de los algoritmos hacia una supervisión verdaderamente responsable.
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
