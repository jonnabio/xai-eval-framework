---
title: "Tesis doctoral: incorporación de los estudios de seguimiento"
subtitle: "Registro de cambios para el tutor"
author: "Jonathan Herrera Vásquez"
date: "12 de octubre de 2026"
lang: es
---

# Propósito de este documento

Desde la versión de la tesis que usted revisó se han completado tres estudios
nuevos y se han añadido controles al estudio de los jueces basados en modelos
de lenguaje. Los cuatro trabajos están enviados a revistas. Este documento
describe cómo se han incorporado a la tesis, qué cambia en cada capítulo y qué
no cambia, y las decisiones de diseño acordadas con usted.

El criterio seguido es el que usted destacó en su última nota: separar lo que se
planificó de lo que se descubrió después. Por eso los estudios nuevos no se
mezclan con los capítulos confirmativos.

# Lo que no cambia

- El objetivo general, los seis objetivos específicos, las hipótesis H1–H3 y
  las proposiciones P1 y P2, con su redacción actual.
- El protocolo FOM-7 y la decisión de la puerta 3.
- Todas las tablas de resultados de los Capítulos 4 y 5 y la resolución de las
  hipótesis.
- El contraste de Wilcoxon sobre bloques agregados y su declaración como
  seguimiento posterior.
- La tabla de amenazas a la validez, salvo una fila (véase más abajo), y la
  frase sobre el límite de constructo.
- Los criterios de selección de métodos.

# Lo que se añade: un capítulo nuevo

Se añade el **Capítulo 6, «Estudios de seguimiento: alcance de validez de las
conclusiones»**, entre la taxonomía y las conclusiones, que pasan a ser el
Capítulo 7. Tiene unas 3,400 palabras y cinco tablas.

El capítulo abre con una sección que declara el estatuto de estos trabajos
antes de reportar ningún resultado:

- son posteriores al plan inferencial congelado en la puerta 1 de FOM-7;
- no añaden objetivos específicos ni hipótesis, y se adscriben a la cláusula
  final del objetivo general («delimitando explícitamente el alcance de validez
  de la evidencia obtenida»);
- cada uno tuvo su propio plan de análisis, registrado en el repositorio antes
  de calcular sus resultados, y los análisis añadidos después se señalan como
  *post hoc*;
- ninguno modifica la resolución de H1–H3, P1 o P2.

Cada estudio examina un eje sobre el cual una conclusión del benchmark podría
no sostenerse.

| Estudio | Pregunta | Resultado principal | Límite principal |
|:--|:--|:--|:--|
| **Fiabilidad ante el Error** | ¿Son menos fiables las explicaciones cuando el modelo se equivoca? | Reanálisis de 265 ejecuciones del benchmark. La estabilidad es menor en las instancias mal clasificadas para los cuatro explicadores. El déficit es grande para SHAP ($d_z = -1.36$) y DiCE ($d_z = -2.15$). El de DiCE se explica por la cercanía a la frontera de decisión; el de SHAP, no. | El contraste externo en German Credit no reproduce el déficit de SHAP. |
| **Concordancia entre Explicadores** | ¿Cuánto coinciden SHAP y LIME sobre la misma instancia? | 31,411 explicaciones pareadas. El solapamiento medio de las cinco características principales es 0.393 en Adult, 0.387 en German Credit y 0.714 en Breast Cancer. Ningún método se reproduce por completo a sí mismo al repetirse. | Tres conjuntos de datos y una configuración por explicador. |
| **Transferencia entre Conjuntos de Datos** | ¿Se mantiene el orden de los métodos en otros conjuntos de datos? | Experimento nuevo: 16 conjuntos de datos, 1,280 ejecuciones. La concordancia de los órdenes entre conjuntos es 0.67 en la brecha de fidelidad, 0.88 en estabilidad, 0.79 en parsimonia y 0.87 en coste. El orden entre Anchors y DiCE no se transfiere. | Describe la concordancia bajo un protocolo de evaluación fijo, no la calidad de las explicaciones en general. |
| **Controles del Estudio de Fiabilidad Inter-juez** | ¿Sobre qué acuerdan los jueces cuando acuerdan? | Hasta el 67 % de la varianza de las puntuaciones se sitúa entre métodos. Al eliminar siete de diez elementos, los tres jueces lo detectan; al asignar los pesos a características equivocadas, solo uno de los tres. | Sin puntuaciones humanas; una llamada por juez en los controles. |

El capítulo cierra con una tabla que indica, para cada conclusión de los
estudios principales, qué añade el seguimiento. En los cinco casos la conclusión
se mantiene, con precisiones sobre su alcance.

El resultado sobre los jueces queda reforzado: los jueces de esta clase
acuerdan sobre el método y sobre la forma visible de una explicación, no sobre
si es correcta.

# Cambios en los capítulos existentes

