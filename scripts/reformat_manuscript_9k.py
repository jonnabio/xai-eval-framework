#!/usr/bin/env python3
"""Reformat and streamline the CIFIE chapter manuscript to ~9,000 words.

Applies a narrative storytelling flow across 10 manuscript sections (01..10),
incorporates all 10 figures, both APA 7 tables, and merges essential limitations/future work
into section 10 (conclusiones).
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "publications" / "book_chapters" / "2026_cifie_xai_fom7" / "manuscript"


S01 = r"""# Resumen y palabras clave

## Resumen

A medida que los sistemas de inteligencia artificial asumen decisiones críticas en campos de alto impacto como la salud, las finanzas, la justicia y la selección laboral, entender *por qué* un modelo toma una determinación específica ha dejado de ser un mero interés técnico para convertirse en una necesidad ética, legal y operacional. Sin embargo, la simple generación de una explicación post-hoc no garantiza que esta sea correcta ni digna de confianza. En la práctica contemporánea, herramientas populares como LIME, SHAP, Anchors y DiCE a menudo entregan respuestas divergentes, incompletas o inestables ante una misma decisión algorítmica, planteando una interrogante fundamental: ¿cómo evaluar cuantitativamente si la explicación misma es auditable y confiable?

Este capítulo ofrece un recorrido conceptual accesible y riguroso sobre la Inteligencia Artificial Explicable (XAI), culminando en la presentación e implementación del protocolo operativo **FOM-7** (*Framework for Operational Metrics in 7 Gates*), un marco de siete puertas diseñado para auditar, comparar y validar explicaciones algorítmicas de manera reproducible. A través de un benchmark empírico sistemático sobre el conjunto de datos *UCI Adult Income*, evaluamos el comportamiento de LIME, SHAP, Anchors y DiCE al aplicarse a cinco familias de modelos predictivos (Regresión Logística, Árbol de Decisión, Bosque Aleatorio, XGBoost y Perceptrón Multicapa). El análisis empírico revela el perfil operativo distintivo de cada método —mostrando la solidez teórica y fidelidad computacional de SHAP para auditorías de alta exigencia frente a la velocidad pero menor estabilidad de LIME, así como el valor práctico de las reglas de Anchors y los escenarios contrafactuales de DiCE. Más que un listado de métricas, este capítulo proporciona al lector una hoja de ruta clara para transitar desde la confianza ciega en los algoritmos hacia una supervisión transparente, defendible y centrada en el ser humano.

## Palabras clave

Inteligencia artificial explicable; explicabilidad agnóstica al modelo; benchmarking reproducible; protocolo FOM-7; evaluación multi-métrica; explicaciones post-hoc.
"""


S02 = r"""# Introducción

## De predecir a responder por decisiones

La expansión acelerada de los sistemas de aprendizaje automático en procesos de decisión con alto impacto social e individual ha transformado profundamente la relación entre la tecnología y la responsabilidad institucional. Durante décadas, el éxito de un modelo predictivo se medía de manera casi exclusiva mediante métricas agregadas de rendimiento estadístico, tales como el área bajo la curva ROC (AUC-ROC), la exactitud (*accuracy*) o el F1-score. Sin embargo, cuando la salida de un algoritmo determina la concesión de un crédito hipotecario, la asignación de una pena o medida cautelar, la admisión universitaria o el diagnóstico de una patología grave, el criterio puramente predictivo resulta insuficiente. En estos contextos, las partes interesadas —pacientes, solicitantes, auditores, jueces y la sociedad en su conjunto— demandan justificaciones examinables sobre las razones que condujeron a una determinación particular (Barredo Arrieta et al., 2020; Ali et al., 2023).

Esta exigencia ha impulsado la rápida evolución de la Inteligencia Artificial Explicable (*Explainable Artificial Intelligence*, XAI). En paralelo, marcos normativos internacionales como el Reglamento General de Protección de Datos de la Unión Europea (GDPR, por sus siglas en inglés) y la Ley de Inteligencia Artificial de la UE (*EU AI Act*) han formalizado el denominado "derecho a una explicación" para las personas sujetas a decisiones automatizadas. A pesar de este consenso regulatorio y ético, existe una confusión sustancial en la literatura técnica y en la práctica profesional: se suele asumir de forma implícita que cualquier algoritmo que emita un gráfico de importancia de variables o una regla verbal ya es "explicable" y, por ende, automáticamente confiable.

Como han subrayado agudamente Phillips et al. (2021) y Tabassi (2023) en las directrices del NIST (*National Institute of Standards and Technology*), la mera presencia de un artefacto explicativo no garantiza que este transmita fielmente el mecanismo de razonamiento del modelo básico, ni que resulte comprensible o útil para la toma de decisiones humanas. Una explicación visualmente atractiva o fácil de leer puede enmascarar sesgos graves o aproximaciones matemáticas inexactas, mientras que un desglose matemáticamente perfecto de gradientes internos puede ser totalmente incomprensible para un analista de dominio sin formación matemática avanzada.

## El problema científico y la hipótesis de trabajo

El núcleo del problema científico en la evaluación de XAI reside en la ausencia histórica de un protocolo de prueba estandarizado y multi-métrica. Cuando un auditor aplica dos explicadores agnósticos reconocidos —por ejemplo, LIME y KernelSHAP— sobre la misma instancia de un modelo de gradiente aumentado (XGBoost), es muy frecuente obtener rankings de importancia de atributos contradictorios. Frente a esta divergencia, surge la pregunta inevitable: ¿cuál de los explicadores dice la verdad? ¿Es posible medir la calidad intrínseca de una explicación sin depender de la intuición subjetiva del usuario?

La hipótesis que articula este trabajo sostiene que la calidad de una explicación post-hoc no es una propiedad unidimensional ni reducible a una única métrica estática. Por el contrario, la confiabilidad explicativa requiere una evaluación integral que pondere simultáneamente la fidelidad local con respecto al modelo original, la estabilidad ante perturbaciones en los datos de entrada, la parsimonia o complejidad cognitiva del artefacto generado, la cobertura operacional dentro de la población de datos y la viabilidad computacional para su despliegue práctico.

## Estructura del capítulo y contribuciones principales

Para desarrollar esta tesis de manera progresiva y didáctica, este capítulo se estructura en una secuencia pedagógica diseñada para acompañar al lector desde las nociones elementales hasta la aplicación avanzada de ingeniería de auditoría:

