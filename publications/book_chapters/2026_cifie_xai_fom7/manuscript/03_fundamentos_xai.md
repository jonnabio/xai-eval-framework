# Qué es y qué no es la inteligencia artificial explicable

## Una familia de métodos y prácticas sociotécnicas

La inteligencia artificial explicable no designa un algoritmo único. Reúne métodos,
modelos, interfaces y prácticas de evaluación destinados a hacer que el
comportamiento o las salidas de un sistema de IA puedan ser examinados por personas
con una finalidad concreta. Las taxonomías del campo incluyen modelos interpretables
por diseño, explicadores post-hoc, descripciones locales y globales, atribuciones,
reglas, ejemplos, contrafactuales, conceptos y visualizaciones, entre otros objetos
(Guidotti et al., 2018; Marcinkevičs & Vogt, 2023; Schwalbe & Finzel, 2023). Hablar de
XAI, por tanto, exige precisar qué se explica, para quién, con qué propósito y mediante
qué evidencia se evaluará la explicación.

El objeto de explicación puede ser una predicción individual, el comportamiento
global de un modelo, un patrón aprendido, una representación interna, un error o una
decisión sociotécnica más amplia. Estos objetos no son intercambiables. Explicar por
qué un clasificador asignó una etiqueta a una instancia no equivale a explicar cómo
fue construido, si sus datos son adecuados o por qué una organización decidió usarlo.
La primera pregunta puede abordarse con un artefacto post-hoc; las demás requieren
documentación del sistema, evidencia del dominio y análisis institucional.

Esta amplitud convierte la XAI en una práctica sociotécnica. El resultado depende del
modelo y del explicador, pero también de la interfaz, el lenguaje, la competencia de
la audiencia, el contexto de decisión y las posibilidades de actuar. Una explicación
no es significativa en abstracto: se vuelve significativa cuando una persona puede
relacionarla con su pregunta sin que esa adaptación distorsione el proceso explicado
(Miller, 2019; Phillips et al., 2021).

## Interpretabilidad, explicabilidad y transparencia

No existe una frontera terminológica aceptada de manera universal, pero conviene
separar tres ideas. En este capítulo, la **interpretabilidad** es la relación por la
que una audiencia puede comprender aspectos relevantes del funcionamiento o de la
salida de un sistema para una tarea. No es solo una propiedad interna: un modelo puede
ser sencillo para una persona experta y opaco para otra audiencia. La
**explicabilidad** comprende los procedimientos y artefactos que intentan producir esa
comprensión o aportar razones examinables. La **transparencia** se refiere a la
visibilidad de elementos del sistema y de su proceso, como estructura, datos,
supuestos, documentación, versiones y responsabilidades (Lipton, 2018; Murdoch et
al., 2019).

Las tres nociones se apoyan, pero no se sustituyen. Conocer la fórmula de un modelo no
garantiza que una persona pueda emplearla en una decisión. Recibir una explicación
post-hoc tampoco vuelve transparente el modelo: el artefacto puede aproximar una
región de su comportamiento sin revelar el mecanismo completo. Asimismo, publicar
documentación técnica mejora la transparencia del proceso, pero no demuestra que una
explicación individual refleje con exactitud la salida. Por ello, la claridad debe
evaluarse junto con la precisión explicativa y con los límites de conocimiento del
sistema (Phillips et al., 2021).

Esta distinción evita usar “interpretable” como sinónimo de “confiable”. La
interpretabilidad puede facilitar inspección y crítica, pero la confiabilidad depende
además de validez, seguridad, robustez, privacidad, equidad y gobernanza. La
explicabilidad contribuye a examinar esas propiedades; no las certifica por sí sola
(Tabassi, 2023).

## Modelos interpretables por diseño y explicaciones post-hoc

Un modelo interpretable por diseño permite examinar su lógica predictiva de forma
relativamente directa. Reglas breves, árboles poco profundos o modelos aditivos con
componentes controlados pueden ofrecer una relación más inmediata entre estructura y
salida. La interpretabilidad, sin embargo, no depende únicamente del nombre de la
familia: un árbol extenso o una regla con numerosas excepciones puede dejar de ser
comprensible en la práctica. En problemas de alto impacto, cuando un modelo
interpretable alcanza un desempeño adecuado y satisface las necesidades del dominio,
su uso debe considerarse antes de adoptar una caja negra acompañada de una
explicación aproximada (Rudin et al., 2022).

