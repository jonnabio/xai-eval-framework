# Diseño empírico del benchmark

Fuente inicial: `thesis/capitulo-3-diseno-experimental.qmd`, `tables/table_metrics.md`, `tables/table_fom7_gates.md` y `tables/table_results_summary.md`.

## Enfoque general

El diseño empírico operacionaliza la evaluación de métodos XAI agnósticos al modelo como un benchmark cuantitativo, reproducible y multi-métrico. Su finalidad es comparar LIME, SHAP, Anchors y DiCE bajo condiciones controladas, evitando que las diferencias observadas se confundan con variaciones no documentadas de modelo, semilla, muestra, configuración o artefacto. En lugar de tratar las explicaciones como productos aislados, el diseño las inserta en una cadena experimental completa: modelos predictivos congelados, explicadores configurados, artefactos auditados, métricas operacionalizadas y pruebas estadísticas aplicadas sobre unidades de análisis explícitas.

El estudio se ubica en una lógica funcionalmente fundamentada (*functionally-grounded*): las métricas utilizadas son proxies computacionales de calidad explicativa y no evidencia directa de utilidad humana, plausibilidad semántica o causalidad. Esta delimitación es central para sostener afirmaciones prudentes y auditables. En la taxonomía de Doshi-Velez y Kim (2017), el capítulo no evalúa si una explicación mejora decisiones humanas en una tarea real; evalúa si un conjunto de métodos produce artefactos comparables bajo métricas reproducibles. Esa elección permite control experimental, pero exige que cada conclusión conserve su alcance: datos tabulares, UCI Adult Income, configuraciones declaradas y explicadores post-hoc.

El diseño traduce la discusión conceptual de las secciones anteriores en decisiones operativas. La crisis de evaluación se responde mediante separación de cohortes, congelamiento de modelos, muestreo estratificado, métricas primarias, auditoría FOM-7 y pruebas no paramétricas. La unidad central de la sección no es una cifra de resultado, sino la arquitectura que hace admisible esa cifra. Por ello, las decisiones de partición, preprocesamiento, muestreo, ejecución y análisis se presentan como controles metodológicos y no como detalles secundarios de implementación.

## Fases experimentales

El diseño distingue dos cohortes de evidencia con funciones diferenciadas. La primera, EXP1, funciona como fase de calibración y reproducibilidad. Su propósito es verificar la implementación del pipeline, entrenar y congelar los artefactos de modelo compartidos por todos los explicadores en EXP2, y estimar la dispersión métrica bajo variación de semilla. EXP1 opera como una fase de control: permite observar si las métricas principales son suficientemente estables y si los modelos cumplen umbrales mínimos de desempeño, pero no sostiene las afirmaciones confirmativas principales.

La segunda cohorte, EXP2, constituye el benchmark primario. En esta fase se ejecuta el diseño factorial completo y se producen los artefactos que alimentan las pruebas estadísticas, los perfiles por método y las afirmaciones empíricas del capítulo. La separación entre EXP1 y EXP2 reduce la contaminación entre decisiones exploratorias y evidencia confirmatoria. Esta separación es importante porque, en evaluación XAI, los ajustes de configuración después de observar resultados pueden cambiar tanto las métricas como la interpretación de los métodos. FOM-7 convierte esta separación en una regla de admisibilidad: la calibración informa el diseño, pero la inferencia se formula sobre la cohorte confirmativa.

La función de EXP1 también es reproducible. En la tesis, esta fase establece que las métricas de calidad presentan coeficientes de variación inferiores al 9% bajo variación de semilla, mientras que el coste computacional exhibe mayor variabilidad, especialmente en configuraciones con KernelSHAP. Esta diferencia anticipa una tensión que recorre todo el capítulo: la calidad explicativa puede ser más estable que la latencia, y por tanto el coste debe reportarse como dimensión propia del perfil de método, no como simple dato de ingeniería.

## Conjunto de datos y modelos predictivos

El benchmark utiliza el conjunto UCI Adult Income, un problema tabular de clasificación binaria ampliamente utilizado en aprendizaje automático y evaluación XAI por su estructura heterogénea, su variable objetivo clara y la existencia de comparaciones externas. El conjunto contiene variables numéricas y categóricas asociadas con características demográficas, laborales y educativas, y la tarea consiste en predecir si el ingreso anual supera un umbral de 50,000 dólares (Kohavi & Becker, 1996). Su uso es pertinente para este capítulo porque permite evaluar explicadores post-hoc sobre un escenario tabular con transformaciones de preprocesamiento, variables correlacionadas y clases desbalanceadas de forma moderada.

El pipeline de preprocesamiento se aplica de forma determinista: partición estratificada, normalización de valores faltantes, codificación de variables categóricas, escalado de variables numéricas y persistencia del preprocesador ajustado. Las transformaciones se ajustan exclusivamente sobre el conjunto de entrenamiento para evitar fuga de datos. Este control es esencial porque los explicadores operan sobre el espacio transformado que consumen los modelos; si el preprocesamiento variara entre métodos, una diferencia atribuida al explicador podría provenir de diferencias de representación. Por ello, el preprocesador se trata como artefacto compartido y congelado.

