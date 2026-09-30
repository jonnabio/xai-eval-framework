# Por qué importa la inteligencia artificial explicable

Fuente inicial: `references/candidate_literature_2026-09-28.md`, `sources/evidence_map.md` y `planning/chapter_scaffold_2026-09-28.md`.

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

## Ámbitos de aplicación y horizontes próximos

### Por qué examinar la XAI por ámbitos

Las secciones anteriores mostraron que una explicación solo adquiere valor cuando se conoce la pregunta que responde, la audiencia a la que sirve y la evidencia que la respalda. Los ámbitos de aplicación hacen visible esa dependencia. En cada uno cambia la decisión apoyada por el sistema, cambia quién necesita la explicación, cambia el daño que puede causar una explicación engañosa y cambia la evidencia que debería exigirse antes de confiar en ella. Por eso, esta sección no presenta un catálogo de usos, sino cinco ámbitos que plantean exigencias explicativas distintas.

Cada ámbito se examina con la misma pauta: la decisión o tarea, el actor que necesita la explicación, un ejemplo acotado, el beneficio plausible, el modo de fallo y la evidencia necesaria. Los ejemplos son escenarios ilustrativos construidos para aclarar el razonamiento; no describen resultados de un sistema concreto. Las afirmaciones empíricas se apoyan en las fuentes citadas y se limitan a lo que esas fuentes estudiaron. Cada ámbito se cierra con un horizonte próximo, formulado como una trayectoria de investigación o de gobernanza respaldada por la literatura, no como una predicción.

### Salud y biomedicina

En salud, los modelos de aprendizaje automático apoyan tareas como la estratificación del riesgo, la priorización de casos o la lectura de imágenes. La explicación la necesitan actores distintos: el equipo que desarrolla y valida el modelo, el profesional que decide sobre un paciente, el comité que autoriza su uso y la persona afectada por la decisión. La Organización Mundial de la Salud sitúa la transparencia, la explicabilidad y la inteligibilidad entre sus principios éticos para la IA en salud, junto con la protección de la autonomía, la seguridad, la responsabilidad, la equidad y la sostenibilidad, y vincula esos principios con una gobernanza que acompaña todo el ciclo de vida del sistema (World Health Organization, 2021).

Un escenario ilustrativo aclara el beneficio posible. Un equipo evalúa un modelo que estima riesgo a partir de imágenes y examina mapas de relevancia sobre un conjunto de casos. Si las regiones destacadas coinciden de forma sistemática con marcas de adquisición o anotaciones del equipo técnico, y no con hallazgos anatómicos, la explicación ha servido para interrogar el modelo y detectar una dependencia espuria antes del despliegue. Esa es una función valiosa y verificable: ayuda a formular hipótesis sobre el comportamiento del modelo que luego pueden contrastarse.

El modo de fallo aparece cuando la misma herramienta se traslada a la decisión individual. Ghassemi et al. (2021) sostienen, desde una perspectiva crítica, que los enfoques post-hoc actuales pueden ayudar a interrogar un modelo, pero no garantizan que una explicación concreta sea correcta para un paciente concreto; un mapa de calor puede parecer razonable para el clínico y, aun así, no justificar la predicción. Su recomendación es exigir validación rigurosa del desempeño en lugar de confiar en la plausibilidad de la explicación. La evidencia necesaria, por tanto, no es solo una explicación comprensible, sino validación clínica del modelo, estudios sobre cómo cambian las decisiones profesionales y documentación del alcance en que el sistema puede usarse.

**Horizonte próximo.** La trayectoria más respaldada es la integración de la explicabilidad en la gobernanza del ciclo de vida: documentación, validación antes del despliegue y seguimiento posterior (World Health Organization, 2021). La pregunta abierta es empírica: si las explicaciones mejoran decisiones clínicas reales, algo que requiere estudios centrados en humanos y en la aplicación, cuya práctica aún carece de marcos de evaluación homogéneos (Kim et al., 2024).

### Finanzas y decisiones de asignación

En finanzas, la explicabilidad acompaña decisiones que asignan oportunidades o gestionan riesgos. La revisión sistemática de Weber et al. (2024) documenta aplicaciones de XAI en la gestión del riesgo, incluida la evaluación crediticia, en la gestión de carteras, en el análisis de mercados y en la prevención del blanqueo de capitales, con una cobertura de evidencia desigual entre esas áreas. La existencia de aplicaciones no demuestra, por sí sola, su eficacia operativa ni su adecuación regulatoria.