Los métodos post-hoc actúan después del entrenamiento. Consultan el predictor,
analizan sus componentes o generan perturbaciones para construir un artefacto que
describa parte de su comportamiento. Ese artefacto no es el modelo ni una copia
completa de su razonamiento. Su validez depende del procedimiento, la muestra de
referencia, el vecindario, la parametrización y la pregunta. En consecuencia, una
explicación post-hoc debe presentarse como aproximación sometida a prueba, no como
transparencia recuperada.

Dentro de este grupo, un método **agnóstico al modelo** utiliza principalmente
entradas y salidas, por lo que puede aplicarse a distintas familias predictivas. Esa
portabilidad facilita comparaciones, pero no garantiza fidelidad: el explicador solo
observa el comportamiento accesible mediante sus consultas. Un método **específico
del modelo** aprovecha gradientes, activaciones, estructura de árboles u otra
información interna; puede ser más eficiente o preciso dentro de una familia, aunque
menos transferible. Agnosticidad y especificidad son decisiones de diseño, no
calificaciones automáticas de calidad (Marcinkevičs & Vogt, 2023).

## Alcance local y alcance global

Una explicación **local** caracteriza una predicción o el comportamiento del modelo
alrededor de una instancia. Es pertinente cuando se investiga una decisión concreta,
un error o un caso límite. Una explicación **global** intenta resumir patrones del
modelo en una población o región amplia: variables relevantes, reglas recurrentes,
interacciones o formas funcionales. Entre ambas existen escalas intermedias, como
subgrupos, cohortes o regiones del espacio de entrada.

El alcance debe declararse porque una explicación local no autoriza una conclusión
global. Agregar explicaciones individuales tampoco produce necesariamente una
representación global válida: la muestra puede no cubrir regiones relevantes, las
reglas locales pueden ser incompatibles y una media puede ocultar heterogeneidad. A
la inversa, un resumen global puede ser correcto en promedio y poco informativo para
una persona concreta. La unidad de explicación y la unidad de inferencia deben
coincidir con la afirmación final.

Esta precaución es central para FOM-7. Una comparación solo es defendible si conserva
la escala a la que se generó el artefacto, la unidad sobre la que se calculó la
métrica y el nivel al que se formula la conclusión. Cambiar de instancia a modelo, o
de ejecución a promedio, es una operación analítica que debe justificarse y quedar
trazada.

## Objetos explicativos y preguntas diferentes

Las principales familias de objetos explicativos pueden organizarse por la pregunta
que responden. Las **atribuciones** distribuyen relevancia entre características para
una salida y ayudan a preguntar qué variables influyeron según el explicador. Las
**reglas** describen condiciones bajo las cuales una predicción se conserva. Los
**ejemplos**, prototipos y casos similares sitúan la instancia respecto de
observaciones conocidas. Los **contrafactuales** buscan cambios que modificarían la
salida. Las explicaciones basadas en **conceptos** relacionan representaciones del
modelo con categorías de mayor nivel. Los resúmenes globales describen patrones,
interacciones o regiones de decisión.

Cada objeto ofrece información y riesgos distintos. Una atribución ordena variables,
pero no establece que intervenir sobre ellas cambie el resultado en el mundo. Una
regla puede alcanzar alta precisión en una región y cubrir pocos casos. Un ejemplo
similar puede ser comprensible sin representar el mecanismo del predictor. Un
contrafactual puede modificar formalmente la salida y ser imposible, costoso o
injusto para la persona. Una explicación por conceptos depende de que esos conceptos
estén bien definidos y alineados con la representación aprendida. Por ello, métodos
que producen objetos distintos no deben reducirse a una escala universal de calidad
(Karimi et al., 2022; Nauta et al., 2023).

En las secciones posteriores, LIME y SHAP se tratarán como productores de
atribuciones o aproximaciones locales, Anchors como productor de reglas y DiCE como
generador de contrafactuales. Esta descripción no los hace equivalentes. Sirve para
vincular cada método con la pregunta que puede responder, el fallo que debe vigilarse
y la evidencia apropiada para evaluarlo.

## Plausibilidad, fidelidad, estabilidad, robustez y utilidad

Una explicación **plausible** parece razonable para una audiencia. La plausibilidad
facilita comunicación, pero puede provenir de expectativas humanas y no de la lógica
del predictor. La **fidelidad** o *faithfulness* evalúa en qué medida el artefacto
corresponde al comportamiento que pretende describir. Ambas propiedades pueden
divergir: una narrativa convincente puede ser infiel, y una representación fiel puede
resultar difícil de interpretar.

