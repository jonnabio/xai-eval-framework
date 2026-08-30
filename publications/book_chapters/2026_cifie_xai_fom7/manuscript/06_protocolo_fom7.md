# Protocolo FOM-7 para benchmarking auditable

Fuente inicial: `thesis/capitulo-1-marco-teorico.qmd`, `thesis/capitulo-2-fundamentos.qmd`, `thesis/capitulo-3-diseno-experimental.qmd` y `thesis/capitulo-6-conclusiones.qmd`.

## Función metodológica

FOM-7 (*Framework Operation Method*, siete puertas) se define como una secuencia operativa para convertir ejecuciones de benchmarking XAI en evidencia reproducible, comparable y trazable. Su propósito no es introducir un nuevo explicador ni una métrica aislada, sino gobernar el ciclo completo que conecta diseño experimental, ejecución controlada, calificación de artefactos, armonización analítica, inferencia estadística, perfilado de reproducibilidad y reporte de afirmaciones. En términos metodológicos, FOM-7 ocupa la capa que suele quedar implícita entre dos momentos del trabajo empírico: por un lado, la producción de explicaciones y métricas; por otro, la formulación de conclusiones sobre fidelidad, estabilidad, coste o utilidad técnica de un método.

El protocolo responde directamente a la crisis de evaluación descrita en la sección anterior. La existencia de métodos, métricas y herramientas no garantiza por sí misma que los resultados sean admisibles como evidencia científica. Una librería puede calcular métricas correctamente y, aun así, el estudio puede sobreinterpretar sus resultados si no declara qué artefactos son válidos, qué configuraciones fueron congeladas, qué comparaciones son homogéneas, qué pruebas estadísticas son admisibles y qué límites conserva cada afirmación. Esta distinción se alinea con la literatura que separa evaluación funcional, evaluación con humanos y evaluación en aplicación: FOM-7 se ubica principalmente en el dominio *functionally-grounded*, por lo que produce evidencia computacional trazable, no evidencia directa de comprensión humana ni verdad causal de las explicaciones (Doshi-Velez & Kim, 2017; Hedström et al., 2023; Nauta et al., 2023).

FOM-7 opera como puente entre el diagnóstico y la práctica experimental. La fragmentación métrica se traduce en reglas de armonización; la fragilidad de artefactos se traduce en auditoría de integridad; la irreproducibilidad se traduce en semillas declarativas y perfilado de variación; la sobreafirmación se traduce en trazabilidad de *claims*. Por ello, el protocolo no debe leerse como una lista administrativa, sino como una arquitectura de admisibilidad. Cada puerta responde a un modo de fallo observado en benchmarking XAI y establece qué condiciones deben cumplirse antes de que un resultado pueda sostener inferencia confirmativa. La Tabla 3 resume las siete puertas, sus artefactos de entrada y salida, y el tipo de fallo metodológico que cada una busca controlar.

## Regla secuencial de admisibilidad

Las siete puertas de FOM-7 son secuenciales. Cada puerta debe satisfacerse antes de proceder a la siguiente. Si una puerta falla, los resultados afectados no desaparecen necesariamente, pero se degradan a estatus descriptivo y no pueden sostener afirmaciones inferenciales. Esta regla es importante porque separa dos funciones que con frecuencia se mezclan en estudios de XAI: explorar un fenómeno y demostrar una comparación. Un artefacto incompleto puede ser útil para diagnóstico del pipeline; una celda faltante puede informar sobre viabilidad de un método; una métrica calculada sobre una cohorte parcial puede sugerir una hipótesis. Sin embargo, ninguno de esos elementos debe convertirse en afirmación confirmativa si no atraviesa los controles previos.

La regla central puede formularse así: ninguna afirmación inferencial puede formularse si las puertas previas no están satisfechas y si la afirmación no puede trazarse a artefactos fuente verificables. Esta formulación protege el capítulo contra tres riesgos recurrentes. El primero es la deriva de protocolo: cambios post-hoc en configuraciones, hipótesis, criterios de inclusión, métricas o pruebas estadísticas. El segundo es la contaminación de artefactos: uso de salidas vacías, malformadas, incompletas o no comparables. El tercero es la sobreafirmación: conversión de resultados numéricos en conclusiones generales sin declarar alcance, unidad de análisis o límites.