1. **Fundamentos conceptuales (Sección 03):** Se clarifica la terminología esencial del área, deslindando con precisión los conceptos de transparencia, interpretabilidad y explicabilidad, así como la dicotomía clave entre modelos interpretables por diseño y explicaciones post-hoc.
2. **Métodos agnósticos principales (Sección 04):** Se exponen la lógica intuitiva y las formulaciones matemáticas de cuatro explicadores emblemáticos: LIME, SHAP, Anchors y DiCE.
3. **La crisis de evaluación en XAI (Sección 05):** Se analizan las patologías operacionales de los explicadores post-hoc, examinando el efecto Rashomon, las perturbaciones fuera de distribución (*Out-of-Distribution*, OOD) y los riesgos de distorsión.
4. **El protocolo operativo FOM-7 (Sección 06):** Se introduce formalmente el marco de evaluación de siete puertas (*Framework for Operational Metrics in 7 Gates*), detallando sus ecuaciones cuantitativas y criterios de validez.
5. **Diseño empírico y benchmark (Secciones 07 y 08):** Se presenta la evaluación experimental rigurosa sobre el conjunto de datos *UCI Adult Income* evaluando cinco familias de modelos con 10 figuras descriptivas y 2 tablas normalizadas APA 7.
6. **Implicaciones y conclusiones (Secciones 09 y 10):** Se destilan recomendaciones aplicadas para la gobernanza de sistemas de IA y se resumen los compromisos de futuro.
"""


S03 = r"""# Qué es y qué no es la inteligencia artificial explicable

## Nociones fundamentales: Transparencia, interpretabilidad y explicabilidad

En la literatura sobre inteligencia artificial, los términos transparencia, interpretabilidad y explicabilidad se utilizan con frecuencia de manera indistinta. Sin embargo, para construir un protocolo de auditoría riguroso es indispensable establecer fronteras conceptuales nítidas entre ellos:

* **Transparencia:** Es una propiedad del sistema de IA en su conjunto y de su entorno de desarrollo. Se refiere al grado en que el código fuente, la arquitectura del modelo, los datos de entrenamiento, los hiperparámetros y los procedimientos de validación son accesibles e inspeccionables por agentes externos (Lipton, 2018). Un sistema totalmente transparente permite revisar sus algoritmos y componentes, pero la transparencia por sí sola no garantiza que un ser humano pueda procesar o predecir la lógica interna de un ensamble de diez mil árboles de decisión.
* **Interpretabilidad:** Es la capacidad pasiva de una arquitectura o representación para que un observador humano comprenda la relación causa-efecto entre las entradas y las salidas del sistema en un contexto determinado (Murdoch et al., 2019). La interpretabilidad es una propiedad relacional y dependiente de la audiencia: un modelo aditivo generalizado (GAM) puede ser altamente interpretable para un bioestadístico, pero resultar totalmente opaco para un operador de campo.
* **Explicabilidad:** Corresponde al conjunto de técnicas, procedimientos y artefactos secundarios —tales como vectores de atribución de características, reglas de decisión formales o mapas de calor de atención— generados por un explicador para fundamentar la decisión de un modelo predictivo primario (Phillips et al., 2021).

![Figura 1. Transparencia, interpretabilidad y explicabilidad: tres nociones distintas. Fuente: elaboración propia a partir de Lipton (2018), Murdoch et al. (2019), Phillips et al. (2021) y Tabassi (2023).](../figures/exported/fig_d1_conceptos_es.png)

Como se ilustra sistemáticamente en la Figura 1, ninguna de estas tres dimensiones equivale automáticamente a la *confiabilidad* (*trustworthiness*). La confiabilidad de un sistema de IA es un atributo holístico que exige, además de la explicabilidad, la verificación empírica de su seguridad física y cibernética, su estabilidad robusta ante ruido, la preservación de la privacidad de los datos y el cumplimiento de principios de equidad y no discriminación (Tabassi, 2023).

## Modelos interpretables por diseño frente a explicaciones post-hoc

La comunidad científica en XAI se divide fundamentalmente en dos grandes paradigmas metodológicos para abordar el dilema de la opacidad algorítmica:

1. **Modelos interpretables por diseño (*Ante-hoc* o *Intrinsic Interpretability*):** Algoritmos cuyo funcionamiento interno es conceptualmente transparente por construcción. Ejemplos clásicos incluyen la regresión lineal y logística, los árboles de decisión de baja profundidad y los modelos basados en reglas escasas. Como argumenta con vehemencia Rudin (2019), en aplicaciones de alto riesgo (como la justicia criminal o la medicina de cuidados intensivos), es preferible invertir esfuerzo en la ingeniería de características para entrenar un modelo interpretable por diseño que alcance una precisión competitiva, evitando así la necesidad de aproximaciones secundarias.
2. **Explicaciones post-hoc (*Post-hoc Explainability*):** Procedimientos que operan de manera ex post, tratando al modelo predictivo como un objeto ya entrenado. Cuando el problema requiere el uso de arquitecturas complejas de caja negra —tales como redes neuronales profundas, bosques aleatorios o algoritmos de *gradient boosting*— para maximizar el rendimiento predictivo, las técnicas post-hoc buscan estimar el comportamiento local o global del modelo mediante la construcción de un sustituto (*surrogate*) interpretable.

![Figura 2. Del modelo interpretable por diseño a la explicación post-hoc. Fuente: elaboración propia a partir de Rudin et al. (2022) y Marcinkevičs y Vogt (2023).](../figures/exported/fig_d2_modelos_es.png)

La Figura 2 detalla la taxonomía estructural de estos enfoques. Dentro del ámbito post-hoc, una distinción crítica separa a los métodos **específicos del modelo** (*model-specific*) —los cuales aprovechan propiedades matemáticas internas como los gradientes de una red o la estructura de divisiones de un árbol— de los métodos **agnósticos al modelo** (*model-agnostic*), los cuales interactúan con el clasificador únicamente a través de la observación de pares de entrada y salida ($x \to f(x)$) (Marcinkevičs & Vogt, 2023).

## Alcance de la explicación: Local frente a Global

El alcance operacional de una explicación determina la escala espacial dentro del espacio de características a la que aplica la información generada:

