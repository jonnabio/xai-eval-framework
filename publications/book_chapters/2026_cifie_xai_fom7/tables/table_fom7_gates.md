**Tabla 2**

*Puertas del protocolo FOM-7*

| Puerta | Propósito | Artefacto de salida | Fallo que controla |
| ------ | --------- | ------------------- | ------------------ |
| 1. Congelación | Fijar diseño, versiones, configuraciones, métodos, métricas y plan inferencial antes de la ejecución confirmativa. | Diseño factorial declarado y protocolo congelado. | Deriva de protocolo; cambios *post hoc* de hipótesis, métricas o criterios. |
| 2. Ejecución | Ejecutar cada celda desde una configuración declarativa, con semillas fijas y registro del contexto de ejecución. | Resultados crudos por celda. | Ejecuciones *ad hoc*; semillas no registradas; cambios de configuración durante la corrida. |
| 3. Auditoría | Calificar la integridad de los resultados mediante inspección determinista de artefactos. | Inventario de celdas analizables. | Archivos vacíos, esquemas incompatibles, valores inválidos y reconstrucciones no documentadas. |
| 4. Armonización | Convertir resultados heterogéneos en tablas comparables. | Métricas a nivel de ejecución y de bloque. | Campos no comparables, mezclas de esquema y errores de agregación. |
| 5. Exportación | Generar tablas inferenciales deterministas desde entradas calificadas. | Resultados de Friedman, Nemenyi y Wilcoxon. | Cálculos manuales, doble conteo, pseudorreplicación y uso de artefactos no calificados. |
| 6. Perfilado | Cuantificar la reproducibilidad bajo semillas y la variabilidad residual. | Coeficiente de variación por método y métrica. | Confundir la variación de semilla con un efecto del método o con un fallo del protocolo. |
| 7. Reporte | Vincular cada afirmación con evidencia identificable y con sus límites de interpretación. | Afirmaciones trazables y delimitadas. | Sobreafirmación, afirmaciones no auditables y conclusiones sin fuente verificable. |

*Nota.* Una afirmación inferencial solo es elegible si las puertas anteriores se satisfacen y si puede trazarse a evidencia fuente; en caso contrario, se formula como observación descriptiva o como hipótesis pendiente de validación. Elaboración propia a partir de Herrera-Vásquez (2026).