Se consideran cinco familias de modelos: regresión logística (`logreg`), bosque aleatorio (`rf`), XGBoost (`xgb`), máquina de vectores soporte (`svm`) y perceptrón multicapa (`mlp`). Esta selección permite observar explicadores sobre fronteras de decisión lineales, basadas en árboles, con kernel y neuronales. La inclusión de bosque aleatorio sigue la tradición de modelos de ensamblado introducida por Breiman (2001), mientras que XGBoost y los modelos no lineales amplían la diversidad de mecanismos predictivos. El objetivo no es evaluar qué modelo predictivo es superior, sino someter los explicadores a familias de decisión con estructuras distintas y verificar si los perfiles XAI se mantienen bajo esa heterogeneidad.

## Diseño factorial EXP2

El benchmark primario adopta un diseño cruzado:

```text
modelo x método XAI x semilla x tamaño de muestra
```

Formalmente, el diseño planificado corresponde a:

```text
5 modelos x 4 métodos x 5 semillas x 3 tamaños de muestra = 300 celdas
```

Los factores son: modelos (`logreg`, `rf`, `xgb`, `svm`, `mlp`), métodos (`shap`, `lime`, `anchors`, `dice`), semillas (42, 123, 456, 789, 999) y tamaños de muestra por estrato (50, 100 y 200). Cada celda produce un artefacto independiente de resultados. La variación de semilla permite analizar reproducibilidad, mientras que la variación de tamaño de muestra permite examinar la estabilidad de patrones bajo distintos volúmenes de evidencia local. Esta estructura cruzada evita que una comparación entre explicadores dependa de un único modelo, una única semilla o una única escala de muestra.

El diseño planificado produce 300 celdas, pero el análisis confirmativo utiliza 275 celdas calificadas tras la auditoría FOM-7. Esta distinción entre diseño planificado y cobertura analítica es deliberada. Los artefactos faltantes o no armonizables no se reemplazan de forma sintética ni se ocultan en promedios globales; se registran como parte de la evidencia. SHAP y LIME alcanzan cobertura completa, DiCE conserva 68 de 75 celdas y Anchors 57 de 75, con impacto interpretativo específico para reglas y contrafactuales. La Figura 1 presenta esta cobertura analítica por modelo y método.

## Muestreo de instancias

Las instancias se seleccionan mediante muestreo estratificado por cuadrante de error: verdaderos positivos, verdaderos negativos, falsos positivos y falsos negativos. Esta estrategia evita evaluar los explicadores únicamente sobre aciertos del modelo y obliga a observar su comportamiento en regiones de decisión correctas e incorrectas. En un benchmark de explicabilidad, esta decisión es importante porque una explicación puede parecer razonable cuando el modelo acierta y resultar más difícil de interpretar cuando el modelo falla. Incluir falsos positivos y falsos negativos aproxima el diseño a escenarios de auditoría, donde los errores del modelo suelen ser tan relevantes como sus aciertos.

El tamaño nominal de una ejecución depende del número de instancias por cuadrante, aunque la disponibilidad real puede variar por modelo y estrato. En la tesis, el rango observado va de 27 a 800 instancias por ejecución, con mediana de 400. Esta variación no invalida el diseño porque la inferencia se realiza sobre agregados controlados, no sobre instancias tratadas como réplicas independientes. Además, la estratificación por cuadrante de error permite que cada explicador sea examinado en condiciones de decisión más ricas que una muestra aleatoria simple del conjunto de prueba.

![Figura 1. Cobertura analítica EXP2 por modelo y método. Fuente: figura derivada de `thesis/assets/figures/fig_cobertura_exp2_es.png`.](../figures/exported/fig_cobertura_exp2_es.png)

## Configuración de explicadores

SHAP se ejecuta con variantes acordes al modelo base: `TreeExplainer` para modelos de árboles y `KernelExplainer` para modelos donde se requiere aproximación más general. LIME utiliza `LimeTabularExplainer` con parámetros congelados de muestreo, número de características y ancho de kernel. Anchors emplea reglas locales con umbral de precisión efectivo de 0.95. DiCE genera contrafactuales orientados a la clase opuesta, usando diferencias entre instancia original y contrafactual como base de importancia. Estas configuraciones deben interpretarse como parte del protocolo experimental. No se evalúan nombres abstractos de métodos, sino implementaciones concretas con parámetros específicos, artefactos registrados y límites conocidos.

La decisión de registrar configuraciones efectivas es crucial porque el nombre de un explicador no determina por sí solo la evidencia que produce. KernelSHAP y TreeSHAP difieren en coste y supuestos; LIME depende de perturbaciones y vecindario; Anchors depende de condiciones de búsqueda y umbral; DiCE depende de restricciones contrafactuales y del modo de generación. Por ello, el diseño empírico no compara etiquetas, sino ejecuciones protocolizadas. Cualquier conclusión posterior debe conservar esta configuración como parte de su alcance.

## Métricas primarias