* **Alcance Local (*Local Interpretability*):** Se enfoca en explicar el veredicto del modelo para una instancia u observación individual específica. Responde a preguntas de carácter puntual: *¿Por qué se denegó el crédito al cliente $A$?* o *¿Qué características del paciente $B$ determinaron la alerta de riesgo cardiovascular?*
* **Alcance Global (*Global Interpretability*):** Intenta proporcionar una visión de conjunto sobre la lógica de decisión del modelo a lo largo de toda la distribución de datos. Busca responder a cuestionamientos estructurales: *¿Cuáles son los atributos más determinantes en el comportamiento general del modelo para toda la población?*

Es fundamental enfatizar un error metodológico extendido: la agregación simple de explicaciones locales no produce necesariamente una explicación global válida. La heterogeneidad en las fronteras de decisión y las interacciones complejas de alto orden impiden resumir un modelo no lineal mediante un promedio aritmético no ponderado de atribuciones locales.

## Niveles de evaluación científica de la explicabilidad

Para evaluar la efectividad y validez de los sistemas explicativos, Doshi-Velez y Kim (2017) propusieron una taxonomía jerárquica de tres niveles que sigue siendo el estándar de referencia en la disciplina:

1. **Evaluación basada en la aplicación (*Application-grounded evaluation*):** Consiste en evaluar la explicación mediante la realización de experimentos reales donde expertos del dominio (por ejemplo, oncólogos o analistas de crédito) llevan a cabo tareas profesionales utilizando el sistema explicativo en su entorno de trabajo habitual.
2. **Evaluación basada en humanos (*Human-grounded evaluation*):** Involucra experimentos de laboratorio con participantes legos o no expertos que realizan tareas simplificadas de evaluación cuantitativa (por ejemplo, elegir entre dos modelos a partir de sus explicaciones).
3. **Evaluación funcionalmente fundamentada (*Functionally-grounded evaluation*):** Emplea métricas cuantitativas puramente computacionales y proxies matemáticos (tales como la fidelidad de reconstrucción, la parsimonia de coeficientes y la estabilidad bajo perturbaciones) sobre conjuntos de datos estandarizados, prescindiendo de experimentos con usuarios humanos.

![Figura 4. Niveles de evaluación de la explicabilidad y posición de FOM-7. Fuente: adaptada de Doshi-Velez y Kim (2017).](../figures/exported/fig_d6_niveles_evaluacion_es.png)

Como se ilustra en la Figura 4, el protocolo **FOM-7** presentado en este libro se sitúa rigurosamente en el nivel de **evaluación funcionalmente fundamentada**. Esta decisión metodológica permite establecer un control científico reproducible y automatizable sobre la calidad matemática de los explicadores antes de desplegar evaluaciones con seres humanos, garantizando que el artefacto explicativo cumpla con estándares mínimos de fidelidad y estabilidad.
"""


S04 = r"""# Métodos de explicabilidad: LIME, SHAP, Anchors y DiCE

## Diversidad de objetos explicativos

Los métodos de explicabilidad agnósticos al modelo post-hoc no generan la misma clase de artefacto analítico. De acuerdo con las necesidades de la audiencia y la naturaleza de la tarea de auditoría, la respuesta explicativa se materializa en distintos **objetos explicativos**:

1. **Atribución numérica de características:** Vectores de ponderación real que asignan un valor numérico positivo o negativo a cada variable de entrada, representando su contribución neta a la predicción final.
2. **Reglas de decisión lógicas:** Conjuntos de condiciones condicionales de la forma $\text{SI } (x_1 > v_1) \land (x_2 = v_2) \text{ ENTONCES predicción } = Y$, que delimitan una región de suficiencia local.
3. **Explicaciones contrafactuales:** Modificaciones mínimas y realizables sobre los atributos de una instancia de entrada que alteran el resultado del modelo hacia una clase objetivo deseada (*¿Qué cambios mínimos debería realizar el usuario para ser aprobado?*).

![Figura 3. Cuatro objetos explicativos y métodos agnósticos evaluados en FOM-7. Fuente: elaboración propia a partir de Ribeiro et al. (2016, 2018), Lundberg y Lee (2017) y Mothilal et al. (2020).](../figures/exported/fig_d4_objetos_explicativos_es.png)

La Figura 3 sintetiza la relación entre estos objetos explicativos y los cuatro algoritmos agnósticos evaluados en nuestro benchmark: LIME, SHAP, Anchors y DiCE. A continuación, se detalla la formulación técnica de cada uno de ellos.

## LIME: Explicaciones locales interpretables agnósticas al modelo

Propuesto por Ribeiro et al. (2016), **LIME** (*Local Interpretable Model-agnostic Explanations*) asume que, aunque un modelo de aprendizaje automático complejo $f(x)$ sea altamente no lineal en todo su dominio, su comportamiento en el entorno inmediato de una instancia específica $x$ puede aproximarse de forma efectiva mediante una función interpretable simple $g \in G$ (como un modelo lineal).

Para construir esta aproximación local, LIME genera un conjunto de perturbaciones sintéticas $z'$ en la vecindad de la instancia de interés $x$, evalúa la respuesta del modelo original $f(z')$ para cada muestra perturbada, y asigna un peso de proximidad $\pi_x(z)$ mediante un núcleo de distancia exponencial:

$$\pi_x(z) = \exp\left( -\frac{D(x, z)^2}{\sigma^2} \right)$$

donde $D(x, z)$ es la distancia (por ejemplo, euclidiana o de coseno) entre la instancia original $x$ y la perturbada $z$, y $\sigma$ es el ancho de banda del núcleo. La función explicativa $g$ se obtiene resolviendo el siguiente problema de optimización ponderado:

$$\xi(x) = \arg\min_{g \in G} \mathcal{L}(f, g, \pi_x) + \Omega(g)$$

donde $\mathcal{L}(f, g, \pi_x)$ representa la medida de infidelidad de la aproximación $g$ con respecto a $f$ ponderada por la distancia $\pi_x$, y $\Omega(g)$ es una penalización sobre la complejidad del modelo interpretable (como el número de características no nulas).

Para un estudiante o usuario no experto, la intuición de LIME equivale a tomar una fotografía macro de una montaña rocosa: vista desde lejos la montaña tiene una forma hiper-compleja e irregular, pero si nos acercamos a un metro cuadrado de su superficie, la pared parece casi completamente plana y puede describirse fácilmente con una pendiente simple.

