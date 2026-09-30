# Por qué importa la inteligencia artificial explicable

## De predecir a responder por decisiones

La expansión de la inteligencia artificial en actividades científicas,
profesionales y administrativas ha trasladado parte del problema desde la capacidad
de predecir hacia la capacidad de responder por una predicción. En una tarea de bajo
impacto puede bastar con que el sistema funcione de manera adecuada. Cuando su salida
orienta un diagnóstico, una asignación de crédito, una alerta de seguridad, una
decisión laboral o una intervención automatizada, también importa conocer qué
información utilizó, bajo qué condiciones puede fallar, quién debe supervisarlo y qué
evidencia permite cuestionar su resultado. La inteligencia artificial explicable
(*explainable artificial intelligence*, XAI) adquiere relevancia en ese tránsito: no
como ornamento comunicativo añadido a un modelo, sino como conjunto de recursos para
investigar, justificar y delimitar su comportamiento en un contexto de uso (Barredo Arrieta
et al., 2020; Ali et al., 2023).

Esta función no se reduce a “abrir” una caja negra. Un sistema puede documentar su
arquitectura y seguir siendo difícil de comprender para quien toma una decisión; a la
inversa, una explicación sencilla puede ser intuitiva y, sin embargo, describir de
forma inexacta el proceso que produjo la salida. Los principios propuestos por
Phillips et al. (2021) separan precisamente la existencia de una explicación, su
significado para una persona concreta, su correspondencia con el proceso del sistema
y el reconocimiento de los límites de conocimiento. La separación es crucial: que
una explicación exista o resulte legible no establece todavía que sea correcta,
útil o suficiente.

Por ello, el problema científico de la XAI no consiste únicamente en generar
representaciones comprensibles. Consiste en determinar cuándo un artefacto
explicativo aporta evidencia para una finalidad definida. Una explicación dirigida a
depurar un modelo responde una pregunta distinta de otra destinada a apoyar una
decisión profesional, documentar una auditoría o permitir que una persona afectada
comprenda y cuestione un resultado. Su calidad depende de la relación entre modelo,
objeto explicativo, audiencia, tarea, riesgo y criterio de evaluación.

## Funciones de la explicación durante el ciclo de vida

La necesidad de explicación aparece antes, durante y después del despliegue. En el
diseño, los artefactos explicativos pueden ayudar a descubrir dependencias espurias,
variables proxy, fugas de información o comportamientos incompatibles con el
conocimiento del dominio. En la validación, permiten formular pruebas dirigidas sobre
casos límite y comparar si distintos modelos apoyan sus salidas en patrones
semejantes. Durante la operación, pueden contribuir al monitoreo de cambios, al
análisis de incidentes y a la identificación de condiciones en las que una salida no
debería aceptarse sin revisión. Después de una decisión, pueden apoyar la
documentación, la auditoría y la contestabilidad. Estas funciones pertenecen a un
ciclo de gestión del riesgo y no a un único momento de visualización (Tabassi, 2023).

Cada función exige evidencia diferente. Para depurar, puede ser útil localizar qué
características influyen en predicciones anómalas; para validar, importa comprobar si
esa señal se conserva ante perturbaciones relevantes; para supervisar, deben
comunicarse incertidumbre, límites y condiciones de uso; para auditar, se necesita
trazabilidad entre datos, versión del modelo, configuración del explicador y
conclusión. Una misma gráfica no satisface automáticamente todas esas necesidades.
Tampoco todo fallo requiere otro algoritmo explicativo: en ocasiones la respuesta
adecuada es mejorar los datos, restringir el ámbito de uso, elegir un modelo
interpretable por diseño o impedir que el sistema decida sin intervención humana.

Entender la explicación como parte del ciclo de vida evita dos reducciones frecuentes.
La primera consiste en identificar XAI con una imagen o lista de importancias
producida después del entrenamiento. La segunda consiste en evaluar esa salida fuera
del proceso que pretende apoyar. Una explicación útil para diagnosticar un error de
desarrollo puede ser inadecuada para comunicar una decisión individual. Del mismo
modo, una representación eficaz en una demostración controlada puede perder valor si
el modelo, los datos o las condiciones operativas cambian.

## Audiencias, preguntas y responsabilidades distintas

No existe una explicación universal porque tampoco existe un destinatario universal.
Quien desarrolla un sistema necesita información que permita reproducir y corregir
su comportamiento. Un equipo de validación necesita pruebas independientes y
criterios de aceptación. Un profesional del dominio necesita conocer la pertinencia
de la evidencia, los límites y la posibilidad de apartarse de la recomendación. La
dirección de una organización requiere comprender exposición al riesgo y controles.
Una autoridad supervisora necesita documentación verificable. La persona afectada
por una decisión necesita una comunicación comprensible, específica y vinculada con
las posibilidades reales de revisión o actuación.

Phillips et al. (2021) sostienen que el significado de una explicación depende del
usuario y de la situación, mientras Miller (2019) muestra que las explicaciones
humanas suelen ser selectivas, sociales y contrastivas: con frecuencia responden por
qué ocurrió un resultado en lugar de otro. Estas observaciones ayudan a diseñar la
comunicación, pero no eliminan la obligación técnica de comprobar que lo comunicado
corresponde al comportamiento del sistema. La explicación destinada a una persona
afectada puede priorizar claridad y contraste; la dirigida a un auditor puede exigir
artefactos, parámetros y pruebas que serían impropios para esa comunicación. Adaptar
el formato no autoriza a cambiar el hecho explicado ni a ocultar incertidumbre.

