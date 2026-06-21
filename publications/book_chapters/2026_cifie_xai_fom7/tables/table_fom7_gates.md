# Compuertas del protocolo FOM-7

| Compuerta FOM-7 | Propósito | Artefacto esperado | Rol en la elegibilidad de afirmaciones |
| --------------- | --------- | ------------------ | -------------------------------------- |
| 1. Congelamiento del protocolo | Fijar diseño experimental, métricas, métodos, parámetros y criterios antes de ejecutar el benchmark. | Protocolo congelado y versionado. | Impide ajustar afirmaciones a posteriori sin trazabilidad metodológica. |
| 2. Ejecución controlada por lotes | Ejecutar celdas experimentales bajo condiciones reproducibles y registradas. | Registros de ejecución por lote, semillas, configuración y estado de corrida. | Permite vincular cada resultado con una ejecución controlada. |
| 3. Auditoría de artefactos | Verificar integridad, completitud y consistencia de salidas generadas. | Inventario de artefactos, validaciones y reporte de anomalías. | Excluye afirmaciones basadas en artefactos incompletos o inconsistentes. |
| 4. Armonización inferencial | Unificar métricas, comparaciones y pruebas estadísticas para análisis comparable. | Dataset analítico armonizado y especificación estadística. | Asegura que las comparaciones se basen en criterios comunes. |
| 5. Exportación determinista de artefactos pareados | Producir salidas reproducibles que conecten resultados, tablas, figuras y evidencia fuente. | Paquetes exportados con pares resultado-evidencia. | Hace auditable el origen de tablas, figuras y afirmaciones. |
| 6. Perfilado de dispersión entre ejecuciones | Medir variabilidad, estabilidad y sensibilidad entre corridas. | Reporte de dispersión y estabilidad por método/celda. | Evita afirmar superioridad sin considerar variabilidad experimental. |
| 7. Reporte de afirmaciones trazables a evidencia fuente | Formular conclusiones conectadas explícitamente con datos, métricas y artefactos verificables. | Matriz de afirmaciones, evidencia y límites de interpretación. | Determina qué afirmaciones son defendibles en el manuscrito. |