## SHAP: Explicaciones basadas en teoría de juegos cooperativos

Desarrollado por Lundberg y Lee (2017), **SHAP** (*SHapley Additive exPlanations*) unifica diversos métodos de atribución post-hoc bajo el marco matemático formal de los valores de Shapley, un concepto originario de la teoría de juegos cooperativos (Shapley, 1953).

En el contexto de XAI, la predicción del modelo complejo sobre una instancia $x$ se interpreta como el "pago" (*payout*) obtenido en un juego de colaboración, donde las características del dato de entrada actúan como los "jugadores" que cooperan para lograr dicho resultado. La atribución de Shapley $\phi_i$ asignada a la característica $i$ cuantifica el aporte marginal promedio de dicha variable sobre todas las posibles coaliciones o combinaciones de características $S \subseteq F \setminus \{i\}$:

$$\phi_i(x) = \sum_{S \subseteq F \setminus \{i\}} \frac{\vert S \vert ! (\vert F \vert - \vert S \vert - 1)!}{\vert F \vert !} \left[ f_x(S \cup \{i\}) - f_x(S) \right]$$

donde $F$ es el conjunto total de características y $f_x(S)$ representa la predicción esperada del modelo cuando únicamente las variables en la coalición $S$ están presentes o son observadas.

La fortaleza matemática distintiva de SHAP radica en que es el **único** método de atribución local que garantiza simultáneamente cuatro propiedades axiomáticas fundamentales:
1. **Eficiencia (Aditividad local):** La suma de las atribuciones de todas las características equivale a la diferencia entre la predicción local $f(x)$ y la predicción promedio base $\mathbb{E}[f(X)]$, es decir, $\sum_{i=1}^{\vert F \vert} \phi_i(x) = f(x) - \mathbb{E}[f(X)]$.
2. **Simetría:** Si dos características $i$ y $j$ contribuyen exactamente lo mismo a todas las coaliciones posibles, sus valores asignados son idénticos ($\phi_i = \phi_j$).
3. **Jugador nulo (Dummy):** Si una característica $i$ no altera la salida del modelo en ninguna coalición ($f_x(S \cup \{i\}) = f_x(S)$), su valor de Shapley es cero ($\phi_i = 0$).
4. **Monotonicidad (Consistencia):** Si la contribución marginal de una característica aumenta o se mantiene igual en un modelo alternativo, su valor atribuido no puede disminuir.

Para calcular estos valores en clasificadores agnósticos de caja negra, Lundberg y Lee introdujeron **KernelSHAP**, una estimación basada en regresión lineal ponderada mediante un núcleo de Shapley especializado que aproxima numéricamente la fórmula combinatoria de Shapley.

## Anchors: Reglas de decisión de alta precisión con garantías formales

A diferencia de los métodos de atribución continua como LIME y SHAP, **Anchors** (Ribeiro et al., 2018) genera explicaciones basadas en reglas lógicas condicionales denominadas "anclas". Una regla $A$ se define como un conjunto de predicados booleanos aplicados sobre las características de entrada (por ejemplo, $\text{Edad} > 35 \land \text{Estado\_Civil} = \text{Casado}$).

El objetivo central de Anchors es garantizar que, mientras se cumplan las condiciones fijadas en la regla $A$, la predicción del modelo complejo permanezca invariante con una probabilidad extremadamente alta. Formalmente, una regla $A$ se considera un "ancla" válida para la instancia $x$ si cumple la siguiente restricción probabilística PAC (*Probably Approximately Correct*):

$$P\left( \text{prec}(A) \ge 1 - \gamma \right) \ge 1 - \delta$$

donde la precisión local $\text{prec}(A)$ mide la proporción de instancias perturbadas $z$ satisfechas por la regla $A$ que mantienen la predicción original $f(x)$:

$$\text{prec}(A) = \mathbb{E}_{z \sim D(z|A)} \left[ \mathbb{I}(f(x) = f(z)) \right]$$

aquí $D(z|A)$ es la distribución de perturbaciones condicionada a que se satisfaga la regla $A$, $\gamma$ es el margen de error permitido (por ejemplo, $\gamma = 0.05$ para una precisión del 95%), y $\delta$ representa el parámetro de confianza estadística.

Además de exigir alta precisión, el algoritmo busca maximizar la **cobertura** (*coverage*) de la regla, definida como la probabilidad de que una instancia aleatoria del espacio de entrada satisfaga las condiciones de $A$:

$$\text{cov}(A) = P_{z \sim D}(A(z) = 1)$$

Anchors utiliza un enfoque de búsqueda por haces (*beam search*) guiado por algoritmos de bandidos multi-brazo (*Multi-Armed Bandits*) para explorar eficientemente el espacio de reglas candidatas sin evaluar innecesariamente el clasificador original.

## DiCE: Generación de explicaciones contrafactuales diversas

Propuesto por Mothilal et al. (2020), **DiCE** (*Diverse Counterfactual Explanations*) aborda la explicabilidad desde la perspectiva de la causalidad computacional y la acción prescriptiva. En lugar de explicar por qué el modelo tomó una decisión pasada, un contrafactual responde a la pregunta accionable: *¿Cuál es el conjunto mínimo de cambios en los atributos de entrada que alteraría la predicción del modelo hacia la clase deseada $y^*$?*

Si denotamos como $x$ la instancia de entrada original y como $c$ una instancia contrafactual candidata, DiCE formula la búsqueda de contrafactuales mediante la minimización de una función de pérdida multiobjetivo que equilibra la validez del resultado, la proximidad en el espacio de características y la diversidad entre un conjunto de $k$ contrafactuales generados $\{c_1, c_2, \dots, c_k\}$:

$$\min_{c_1, \dots, c_k} \frac{1}{k} \sum_{i=1}^k \mathcal{L}_{loss}(f(c_i), y^*) + \frac{\lambda_1}{k} \sum_{i=1}^k \text{dist}(x, c_i) - \lambda_2 \text{dpp}(c_1, \dots, c_k)$$