La evaluación crediticia muestra con claridad por qué una misma decisión exige explicaciones diferentes. Ante la denegación de un crédito, un analista de riesgos necesita saber si el modelo se apoya en variables que actúan como sustitutos de atributos protegidos o en patrones incompatibles con la política de la entidad; para ello son útiles las atribuciones agregadas y las auditorías sobre subgrupos. La persona solicitante necesita otra cosa: entender la decisión, poder impugnarla y saber qué cambios razonables podrían alterar el resultado. Esa segunda necesidad remite a las explicaciones contrafactuales y al llamado *recourse* algorítmico (Wachter et al., 2017; Karimi et al., 2022). La normativa refuerza esta distinción: el Reglamento de Inteligencia Artificial de la Unión Europea clasifica como de alto riesgo los sistemas destinados a evaluar la solvencia de personas físicas y exige, para esos sistemas, un grado de transparencia que permita a quienes los despliegan interpretar sus resultados y usarlos adecuadamente (European Parliament & Council of the European Union, 2024).

Los modos de fallo son conocidos. Las variables correlacionadas pueden repartir la importancia de forma engañosa, y un contrafactual válido para el modelo puede proponer cambios imposibles, costosos o ajenos a la situación real de la persona. La literatura sobre contrafactuales advierte que una alternativa puede satisfacer la condición formal de cambiar la predicción y, aun así, apoyarse en regiones poco plausibles de los datos o ignorar restricciones de factibilidad (Laugel et al., 2019; Poyiadzi et al., 2020; Karimi et al., 2022). El caso empírico de este capítulo emplea un problema tabular de ingresos con variables demográficas y laborales; sus resultados ilustran el tipo de evaluación aplicable a este ámbito, pero no se trasladan automáticamente al crédito.

**Horizonte próximo.** La combinación de obligaciones de transparencia y de decisiones con consecuencias individuales hace previsible una demanda creciente de explicaciones auditables y de recursos contrafactuales factibles. La brecha científica es la evaluación del *recourse*: demostrar que una alternativa propuesta es viable, estable y justa para la persona, y no solo válida para el modelo.

### Ciberseguridad e infraestructura crítica

En ciberseguridad, los modelos apoyan la detección de intrusiones, software malicioso y otras amenazas, y las explicaciones se dirigen sobre todo a analistas que deben decidir con rapidez qué alertas investigar. La revisión de Rjoub et al. (2023) organiza estos usos y subraya desafíos propios del ámbito, entre ellos las restricciones operativas y la presencia de adversarios.

El escenario típico es el de un analista que recibe una alerta sobre un dominio o un flujo de red y necesita saber qué rasgos llevaron al detector a marcarlo. Una explicación útil puede ayudar a priorizar alertas, a descartar falsos positivos y a documentar la decisión. Sin embargo, la evidencia disponible invita a la cautela. En un estudio con participantes con conocimientos de ciberseguridad, Roch et al. (2026) observaron que las explicaciones no mejoraron el desempeño ni la confianza en la tarea estudiada, de bloqueo de dominios maliciosos. El resultado se limita a esa población, esa tarea y ese diseño de explicación, pero muestra que la utilidad para el analista no puede darse por supuesta.

El ámbito añade un modo de fallo que en otros es secundario: el adversario. Se ha demostrado que explicadores post-hoc como LIME y SHAP pueden ser manipulados para ocultar el comportamiento real de un modelo (Slack et al., 2020). En un entorno donde un atacante tiene incentivos para evadir la detección, una explicación también es una superficie de ataque. La evidencia necesaria incluye, por tanto, pruebas de robustez de las explicaciones y evaluación dentro del flujo de trabajo real del analista.

**Horizonte próximo.** La trayectoria más probable es la incorporación de explicaciones en los flujos de triaje de alertas. Las necesidades de investigación son la evaluación operativa, con tiempos, carga de trabajo y errores reales, y la evidencia sobre ataques dirigidos específicamente a las explicaciones en sistemas desplegados, todavía escasa.

### Sistemas autónomos e industriales

En los sistemas autónomos, las decisiones se encadenan en tiempo real y los errores pueden tener consecuencias físicas. La revisión sistemática de Kuznietsov et al. (2024) sobre conducción autónoma distingue varias funciones de la XAI: el diseño de componentes interpretables, las explicaciones mediante modelos sustitutos, el monitoreo del sistema, la validación y la comunicación con los ocupantes y otros usuarios. Un ingeniero que revisa por qué un vehículo frenó ante un obstáculo inexistente, o por qué un modelo de mantenimiento predictivo anticipó una avería en una línea industrial, usa la explicación como herramienta de diagnóstico y de validación.