En la tesis, esta regla también evita la pseudorreplicación. Las métricas pueden computarse por instancia, pero la unidad de análisis inferencial debe respetar la estructura del diseño, especialmente cuando se comparan métodos sobre modelos, semillas y tamaños de muestra. FOM-7 obliga a distinguir entre métricas de instancia, resúmenes de ejecución, bloques comparables y pruebas inferenciales. Así, una diferencia numérica solo se vuelve evidencia comparativa cuando procede de artefactos calificados, unidades homogéneas y una prueba compatible con el diseño. Esta disciplina convierte al protocolo en una defensa contra la apariencia de precisión que producen las tablas cuando el camino desde dato crudo hasta afirmación no está regulado.

## Flujo operativo

El flujo compacto del protocolo es:

```text
Congelación -> Ejecución -> Auditoría -> Armonización -> Exportación -> Perfilado -> Reporte
```

La secuencia resume una lógica de control acumulativo. La congelación impide que el diseño se adapte a los resultados; la ejecución controlada evita corridas ad-hoc; la auditoría filtra artefactos inválidos; la armonización transforma salidas heterogéneas en tablas comparables; la exportación inferencial fija los insumos estadísticos; el perfilado estima variación residual; y el reporte vincula cada afirmación con evidencia identificable. El valor de la secuencia está en que ninguna puerta compensa por completo la ausencia de otra. Una prueba estadística correcta no repara artefactos malformados; una tabla armonizada no corrige una configuración modificada post-hoc; una afirmación elegante no sustituye trazabilidad.

## Puertas del protocolo

### Puerta 1: Congelación del protocolo

La primera puerta bloquea versiones de código, archivos de configuración YAML, factores del diseño, métodos, métricas y plan inferencial antes de iniciar cualquier ejecución confirmativa. En la tesis, esta puerta se formaliza mediante `configs/experiments/exp2_scaled/manifest.yaml` y código versionado. Su función principal es impedir que decisiones analíticas se ajusten retrospectivamente al resultado observado. En un benchmark con múltiples métodos, semillas, modelos y tamaños de muestra, pequeñas modificaciones en parámetros de explicador, umbrales de inclusión o reglas de agregación pueden cambiar la interpretación de la evidencia. Por ello, la congelación transforma el diseño en un compromiso previo y auditable.

Esta puerta no elimina la exploración; la ubica en su lugar adecuado. La tesis distingue entre EXP1, orientado a calibración y reproducibilidad, y EXP2, orientado a inferencia confirmativa. La separación evita que aprendizajes obtenidos durante la calibración contaminen las afirmaciones confirmativas. Esta lógica es consistente con recomendaciones recientes sobre benchmarking funcional y evaluación responsable de explicaciones, que enfatizan la necesidad de declarar configuraciones, semillas y condiciones de comparación antes de extraer conclusiones (Agarwal et al., 2022; Canha et al., 2025; Zheng et al., 2025).

### Puerta 2: Ejecución por lotes controlada

La segunda puerta ejecuta las celdas experimentales desde manifiestos declarativos, con semillas fijas y registro del contexto de ejecución. Su regla central es impedir modificaciones ad-hoc de configuración durante la corrida confirmativa. La ejecución por lotes no es solo una conveniencia técnica: es una forma de garantizar que cada combinación de modelo, método, semilla y tamaño de muestra se produzca bajo el mismo régimen de control. Cuando las explicaciones post-hoc dependen de perturbaciones, vecindarios artificiales, conjuntos de referencia o generadores estocásticos, registrar la semilla y la configuración se vuelve parte de la evidencia.

En FOM-7, la ejecución controlada también delimita responsabilidades. Si una celda falla, el fallo queda asociado a una configuración y a un artefacto identificable, no a una intervención manual invisible. Esta trazabilidad permite distinguir entre errores de implementación, limitaciones del método, problemas de coste, incompatibilidades de esquema o ausencia de resultados. De ese modo, el protocolo no oculta las fallas; las convierte en información auditable sobre la viabilidad operativa del benchmark.

