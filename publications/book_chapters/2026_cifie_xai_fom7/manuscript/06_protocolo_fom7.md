# Protocolo FOM-7 para benchmarking auditable

Fuente inicial: `thesis/capitulo-1-marco-teorico.qmd`, `thesis/capitulo-2-fundamentos.qmd`, `thesis/capitulo-3-diseno-experimental.qmd` y `thesis/capitulo-6-conclusiones.qmd`.

## Función metodológica

FOM-7 (*Framework Operation Method*, siete puertas) se define como una secuencia operativa para convertir ejecuciones de benchmarking XAI en evidencia reproducible, comparable y trazable. Su propósito no es introducir un nuevo explicador ni una métrica aislada, sino gobernar el ciclo completo que conecta diseño experimental, ejecución controlada, calificación de artefactos, armonización analítica, inferencia estadística, reproducibilidad y reporte de afirmaciones.

El protocolo responde a una brecha identificada en la evaluación de XAI: la existencia de métodos, métricas y toolkits no garantiza por sí misma que los resultados sean admisibles como evidencia científica. Un toolkit puede calcular métricas correctamente y, aun así, el estudio puede sobreinterpretar sus resultados si no declara qué artefactos son válidos, qué configuraciones fueron congeladas, qué pruebas estadísticas son admisibles y qué límites conserva cada afirmación.

## Regla secuencial de admisibilidad

Las siete puertas de FOM-7 son secuenciales. Cada puerta debe satisfacerse antes de proceder a la siguiente. Si una puerta falla, los resultados afectados no desaparecen necesariamente, pero se degradan a estatus descriptivo y no pueden sostener afirmaciones inferenciales.

La regla central puede formularse así:

> Ninguna afirmación inferencial puede formularse si las puertas previas no están satisfechas y si la afirmación no puede trazarse a artefactos fuente verificables.

Esta regla evita tres riesgos recurrentes en benchmarking XAI:

- Deriva de protocolo: cambios post-hoc en configuraciones, hipótesis, criterios de inclusión o métricas.
- Contaminación de artefactos: uso de salidas vacías, malformadas, incompletas o no comparables.
- Sobreafirmación: conversión de resultados numéricos en conclusiones generales sin declarar alcance, unidad de análisis o límites.

## Flujo operativo

El flujo compacto del protocolo es:

```text
Congelación -> Ejecución -> Auditoría -> Armonización -> Exportación -> Perfilado -> Reporte
```

## Puertas del protocolo

### Puerta 1: Congelación del protocolo

Bloquea versiones de código, archivos de configuración YAML, factores del diseño, métodos, métricas y plan inferencial antes de iniciar cualquier ejecución confirmativa. En la tesis, esta puerta se formaliza mediante `configs/experiments/exp2_scaled/manifest.yaml` y código versionado.

### Puerta 2: Ejecución por lotes controlada

Ejecuta las celdas experimentales desde manifiestos declarativos, con semillas fijas y registro del contexto de ejecución. La regla impide modificaciones ad-hoc de configuración durante la ejecución confirmativa.

### Puerta 3: Auditoría de integridad de artefactos

Inspecciona de forma determinista cada `results.json` para detectar archivos vacíos, esquemas incompatibles o valores numéricos inválidos. Los artefactos excluidos no deben reemplazarse mediante reconstrucciones sintéticas. En EXP2, esta puerta explica la exclusión de celdas faltantes o no calificadas antes de las pruebas confirmativas.

### Puerta 4: Armonización a tablas listas para el análisis

Convierte artefactos heterogéneos en tablas comparables mediante estandarización de claves, campos de métricas y niveles de agregación. La finalidad es evitar mezclas de esquema, doble conteo o comparaciones entre unidades analíticas incompatibles.

### Puerta 5: Exportación inferencial

Genera de forma determinista las tablas de pruebas omnibus y pareadas exclusivamente desde entradas calificadas. En la tesis, la superposición de recuperación para `mlp_shap`/`svm_shap` mediante `outputs/batch_results.csv` es una excepción documentada, no una reconstrucción arbitraria.

### Puerta 6: Perfilado de reproducibilidad

Cuantifica la dispersión entre ejecuciones y el coeficiente de variación en configuraciones replicadas. Esta puerta fundamenta la proposición P1 y permite distinguir variabilidad atribuible al método, al protocolo, a semillas o a condiciones computacionales.

### Puerta 7: Reporte con trazabilidad de afirmaciones

Permite emitir afirmaciones inferenciales solo cuando todas las puertas previas están satisfechas y la afirmación se vincula con evidencia identificable: resultados, tablas, scripts, configuraciones y límites de interpretación. Las afirmaciones no trazables deben presentarse como descriptivas.

## Relación con el capítulo

Dentro de este capítulo, FOM-7 debe presentarse como protocolo de gobernanza metodológica para evaluación de XAI. Su valor no reside en declarar que un método domina universalmente, sino en hacer defendible el paso desde explicaciones post-hoc y métricas computadas hacia afirmaciones científicas delimitadas.

La formulación recomendada para los resultados no es "este explicador es mejor", sino "este explicador exhibe mayor fidelidad, estabilidad o eficiencia bajo estas condiciones, con esta métrica, esta unidad de análisis y esta evidencia fuente".

## Límites explícitos

FOM-7 no demuestra utilidad humana directa, verdad causal de las explicaciones ni superioridad universal de un método. Su alcance es functionally-grounded: produce evidencia comparativa, reproducible y trazable sobre métodos post-hoc bajo condiciones experimentales controladas. Las dimensiones human-grounded o application-grounded requerirían protocolos adicionales con usuarios, tareas, escalas e instrumentos propios.
