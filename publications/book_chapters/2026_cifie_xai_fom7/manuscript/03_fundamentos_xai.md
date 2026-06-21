# Fundamentos técnicos de la explicabilidad agnóstica al modelo

Fuente inicial: `thesis/capitulo-2-fundamentos.qmd`, `references/references.bib` y `tables/table_metrics.md`.

## De modelos de caja negra a artefactos explicativos

La explicabilidad en inteligencia artificial surge de una tensión metodológica: los modelos con alta capacidad predictiva pueden capturar relaciones complejas, pero su lógica interna no siempre se presenta en una forma directamente comprensible o auditable para investigadores, usuarios, reguladores o responsables técnicos. En este contexto, la expresión "modelo de caja negra" no implica ausencia de estructura, sino dificultad para inspeccionar cómo esa estructura produce una predicción concreta.

La XAI post-hoc responde a esta dificultad mediante artefactos explicativos construidos después del entrenamiento del modelo. Estos artefactos no son el modelo en sí mismo; son representaciones, aproximaciones o consultas organizadas que buscan describir algún aspecto de su comportamiento. LIME aproxima localmente la decisión mediante un sustituto interpretable; SHAP asigna contribuciones aditivas a características; Anchors produce reglas locales de alta precisión; DiCE genera alternativas contrafactuales capaces de modificar la predicción [@ribeiro2016; @lundberg2017; @ribeiro2018; @mothilal2020].

Esta diversidad impide tratar la explicabilidad como una propiedad única. Una regla, una atribución y un contrafactual no responden la misma pregunta. Por ello, una evaluación técnicamente defendible debe declarar qué objeto explicativo se evalúa, qué propiedad se mide y qué tipo de afirmación puede sostenerse a partir de la evidencia generada.

## Interpretabilidad, explicabilidad y transparencia

La interpretabilidad se relaciona con la posibilidad de comprender la estructura o el funcionamiento de un modelo. En modelos transparentes, como reglas simples o modelos lineales de baja complejidad, parte de esa comprensión puede derivarse directamente del objeto predictivo. La explicabilidad, en cambio, se refiere a la producción de razones, representaciones o artefactos que hacen inteligible una predicción o comportamiento del modelo para un propósito determinado.

La transparencia pertenece principalmente al modelo; la explicación pertenece al ecosistema de interpretación. Una explicación post-hoc puede ser clara y aun así representar de forma imperfecta el mecanismo decisional. De manera inversa, un modelo formalmente transparente puede resultar difícil de interpretar si contiene demasiadas variables, interacciones o reglas. Esta distinción justifica que el capítulo no evalúe "comprensión" en abstracto, sino artefactos explicativos concretos bajo condiciones experimentales controladas.

## Métodos agnósticos y métodos específicos del modelo

Los métodos agnósticos al modelo tratan al predictor como una caja negra: consultan entradas y salidas sin requerir acceso a parámetros internos, gradientes o estructura específica. Esta propiedad favorece la portabilidad experimental, porque un mismo procedimiento puede aplicarse a distintos clasificadores. Sin embargo, también introduce un límite: el explicador observa el comportamiento externo del modelo mediante consultas, no necesariamente su mecanismo interno.

Los métodos específicos del modelo aprovechan información interna de determinadas familias predictivas. Por ejemplo, algunas variantes de SHAP pueden explotar la estructura de modelos basados en árboles para reducir coste y mejorar eficiencia. Esta diferencia muestra que la comparación entre explicadores debe registrar no solo el nombre del método, sino su variante, acceso al modelo, conjunto de referencia, parámetros y coste computacional.

FOM-7 conserva esta distinción porque la portabilidad no equivale automáticamente a fidelidad. Un método agnóstico puede ser aplicable a más modelos, pero sus resultados dependen del muestreo, las perturbaciones y los supuestos operacionales utilizados. Un método específico puede ser más eficiente o preciso en una familia concreta, pero menos generalizable.