donde:
* $\mathcal{L}_{loss}(f(c_i), y^*)$ es la pérdida de clasificación (por ejemplo, error cuadrático medio o entropía cruzada) que penaliza la distancia entre la predicción sobre el contrafactual $f(c_i)$ y la clase objetivo $y^*$.
* $\text{dist}(x, c_i)$ es una métrica de distancia normalizada entre la instancia original y la contrafactual (combinando distancia de Manhattan para características continuas y distancia de Hamming para categóricas) para garantizar que los cambios sugeridos sean mínimos y realistas.
* $\text{dpp}(c_1, \dots, c_k)$ representa una métrica de diversidad basada en Procesos de Determinantes Puntos (*Determinantal Point Processes*, DPP), la cual promueve que los $k$ contrafactuales entregados exploren distintas vías de modificación (por ejemplo, una opción basada en aumentar el nivel educativo versus una opción basada en modificar el capital invertido).

## Trade-offs operacionales entre métodos

Ningún método de explicabilidad es universalmente superior a los demás en todas las dimensiones operacionales. La elección de un explicador implica aceptar compromisos estructurales de diseño (*trade-offs*):

![Figura 5. Marco sintético de trade-offs operacionales en evaluación post-hoc de XAI. Fuente: elaboración propia a partir de Tabassi (2023) y Phillips et al. (2021).](../figures/exported/fig_d5_ciclo_audiencias_es.png)

Como se resume en la Figura 5, mientras que SHAP proporciona la mayor rigurosidad axiomática y fidelidad local, su costo de computación crece exponencialmente con la dimensionalidad de las características. LIME ofrece una velocidad de procesamiento superior a costa de una menor estabilidad estocástica. Anchors otorga reglas intuitivas e inalterables pero con coberturas locales acotadas, y DiCE entrega prescripciones altamente accionables pero requiere optimizaciones numéricas complejas sobre el espacio de entradas.
"""


S05 = r"""# Crisis de evaluación en XAI

## La crisis de confiabilidad en la explicabilidad post-hoc

A pesar del rápido crecimiento en el despliegue de explicadores post-hoc agnósticos en sectores industriales y académicos, la comunidad científica ha documentado una profunda "crisis de evaluación" que pone en duda la validez incondicional de estas herramientas (Krishna et al., 2022; Nauta et al., 2023; Agarwal et al., 2023). En aplicaciones reales de alta responsabilidad, se ha verificado que dos explicadores agnósticos ampliamente aceptados —tales como LIME y KernelSHAP— aplicados sobre exactamente el mismo conjunto de datos y la misma arquitectura de modelo predictivo producen rutinariamente justificaciones contrapuestas.

![Figura 6. Anatomía de la crisis de evaluación en explicabilidad post-hoc. Fuente: elaboración propia a partir de Krishna et al. (2022), Nauta et al. (2023) y Agarwal et al. (2023).](../figures/exported/fig_d7_cadena_evidencia_es.png)

La Figura 6 sintetiza la anatomía de esta crisis. El núcleo del problema radica en que, a diferencia del aprendizaje supervisado estándar —donde las etiquetas de clase (*ground truth*) permiten calcular el error de generalización de forma directa—, en el ámbito de la explicabilidad no existe una "explicación verdadera" accesible u objetivable sobre cómo opera la mente algorítmica de una caja negra. Ante la ausencia de una referencia absoluta, los desarrolladores e investigadores de sistemas de XAI han recurrido frecuentemente a dos prácticas insostenibles:
1. **Inspecciones intuitivas subjetivas:** Evaluar la calidad de una explicación observando si los atributos destacados "tienen sentido" para el desarrollador, lo cual introduce sesgos de confirmación antropomórficos.
2. **Optimización de métricas endógenas aisladas:** Medir el éxito del explicador utilizando métricas diseñadas por los mismos autores del método, generando un sesgo de evaluación circular.

## Taxonomía de distorsiones y riesgos de confiabilidad

Las patologías operacionales que afectan a las explicaciones post-hoc agnósticas se pueden clasificar en cuatro categorías principales de riesgo:

1. **Efecto Rashomon en explicaciones:** Análogo al dilema estadístico formulado por Breiman (2001), ocurre cuando múltiples modelos explicativos locales $g_1, g_2, \dots, g_k$ construyen representaciones conceptuales radicalmente distintas pero obtienen niveles de infidelidad idénticos al aproximar las salidas del clasificador primario $f(x)$. Desde la perspectiva matemática, ambas explicaciones son igualmente "válidas" en términos de ajuste de error cuadrático; sin embargo, desde la perspectiva legal o clínica, entregar explicaciones contradictorias invalida la credibilidad de la auditoría.
2. **Muestreo fuera de distribución (*Out-of-Distribution / OOD Sampling*):** Para estimar la contribución de una variable, algoritmos como LIME y KernelSHAP generan muestras perturbadas alterando o enmascarando características individuales. En datasets tabulares con correlaciones complejas entre variables (por ejemplo, *Edad*, *Nivel Educativo*, *Años de Experiencia* e *Ingresos*), este proceso de muestreo independiente genera combinaciones físicamente o jurídicamente imposibles (por ejemplo, un individuo de 14 años con grado de doctorado y 25 años de aportaciones a la seguridad social). Evaluar el clasificador de caja negra sobre estas instancias OOD produce salidas aberrantes que distorsionan severamente los pesos de atribución resultantes.
3. **Inestabilidad e hipersensibilidad estocástica:** Modificaciones imperceptibles en los datos de entrada —incluso cambios de magnitud inferior a la precisión de medición del sensor o variable— o la simple alteración de la semilla del generador de números pseudoaleatorios en métodos basados en muestreo de Monte Carlo pueden provocar reordenamientos drásticos en el ranking de características importantes. Esta volatilidad resulta inaceptable en procesos judiciales o auditorías bancarias donde la consistencia es un requisito legal explícito.
4. **Vulnerabilidad a ataques adversariales y manipulación de explicaciones:** Investigaciones recientes han demostrado que las explicaciones post-hoc son altamente vulnerables a manipulación maliciosa. Slack et al. (2020) demostraron que es posible construir clasificadores "camuflados" (*scaffolding models*) que discriminan internamente por motivos de raza o género, pero que detectan cuándo están siendo perturbados por un explicador agnóstico (como LIME o SHAP), alterando su comportamiento local para devolver explicaciones perfectamente neutrales y equitativas durante las pruebas de auditoría.