El benchmark utiliza cinco métricas primarias, resumidas en la Tabla 1: fidelidad, estabilidad, parsimonia, brecha de fidelidad y coste computacional. La fidelidad mide la alineación entre importancias y efecto predictivo observado; la estabilidad mide similitud entre explicaciones bajo perturbaciones controladas; la parsimonia aproxima concisión mediante proporción de características activas; la brecha de fidelidad estima el cambio en la salida del modelo al enmascarar características principales; y el coste registra tiempo de ejecución por instancia explicada.

Estas métricas se computan por instancia y se agregan a nivel de ejecución mediante media aritmética. La unidad inferencial no es la instancia aislada, sino la ejecución agregada y, para las pruebas globales, el bloque experimental. Esta jerarquía evita pseudorreplicación y mantiene coherencia entre el nivel donde se calcula una métrica y el nivel donde se sostiene una afirmación. Además, cada métrica conserva dirección e interpretación propias: fidelidad, estabilidad y brecha buscan valores mayores; parsimonia y coste se leen en sentido inverso. Una lectura multi-métrica evita confundir calidad explicativa con una única escala.

## Unidades de análisis

El análisis adopta una jerarquía explícita. A nivel de instancia se calculan métricas individuales. A nivel de ejecución se obtiene el promedio para una combinación de modelo, método, semilla y tamaño. A nivel de bloque, las pruebas Friedman consideran pares modelo-tamaño $(g,n)$, generando 15 bloques completos. Esta jerarquía es el control principal contra la pseudorreplicación: muchas instancias explicadas dentro de una misma celda no equivalen a muchas réplicas independientes del método.

Para el contraste SHAP-LIME, la unidad primaria es la celda pareada $(g,s,n)$. Esto permite comparar ambos métodos en 75 coordenadas experimentales coincidentes, reduciendo la confusión por modelo, semilla o tamaño de muestra. La comparación pareada es más estricta que una comparación de promedios independientes porque exige que ambos métodos existan en la misma coordenada experimental. En este caso, la cobertura completa de SHAP y LIME permite sostener una inferencia más limpia sobre la frontera calidad-coste entre ambos métodos.

## Control FOM-7

El diseño se gobierna mediante FOM-7, resumido en la Tabla 3. Las puertas controlan congelación del protocolo, ejecución declarativa, auditoría de artefactos, armonización de tablas, exportación inferencial, perfilado de reproducibilidad y trazabilidad de afirmaciones. Esta estructura es necesaria porque el benchmark no solo produce resultados; produce resultados que deben ser admisibles como evidencia. Una celda con artefacto vacío, esquema incompatible o valores inválidos no puede alimentar pruebas confirmativas. Una afirmación sin trazabilidad a tabla, script, configuración o límite de alcance no debe presentarse como inferencial.

En la práctica, FOM-7 conecta el diseño con los resultados. La puerta 3 explica por qué las 25 celdas no calificadas se excluyen de ciertas pruebas; la puerta 4 permite transformar artefactos heterogéneos en tablas comparables; la puerta 5 genera tablas de Friedman, Nemenyi y Wilcoxon desde entradas calificadas; la puerta 6 sostiene la lectura de reproducibilidad; y la puerta 7 obliga a que cada afirmación pueda regresar a un artefacto fuente. Este control evita que el capítulo dependa de una confianza informal en el pipeline y convierte la auditabilidad en parte del método.

## Plan inferencial

Las diferencias globales entre métodos se evalúan mediante pruebas de Friedman y comparaciones post-hoc de Nemenyi sobre bloques completos. Esta elección es apropiada para comparar varios tratamientos sobre bloques relacionados y se apoya en la tradición de pruebas no paramétricas para comparación de clasificadores y métodos sobre diseños repetidos (Friedman, 1937; Demšar, 2006). Cuando Friedman rechaza la hipótesis nula, Nemenyi permite localizar diferencias de rangos entre métodos sin asumir normalidad fuerte de las métricas (Nemenyi, 1963).

El análisis pareado SHAP-LIME utiliza pruebas bilaterales de Wilcoxon sobre celdas coincidentes, con corrección de multiplicidad Holm-Bonferroni y reporte de tamaños de efecto. Wilcoxon es adecuado para contrastar diferencias pareadas cuando no se desea asumir normalidad de las diferencias (Wilcoxon, 1945), mientras que el tamaño de efecto permite evaluar magnitud práctica y no solo significación estadística (Lakens, 2013). La reproducibilidad se examina mediante coeficientes de variación en configuraciones replicadas, especialmente para distinguir señales estables de variación inducida por semilla.

El objetivo del plan inferencial no es producir un ranking universal de explicadores, sino determinar qué diferencias son defendibles bajo el diseño, con qué tamaño de efecto, sobre qué unidad de análisis y dentro de qué alcance empírico. Por ello, los resultados posteriores deben leerse como afirmaciones condicionadas: diferencias entre métodos sobre Adult Income, con cinco familias de modelos, cinco semillas, tres tamaños de muestra, métricas definidas y artefactos calificados por FOM-7.