### Puerta 3: Auditoría de integridad de artefactos

La tercera puerta inspecciona de forma determinista cada `results.json` para detectar archivos vacíos, esquemas incompatibles o valores numéricos inválidos. Los artefactos excluidos no deben reemplazarse mediante reconstrucciones sintéticas no documentadas. En EXP2, esta puerta explica la exclusión de celdas faltantes o no calificadas antes de las pruebas confirmativas. Su función es proteger la inferencia de datos aparentemente disponibles pero metodológicamente inadmisibles.

La auditoría de integridad es especialmente importante en XAI porque los métodos evaluados no siempre fallan de manera homogénea. Un método puede completar todas sus celdas, otro puede fallar en ciertos modelos, y otro puede producir salidas válidas pero difíciles de comparar con atribuciones continuas. Si esas diferencias se ignoran, el análisis puede mezclar evidencia válida, evidencia incompleta y artefactos no comparables. La puerta 3 obliga a registrar qué celdas entran al análisis y cuáles quedan fuera. En el capítulo, esta lógica explica por qué la cobertura de SHAP y LIME, Anchors y DiCE debe reportarse como parte de los resultados, no como detalle técnico secundario.

### Puerta 4: Armonización a tablas listas para el análisis

La cuarta puerta convierte artefactos heterogéneos en tablas comparables mediante estandarización de claves, campos de métricas y niveles de agregación. Su finalidad es evitar mezclas de esquema, doble conteo o comparaciones entre unidades analíticas incompatibles. En un benchmark que integra LIME, SHAP, Anchors y DiCE, esta puerta es indispensable porque los métodos producen objetos distintos: pesos locales, atribuciones aditivas, reglas y contrafactuales. La armonización no debe borrar esa diferencia; debe construir una tabla común sin fingir que los objetos son idénticos.

Esta puerta también fija el nivel en que la evidencia será leída. Las métricas pueden existir a nivel de instancia, ejecución, método, bloque o resumen global, pero no todas esas unidades son válidas para todas las inferencias. Una comparación confirmativa debe evitar contar múltiples instancias como réplicas independientes cuando pertenecen a una misma combinación experimental. Por ello, FOM-7 convierte la armonización en una operación metodológica, no solo en una transformación de formato. La tabla lista para análisis debe preservar método, modelo, semilla, tamaño de muestra, métrica, unidad de agregación y estado de calificación.

### Puerta 5: Exportación inferencial

La quinta puerta genera de forma determinista las tablas de pruebas omnibus y pareadas exclusivamente desde entradas calificadas. En la tesis, la superposición de recuperación para `mlp_shap`/`svm_shap` mediante `outputs/batch_results.csv` se trata como una excepción documentada, no como una reconstrucción arbitraria. Esta precisión importa porque la inferencia estadística solo es defendible si sus insumos son reproducibles y si las excepciones están registradas antes de interpretar el resultado.

La exportación inferencial controla tres fallos: cálculos manuales no reproducibles, doble conteo de celdas y uso de artefactos no calificados. También obliga a alinear la prueba con el diseño. Las pruebas de Friedman y Nemenyi requieren bloques completos y comparables; las pruebas pareadas como Wilcoxon requieren celdas emparejadas; los ajustes por multiplicidad deben aplicarse cuando se realizan comparaciones múltiples. FOM-7 no decide por sí mismo qué prueba es universalmente correcta; exige que la prueba seleccionada sea compatible con la unidad de análisis, la estructura de dependencia y la pregunta inferencial.

### Puerta 6: Perfilado de reproducibilidad

La sexta puerta cuantifica la dispersión entre ejecuciones y el coeficiente de variación en configuraciones replicadas. Esta puerta fundamenta la proposición P1 y permite distinguir variabilidad atribuible al método, al protocolo, a semillas o a condiciones computacionales. Su función es crucial porque un método puede exhibir buen promedio y, aun así, ser demasiado variable para sostener una afirmación robusta. En XAI, la reproducibilidad debe abarcar no solo el modelo predictivo, sino también las explicaciones, las métricas y las conclusiones derivadas de ellas.