La **estabilidad** examina si casos o ejecuciones próximos producen explicaciones
semejantes bajo condiciones definidas. La **robustez** plantea un desafío más amplio:
si la explicación conserva propiedades relevantes ante perturbaciones, cambios de
distribución, variaciones de configuración o acciones adversariales. Ninguna de las
dos debe presumirse. Un explicador puede ser estable frente a ruido leve y frágil ante
un cambio operativo, o mostrar buen desempeño promedio con variabilidad importante
entre instancias (Alvarez-Melis & Jaakkola, 2018; Nauta et al., 2023).

La **utilidad humana** se refiere a la contribución de la explicación a una tarea y a
una audiencia. Puede observarse mediante comprensión, detección de errores,
desempeño, carga cognitiva, confianza calibrada o capacidad de actuar. Estas medidas
no son sustitutos automáticos entre sí. La revisión de Kim et al. (2024) muestra que
la evaluación centrada en personas abarca la calidad experimentada de la explicación,
la interacción humano-IA y el desempeño conjunto. En consecuencia, una métrica
computacional de fidelidad no demuestra utilidad humana, y una valoración subjetiva
positiva no demuestra fidelidad.

La calidad explicativa es, por tanto, multidimensional y dependiente del propósito.
Acumular métricas sin definir sus constructos genera tanta ambigüedad como depender de
un único indicador. La evaluación debe explicar qué propiedad aproxima cada medida,
qué evidencia produce y qué conclusión no permite (Doshi-Velez & Kim, 2017; Pawlicki
et al., 2024; Bhattacharya & Verbert, 2024).

## Lo que una explicación no demuestra

Una explicación predictiva no establece **causalidad**. Las atribuciones describen la
relación entre características y salida bajo un procedimiento; no prueban que una
intervención sobre una característica produzca el efecto observado. Incluso los
contrafactuales algorítmicos pueden proponer combinaciones fuera de la distribución o
acciones que ignoran restricciones causales y sociales (Laugel et al., 2019; Karimi
et al., 2022).

Tampoco establece **justicia**. Una explicación puede ayudar a detectar una variable
proxy o una dependencia problemática, pero no certifica igualdad de desempeño,
ausencia de discriminación ni distribución justa de consecuencias. Esas afirmaciones
requieren definiciones normativas, análisis por grupos y evidencia independiente.

No demuestra **seguridad** ni **robustez operativa**. Un artefacto estable en el
benchmark puede fallar ante entradas adversariales, cambio de distribución o una
versión distinta del modelo. Se ha mostrado, además, que explicadores post-hoc pueden
ser manipulados para ocultar comportamientos problemáticos bajo condiciones de ataque
(Slack et al., 2020). La explicación puede formar parte de una investigación de
seguridad; no constituye por sí misma un caso de seguridad.

Por último, no prueba la **corrección de la decisión**. Una explicación fiel de un
modelo equivocado describe fielmente su error. Para evaluar corrección se necesitan
datos válidos, desempeño pertinente, conocimiento del dominio y criterios de decisión
externos al explicador. Esta separación impide que la XAI se utilice como sello
general de confianza.

## Niveles de evaluación y alcance de FOM-7

Doshi-Velez y Kim (2017) distinguen evaluación centrada en la aplicación, evaluación
centrada en humanos y evaluación funcionalmente fundamentada. La primera utiliza
personas expertas y tareas reales; la segunda estudia personas en tareas
simplificadas; la tercera emplea proxies computacionales sin participantes. Ningún
nivel domina en todos los casos. Cada uno responde preguntas diferentes y exige un
diseño compatible con la afirmación buscada.

FOM-7 se sitúa principalmente en el nivel funcionalmente fundamentado. Controla el
protocolo, la ejecución, los artefactos, la armonización, la inferencia, la
reproducibilidad y la trazabilidad de comparaciones computacionales. Ese alcance
permite sostener afirmaciones acotadas sobre fidelidad, estabilidad, parsimonia,
cobertura o coste bajo las condiciones estudiadas. No autoriza por sí mismo
conclusiones sobre comprensión, confianza calibrada, impacto profesional, causalidad
o consecuencias de despliegue.

Esta taxonomía fija el vocabulario del resto del capítulo. Las aplicaciones se
examinarán según decisión, actor, riesgo y evidencia necesaria; las familias de
métodos se presentarán por el objeto que producen; las brechas se organizarán por el
tipo de validez que falta; y el caso empírico mostrará cómo un protocolo puede
convertir comparaciones heterogéneas en afirmaciones auditables sin convertirlas en
verdades universales.
