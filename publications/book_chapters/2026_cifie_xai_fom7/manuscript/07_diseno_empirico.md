# Diseño empírico del benchmark

Fuente inicial: `thesis/capitulo-3-diseno-experimental.qmd`, `tables/table_metrics.md`, `tables/table_fom7_gates.md` y `tables/table_results_summary.md`.

## Enfoque general

El diseño empírico operacionaliza la evaluación de métodos XAI agnósticos al modelo como un benchmark cuantitativo, reproducible y multi-métrico. Su finalidad es comparar LIME, SHAP, Anchors y DiCE bajo condiciones controladas, evitando que las diferencias observadas se confundan con variaciones no documentadas de modelo, semilla, muestra, configuración o artefacto.

El estudio se ubica en una lógica *functionally-grounded* o funcionalmente fundamentada: las métricas utilizadas son proxies computacionales de calidad explicativa y no evidencia directa de utilidad humana, plausibilidad semántica o causalidad. Esta delimitación es central para sostener afirmaciones prudentes y auditables.

## Fases experimentales

El diseño distingue dos cohortes de evidencia. La primera, EXP1, funciona como fase de calibración y reproducibilidad. Su propósito es verificar la implementación del pipeline, entrenar y congelar modelos, y estimar dispersión métrica bajo variación de semilla. EXP1 no se utiliza para sostener las afirmaciones confirmativas principales.

La segunda, EXP2, constituye el benchmark primario. En esta fase se ejecuta el diseño factorial completo y se producen los artefactos que alimentan las pruebas estadísticas, los perfiles por método y las afirmaciones empíricas del capítulo. La separación entre EXP1 y EXP2 reduce la contaminación entre decisiones exploratorias y evidencia confirmatoria.

## Dataset y modelos predictivos

El benchmark utiliza el conjunto UCI Adult Income, un conjunto de datos tabular con variable objetivo binaria y características numéricas y categóricas. Su uso es pertinente para XAI porque permite evaluar explicadores post-hoc en un contexto tabular heterogéneo y ampliamente utilizado en comparaciones de explicabilidad.

El pipeline de preprocesamiento se aplica de forma determinista: partición estratificada, tratamiento de valores faltantes, codificación de variables categóricas, escalado de variables numéricas y persistencia del preprocesador ajustado. Las transformaciones se ajustan exclusivamente sobre el conjunto de entrenamiento para evitar fuga de datos.

Se consideran cinco familias de modelos: regresión logística (`logreg`), bosque aleatorio (`rf`), XGBoost (`xgb`), máquina de vectores soporte (`svm`) y perceptrón multicapa (`mlp`). Esta selección permite observar explicadores sobre fronteras de decisión lineales, basadas en árboles, con kernel y neuronales.

## Diseño factorial EXP2

El benchmark primario adopta un diseño cruzado:

```text
modelo x método XAI x semilla x tamaño de muestra
```

Formalmente, el diseño planificado corresponde a:

```text
5 modelos x 4 métodos x 5 semillas x 3 tamaños de muestra = 300 celdas
```

Los factores son:

- modelos: `logreg`, `rf`, `xgb`, `svm`, `mlp`;
- métodos: `shap`, `lime`, `anchors`, `dice`;
- semillas: 42, 123, 456, 789, 999;
- tamaños de muestra por estrato: 50, 100 y 200.

Cada celda produce un artefacto independiente de resultados. La variación de semilla permite analizar reproducibilidad, mientras que la variación de tamaño de muestra permite examinar la estabilidad de los patrones bajo distintos volúmenes de evidencia local.

## Muestreo de instancias

Las instancias se seleccionan mediante muestreo estratificado por cuadrante de error: verdaderos positivos, verdaderos negativos, falsos positivos y falsos negativos. Esta estrategia evita evaluar los explicadores únicamente sobre aciertos del modelo y obliga a observar su comportamiento en regiones de decisión correctas e incorrectas.

El tamaño nominal de una ejecución depende del número de instancias por cuadrante, aunque la disponibilidad real puede variar por modelo y estrato. Esta decisión vincula la evaluación XAI con situaciones de auditoría más realistas: un explicador debe examinarse no solo cuando el modelo acierta, sino también cuando falla.

## Configuración de explicadores

SHAP se ejecuta con variantes acordes al modelo base: `TreeExplainer` para modelos de árboles y `KernelExplainer` para modelos donde se requiere aproximación más general. LIME utiliza `LimeTabularExplainer` con parámetros congelados de muestreo, número de características y ancho de kernel. Anchors emplea reglas locales con umbral de precisión efectivo de 0.95. DiCE genera contrafactuales orientados a la clase opuesta, usando diferencias entre instancia original y contrafactual como base de importancia.

Estas configuraciones deben interpretarse como parte del protocolo experimental. No se evalúan nombres abstractos de métodos, sino implementaciones concretas con parámetros específicos, artefactos registrados y límites conocidos.

## Métricas primarias

El benchmark utiliza cinco métricas primarias, descritas en `tables/table_metrics.md`:

- fidelidad: alineación entre importancias y efecto predictivo observado;
- estabilidad: similitud entre explicaciones bajo perturbaciones controladas;
- parsimonia: proporción de características activas;
- brecha de fidelidad: cambio en la salida del modelo al enmascarar las características principales;
- coste computacional: tiempo por instancia explicada.

Estas métricas se computan por instancia y se agregan a nivel de ejecución. La unidad inferencial no es la instancia aislada, sino la ejecución agregada y, para las pruebas globales, el bloque experimental.

## Unidades de análisis

El análisis evita la pseudorreplicación mediante una jerarquía de niveles. A nivel de instancia se calculan métricas individuales. A nivel de ejecución se obtiene el promedio para una combinación de modelo, método, semilla y tamaño. A nivel de bloque, las pruebas Friedman consideran pares modelo-tamaño $(g,n)$, generando 15 bloques completos.

Para el contraste SHAP-LIME, la unidad primaria es la celda pareada $(g,s,n)$. Esto permite comparar ambos métodos en 75 coordenadas experimentales coincidentes, reduciendo la confusión por modelo, semilla o tamaño de muestra.

## Control FOM-7

El diseño se gobierna mediante FOM-7, resumido en `tables/table_fom7_gates.md`. Las compuertas controlan congelación del protocolo, ejecución declarativa, auditoría de artefactos, armonización de tablas, exportación inferencial, perfilado de reproducibilidad y trazabilidad de afirmaciones.

Esta estructura es necesaria porque el benchmark no solo produce resultados; produce resultados que deben ser admisibles como evidencia. Una celda con artefacto vacío, esquema incompatible o valores inválidos no puede alimentar pruebas confirmativas. Una afirmación sin trazabilidad a tabla, script, configuración o límite de alcance no debe presentarse como inferencial.

## Plan inferencial

Las diferencias globales entre métodos se evalúan mediante pruebas de Friedman y comparaciones post-hoc de Nemenyi sobre bloques completos. El análisis pareado SHAP-LIME utiliza pruebas bilaterales de Wilcoxon y corrección de multiplicidad Holm-Bonferroni. La reproducibilidad se examina mediante coeficientes de variación en configuraciones replicadas.

El objetivo del plan inferencial no es producir un ranking universal de explicadores, sino determinar qué diferencias son defendibles bajo el diseño, con qué tamaño de efecto, sobre qué unidad de análisis y dentro de qué alcance empírico.