En el diseño de la tesis, EXP1 cumple una función específica de calibración y perfilado de dispersión. No alimenta las hipótesis confirmativas H1-H3 de EXP2, pero sí informa el rango de variación esperada bajo semillas y permite interpretar la estabilidad del pipeline. Esta separación conserva la integridad inferencial: las réplicas de calibración ayudan a entender la reproducibilidad, mientras que el benchmark primario sostiene las comparaciones confirmativas. La puerta 6, por tanto, no es un apéndice posterior; es el mecanismo que impide confundir variación de semilla con efecto real del método.

### Puerta 7: Reporte con trazabilidad de afirmaciones

La séptima puerta permite emitir afirmaciones inferenciales solo cuando todas las puertas previas están satisfechas y la afirmación se vincula con evidencia identificable: resultados, tablas, scripts, configuraciones y límites de interpretación. Las afirmaciones no trazables deben presentarse como descriptivas. Esta puerta es la culminación del protocolo porque transforma el control técnico previo en lenguaje científico disciplinado. El objetivo no es producir resultados más vistosos, sino formular conclusiones que puedan ser auditadas.

La trazabilidad exige que cada afirmación conserve sus condiciones de validez. Si se afirma que SHAP presenta mayor fidelidad y estabilidad, la frase debe conservar el contexto EXP2, el conjunto Adult Income, las métricas definidas, las celdas calificadas, las pruebas aplicadas y el alcance tabular del benchmark. Si se afirma que LIME es eficiente pero inestable, debe indicarse que esa lectura procede de coste, parsimonia y estabilidad bajo semillas. Si se discuten Anchors o DiCE, debe preservarse que sus objetos explicativos son reglas y contrafactuales, no simplemente atribuciones numéricas. Así, la puerta 7 convierte el reporte en una práctica de gobernanza de evidencia.

## Relación con el capítulo

Dentro de este capítulo, FOM-7 debe presentarse como protocolo de gobernanza metodológica para evaluación de XAI. Su valor no reside en declarar que un método domina universalmente, sino en hacer defendible el paso desde explicaciones post-hoc y métricas computadas hacia afirmaciones científicas delimitadas. La formulación recomendada para los resultados no es "este explicador es mejor", sino "este explicador exhibe mayor fidelidad, estabilidad o eficiencia bajo estas condiciones, con esta métrica, esta unidad de análisis y esta evidencia fuente".

La función de FOM-7 dentro del argumento general es doble. Primero, responde a la crisis de evaluación mostrando cómo una cadena de controles puede reducir fragmentación, irreproducibilidad y sobreafirmación. Segundo, prepara la lectura de los resultados empíricos: las diferencias entre SHAP, LIME, Anchors y DiCE no se presentarán como jerarquía universal, sino como perfiles admisibles bajo un diseño concreto. Este puente es lo que permite que el capítulo avance desde fundamentos y crisis hacia diseño experimental y resultados sin perder disciplina inferencial.

## Límites explícitos

FOM-7 no demuestra utilidad humana directa, verdad causal de las explicaciones ni superioridad universal de un método. Su alcance es funcionalmente fundamentado (*functionally-grounded*): produce evidencia comparativa, reproducible y trazable sobre métodos post-hoc bajo condiciones experimentales controladas. Las dimensiones centradas en humanos (*human-grounded*) o centradas en aplicación (*application-grounded*) requerirían protocolos adicionales con usuarios, tareas, escalas e instrumentos propios.

Estos límites no debilitan el protocolo; delimitan su contribución. FOM-7 no sustituye estudios con usuarios, análisis causal, auditorías regulatorias completas ni evaluación de impacto en despliegue. Lo que aporta es una condición previa: antes de preguntar si una explicación ayuda a una persona o mejora una decisión real, debe saberse si el artefacto explicativo es reproducible, comparable, métricamente interpretable y trazable. En esa medida, FOM-7 funciona como infraestructura metodológica para futuras extensiones human-centered o application-grounded, pero no reclama haberlas realizado.
