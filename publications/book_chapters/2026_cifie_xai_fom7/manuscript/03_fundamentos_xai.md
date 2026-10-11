# Qué es y qué no es la inteligencia artificial explicable

## XAI: conceptos, modelos y objetos explicativos

La XAI reúne modelos, explicadores, interfaces y prácticas para examinar salidas o comportamientos de IA con un propósito definido; no designa un algoritmo único. Incluye atribuciones, reglas, ejemplos, contrafactuales y resúmenes locales o globales (Guidotti et al., 2018; Marcinkevičs & Vogt, 2023; Schwalbe & Finzel, 2024). El objeto puede ser una predicción, un patrón del modelo o una decisión sociotécnica; esas preguntas no son intercambiables. La explicación depende también de la audiencia, el contexto y la posibilidad de actuar (Miller, 2019; Phillips et al., 2021).

En este capítulo, **interpretabilidad** describe si una audiencia comprende aspectos relevantes del sistema para una tarea; **explicabilidad**, los procedimientos y artefactos que buscan ofrecer razones examinables; y **transparencia**, la visibilidad de estructura, datos, supuestos, versiones y responsabilidades (Lipton, 2018; Murdoch et al., 2019). Véase la Figura 1. Se relacionan, pero no se sustituyen: una explicación post-hoc no revela todo el mecanismo, y la claridad no prueba fidelidad (Phillips et al., 2021). Ninguna de estas propiedades certifica por sí sola confiabilidad, seguridad, equidad o validez (Tabassi, 2023).

![Figura 1. Transparencia, interpretabilidad y explicabilidad: tres nociones distintas. Fuente: elaboración propia a partir de Lipton (2018), Murdoch et al. (2019), Phillips et al. (2021) y Tabassi (2023).](../figures/exported/fig_d1_conceptos_es.png)

Los modelos interpretables por diseño —por ejemplo, reglas breves, árboles poco profundos y modelos aditivos— exponen su lógica de forma directa, aunque la complejidad puede reducir su comprensión práctica. Si alcanzan desempeño adecuado para el dominio, deben considerarse antes que una caja negra post-hoc (Rudin et al., 2022). Véase la Figura 2. Los explicadores post-hoc construyen aproximaciones a partir de consultas o componentes del predictor; no recuperan el modelo completo. Los métodos agnósticos usan entradas y salidas, mientras los específicos aprovechan información interna. Ningún enfoque garantiza fidelidad por su etiqueta: la validez depende de configuración, referencia y pregunta (Marcinkevičs & Vogt, 2023).

![Figura 2. Del modelo interpretable por diseño a la explicación post-hoc. Fuente: elaboración propia a partir de Rudin et al. (2022) y Marcinkevičs y Vogt (2023).](../figures/exported/fig_d2_modelos_es.png)

Una explicación **local** caracteriza una instancia o región próxima; una **global** resume patrones de una población. Subgrupos y cohortes son escalas intermedias. Lo local no autoriza generalizar: agregar explicaciones puede ocultar heterogeneidad, y un promedio global puede no describir un caso. FOM-7 exige alinear escala del artefacto, unidad de análisis y alcance de la conclusión.

Las **atribuciones** asignan relevancia a características; las **reglas** expresan condiciones suficientes; los **ejemplos** sitúan un caso respecto de otros; los **contrafactuales** proponen cambios; y los **conceptos** relacionan representaciones con categorías. Véase la Figura 3. Sus riesgos difieren: una atribución no prueba causalidad, una regla precisa puede tener poca cobertura y un contrafactual puede ser inviable. Por ello, objetos distintos no deben reducirse a una escala universal (Karimi et al., 2022; Nauta et al., 2023). LIME y SHAP producen atribuciones; Anchors, reglas; DiCE, contrafactuales.

![Figura 3. Un mismo caso explicado mediante cuatro objetos explicativos. Fuente: elaboración propia a partir de Ribeiro et al. (2016), Lundberg y Lee (2017), Ribeiro et al. (2018) y Mothilal et al. (2020); caso y valores ilustrativos.](../figures/exported/fig_d4_objetos_explicativos_es.png)

## Qué propiedades puede demostrar una explicación

La **plausibilidad** describe si una explicación parece razonable; la **fidelidad**, cuánto corresponde al comportamiento del predictor. Pueden divergir. La **estabilidad** mide consistencia bajo variaciones definidas; la **robustez**, resistencia ante perturbaciones, cambios de distribución o ataques (Alvarez-Melis & Jaakkola, 2018; Nauta et al., 2023). La utilidad humana requiere evaluar una tarea y audiencia concretas —comprensión, interacción o desempeño— y no se deduce de fidelidad ni de satisfacción declarada (Kim et al., 2024). La evaluación debe definir qué constructo aproxima cada métrica y qué inferencia permite (Doshi-Velez & Kim, 2017; Pawlicki et al., 2024; Bhattacharya & Verbert, 2024).

Una explicación no prueba **causalidad**: atribuciones no son efectos de intervención y contrafactuales pueden ignorar restricciones causales o sociales (Laugel et al., 2019; Karimi et al., 2022). Tampoco certifica **justicia**, ausencia de sesgo o corrección de una decisión; se requieren análisis por grupos y criterios externos al explicador. No garantiza **seguridad**: explicadores post-hoc pueden manipularse para ocultar comportamientos (Slack et al., 2020). Una explicación fiel también puede describir el error de un modelo.

## Niveles de evaluación y alcance de FOM-7

La evaluación puede ser *application-grounded* (expertos y tareas reales), *human-grounded* (personas en tareas simplificadas) o *functionally grounded* (proxies computacionales sin participantes) (Doshi-Velez & Kim, 2017). Véase la Figura 4. FOM-7 se sitúa en este último nivel: gobierna comparaciones computacionales y permite afirmaciones acotadas sobre las métricas observadas, pero no demuestra comprensión, impacto profesional, causalidad ni efectos de despliegue.

![Figura 4. Niveles de evaluación de la explicabilidad y posición de FOM-7. Fuente: adaptada de Doshi-Velez y Kim (2017).](../figures/exported/fig_d6_niveles_evaluacion_es.png)
