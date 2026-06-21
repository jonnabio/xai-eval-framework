# Discusión

## Lectura integrada de los hallazgos

Los resultados del benchmark no sostienen una jerarquía universal de métodos XAI, sino una frontera de uso condicionada por el objetivo explicativo. Esta distinción es central para interpretar el capítulo: LIME, SHAP, Anchors y DiCE no producen el mismo tipo de objeto explicativo, no fallan por las mismas razones y no deberían seleccionarse mediante una única escala de calidad.

Bajo las condiciones evaluadas en EXP2, SHAP presenta el perfil más sólido para auditoría técnica. La ventaja frente a LIME en fidelidad y estabilidad aparece en las 75 celdas pareadas, con tamaños de efecto muy grandes. Esta regularidad empírica respalda una recomendación práctica: cuando el objetivo es defender explicaciones ante revisión técnica, comparar resultados entre modelos o sostener inferencias sobre comportamiento local, SHAP ofrece la opción más robusta dentro del diseño Adult/tabular analizado.

LIME conserva, sin embargo, un lugar metodológico claro. Su coste medio bajo y su parsimonia lo hacen atractivo para escenarios de exploración rápida, baja latencia o comunicación concisa. La advertencia es igualmente clara: su estabilidad casi nula bajo las condiciones evaluadas impide tratar sus explicaciones como evidencia estable en auditoría. En este sentido, el resultado no invalida LIME como herramienta, pero sí restringe el tipo de afirmación que puede sostenerse a partir de sus salidas.

Anchors y DiCE obligan a ampliar la discusión más allá del eje atribucional. Anchors produce reglas condicionales locales; DiCE produce contrafactuales orientados a acción. Su evaluación mediante métricas de atribución sirve para caracterizar límites comparativos, pero no agota su utilidad. La baja fidelidad de DiCE, por ejemplo, no equivale a fracaso explicativo si la pregunta relevante es qué cambios podrían modificar una predicción. Del mismo modo, la cobertura incompleta de Anchors debe interpretarse como una señal operativa relevante, no como una simple anomalía experimental.

## De métricas aisladas a perfiles explicativos

El hallazgo conceptual más importante es la disociación entre fidelidad, estabilidad, coste y forma explicativa. Una evaluación que use solo fidelidad habría favorecido SHAP, pero habría invisibilizado su coste. Una evaluación centrada solo en parsimonia habría favorecido LIME, pero habría omitido su inestabilidad. Una evaluación centrada solo en interpretabilidad semántica habría destacado Anchors o DiCE, pero sin resolver la trazabilidad inferencial de sus resultados.

Por ello, el capítulo propone interpretar los métodos como perfiles. SHAP corresponde al perfil de auditoría de alta fidelidad y estabilidad; LIME al perfil de explicación rápida y económica; Anchors al perfil de regla local condicional; DiCE al perfil contrafactual y de exploración de alternativas. Esta lectura es más útil que un ranking único porque conecta la selección del método con el propósito de uso.

![Figura 7. Perfil multidimensional normalizado por método. Fuente: figura derivada de `thesis/assets/figures/fig_radar_metodos_es.png`.](../figures/exported/fig_radar_metodos_es.png)

La literatura ha señalado de forma recurrente que la interpretabilidad no es un constructo unitario y que la evaluación de XAI debe explicitar qué propiedad se mide, para qué tarea y con qué supuesto de validez [@doshi-velez2017; @alvarezmelis2018; @nauta2023]. Los resultados aquí discutidos refuerzan esa posición desde una evidencia empírica controlada: no basta con preguntar qué método explica mejor, sino qué tipo de explicación se necesita y qué riesgos se aceptan.

## Papel metodológico de FOM-7

FOM-7 funciona como la infraestructura que hace defendible esta interpretación. Sin una secuencia de puertas, la comparación entre métodos podría confundirse con una colección de salidas experimentales: algunas completas, otras incompletas, algunas comparables y otras no. El protocolo separa explícitamente ejecución, auditoría, armonización, inferencia y reporte, de modo que cada afirmación conserve su unidad de análisis y su evidencia fuente.

La puerta de auditoría es especialmente relevante para EXP2. El diseño planificado contemplaba 300 celdas, pero solo 275 fueron calificadas. En lugar de ocultar esta pérdida o completarla mediante reconstrucciones no verificables, FOM-7 obliga a reportarla y a delimitar su impacto. Esto preserva la validez de las pruebas confirmativas donde los bloques son completos, y al mismo tiempo impide sobreextender conclusiones sobre métodos con cobertura menor.

La puerta de reporte también modifica el tono de las conclusiones. Una afirmación admisible no dice simplemente que SHAP es superior, sino que SHAP mostró mayor fidelidad y estabilidad que LIME en 75 celdas pareadas del benchmark Adult/tabular, bajo las métricas y configuraciones especificadas. Esta formulación es más estrecha, pero también más científica: reduce la generalidad retórica para aumentar la auditabilidad.

## Implicaciones para selección de métodos XAI

La selección práctica de métodos debería comenzar por el objetivo de explicación. Si se requiere auditoría técnica, trazabilidad y consistencia, la evidencia favorece SHAP, aceptando su coste computacional. Si se requiere explicación rápida y compacta, LIME puede ser adecuado, siempre que no se usen sus salidas como evidencia estable sin controles adicionales. Si se requiere comunicar una condición local en forma de regla, Anchors ofrece una semántica más directa, pero exige revisar cobertura y coste. Si se requiere explorar acciones o cambios contrafactuales, DiCE responde a una pregunta distinta de la atribución y debe evaluarse con criterios de acción correctiva, plausibilidad y factibilidad.

Esta lectura desplaza la recomendación desde "el mejor método" hacia "el método admisible para una tarea y un riesgo". En aplicaciones de alto impacto, esa diferencia no es menor. Una explicación barata pero inestable puede ser aceptable para exploración interna y problemática para auditoría. Una explicación estable pero costosa puede ser inviable en baja latencia y apropiada para revisión diferida. Una regla clara puede ser comunicativamente potente, pero insuficiente si la cobertura es baja. Un contrafactual puede orientar acción, pero requiere restricciones causales o de dominio antes de traducirse en recomendación real.

## Relación con el estado del campo

El capítulo se alinea con la crítica contemporánea a la proliferación de métricas y herramientas sin gobernanza experimental. Recursos como OpenXAI, Quantus y revisiones recientes han ampliado el repertorio de evaluación, pero la dificultad persiste cuando los estudios no declaran criterios de admisibilidad, alcance inferencial o trazabilidad de artefactos [@agarwal2022; @hedstrom2023; @canha2025].

La contribución específica de FOM-7 no es reemplazar esos recursos, sino ordenar su uso dentro de una secuencia verificable. Las métricas siguen siendo necesarias, pero dejan de operar como evidencia autosuficiente. Su valor depende de que el diseño esté congelado, los artefactos sean íntegros, las unidades de análisis sean comparables y las conclusiones declaren límites.

En conjunto, la discusión sugiere que la madurez de XAI no depende solo de producir explicadores más sofisticados. También depende de construir prácticas de evaluación capaces de distinguir evidencia fuerte, evidencia descriptiva y observaciones aún no generalizables.
