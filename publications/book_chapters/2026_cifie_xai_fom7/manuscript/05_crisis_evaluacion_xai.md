# La crisis de evaluación en XAI

Fuente inicial: `thesis/capitulo-1-marco-teorico.qmd`, `thesis/capitulo-2-fundamentos.qmd`, `pub/fragments/paper_c_abstract_en.tex`, `references/references.bib` y `tables/table_metrics.md`.

## Un campo con métodos maduros y evaluación fragmentada

La XAI ha consolidado métodos post-hoc ampliamente utilizados, entre ellos LIME, SHAP, Anchors y DiCE. Sin embargo, la capacidad del campo para evaluar esos métodos de manera comparativa, reproducible y estadísticamente defendible no ha avanzado al mismo ritmo. La literatura dispone de explicadores, herramientas y taxonomías, pero todavía persiste una brecha entre calcular métricas y construir evidencia acumulable.

Esta brecha se manifiesta como una crisis de evaluación. No se trata de ausencia total de métricas, sino de proliferación de métricas inconexas, criterios variables de inclusión de instancias, configuraciones poco documentadas, falta de separación entre evidencia exploratoria y confirmatoria, y ausencia de reglas explícitas para convertir resultados numéricos en afirmaciones admisibles [@doshi-velez2017; @canha2025; @abdulkadir2023; @pawlicki2024; @altukhi2025; @bhattacharya2024].

El resultado práctico es que muchos estudios son difíciles de comparar entre sí. Dos investigaciones pueden evaluar "LIME" o "SHAP" y, aun así, trabajar con configuraciones, semillas, perturbaciones, conjuntos de referencia, métricas y reglas de agregación distintas. Bajo esas condiciones, el nombre del método deja de ser una unidad experimental suficiente.

## La insuficiencia de la fidelidad aislada

La fidelidad ha sido una de las métricas más utilizadas en evaluación XAI, pero no basta para caracterizar la calidad explicativa. Una explicación puede ser relativamente fiel y, al mismo tiempo, inestable, poco parsimoniosa, computacionalmente inviable o inadecuada para el objeto explicativo que produce el método. Evaluar solo fidelidad puede ocultar fallas críticas de consistencia o factibilidad.

Además, la fidelidad depende de su operacionalización. Si se evalúa mediante perturbación o enmascaramiento de características, el resultado puede verse afectado por instancias fuera de distribución, dependencias entre variables o supuestos de ausencia/presencia de características. En ese caso, la métrica puede medir tanto la calidad del explicador como artefactos del procedimiento de perturbación [@alvarezmelis2018; @zheng2025].

Esta limitación exige un enfoque multi-métrico. En el marco de la tesis, las dimensiones primarias son fidelidad, estabilidad, parsimonia, brecha de fidelidad y coste computacional. Cada una captura una propiedad distinta y ninguna debe sustituir a las demás. La evaluación defendible requiere leer perfiles de métodos, no coronar un ganador universal a partir de una única escala.

## Brecha entre métrica, constructo y afirmación

Una métrica solo es útil si se mantiene conectada con el constructo que pretende medir. La crisis de evaluación aparece cuando una cifra se transforma en una afirmación más fuerte que la evidencia disponible. Una métrica de fidelidad local no demuestra utilidad humana; una métrica de estabilidad no prueba causalidad; una regla precisa no garantiza cobertura amplia; un contrafactual válido para el modelo no implica que la acción sea posible para una persona.

Esta brecha de constructo es especialmente visible porque los métodos producen objetos explicativos heterogéneos. LIME genera sustitutos locales; SHAP produce atribuciones; Anchors formula reglas; DiCE genera contrafactuales. Forzar todos esos artefactos a una misma escala puede castigar a un método por no producir el tipo de salida que la métrica espera. Por ello, las revisiones recientes insisten en interpretar la evaluación XAI como un espacio multidimensional de propiedades, fuentes de evidencia y contextos de tarea [@nauta2023; @abdulkadir2023; @bhattacharya2024].

La consecuencia metodológica es clara: una afirmación comparativa debe declarar qué objeto se evaluó, con qué métrica, bajo qué diseño, con qué unidad de análisis y con qué límite de interpretación. Sin esa información, el resultado puede parecer cuantitativo y, sin embargo, ser débil como evidencia científica.

## Reproducibilidad y trazabilidad insuficientes

La reproducibilidad en XAI no se limita a publicar código. También requiere versionar datos, modelos, semillas, configuraciones de explicadores, parámetros de perturbación, definiciones métricas, reglas de agregación y scripts de análisis. Las explicaciones post-hoc agregan puntos de variación que no siempre aparecen en el entrenamiento del modelo base: vecindarios artificiales, conjuntos de referencia, umbrales de reglas, generadores contrafactuales y estrategias de muestreo.

Cuando esos elementos no se registran, dos ejecuciones pueden producir explicaciones diferentes sin que el lector pueda distinguir si la diferencia proviene del modelo, del explicador, de la semilla, de la métrica o del entorno computacional. Esto debilita la auditabilidad de resultados y dificulta la acumulación de evidencia.

La trazabilidad también es necesaria para controlar la sobreafirmación. Cada afirmación fuerte debería poder regresar a un artefacto fuente: tabla, figura, configuración, script, prueba estadística o decisión metodológica. Si se afirma que un método es más estable, debe quedar claro en qué dataset, modelo, métrica, configuración y unidad experimental se observó esa estabilidad.

## Herramientas sin protocolo de gobernanza suficiente

Herramientas como Quantus y OpenXAI han contribuido a estandarizar y facilitar la evaluación XAI [@hedstrom2023; @agarwal2022]. Quantus organiza familias de métricas y reduce fricción técnica. OpenXAI promueve comparabilidad y transparencia en la evaluación de explicaciones post-hoc. Estas contribuciones son importantes, pero no resuelven por sí solas el problema de gobernanza metodológica.

Antes de ejecutar una métrica deben definirse las reglas del experimento: qué artefactos son admisibles, cómo se congelan configuraciones, qué salidas se excluyen, cómo se armonizan esquemas, qué pruebas estadísticas son válidas, cómo se controla multiplicidad y qué límites conserva cada afirmación. Una herramienta puede ofrecer métricas; un protocolo debe gobernar cuándo esas métricas pueden transformarse en evidencia.

La contribución necesaria, por tanto, no consiste solo en ampliar el catálogo de métricas. Consiste en integrar métricas, artefactos, reproducibilidad, inferencia y trazabilidad dentro de una secuencia operativa. Ese es el punto en el que la crisis de evaluación conduce al protocolo FOM-7.

## Implicación para el capítulo

El capítulo debe presentar la evaluación XAI como un problema de admisibilidad de evidencia. No basta con generar explicaciones plausibles ni con producir tablas de métricas. Es necesario demostrar que los resultados provienen de artefactos válidos, que las comparaciones son homogéneas, que la variabilidad fue controlada, que la inferencia es apropiada y que las afirmaciones son trazables.

Esta transición prepara la función de FOM-7: convertir una evaluación fragmentada en una cadena auditable de decisiones, artefactos, métricas, pruebas y afirmaciones delimitadas.
