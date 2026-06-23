# Implicaciones para la evaluación auditable de XAI

## De la selección de métodos a la gobernanza de evidencia

La aplicación empírica muestra que la selección de métodos XAI no puede resolverse mediante una jerarquía universal. LIME, SHAP, Anchors y DiCE producen objetos explicativos distintos, responden preguntas distintas y exhiben compromisos distintos entre fidelidad, estabilidad, coste, cobertura y forma de explicación. Por ello, la pregunta editorialmente más valiosa para un capítulo de libro no es qué método "gana", sino qué condiciones hacen admisible una afirmación sobre cada método.

Este desplazamiento cambia la función del benchmark. Los resultados no se presentan como una competencia cerrada entre explicadores, sino como evidencia de que la evaluación XAI necesita una capa de gobernanza. SHAP ilustra el perfil de auditoría de alta fidelidad y estabilidad; LIME ilustra la tensión entre bajo coste y fragilidad; Anchors ilustra el problema de comparar reglas con métricas de atribución; DiCE ilustra la necesidad de criterios propios para contrafactuales. En conjunto, los cuatro métodos funcionan como casos de una tesis más general: la explicabilidad útil depende de la relación entre objetivo, artefacto, métrica y alcance.

## FOM-7 como disciplina de formulación

La contribución metodológica de FOM-7 es hacer visible el camino entre una salida experimental y una afirmación publicable. Sin una secuencia de puertas, la comparación entre métodos podría confundirse con una colección de resultados: algunos completos, otros incompletos, algunos comparables y otros no. FOM-7 separa ejecución, auditoría, armonización, inferencia, reproducibilidad y reporte, de modo que cada conclusión conserve su unidad de análisis y su evidencia fuente.

Esta disciplina modifica el lenguaje científico. Una afirmación admisible no dice simplemente que SHAP es superior; dice que SHAP mostró mayor fidelidad y estabilidad bajo EXP2, sobre Adult Income, en celdas calificadas, con métricas definidas y pruebas no paramétricas específicas. Una afirmación admisible no dice que LIME sea inadecuado; dice que LIME fue eficiente y parsimonioso, pero inestable bajo semillas y perturbaciones controladas. Esta forma de escribir es más estrecha, pero también más robusta: reduce generalidad retórica para aumentar auditabilidad.

## Implicaciones prácticas

Para auditoría técnica, la evidencia favorece métodos con mayor fidelidad y estabilidad, aun cuando el coste sea mayor. En el benchmark, ese perfil corresponde principalmente a SHAP, con la advertencia de que su viabilidad depende de la variante del explicador y del modelo base. Para exploración rápida, baja latencia o comunicación preliminar, LIME conserva un lugar claro, siempre que sus salidas no se usen como evidencia estable sin controles adicionales. Para explicaciones condicionales, Anchors puede ser útil si se reportan precisión, cobertura y complejidad de regla. Para escenarios orientados a acción o corrección, DiCE responde a una pregunta distinta y debe evaluarse con criterios de validez, proximidad, diversidad y factibilidad.

La recomendación práctica, por tanto, es condicional: seleccionar el método según tarea, riesgo, objeto explicativo y tolerancia al coste. En aplicaciones de alto impacto, una explicación barata pero inestable puede ser aceptable para exploración interna y problemática para auditoría. Una explicación estable pero costosa puede ser inviable en baja latencia y apropiada para revisión diferida. Una regla clara puede ser comunicativamente potente, pero insuficiente si la cobertura es baja. Un contrafactual puede orientar acción, pero requiere restricciones causales o de dominio antes de traducirse en recomendación real.

## Relación con el estado del campo

El capítulo se alinea con la crítica contemporánea a la proliferación de métricas y herramientas sin gobernanza experimental. Recursos como OpenXAI, Quantus y revisiones recientes han ampliado el repertorio de evaluación, pero la dificultad persiste cuando los estudios no declaran criterios de admisibilidad, alcance inferencial o trazabilidad de artefactos (Agarwal et al., 2022; Hedström et al., 2023; Canha et al., 2025). La contribución específica de FOM-7 no es reemplazar esos recursos, sino ordenar su uso dentro de una secuencia verificable.

En conjunto, la discusión sugiere que la madurez de XAI no depende solo de producir explicadores más sofisticados. También depende de construir prácticas de evaluación capaces de distinguir evidencia fuerte, evidencia descriptiva y observaciones aún no generalizables. Esta es la razón por la que el capítulo propone pasar de explicaciones plausibles a evidencia auditable: no para reducir la XAI a métricas, sino para impedir que las métricas se conviertan en afirmaciones sin control metodológico.