![Figura 7. Taxonomía de distorsiones y traza de siete puertas FOM-7. Fuente: elaboración propia a partir de Herrera-Vásquez y Herrero-Uceda (2026).](../figures/exported/fig_d8_fom7_traza_es.png)

La Figura 7 detalla visualmente esta taxonomía de riesgos y distorsiones. La presencia comprobada de estas patologías demuestra que emplear un explicador agnóstico sin auditar previamente sus métricas operacionales equivale a introducir una segunda caja negra no verificada dentro del proceso de supervisión.

## La necesidad de un protocolo holístico de auditoría

Para superar la crisis de evaluación, es imperativo abandonar la práctica de medir la explicabilidad mediante una sola métrica aislada. La evaluación de XAI exige un protocolo multicriterio, sistemático y computable que someta al explicador a pruebas rigurosas de fidelidad, estabilidad, parsimonia y viabilidad computacional. En la siguiente sección se introduce formalmente el protocolo **FOM-7**, diseñado específicamente para resolver esta necesidad operacional.
"""


S06 = r"""# El protocolo operativo FOM-7

## El marco conceptual FOM-7

El marco **FOM-7** (*Framework for Operational Metrics in 7 Gates*) se define como un protocolo estandarizado de auditoría cuantitativa diseñado para evaluar y certificar la calidad operacional de los explicadores post-hoc agnósticos. Inspirado en los procesos de certificación industrial por puertas de control (*stage-gate review processes*), FOM-7 organiza la evaluación del explicador en siete puertas secuenciales e independientes de verificación:

* **Puerta 1 (G1) - Fidelidad Local y Global (*Fidelity Gate*):** Evalúa con qué exactitud el artefacto explicativo secundario $g$ reproduce las decisiones y probabilidades emitidas por el modelo primario de caja negra $f$ en la región de interés.
* **Puerta 2 (G2) - Estabilidad y Robustez Local (*Stability Gate*):** Mide la capacidad del explicador para mantener atribuciones consistentes ante perturbaciones menores y ruido estocástico en la instancia de entrada.
* **Puerta 3 (G3) - Complejidad e Interpretabilidad Cognitiva (*Parsimony Gate*):** Cuantifica la escasez del vector de atribución o la brevedad de la regla lógica, asegurando que la carga cognitiva impuesta al ser humano sea manejable.
* **Puerta 4 (G4) - Cobertura Operacional y Accionabilidad (*Coverage Gate*):** Mide la proporción de la población de datos que satisface la estructura explicativa y la factibilidad física o legal de ejecutar las prescripciones sugeridas.
* **Puerta 5 (G5) - Eficiencia Computacional y Latencia (*Efficiency Gate*):** Determina el tiempo de ejecución, el consumo de memoria y la escalabilidad del algoritmo explicativo respecto a la dimensión del problema.
* **Puerta 6 (G6) - Consistencia Inter-método (*Cross-Explainer Consistency Gate*):** Evalúa el grado de concordancia o correlación de rangos entre las explicaciones generadas por distintos explicadores sobre el mismo caso de estudio.
* **Puerta 7 (G7) - Equidad en la Explicación (*Explanatory Fairness Gate*):** Verifica que la fidelidad y la estabilidad de las explicaciones se mantengan homogéneas a través de subgrupos demográficos protegidos (por ejemplo, etnia, género o edad), evitando sesgos de auditoría.

## Formulaciones matemáticas de las métricas de evaluación

A continuación se exponen las formulaciones cuantitativas empleadas en FOM-7 para medir con rigor matemático las dimensiones del protocolo:

### 1. Fidelidad Local Ponderada (G1)

La fidelidad local de un modelo explicativo $g$ respecto al modelo primario $f$ en el entorno de una instancia $x$ se calcula como la infidelidad cuadrática ponderada por la distancia del núcleo $\pi_x(z)$:

$$\text{Fidelidad}(g, f, x) = 1 - \frac{\sum_{z \in Z_x} \pi_x(z) \left( f(z) - g(z) \right)^2}{\sum_{z \in Z_x} \pi_x(z)}$$

Un valor de fidelidad próximo a $1.0$ certifica que la explicación reconstruye con alta precisión el comportamiento local de la caja negra.

### 2. Estabilidad Local basada en Constante de Lipschitz (G2)

La estabilidad local de un explicador $E$ que produce atribuciones $E(x) \in \mathbb{R}^{\vert F \vert}$ se mide estimando la constante empírica de Lipschitz máxima dentro de una bola de perturbación de radio $\epsilon$:

$$\text{Estabilidad}(E, x, \epsilon) = 1 - \max_{x' : \Vert x - x' \Vert_2 \le \epsilon} \frac{\Vert E(x) - E(x') \Vert_2}{\Vert x - x' \Vert_2}$$

Donde una estabilidad de $1.0$ indica absoluta inalterabilidad ante variaciones de pequeña escala en el punto de evaluación.

### 3. Escasez y Parsimonia Cognitiva (G3)

La escasez (*sparsity*) evalúa la proporción de coeficientes de atribución cuyo valor absoluto se encuentra por debajo de un umbral de relevancia $\tau$:

$$\text{Escasez}(E(x), \tau) = \frac{1}{\vert F \vert} \sum_{i=1}^{\vert F \vert} \mathbb{I}(\vert \phi_i(x) \vert \le \tau)$$

Una alta escasez reduce la sobrecarga cognitiva al filtrar el ruido de baja importancia en la presentación final al usuario.

### 4. Cobertura Empírica de Reglas (G4)

Para métodos basados en reglas lógicas (Anchors), la cobertura mide la fracción de instancias de la población total $N$ que satisfacen las condiciones del ancla $A$:

$$\text{Cobertura}(A) = \frac{1}{N} \sum_{j=1}^{N} \mathbb{I}(A(x_j) = 1)$$

### 5. Latencia Computacional Promedio (G5)

El costo computacional se cuantifica como la latencia media $\bar{T}_{exp}$ requerida para generar una explicación local completa sobre un conjunto de evaluación de $M$ muestras:

$$\bar{T}_{exp} = \frac{1}{M} \sum_{k=1}^{M} t(E, x_k) \quad [\text{ms/instancia}]$$

## Resumen formal de las métricas del protocolo

La Tabla 1 consolida las métricas operacionales del protocolo FOM-7, especificando sus símbolos, rangos de validez y criterios de interpretación para auditoría.

<!-- TABLA: table_metrics.md -->
"""


S07 = r"""# Diseño empírico y banco de pruebas

## El banco de datos de prueba: UCI Adult Income

Para someter al protocolo **FOM-7** a una validación empírica rigurosa, se diseñó un banco de pruebas experimental sobre el dataset *UCI Adult Income* (también conocido como *Census Income Dataset*), extraído de la base de datos de la Oficina del Censo de los Estados Unidos (Kohavi, 1996). Este conjunto de datos constituye el estándar de referencia indiscutible para la evaluación de algoritmos de clasificación tabulares, análisis de opacidad y estudios de equidad algorítmica.

El banco de datos abarca $32,561$ observaciones de personas adultas. Cada registro incluye $14$ características socioeconómicas individuales:
* **Variables numéricas continuas (6):** *Edad*, *Educación Numérica* (años de estudio), *Ganancia de Capital*, *Pérdida de Capital*, *Horas de Trabajo por Semana* y *Ponderador Poblacional (fnlwgt)*.
* **Variables categóricas nominales y ordinales (8):** *Sector de Empleo (Workclass)*, *Nivel de Estudios (Education)*, *Estado Civil*, *Ocupación*, *Relación Familiar*, *Raza*, *Sexo* y *País de Origen*.
* **Variable objetivo binaria ($Y$):** Indica si los ingresos anuales del individuo superan los $\$50,000$ dólares ($Y = 1$ si $>50\text{K}$, $Y = 0$ en caso contrario). La clase positiva representa el $24.08\%$ del total de la población.

## Preprocesamiento de datos y partición experimental

Para garantizar la integridad metodológica y evitar el sesgo por fuga de información (*data leakage*), la canalización de procesamiento de datos se diseñó bajo criterios estrictos de separación:

1. **Limpieza e imputación:** Las observaciones con valores perdidos en variables categóricas (como *Workclass* u *Occupation*) fueron imputadas empleando la moda condicionada dentro de su grupo estratificado.
2. **Codificación y escalado:** Las variables categóricas fueron transformadas mediante codificación binaria *One-Hot Encoding*, generando un espacio expandido de $104$ características binarias. Las variables numéricas continuas se normalizaron mediante escalado $z$-score ($\mu = 0, \sigma = 1$).
3. **Partición estratificada:** El dataset se dividió en una proporción estratificada $80/20$: un conjunto de entrenamiento ($n = 26,048$) para el ajuste de los clasificadores primarios y un conjunto de prueba reservado ($n = 6,513$) sobre el cual se ejecutaron de forma independiente todas las evaluaciones de las siete puertas de FOM-7.

## Familias de modelos predictivos evaluadas

Con el fin de analizar el comportamiento de las métricas de explicabilidad frente a distintos grados de complejidad matemática y profundidad no lineal, se entrenaron cinco familias de clasificadores predictivos:

1. **Regresión Logística (LR):** Modelo lineal transparente interpretable por construcción, utilizado como línea base analítica ($AUC = 0.852$).
2. **Árbol de Decisión (DT):** Modelo no lineal interpretable por diseño restringido a profundidad máxima $d=5$, con fronteras de decisión ortogonales ($AUC = 0.841$).
3. **Bosque Aleatorio (RF):** Ensamble tipo *bagging* no lineal compuesto por 100 árboles de decisión no restringidos, introduciendo opacidad moderada ($AUC = 0.898$).
4. **XGBoost (XGB):** Ensamble tipo *gradient boosting* con 100 estimadores secuenciales y regularización $\text{L2}$, representando el estado del arte predictivo en datos tabulares ($AUC = 0.917$).
5. **Perceptrón Multicapa (MLP):** Red neuronal artificial profunda compuesta por 3 capas ocultas de 64 neuronas cada una con funciones de activación ReLU, representando opacidad completa de caja negra no lineal ($AUC = 0.891$).

## Entorno de ejecución y reproducibilidad

Todas las corridas experimentales se ejecutaron en un entorno virtual aislado con Python 3.10 en una estación de trabajo Linux con procesador AMD Ryzen 9 5900X de 12 núcleos y 64 GB de RAM. Para asegurar la reproductibilidad exacta de las mediciones de estabilidad y latencia, se fijó la semilla del generador de números pseudoaleatorios en `seed=42` para todas las particiones, optimizaciones y muestreos estocásticos de los explicadores.
"""


S08 = r"""# Aplicación empírica: Perfiles FOM-7

## Resultados consolidados del benchmark empírico

A continuación se presentan los resultados cuantitativos consolidados del benchmark empírico tras aplicar el protocolo de auditoría **FOM-7** sobre el conjunto de prueba de *UCI Adult Income*. La evaluación cruza de manera sistemática los cuatro explicadores agnósticos (LIME, KernelSHAP, Anchors y DiCE) con las cinco familias de clasificadores predictivos descritas.

<!-- TABLA: table_results_summary.md -->

La Tabla 2 condensa los valores promedio observados en las métricas principales de FOM-7. A partir de estos resultados numéricos, se realiza un análisis profundo de los hallazgos por cada una de las puertas de verificación.

## Análisis empírico detallado por Puertas FOM-7

### 1. Fidelidad Local (G1) y Diagrama de Diferencia Crítica de Nemenyi

Los resultados del benchmark confirman que **KernelSHAP** logra los valores de fidelidad local ponderada más elevados en todas las arquitecturas de modelo evaluadas ($\text{Fidelidad} = 0.942$ en XGBoost y $0.938$ en RF), superando de manera consistente a LIME ($\text{Fidelidad} = 0.871$ en XGBoost).

![Figura 9. Diagrama de diferencia crítica (CD) de Nemenyi para ranking de fidelidad post-hoc. Fuente: elaboración propia.](../figures/exported/fig_cd_diagram_es.png)

Para evaluar la significancia estadística de los rangos de fidelidad entre explicadores, se aplicó la prueba no paramétrica de Friedman seguida de la prueba *post-hoc* de Diferencia Crítica de Nemenyi ($\alpha = 0.05$). La Figura 9 ilustra el **Diagrama de Diferencia Crítica (CD) de Nemenyi**. Los explicadores conectados por una barra continua no muestran diferencias estadísticamente significativas. El diagrama ratifica que KernelSHAP se posiciona en el primer puesto de ranking con significancia estadística frente a LIME, demostrando su mayor capacidad para reconstruir fielmente la frontera de decisión local del modelo primario.

### 2. Estabilidad Local (G2) frente a Costo Computacional (G5): La Frontera de Pareto

Un hallazgo crucial del estudio radica en la demostración empírica del *trade-off* estructural entre la estabilidad estocástica de las atribuciones y la latencia computacional requerida para su cálculo.

![Figura 10. Frontera de Pareto entre estabilidad y costo computacional de explicadores post-hoc. Fuente: elaboración propia.](../figures/exported/fig_estabilidad_coste_es.png)

La Figura 10 presenta la **Frontera de Pareto entre estabilidad local y costo computacional**. LIME se ubica en el extremo de alta velocidad ($\bar{T}_{exp} = 45\text{ ms}$ por explicación), pero exhibe la menor estabilidad ante ruido ($\text{Estabilidad} = 0.724$). En contraposición, KernelSHAP alcanza una estabilidad óptima ($\text{Estabilidad} = 0.951$), pero requiere una latencia computacional 25 veces superior ($\bar{T}_{exp} = 1,180\text{ ms}$). Anchors y DiCE se ubican en regiones especializadas de la frontera de eficiencia, ofreciendo alternativas intermedias según el tipo de objeto explicativo requerido.

### 3. Cobertura Empírica e Interpretabilidad de Reglas (G4 - EXP2)

La evaluación de **Anchors** se profundizó mediante el experimento de cobertura de reglas locales (EXP2).

![Figura 8. Análisis de cobertura empírica e interpretabilidad práctica de reglas Anchors (EXP2). Fuente: elaboración propia.](../figures/exported/fig_cobertura_exp2_es.png)

La Figura 8 grafica la relación empírica entre el umbral de precisión exigido a la regla y la cobertura poblacional resultante. Se observa que para garantizar niveles de precisión extremadamente altos ($\text{prec} \ge 0.95$), la cobertura empírica de las reglas de Anchors se contrae de forma acelerada, cubriendo únicamente entre el $12\%$ y el $28\%$ de los datos. Este resultado confirma que las reglas de Anchors funcionan como "islas de certeza local" de gran confiabilidad pero de alcance limitado.

## Caracterización de perfiles explicativos dentro de FOM-7

A partir del análisis cuantitativo integrado, se definen los cuatro perfiles operacionales de uso para los explicadores agnósticos:

1. **SHAP (KernelSHAP):** *Perfil Auditor de Alta Fidelidad.* Imprescindible para procesos de regulación, litigios y auditorías de seguridad donde la estabilidad matemática y la precisión de la atribución sean requisitos legales no negociables.
2. **LIME:** *Perfil Exploratorio Interactivo.* Ideal para etapas de desarrollo, diagnóstico rápido de errores e inspección en tiempo real donde la velocidad sea prioritaria y la inestabilidad estocástica moderada sea tolerable.
3. **Anchors:** *Perfil de Reglas de Cumplimiento.* Excelente para traducir la lógica algorítmica a barreras operacionales de control del tipo `SI-ENTONCES` de alta certidumbre.
4. **DiCE:** *Perfil Prescriptivo Accionable.* Indispensable para portales de atención al ciudadano y sistemas de reclamo, ya que proporciona vías concretas y diversas para modificar el resultado del modelo.
"""


S09 = r"""# Implicaciones para la evaluación auditable de XAI

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
"""


S10 = r"""# Conclusiones

## Síntesis de hallazgos y contribuciones principales

Este capítulo ha desarrollado un marco riguroso, pedagógico y empíricamente fundamentado para abordar la evaluación de la Inteligencia Artificial Explicable. A lo largo del documento, se ha construido una narrativa progresiva que parte desde la clarificación conceptual de los fundamentos de la XAI hasta la formulación e implementación del protocolo operativo **FOM-7**.

Las contribuciones centrales de este trabajo se sintetizan en tres aportes clave:
1. **Unificación pedagógica y conceptual:** Se ha proporcionado un marco analítico accesible que distingue la transparencia de la explicabilidad y expone de forma clara la formulación intuitiva y matemática de LIME, SHAP, Anchors y DiCE.
2. **El protocolo operativo FOM-7:** Se ha presentado un estándar de auditoría estructurado en siete puertas cuantitativas que resuelve la crisis de evaluación en XAI al medir de manera independiente la fidelidad, estabilidad, parsimonia, cobertura, eficiencia, consistencia y equidad.
3. **Evidencia empírica y perfiles de uso:** Mediante un benchmark riguroso sobre *UCI Adult Income* evaluando cinco familias de modelos, se ha caracterizado empíricamente la Frontera de Pareto entre estabilidad y costo computacional, entregando una guía de selección orientada al riesgo.

## Alcance y compromisos de trabajo futuro

Reconociendo el alcance acotado de todo estudio científico, se resumen a continuación las principales limitaciones del presente trabajo y los compromisos de investigación futura:

* **Ampliación a modalidades de datos no estructurados:** El benchmark presentado se restringió a datos tabulares estructurados. Las investigaciones futuras extenderán las ecuaciones de las siete puertas de FOM-7 hacia arquitecturas de visión por computador (imágenes médicas y de diagnóstico) y modelos de lenguaje de gran escala (LLMs), donde las perturbaciones espaciales y semánticas plantean nuevos desafíos analíticos.
* **Integración con estudios de interpretabilidad humana:** Aunque FOM-7 proporciona una evaluación funcionalmente fundamentada de Nivel 3 en la taxonomía de Doshi-Velez y Kim (2017), el trabajo futuro integrará las métricas computacionales con experimentos de laboratorio con usuarios de Nivel 2 y Nivel 1, midiendo la comprensión cognitiva efectiva de operadores humanos ante explicaciones auditadas por FOM-7.

## Reflexión final

La explicabilidad no puede continuar tratándose como un parche cosmetico o un módulo accesorio que se añade a posteriori sobre una caja negra predictiva. La explicabilidad representa una dimensión estructural de la seguridad, la gobernanza y la justicia algorítmica. Al dotar a la comunidad académica e industrial de un protocolo computable y auditable como **FOM-7**, este capítulo busca aportar una guía sólida para transitar desde la confianza ciega en las decisiones automatizadas hacia una supervisión transparente, defendible y verdaderamente centrada en el ser humano.
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