| Lugar | Cambio |
|:--|:--|
| Resumen y Abstract | Una frase añadida, idéntica en ambos idiomas y sin cifras nuevas, que enumera los cuatro trabajos de seguimiento. |
| Introducción | «Seis capítulos» pasa a «siete»; una frase sobre los trabajos de seguimiento; el párrafo de estructura menciona el Capítulo 6 nuevo. |
| Capítulo 1, tabla de estudios | Tres filas nuevas, marcadas como «seguimiento» y adscritas al objetivo general. Un párrafo bajo la tabla declara su estatuto. La columna de capítulos del Estudio de Fiabilidad Inter-juez añade el 6. |
| Capítulo 3, amenazas a la validez | Fila de validez externa: el control aplicado menciona el estudio sobre 16 conjuntos de datos; el riesgo residual precisa que ese estudio cubre el orden de los métodos y no los valores del benchmark. |
| Capítulo 3, estudios complementarios | Un párrafo que remite al Capítulo 6. Una frase sobre la condición primaria de la segunda cohorte de jueces (véase «Dos precisiones»). |
| Capítulo 5, estudio inter-juez | Un párrafo, «Controles posteriores», que remite al Capítulo 6. El cierre del capítulo anuncia los Capítulos 6 y 7. |
| Capítulo 7 (conclusiones) | Subsección nueva, «Aportes de los estudios de seguimiento», con cuatro precisiones y tres recomendaciones de reporte. Se actualizan la primera limitación, una celda de la tabla de fronteras de generalización, la línea futura 4 y la síntesis final. |
| Apéndices | Apéndice G nuevo, con el plan, el código, los resultados y el archivo Zenodo de cada estudio de seguimiento. |
| Todo el documento | Las menciones literales al «Capítulo 6» como conclusiones pasan a «Capítulo 7». |

Las tres recomendaciones de reporte que se incorporan a las conclusiones son:
reportar la calidad de la explicación por separado para predicciones correctas
e incorrectas; acompañar toda comparación entre explicadores de la
repetibilidad de cada uno; y declarar el protocolo del que depende un orden
entre métodos antes de tratarlo como propiedad de los métodos.

# Dos precisiones sobre lo ya escrito

La revisión posterior del estudio de jueces encontró dos hechos que afectan a
la lectura del Capítulo 5, y la tesis ahora los declara.

1. **La condición «con la etiqueta oculta» no la ocultaba de forma efectiva.**
   El registro entregado a los jueces contenía las métricas técnicas y el
   resultado de la predicción, de los que se deduce la etiqueta. Se añadió una
   condición sin esa información. El resultado negativo de P2 no cambia.
2. **Anchors y DiCE se puntuaron en un formato que no es el suyo.** El formato
   común presenta la regla sin umbrales y el contrafactual sin dirección. Los
   controles posteriores se restringen por ello a SHAP y LIME.

# Correcciones menores halladas en la revisión final

- **Tres figuras del Capítulo 4** habían sido sustituidas por error, el 5 de
  octubre, por sus versiones en blanco y negro preparadas para el capítulo de
  libro. Los datos eran los mismos, pero una etiqueta de la matriz de
  correlación no se leía. Se han restaurado las versiones en color y se ha
  corregido el generador para que no vuelva a ocurrir.
- **Apéndice B:** una referencia a la «Tabla 3.1» estaba escrita a mano; ahora
  es una referencia cruzada generada.
- **Apéndice C:** la tabla de sensibilidad de KernelSHAP al conjunto de
  referencia declara ahora que sus archivos de salida no se conservan y que se
  reporta como medición exploratoria.
- **Barrido de cifras.** La verificación automática cubre ahora todos los
  archivos de la tesis. La introducción y los Capítulos 1 y 2 no tenían ninguna
  cifra sin registrar; los apéndices tenían diez, todas resueltas.

# Decisiones de diseño acordadas

Las cuatro decisiones siguientes se acordaron con usted el 12 de octubre de
2026 y son las que aplica el texto.

1. **Capítulo propio para los estudios de seguimiento.** La alternativa era
   repartir su diseño en el Capítulo 3 y sus resultados en el Capítulo 4. Se
   descartó porque mezcla resultados posteriores con los confirmativos.
2. **Ningún objetivo específico nuevo.** La alternativa era un objetivo
   exploratorio OE7, redactado como OE6. Se descartó porque un objetivo se
   formula antes de su resultado.
3. **Nombres de los estudios:** Estudio de Fiabilidad ante el Error, Estudio de
   Concordancia entre Explicadores y Estudio de Transferencia entre Conjuntos
   de Datos.
4. **Extensión.** El capítulo nuevo resume cada estudio en una o dos páginas.

# Verificación realizada

- Las 79 cifras del capítulo nuevo se vuelven a derivar de los archivos de
  resultados en la verificación automática; ninguna se escribió a mano.
- La verificación completa pasa: 1,387 afirmaciones, 1,728 lugares, 38 archivos
  cubiertos.
- La tesis se ha renderizado completa a Word: siete capítulos, ninguna
  referencia cruzada sin resolver.
- Se ha repasado la lista de enunciados de primer nivel (objetivos, hipótesis,
  proposiciones, Resumen y Abstract) frente al cuerpo: son coherentes.

Queda pendiente, antes del depósito, comprobar la política de publicación previa
de cada revista con un artículo en revisión, dado que la tesis incluirá sus
resultados.
