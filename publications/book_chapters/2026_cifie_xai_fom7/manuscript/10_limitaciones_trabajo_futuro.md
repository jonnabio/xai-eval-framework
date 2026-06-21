# Limitaciones y trabajo futuro

## Alcance empírico delimitado

La primera limitación es el universo empírico del benchmark. Los resultados proceden de UCI Adult Income, un conjunto de datos tabular, binario y de tamaño moderado. Este contexto permite comparaciones controladas entre métodos, modelos, semillas y tamaños de muestra, pero no autoriza una generalización directa a imágenes, texto, series temporales o dominios multimodales.

La restricción no es solo de datos, sino también de constructos. En datos tabulares, la fidelidad puede operacionalizarse mediante enmascaramiento de características y la estabilidad mediante perturbaciones locales con similitud coseno. En imágenes o texto, esas mismas operaciones podrían alterar el significado semántico de la instancia, por lo que las métricas deberían redefinirse o validarse antes de transferir conclusiones.

En consecuencia, la afirmación más fuerte del capítulo debe mantenerse dentro de su frontera: SHAP mostró el perfil más robusto de fidelidad y estabilidad en el benchmark Adult/tabular bajo las métricas especificadas. No se demuestra que SHAP sea universalmente superior en toda modalidad, tarea o entorno de despliegue.

## Dependencia de operacionalizaciones métricas

Las conclusiones dependen de las definiciones de fidelidad, estabilidad, parsimonia, brecha de fidelidad y coste empleadas en el estudio. Estas métricas fueron seleccionadas porque permiten comparar métodos post-hoc de forma controlada, pero no agotan el espacio de evaluación XAI.

La fidelidad basada en enmascaramiento puede verse afectada por correlaciones entre variables, como ocurre en pares de características redundantes o semánticamente relacionadas. Si enmascarar una variable rompe relaciones presentes en los datos, la magnitud del cambio predictivo puede reflejar tanto importancia local como artefactos de intervención. De forma similar, la estabilidad medida con perturbación gaussiana y similitud coseno captura una forma concreta de robustez local, no todas las nociones posibles de consistencia.

Otros enfoques, como pruebas de eliminación progresiva, métricas de sensibilidad Lipschitz, evaluaciones basadas en causalidad o criterios de plausibilidad contrafactual, podrían alterar la posición relativa de los métodos. Por ello, los resultados deben leerse como evidencia bajo una familia explícita de métricas, no como veredicto definitivo sobre calidad explicativa.

## Configuración de métodos y sensibilidad

La configuración de cada método también condiciona los perfiles observados. En LIME, el límite de características explicadas contribuye a su parsimonia; esta ventaja no debe interpretarse como propiedad puramente intrínseca del algoritmo. A la vez, la inestabilidad observada persiste como advertencia sustantiva bajo la configuración evaluada, especialmente en un contexto tabular con codificación de variables categóricas.

SHAP presenta una limitación distinta: su coste computacional depende fuertemente del modelo base y de la variante usada. TreeSHAP puede ser eficiente en modelos de árboles, mientras KernelSHAP puede volverse costoso para SVM o MLP. La conclusión favorable a SHAP debe acompañarse siempre de esta restricción operativa.

Anchors y DiCE requieren aún más cuidado. Anchors depende de umbrales de precisión, cobertura y estrategias de búsqueda; DiCE depende de restricciones de factibilidad, diversidad y proximidad. Una configuración distinta podría cambiar cobertura, coste y utilidad práctica. La comparación presentada caracteriza un diseño controlado, no todas las configuraciones razonables de estos métodos.

## Ausencia de validación humana directa

El estudio es principalmente funcional y computacional. Evalúa si las explicaciones son fieles, estables, parsimoniosas o costosas bajo métricas definidas, pero no mide comprensión humana, utilidad en la toma de decisiones, calibración de confianza ni desempeño de usuarios en tareas reales.

Esta limitación es importante porque una explicación técnicamente fiel puede no ser comprensible, y una explicación comprensible puede inducir confianza indebida. Del mismo modo, un contrafactual plausible desde el modelo puede no ser accionable para una persona si viola restricciones sociales, legales, económicas o causales.

Por tanto, FOM-7 debe entenderse como una infraestructura para evidencia comparativa trazable, no como sustituto de estudios con usuarios. Las dimensiones centradas en humanos (*human-grounded*) y centradas en aplicación (*application-grounded*) requieren instrumentos propios, tareas representativas y criterios de validez adicionales [@doshi-velez2017].

## Cobertura incompleta y artefactos faltantes

La cobertura incompleta de Anchors y DiCE limita la precisión de las conclusiones sobre ambos métodos. FOM-7 trata esta situación mediante exclusión controlada de artefactos no calificados y reporte explícito de cobertura, pero no elimina la incertidumbre asociada a celdas faltantes.

Este punto es metodológicamente productivo: muestra por qué una evaluación auditable debe reportar no solo métricas finales, sino también condiciones de producción de evidencia. La ausencia de artefactos puede ser tan informativa como una puntuación baja, porque revela límites de viabilidad, escalabilidad o compatibilidad entre método, modelo y configuración.

## Generalización de FOM-7

FOM-7 fue aplicado y documentado dentro de un entorno experimental controlado, con modelos congelados, configuraciones declarativas y artefactos versionados. Esa aplicación respalda su utilidad como protocolo de gobernanza para benchmarking XAI, pero aún requiere replicación independiente.

Su valor fuera del caso Adult/tabular dependerá de adaptar las puertas a nuevas modalidades, métricas y riesgos. La secuencia general puede mantenerse, pero los criterios de auditoría, armonización y reporte deberán especificarse de nuevo para cada dominio. En particular, el protocolo no resuelve por sí mismo problemas de validez causal, justicia algorítmica, utilidad clínica, cumplimiento regulatorio o impacto organizacional.

## Trabajo futuro

Una primera línea de trabajo consiste en extender el benchmark a otras modalidades. Imágenes, texto y series temporales permitirían probar si la disociación entre fidelidad, estabilidad, coste y forma explicativa se mantiene cuando las unidades semánticas dejan de ser columnas tabulares.

Una segunda línea es realizar estudios con usuarios. Estos estudios deberían evaluar comprensión, utilidad decisional, confianza calibrada y carga cognitiva, conectando métricas funcionales con desempeño humano. También permitirían examinar si reglas, atribuciones y contrafactuales producen beneficios distintos según la tarea.

Una tercera línea es analizar sensibilidad de hiperparámetros. En SHAP, conviene estudiar tamaño y selección del conjunto de referencia; en LIME, número de muestras, ancho de kernel y número de características; en Anchors, umbrales de precisión y cobertura; en DiCE, restricciones de factibilidad, diversidad y proximidad.

Una cuarta línea es replicar los contrastes SHAP-LIME y los perfiles Anchors-DiCE en conjuntos de datos de alto impacto, como crédito, salud o justicia. Estas réplicas deberían conservar el principio FOM-7: hipótesis congeladas, artefactos auditados, tablas armonizadas, inferencia trazable y límites explícitos.

Finalmente, el trabajo futuro debería formalizar mejor la dimensión de comprensibilidad dentro de la taxonomía de evaluación. La parsimonia es una aproximación útil, pero insuficiente. La comprensibilidad depende de semántica, familiaridad del usuario, formato, contexto de decisión y consecuencias de la explicación. Integrar esa dimensión sin perder trazabilidad metodológica es una tarea central para la siguiente generación de evaluación XAI.