La consecuencia metodológica es directa: antes de seleccionar un método XAI deben
declararse la pregunta, la audiencia y la acción que la explicación pretende apoyar.
Sin esa especificación, términos como “comprensible”, “útil” o “accionable” carecen
de un criterio verificable. Una evaluación rigurosa debe distinguir, además, entre
percepción subjetiva, comprensión demostrada, desempeño en una tarea y posibilidad
de actuar. Son resultados relacionados, pero no equivalentes.

## Explicabilidad, confianza y confiabilidad

La explicabilidad es una dimensión de la IA confiable, no un sustituto de las demás.
El marco de gestión de riesgos de NIST sitúa explicabilidad e interpretabilidad junto
con validez y fiabilidad, seguridad, resiliencia, privacidad, equidad, transparencia
y rendición de cuentas; también advierte que estas características dependen del
contexto y pueden entrar en tensión (Tabassi, 2023). Una explicación técnicamente
fiel no corrige un conjunto de datos sesgado, no garantiza seguridad y no convierte
una predicción en causal. Del mismo modo, una interfaz clara no compensa un modelo
inválido para la población o el uso previstos.

También debe distinguirse confianza de confianza calibrada. El objetivo no es elevar
la aceptación del sistema, sino favorecer una dependencia proporcional a su
competencia y a la evidencia disponible. Una explicación persuasiva puede aumentar
la confianza aun cuando sea incompleta; una explicación compleja pero exacta puede
no ayudar a una persona a decidir. La revisión sistemática de Kim et al. (2024)
organiza la evaluación humana en dimensiones diferentes: calidad de la explicación
en contexto, contribución a la interacción humano-IA y contribución al desempeño.
Que una persona declare comprender o confiar en el sistema no demuestra por sí mismo
que decida mejor.

La evidencia experimental refuerza esta cautela. En las tareas estudiadas por
Alufaisan et al. (2021), proporcionar una predicción de IA tendió a mejorar la
exactitud humana, pero añadir información explicativa no produjo evidencia concluyente
de una mejora adicional. En una serie de experimentos prerregistrados sobre modelos
de precios de vivienda, Poursabzi-Sangdeh et al. (2021) observaron que un modelo claro
y con pocas variables facilitaba simular sus predicciones, sin mejorar necesariamente
el seguimiento apropiado de la recomendación; en condiciones concretas, la
transparencia incluso dificultó detectar y corregir errores grandes. Estos resultados
no prueban que las explicaciones nunca ayuden. Muestran que comprensión del modelo,
confianza, corrección de errores y desempeño decisional deben medirse por separado y
dentro de la tarea experimental que los produce.

## Supervisión, gobernanza y contestabilidad

La importancia práctica de la XAI también se refleja en marcos de gobernanza que
vinculan transparencia con uso apropiado y supervisión humana. Para los sistemas de
alto riesgo dentro de su ámbito, el artículo 13 del Reglamento de Inteligencia
Artificial de la Unión Europea exige un grado de transparencia que permita a los
responsables del despliegue interpretar la salida y utilizarla adecuadamente; el
artículo 14 relaciona la supervisión con comprender capacidades y límites, reconocer
el sesgo de automatización y poder ignorar, revertir o interrumpir una salida cuando
corresponda (European Parliament & Council of the European Union, 2024). Esta
exigencia no prescribe un explicador universal ni demuestra la eficacia de una
técnica concreta. Sí muestra que la interpretación debe integrarse con información
sobre desempeño, limitaciones, documentación y capacidad real de intervención.

La contestabilidad amplía esa lógica. Una explicación solo contribuye a impugnar una
decisión si identifica un resultado concreto, se conecta con el proceso que puede
revisarlo y no ofrece cambios imposibles como si fueran opciones reales. Por tanto,
la gobernanza de explicaciones abarca más que su forma: incluye procedencia,
responsabilidad, registro de versiones, conservación de evidencia y vías para actuar
ante un error. En ausencia de esas condiciones, la explicación corre el riesgo de
convertirse en una justificación unilateral del sistema.

## Objetivo, tesis y recorrido del capítulo

Este capítulo ofrece una síntesis científica y legible de los fundamentos, las
aplicaciones emergentes y las principales brechas de la XAI, y presenta FOM-7 como
una respuesta metodológica acotada al problema de evaluar comparativamente
explicaciones post-hoc. Su pregunta rectora es: ¿bajo qué condiciones una explicación
de un sistema de IA puede considerarse evidencia útil, reproducible y defendible para
una audiencia y un propósito concretos?

La tesis central es que una explicación no se convierte en evidencia por ser clara o
convincente. Debe existir correspondencia entre la pregunta formulada, el objeto
explicativo, el constructo evaluado, la audiencia, el diseño de prueba y el alcance de
la afirmación. Desde esa tesis, el capítulo define primero qué es y qué no es XAI;
examina después áreas de aplicación mediante ejemplos y límites; organiza las
brechas técnicas, humanas, causales, operativas y de gobernanza; y finalmente presenta
FOM-7 y el caso Adult/tabular como demostración de una evaluación funcionalmente
fundamentada. El caso no establece un ranking universal de explicadores. Su función
es mostrar cómo la trazabilidad y el control del diseño permiten distinguir una
salida plausible de una afirmación empírica defendible.
