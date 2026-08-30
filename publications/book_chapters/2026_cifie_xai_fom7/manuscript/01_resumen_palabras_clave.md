# Resumen y palabras clave

## Resumen

La explicabilidad en inteligencia artificial suele presentarse como respuesta a la opacidad de los modelos de aprendizaje automático, pero producir explicaciones no equivale a demostrar que esas explicaciones sean fieles, estables, comparables o técnicamente defendibles. Este capítulo aborda esa brecha mediante FOM-7, un protocolo operativo de siete puertas para convertir el benchmarking de métodos post-hoc en evidencia reproducible, multi-métrica y auditable. El capítulo integra fundamentos de XAI, una crítica a la crisis de evaluación y un benchmark empírico sobre UCI Adult Income que compara LIME, SHAP, Anchors y DiCE en cinco familias de modelos, cinco semillas y tres tamaños de muestra. Tras la auditoría de artefactos, el análisis utiliza 275 celdas calificadas y pruebas no paramétricas con control de multiplicidad. Los resultados muestran diferencias globales significativas en fidelidad y estabilidad; SHAP presenta el perfil más fuerte para auditoría técnica, mientras LIME conserva ventajas de coste y parsimonia con una limitación crítica de estabilidad. Anchors y DiCE requieren lectura diferenciada porque producen reglas y contrafactuales, no solo atribuciones de características. La contribución central es metodológica: desplazar la evaluación XAI desde rankings aislados hacia perfiles explicativos trazables, delimitados por objetivo, métrica, evidencia y alcance.

## Palabras clave

Inteligencia artificial explicable; explicabilidad agnóstica al modelo; benchmarking reproducible; protocolo FOM-7; evaluación multi-métrica; explicaciones post-hoc.
