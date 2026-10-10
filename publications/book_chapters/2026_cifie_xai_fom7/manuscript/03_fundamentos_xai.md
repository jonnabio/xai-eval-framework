# Qué es y qué no es la inteligencia artificial explicable

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