Ese uso técnico debe distinguirse de la comunicación con las personas. Kaufman et al. (2025) mostraron, en escenarios simulados, que explicaciones erróneas de un vehículo autónomo redujeron la comodidad, la dependencia, la satisfacción y la confianza en la conducción de los participantes, aun cuando el comportamiento de conducción se mantenía constante. El resultado mide juicios humanos, no seguridad del vehículo, pero indica que la calidad de la explicación influye en la respuesta de las personas con independencia de lo que el sistema haga.

El modo de fallo principal es confundir una justificación legible con una garantía. Una explicación puede contribuir a la validación y al análisis de fallos, pero no constituye por sí misma un caso de seguridad (Kuznietsov et al., 2024). La evidencia necesaria incluye pruebas del sistema completo, análisis de escenarios límite y mecanismos para detectar cuándo el entorno se aleja de las condiciones de validación.

**Horizonte próximo.** La literatura apunta a integrar las explicaciones en el monitoreo y la validación continuos, más que a ofrecerlas solo como comunicación. Una dificultad transversal refuerza esta dirección: una explicación ajustada a una distribución de datos puede dejar de aproximar adecuadamente el modelo cuando la distribución cambia, lo que obliga a evaluar las explicaciones también frente a esos cambios (Lakkaraju et al., 2020).

### Modelos fundacionales, de lenguaje y multimodales

Los modelos de lenguaje de gran escala amplían y transforman el problema. Zhao et al. (2024) muestran que su explicabilidad exige métodos adaptados al tamaño de los modelos y a su forma de uso, y que la evaluación de esas explicaciones, incluida su fidelidad al proceso interno, enfrenta problemas distintos de los de la XAI tabular. Además, estos modelos pueden generar por sí mismos razonamientos en lenguaje natural, lo que crea una tentación nueva: tratar la justificación que el modelo escribe como si describiera cómo llegó a su respuesta.

La evidencia experimental muestra por qué esa tentación es arriesgada. Turpin et al. (2023) introdujeron sesgos controlados en las indicaciones y observaron que los razonamientos en cadena podían omitir los factores que efectivamente influyeron en la respuesta y justificar respuestas sesgadas. Zaman y Srivastava (2026) matizan esa conclusión: que un razonamiento no mencione un factor no basta para declararlo infiel, porque puede ser incompleto sin ser engañoso, y las conclusiones varían según la métrica y el presupuesto de inferencia. El debate no está cerrado, pero ambos trabajos coinciden en un punto metodológico: la fidelidad de una explicación generada depende de cómo se mida.

Un equipo que verifica si un asistente responde a partir de los documentos que se le proporcionan ilustra la exigencia práctica. La explicación que el propio modelo redacta no demuestra por sí sola que la respuesta se apoye en esas fuentes; se requieren pruebas que manipulen la evidencia disponible y observen si la respuesta cambia en consecuencia.

**Horizonte próximo.** La explicabilidad de estos modelos es uno de los frentes más activos del campo, y su evaluación sigue abierta. Las extensiones a sistemas multimodales plantean las mismas preguntas con mayor complejidad, y la evidencia sobre la fidelidad de sus explicaciones es todavía limitada.

### Lo que los ámbitos tienen en común

Los cinco ámbitos confirman tres ideas que recorren el capítulo. Primero, ningún tipo de explicación sirve a todas las audiencias: el equipo técnico, el profesional que decide, la persona afectada y el regulador formulan preguntas distintas sobre el mismo sistema. Segundo, el beneficio de una explicación depende de la evidencia que la respalda, no de su claridad; en varios de los estudios citados, las explicaciones no mejoraron el desempeño en la tarea, y las explicaciones erróneas deterioraron la respuesta de las personas. Tercero, cada ámbito añade condiciones propias, como la validación clínica, la factibilidad del *recourse*, la presencia de adversarios, la seguridad física o la fidelidad de razonamientos generados.

Estas coincidencias explican el orden del resto del capítulo. Antes de comparar métodos concretos es necesario entender qué objeto explicativo produce cada familia y por qué evaluar esos objetos resulta difícil. La sección siguiente aborda ese problema, que prepara la presentación de FOM-7 como una respuesta acotada para la evaluación funcional y comparativa de explicaciones.
