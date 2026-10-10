# Qué es y qué no es la inteligencia artificial explicable

## Nociones fundamentales: Transparencia, interpretabilidad y explicabilidad

En la literatura sobre inteligencia artificial, los términos transparencia, interpretabilidad y explicabilidad se utilizan con frecuencia de manera indistinta. Sin embargo, para construir un protocolo de auditoría riguroso es indispensable establecer fronteras conceptuales nítidas entre ellos:

* **Transparencia:** Es una propiedad del sistema de IA en su conjunto y de su entorno de desarrollo. Se refiere al grado en que el código fuente, la arquitectura del modelo, los datos de entrenamiento, los hiperparámetros y los procedimientos de validación son accesibles e inspeccionables por agentes externos (Lipton, 2018). Un sistema totalmente transparente permite revisar sus algoritmos y componentes, pero la transparencia por sí sola no garantiza que un ser humano pueda procesar o predecir la lógica interna de un ensamble de diez mil árboles de decisión.
* **Interpretabilidad:** Es la capacidad pasiva de una arquitectura o representación para que un observador humano comprenda la relación causa-efecto entre las entradas y las salidas del sistema en un contexto determinado (Murdoch *et al.*, 2019). La interpretabilidad es una propiedad relacional y dependiente de la audiencia: un modelo aditivo generalizado (GAM) puede ser altamente interpretable para un bioestadístico, pero resultar totalmente opaco para un operador de campo.
* **Explicabilidad:** Corresponde al conjunto de técnicas, procedimientos y artefactos secundarios —tales como vectores de atribución de características, reglas de decisión formales o mapas de calor de atención— generados por un explicador para fundamentar la decisión de un modelo predictivo primario (Phillips *et al.*, 2021).

![Figura 1. Transparencia, interpretabilidad y explicabilidad: tres nociones distintas. Fuente: elaboración propia a partir de Lipton (2018), Murdoch *et al.* (2019), Phillips *et al.* (2021) y Tabassi (2023).](../figures/exported/fig_d1_conceptos_es.png)

Como se ilustra sistemáticamente en la Figura 1, ninguna de estas tres dimensiones equivale automáticamente a la *confiabilidad* (*trustworthiness*). La confiabilidad de un sistema de IA es un atributo holístico que exige, además de la explicabilidad, la verificación empírica de su seguridad física y cibernética, su estabilidad robusta ante ruido, la preservación de la privacidad de los datos y el cumplimiento de principios de equidad y no discriminación (Tabassi, 2023).

## La frontera crítica: Atribución estadística frente a intervención causal

Un principio metodológico de vital importancia que suele pasarse por alto en la aplicación de XAI consiste en distinguir la **atribución de características** de la **inferencia causal**. Cuando un método post-hoc asigna un puntaje numérico elevado a una variable (por ejemplo, asignando un peso positivo a la variable *Edad* en la aprobación de un crédito), dicho valor describe exclusivamente el grado en que el modelo predictivo se apoya estadísticamente en esa columna dentro de su espacio de representación local.

Bajo ninguna circunstancia debe interpretarse ese coeficiente como una prueba de que modificar dicha variable en el mundo real producirá un cambio causal directo en el fenómeno subyacente (Pearl, 2009). Confundir la dependencia funcional del algoritmo con una relación causa-efecto real puede inducir a intervenciones erróneas o perjudiciales. Por ejemplo, si un modelo médico asocia erróneamente un historial de asma con un menor riesgo de muerte por neumonía (debido a que los asmáticos ingresan directamente a cuidados intensivos recibiendo atención prioritaria), un explicador post-hoc reflejará fielmente que el asma "protege" al paciente según el clasificador. El explicador es fiel a la lógica interna del algoritmo, pero dicha lógica está desconectada de la causalidad biológica. Por ello, la auditoría mediante XAI evalúa la fidelidad descriptiva del modelo, no su verdad causal ontológica.

## Modelos interpretables por diseño frente a explicaciones post-hoc

La comunidad científica en XAI se divide fundamentalmente en dos grandes paradigmas metodológicos para abordar el dilema de la opacidad algorítmica:

1. **Modelos interpretables por diseño (*Ante-hoc* o *Intrinsic Interpretability*):** Algoritmos cuyo funcionamiento interno es conceptualmente transparente por construcción. Ejemplos clásicos incluyen la regresión lineal y logística, los árboles de decisión de baja profundidad y los modelos basados en reglas escasas. Como argumenta con vehemencia Rudin (2019), en aplicaciones de alto riesgo (como la justicia criminal o la medicina de cuidados intensivos), es preferible invertir esfuerzo en la ingeniería de características para entrenar un modelo interpretable por diseño que alcance una precisión competitiva, evitando así la necesidad de aproximaciones secundarias.
2. **Explicaciones post-hoc (*Post-hoc Explainability*):** Procedimientos que operan de manera ex post, tratando al modelo predictivo como un objeto ya entrenado. Cuando el problema requiere el uso de arquitecturas complejas de caja negra —tales como redes neuronales profundas, bosques aleatorios o algoritmos de *gradient boosting*— para maximizar el rendimiento predictivo, las técnicas post-hoc buscan estimar el comportamiento local o global del modelo mediante la construcción de un sustituto (*surrogate*) interpretable.

![Figura 2. Del modelo interpretable por diseño a la explicación post-hoc. Fuente: elaboración propia a partir de Rudin *et al.* (2022) y Marcinkevičs y Vogt (2023).](../figures/exported/fig_d2_modelos_es.png)

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