## Explicaciones locales y globales

Una explicación local describe el comportamiento del modelo alrededor de una instancia, predicción o vecindario específico. Una explicación global intenta resumir patrones del modelo en una región amplia o en el conjunto de datos completo. LIME, SHAP y Anchors suelen utilizarse localmente, aunque sus salidas pueden agregarse para construir resúmenes globales [@ribeiro2016; @lundberg2017; @ribeiro2018].

La agregación de explicaciones locales no convierte automáticamente un conjunto de explicaciones en una teoría global del modelo. Un patrón estable en una región puede no sostenerse en otra, y una tendencia global puede ocultar heterogeneidades locales relevantes. Por esta razón, las afirmaciones del capítulo deben declarar su escala: instancia, bloque experimental, método, modelo, dataset o benchmark completo.

## Plausibilidad, fidelidad y corrección

Una explicación plausible resulta intuitiva o coherente con expectativas humanas, pero la plausibilidad no garantiza que el artefacto represente fielmente el comportamiento del modelo. Una explicación puede sonar convincente y, aun así, ser inestable, poco fiel o dependiente de una configuración arbitraria. Esta separación es central para evitar que la comunicación persuasiva sustituya a la evaluación técnica.

En este capítulo, la fidelidad se usa como constructo operacional: mide la alineación entre las importancias producidas por el explicador y los cambios observados en la salida del modelo cuando se enmascaran características relevantes. Esta definición no agota la noción más fuerte de *faithfulness*, entendida como correspondencia profunda con el proceso decisional. FOM-7 trata la fidelidad como evidencia medible y trazable, no como prueba automática de verdad causal [@zheng2025].

También debe distinguirse estabilidad de robustez. La estabilidad evalúa si pequeñas perturbaciones de entrada producen explicaciones similares. La robustez remite a resistencia frente a cambios más exigentes, condiciones fuera de distribución, ataques o variaciones de despliegue. Un método puede ser estable bajo ruido leve y frágil ante otros escenarios. Esta distinción ayuda a interpretar por qué el benchmark usa varias métricas y evita decidir calidad explicativa desde un único indicador [@hedstrom2023; @nauta2023].

## Métricas como proxies operacionales

Las métricas del benchmark no miden utilidad humana directa, comprensión subjetiva ni verdad causal. Funcionan como proxies reproducibles para comparar artefactos explicativos bajo un diseño controlado. En la tesis, las métricas primarias son fidelidad, estabilidad, parsimonia, brecha de fidelidad y coste computacional. Cada una cubre una dimensión distinta, con dirección e interpretación propias.

Esta lectura multi-métrica es importante porque los métodos post-hoc producen objetos heterogéneos. Una atribución SHAP puede evaluarse naturalmente por fidelidad y estabilidad; una regla Anchors exige considerar precisión y cobertura; un contrafactual DiCE debe leerse también desde validez, proximidad y factibilidad; un sustituto LIME requiere controlar muestreo y vecindario. El protocolo evita formular rankings absolutos y obliga a declarar qué constructo sostiene cada conclusión.

## Alcance de la evidencia

El capítulo se ubica principalmente en evaluación *functionally-grounded* o funcionalmente fundamentada: utiliza proxies computacionales y artefactos verificables en lugar de estudios directos con usuarios. Esta elección permite reproducibilidad y control estadístico, pero no autoriza conclusiones sobre utilidad humana, satisfacción, confianza calibrada o desempeño en tareas reales. En la terminología de @doshi-velez2017, esas afirmaciones requerirían diseños human-grounded o application-grounded.

Por tanto, el lenguaje inferencial debe conservar el alcance de la evidencia. No debe afirmarse que un método "explica mejor" en términos universales. Debe afirmarse, cuando proceda, que un método presenta mayor fidelidad, estabilidad, parsimonia o eficiencia bajo un dataset, modelo, métrica, configuración y unidad de análisis determinados.
