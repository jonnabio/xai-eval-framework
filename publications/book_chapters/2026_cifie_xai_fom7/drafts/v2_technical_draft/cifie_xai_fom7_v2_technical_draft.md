# Del modelo de caja negra a la evidencia auditable: evaluación reproducible de métodos agnósticos de explicabilidad mediante el protocolo FOM-7

**Jonathan Herrera-Vásquez**  

Universidad Americana de Europa (UNADE)  

ORCID: https://orcid.org/0000-0002-7149-6635

**Miguel Herrero-Uceda**  

Universidad Americana de Europa (UNADE)

---

# Resumen y palabras clave

## Resumen

La explicabilidad en inteligencia artificial suele presentarse como respuesta a la opacidad de los modelos de aprendizaje automático, pero producir explicaciones no equivale a demostrar que esas explicaciones sean fieles, estables, comparables o técnicamente defendibles. Este capítulo aborda esa brecha mediante FOM-7, un protocolo operativo de siete puertas para convertir el benchmarking de métodos post-hoc en evidencia reproducible, multi-métrica y auditable. El capítulo integra fundamentos de XAI, una crítica a la crisis de evaluación y un benchmark empírico sobre UCI Adult Income que compara LIME, SHAP, Anchors y DiCE en cinco familias de modelos, cinco semillas y tres tamaños de muestra. Tras la auditoría de artefactos, el análisis utiliza 275 celdas calificadas y pruebas no paramétricas con control de multiplicidad. Los resultados muestran diferencias globales significativas en fidelidad y estabilidad; SHAP presenta el perfil más fuerte para auditoría técnica, mientras LIME conserva ventajas de coste y parsimonia con una limitación crítica de estabilidad. Anchors y DiCE requieren lectura diferenciada porque producen reglas y contrafactuales, no solo atribuciones de características. La contribución central es metodológica: desplazar la evaluación XAI desde rankings aislados hacia perfiles explicativos trazables, delimitados por objetivo, métrica, evidencia y alcance.

## Palabras clave

Inteligencia artificial explicable; explicabilidad agnóstica al modelo; benchmarking reproducible; protocolo FOM-7; evaluación multi-métrica; explicaciones post-hoc.


# Introducción

## De la opacidad predictiva a la exigencia de evidencia

El avance de los modelos de aprendizaje automático ha intensificado una tensión central en la investigación y aplicación de inteligencia artificial: los sistemas con mayor capacidad predictiva suelen ser también aquellos cuyo funcionamiento interno resulta menos transparente para investigadores, auditores, usuarios y responsables institucionales. La literatura sobre inteligencia artificial explicable (XAI) ha descrito esta tensión como un desplazamiento desde la mera exactitud predictiva hacia condiciones más amplias de comprensión, confianza, trazabilidad y responsabilidad algorítmica (Adadi & Berrada, 2018; Arrieta et al., 2019; Ali et al., 2023). En dominios donde las predicciones automatizadas influyen sobre crédito, salud, educación, empleo, seguridad o servicios públicos, la explicación no puede entenderse como un adorno comunicativo posterior al modelo, sino como una condición metodológica para examinar si el comportamiento observado puede defenderse técnicamente. Esta exigencia se vuelve más importante cuando la explicación se usa para justificar decisiones, detectar sesgos, comunicar resultados a usuarios no técnicos o sostener procesos de auditoría.

La XAI responde a esta dificultad mediante un repertorio amplio de métodos que producen artefactos interpretables: atribuciones de características, reglas locales, modelos sustitutos, resúmenes globales, visualizaciones o ejemplos contrafactuales. Los métodos post-hoc agnósticos al modelo ocupan un lugar especialmente relevante porque pueden aplicarse a modelos ya entrenados sin modificar su arquitectura interna. LIME aproxima localmente la predicción mediante un sustituto interpretable (Ribeiro et al., 2016); SHAP asigna contribuciones aditivas inspiradas en valores de Shapley (Lundberg & Lee, 2017); Anchors formula reglas locales de alta precisión que delimitan condiciones suficientes para conservar una predicción (Ribeiro et al., 2018); y DiCE genera ejemplos contrafactuales diversos orientados a explorar cambios de resultado (Mothilal et al., 2020; Wachter et al., 2017). Sin embargo, esa diversidad también introduce un problema de fondo: una atribución, una regla y un contrafactual no responden la misma pregunta explicativa. Por tanto, tratarlos como salidas intercambiables puede conducir a comparaciones técnicamente débiles.

La discusión contemporánea ha insistido en que interpretabilidad y explicabilidad no son propiedades simples ni universalmente observables. Lipton (2018) advierte que el término interpretabilidad suele usarse con significados distintos, desde transparencia del modelo hasta utilidad de la explicación para una audiencia concreta. Rudin et al. (2022) subrayan, además, que en contextos de alto impacto no siempre basta con explicar modelos opacos: cuando sea posible, deberían preferirse modelos intrínsecamente interpretables. Este capítulo no resuelve esa tensión sustituyendo todos los modelos de caja negra por modelos transparentes; su punto de partida es más acotado. En muchos entornos reales ya existen modelos complejos o se requiere evaluar explicadores post-hoc por razones comparativas, operativas o regulatorias. En ese escenario, la pregunta crítica no es únicamente si una explicación parece razonable, sino si existe evidencia suficiente para tratarla como fiel, estable, reproducible y comparable.

## La crisis de evaluación en XAI

La proliferación de métodos XAI ha sido acompañada por una proliferación igualmente intensa de métricas, herramientas, taxonomías y criterios de evaluación. Revisiones recientes muestran que el campo ha avanzado en la identificación de propiedades como fidelidad, estabilidad, robustez, parsimonia, completitud, sensibilidad o utilidad humana, pero también evidencian una fragmentación persistente: distintos estudios emplean definiciones, unidades de análisis, perturbaciones, conjuntos de referencia y criterios de inclusión que no siempre son comparables entre sí (Abdul Kadir et al., 2023; Nauta et al., 2023; Schwalbe & Finzel, 2023). Esta fragmentación genera una dificultad epistemológica: dos trabajos pueden afirmar que evalúan el mismo explicador y, sin embargo, estar midiendo propiedades distintas bajo condiciones experimentales incompatibles. En consecuencia, la acumulación de evidencia se vuelve frágil, porque las conclusiones no siempre pueden transferirse de un diseño a otro.

La crisis de evaluación no implica ausencia de métricas; por el contrario, el problema surge en parte porque existen muchas métricas y pocas reglas compartidas para decidir cuándo una métrica sostiene una afirmación inferencial. Doshi-Velez y Kim (2017) propusieron distinguir evaluaciones centradas en aplicación, evaluaciones centradas en humanos y evaluaciones funcionalmente fundamentadas, lo que permite ubicar con mayor precisión qué tipo de evidencia aporta cada estudio. En una línea complementaria, Pawlicki et al. (2024) argumentan que la evaluación de XAI requiere múltiples métricas porque una sola dimensión no puede capturar la calidad explicativa completa. Esta observación es decisiva para el capítulo: una explicación puede ser fiel pero inestable, estable pero costosa, concisa pero incompleta, o semánticamente intuitiva pero débil como evidencia del comportamiento del modelo. Por ello, la evaluación defendible exige leer perfiles explicativos y no solo rankings.

Los marcos recientes de evaluación han contribuido a ordenar esta situación. Quantus proporciona una infraestructura amplia para evaluar explicaciones mediante familias de métricas y comparaciones sistemáticas (Hedström et al., 2023), mientras OpenXAI promueve una evaluación transparente de explicaciones post-hoc con énfasis en comparabilidad, fidelidad y sesgos potenciales de evaluación (Agarwal et al., 2022). Asimismo, Canha et al. (2025) plantean la necesidad de marcos funcionalmente fundamentados que hagan explícitos los criterios de evaluación XAI desde una revisión sistemática de la literatura. Estas contribuciones son fundamentales, pero no eliminan por sí solas el problema operativo que enfrenta un estudio empírico concreto: antes de interpretar una métrica debe saberse qué protocolo se congeló, qué artefactos fueron válidos, qué ejecuciones se excluyeron, qué comparaciones son homogéneas, qué pruebas estadísticas son admisibles y qué límites conserva cada conclusión.

Desde esta perspectiva, la evaluación XAI debe entenderse como un problema de gobernanza de evidencia. No basta con generar explicaciones plausibles ni con producir tablas de métricas; es necesario demostrar que las explicaciones proceden de artefactos íntegros, que las métricas fueron operacionalizadas de forma consistente, que las unidades de análisis no inducen pseudorreplicación, que las comparaciones respetan la estructura del diseño y que las afirmaciones finales pueden regresar a una fuente verificable. Este capítulo adopta esa posición metodológica y la traduce en una pregunta directriz: ¿cómo convertir ejecuciones de benchmarking XAI en evidencia reproducible, comparable y auditable sin sobrepasar el alcance de los datos, las métricas y los modelos evaluados?

## Objetivo y contribución del capítulo

El objetivo del capítulo es presentar FOM-7 como un protocolo reproducible para la evaluación multi-métrica de métodos post-hoc agnósticos al modelo, y mostrar su utilidad mediante un benchmark empírico sobre LIME, SHAP, Anchors y DiCE. La contribución no consiste en proponer un nuevo explicador, ni en declarar la superioridad universal de un método, sino en ordenar el proceso mediante el cual las salidas experimentales se transforman en evidencia defendible. FOM-7 se concibe como una secuencia de siete puertas: congelación del protocolo, ejecución controlada, auditoría de artefactos, armonización analítica, exportación inferencial, perfilado de reproducibilidad y reporte trazable. La regla que articula estas puertas es estricta: ninguna afirmación inferencial debe formularse si los controles previos no están satisfechos o si la afirmación no puede vincularse con evidencia fuente verificable.

La aportación del capítulo es doble. En el plano conceptual, integra la discusión sobre opacidad, interpretabilidad, evaluación funcional y gobernanza de evidencia para mostrar que la explicabilidad útil depende de condiciones de admisibilidad metodológica. En el plano empírico, organiza un benchmark tabular que compara cuatro métodos XAI bajo múltiples métricas y permite observar perfiles diferenciados: SHAP aparece como método fuerte en fidelidad y estabilidad bajo las condiciones evaluadas; LIME conserva ventajas de coste y concisión, pero con una limitación crítica de estabilidad; Anchors aporta reglas locales cuya utilidad exige atender precisión, cobertura y coste; y DiCE responde a una lógica contrafactual que no debe juzgarse únicamente como atribución de características. Esta lectura por perfiles coincide con la advertencia general de la literatura: la selección de un método XAI debe depender del objetivo operativo, del tipo de explicación requerido y del riesgo asociado al uso de la evidencia.

## Alcance empírico y estructura del capítulo

El benchmark se acota al conjunto UCI Adult Income, un problema tabular de clasificación binaria. El diseño compara cuatro métodos XAI sobre cinco familias de modelos, cinco semillas y tres tamaños de muestra. Las métricas primarias son fidelidad, estabilidad, parsimonia, brecha de fidelidad y coste computacional, resumidas en la Tabla 1. Este alcance debe conservarse durante toda la lectura: los resultados no se presentan como propiedades universales de LIME, SHAP, Anchors o DiCE, sino como evidencia obtenida bajo condiciones experimentales controladas. Las figuras numeradas en `figures/figure_registry.md` y las tablas de trabajo del capítulo funcionan como controles de trazabilidad para evitar sobreafirmaciones, especialmente cuando se discuten diferencias de cobertura, resultados pareados o perfiles agregados por método.

La exposición se organiza en cinco movimientos argumentales. Primero, se establecen los fundamentos técnicos de la explicabilidad agnóstica al modelo y se distingue entre plausibilidad, fidelidad, estabilidad, utilidad humana y verdad causal. Segundo, se describen los cuatro métodos evaluados como productores de objetos explicativos heterogéneos, lo que justifica una lectura multi-métrica. Tercero, se formula la crisis de evaluación en XAI y se presenta FOM-7 como respuesta metodológica orientada a la trazabilidad. Cuarto, se describen el diseño empírico y los resultados principales del benchmark, con énfasis en la frontera calidad-coste y en la ausencia de un método universalmente dominante. Finalmente, se discuten las implicaciones para auditoría técnica, selección de métodos y trabajo futuro. La tesis que sostiene el capítulo es, por tanto, precisa: la explicabilidad útil no depende únicamente de producir explicaciones plausibles, sino de evaluar cuándo esas explicaciones son fieles, estables, comparables, reproducibles y defendibles.


# Fundamentos técnicos de la explicabilidad agnóstica al modelo


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

La agregación de explicaciones locales no convierte automáticamente un conjunto de explicaciones en una teoría global del modelo. Un patrón estable en una región puede no sostenerse en otra, y una tendencia global puede ocultar heterogeneidades locales relevantes. Por esta razón, las afirmaciones del capítulo deben declarar su escala: instancia, bloque experimental, método, modelo, conjunto de datos o benchmark completo.

## Plausibilidad, fidelidad y corrección

Una explicación plausible resulta intuitiva o coherente con expectativas humanas, pero la plausibilidad no garantiza que el artefacto represente fielmente el comportamiento del modelo. Una explicación puede sonar convincente y, aun así, ser inestable, poco fiel o dependiente de una configuración arbitraria. Esta separación es central para evitar que la comunicación persuasiva sustituya a la evaluación técnica.

En este capítulo, la fidelidad se usa como constructo operacional: mide la alineación entre las importancias producidas por el explicador y los cambios observados en la salida del modelo cuando se enmascaran características relevantes. Esta definición no agota la noción más fuerte de *faithfulness*, entendida como correspondencia profunda con el proceso decisional. FOM-7 trata la fidelidad como evidencia medible y trazable, no como prueba automática de verdad causal [@zheng2025].

También debe distinguirse estabilidad de robustez. La estabilidad evalúa si pequeñas perturbaciones de entrada producen explicaciones similares. La robustez remite a resistencia frente a cambios más exigentes, condiciones fuera de distribución, ataques o variaciones de despliegue. Un método puede ser estable bajo ruido leve y frágil ante otros escenarios. Esta distinción ayuda a interpretar por qué el benchmark usa varias métricas y evita decidir calidad explicativa desde un único indicador [@hedstrom2023; @nauta2023].

## Métricas como proxies operacionales

Las métricas del benchmark no miden utilidad humana directa, comprensión subjetiva ni verdad causal. Funcionan como proxies reproducibles para comparar artefactos explicativos bajo un diseño controlado. En la tesis, las métricas primarias son fidelidad, estabilidad, parsimonia, brecha de fidelidad y coste computacional. Cada una cubre una dimensión distinta, con dirección e interpretación propias.

Esta lectura multi-métrica es importante porque los métodos post-hoc producen objetos heterogéneos. Una atribución SHAP puede evaluarse naturalmente por fidelidad y estabilidad; una regla Anchors exige considerar precisión y cobertura; un contrafactual DiCE debe leerse también desde validez, proximidad y factibilidad; un sustituto LIME requiere controlar muestreo y vecindario. El protocolo evita formular rankings absolutos y obliga a declarar qué constructo sostiene cada conclusión.

## Alcance de la evidencia

El capítulo se ubica principalmente en evaluación funcionalmente fundamentada (*functionally-grounded*): utiliza proxies computacionales y artefactos verificables en lugar de estudios directos con usuarios. Esta elección permite reproducibilidad y control estadístico, pero no autoriza conclusiones sobre utilidad humana, satisfacción, confianza calibrada o desempeño en tareas reales. En la terminología de @doshi-velez2017, esas afirmaciones requerirían diseños centrados en humanos (*human-grounded*) o centrados en aplicación (*application-grounded*).

Por tanto, el lenguaje inferencial debe conservar el alcance de la evidencia. No debe afirmarse que un método "explica mejor" en términos universales. Debe afirmarse, cuando proceda, que un método presenta mayor fidelidad, estabilidad, parsimonia o eficiencia bajo un conjunto de datos, modelo, métrica, configuración y unidad de análisis determinados.


# Métodos post-hoc evaluados: LIME, SHAP, Anchors y DiCE


## Panorama comparativo

Los cuatro métodos analizados representan familias distintas de explicación post-hoc agnóstica o parcialmente agnóstica al modelo. LIME produce sustitutos locales; SHAP genera atribuciones aditivas de características; Anchors formula reglas locales de alta precisión; DiCE construye ejemplos contrafactuales diversos. Esta heterogeneidad es metodológicamente importante porque cada método produce un objeto explicativo diferente y, por tanto, no debe evaluarse como si todos respondieran exactamente la misma pregunta.

La Tabla 2 sintetiza la base matemática, el tipo de salida, las fortalezas y las limitaciones que orientan la comparación empírica.

La comparación del capítulo debe leerse como evaluación de perfiles, no como ranking universal. FOM-7 exige que cada conclusión conserve unido el método, el objeto explicativo, la métrica, el contexto experimental y el alcance de la afirmación.

## LIME: sustitutos locales e inestabilidad potencial

LIME (*Local Interpretable Model-agnostic Explanations*) explica predicciones individuales mediante una aproximación local del modelo de caja negra. El procedimiento genera perturbaciones alrededor de una instancia, consulta el modelo original y ajusta un modelo interpretable, usualmente lineal, ponderando las observaciones según su proximidad a la instancia explicada [@ribeiro2016].

Su base metodológica puede resumirse como una regresión local ponderada sobre un vecindario artificial. La explicación resultante identifica características con pesos positivos o negativos que aproximan la influencia local en la predicción. Esta salida es relativamente sencilla de comunicar y suele tener bajo coste computacional frente a alternativas más complejas.

La principal fortaleza de LIME es su flexibilidad: puede aplicarse a distintos clasificadores sin acceder a su estructura interna. Sin embargo, esa misma flexibilidad introduce sensibilidad al muestreo, al kernel de proximidad, al tamaño del vecindario, al número de perturbaciones y a la selección de características. Por ello, una explicación LIME no debe evaluarse solo por su legibilidad. Debe comprobarse si es fiel al modelo local y si permanece estable ante perturbaciones razonables.

En el benchmark de la tesis, LIME aparece como una alternativa de bajo coste y alta parsimonia, pero con estabilidad casi nula en las condiciones evaluadas. Esta combinación lo vuelve útil para escenarios de latencia o comunicación rápida, pero problemático en auditoría, comparación entre instancias o decisiones de alto riesgo cuando se requiere consistencia explicativa.

## SHAP: atribución aditiva basada en valores de Shapley

SHAP (*SHapley Additive exPlanations*) interpreta una predicción como suma de contribuciones atribuibles a las características. Su fundamento proviene del valor de Shapley en teoría de juegos cooperativos, adaptado al problema de distribuir la salida de un modelo entre variables explicativas [@lundberg2017].

La salida típica de SHAP es un vector de atribuciones, local para una instancia y agregable para análisis globales. Su fortaleza reside en un marco formal unificado para explicaciones aditivas, con propiedades axiomáticas que facilitan la interpretación comparativa. Esta base lo convierte en un referente para análisis de fidelidad y estabilidad en datos tabulares.

No obstante, SHAP requiere decisiones operativas relevantes. El conjunto de referencia, la forma de simular ausencia de características, la dependencia entre variables y la variante concreta del explicador condicionan el significado de las atribuciones. KernelSHAP conserva mayor generalidad, pero puede ser costoso; TreeSHAP aprovecha modelos de árbol y puede ser mucho más eficiente. Por ello, "usar SHAP" no describe por sí solo una configuración experimental completa.

En los resultados extraídos de la tesis, SHAP presenta el perfil global más fuerte en fidelidad y estabilidad dentro del benchmark, aunque con costes heterogéneos por familia de modelo. Su uso dentro del capítulo debe enfatizar esta frontera calidad-coste: SHAP es especialmente defendible cuando la prioridad es evidencia explicativa de alta calidad, pero su viabilidad práctica depende del modelo base y de las restricciones de latencia.

## Anchors: reglas locales de alta precisión

Anchors explica una predicción mediante reglas locales tipo si-entonces. La idea central es encontrar condiciones suficientes bajo las cuales el modelo mantiene la misma predicción con alta probabilidad [@ribeiro2018]. A diferencia de LIME o SHAP, Anchors no produce principalmente pesos de características, sino reglas que delimitan una región de decisión.

La fortaleza de Anchors es comunicativa. Una regla local puede resultar más legible que una lista de atribuciones, sobre todo cuando se necesita explicar condiciones que sostienen una decisión. Sin embargo, la precisión de una regla debe interpretarse junto con su cobertura. Una regla muy estrecha puede ser precisa porque aplica a pocos casos; una regla más amplia puede perder precisión.

Esta tensión convierte a Anchors en un método que exige evaluación cuidadosa. Su salida no se alinea naturalmente con todas las métricas de atribución. Si el benchmark lo evalúa solo con fidelidad de importancia, puede penalizarlo por no producir el mismo tipo de artefacto que SHAP o LIME. Por ello, FOM-7 debe presentar Anchors como evidencia condicional: útil cuando precisión y cobertura se reportan juntas, pero limitada cuando se compara directamente contra métodos de atribución.

En los resultados de la tesis, Anchors muestra cobertura incompleta, coste alto y variable, y valores inferiores de fidelidad y estabilidad frente a SHAP y LIME bajo las métricas usadas. Esta lectura no debe interpretarse como fallo absoluto del método, sino como evidencia de que las reglas locales de alta precisión tienen un objeto explicativo distinto y pueden requerir criterios adicionales de evaluación.

## DiCE: contrafactuales diversos y acción correctiva

DiCE (*Diverse Counterfactual Explanations*) genera ejemplos contrafactuales: instancias alternativas que, con cambios mínimos o controlados, producirían una predicción diferente [@mothilal2020]. Su pregunta principal no es qué característica contribuyó más a la predicción actual, sino qué tendría que cambiar para obtener otro resultado.

Esta orientación ubica a DiCE en una familia distinta de explicaciones. Sus criterios naturales incluyen validez del cambio de predicción, proximidad a la instancia original, diversidad entre alternativas, factibilidad y accionabilidad. La tradición de explicaciones contrafactuales también subraya la relación entre explicación, decisiones automatizadas y posibilidad de acción correctiva [@wachter2017].

DiCE no debe evaluarse como si fuera simplemente un método de atribución. Una baja fidelidad en términos de correlación de importancias puede reflejar que el método optimiza otro objetivo: producir alternativas contrafactuales. Por tanto, sus resultados deben interpretarse en relación con concisión, cambios propuestos, proximidad, diversidad y límites de factibilidad.

En la tesis, DiCE aparece con baja fidelidad bajo métricas de atribución, estabilidad intermedia, alta parsimonia contrafactual y coste moderado. Esta combinación lo vuelve relevante para discutir la ausencia de un método universalmente dominante: puede ser menos adecuado para auditar importancias locales, pero más alineado con escenarios donde interesa explorar alternativas de acción.

## Comparación metodológica y uso dentro de FOM-7

Los cuatro métodos no producen evidencia intercambiable. LIME aproxima localmente una frontera; SHAP reparte contribuciones; Anchors identifica condiciones suficientes; DiCE propone alternativas contrafactuales. La evaluación debe respetar esa ontología de salidas.

Dentro de FOM-7, la comparación se vuelve admisible solo cuando el capítulo declara:

- qué objeto explicativo produce cada método;
- qué métrica se aplica y por qué es pertinente;
- qué unidad experimental sostiene el resultado;
- qué artefactos y scripts respaldan la cifra;
- qué límites conserva la afirmación.

Esta regla permite usar los resultados del benchmark sin sobreafirmar. SHAP puede describirse como fuerte en fidelidad y estabilidad bajo las condiciones evaluadas; LIME como eficiente pero inestable; Anchors como regla local con límites de cobertura; DiCE como método contrafactual cuya calidad no se agota en métricas de atribución. Esa lectura por perfiles es la base técnica para la discusión posterior del capítulo.


# La crisis de evaluación en XAI


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

La trazabilidad también es necesaria para controlar la sobreafirmación. Cada afirmación fuerte debería poder regresar a un artefacto fuente: tabla, figura, configuración, script, prueba estadística o decisión metodológica. Si se afirma que un método es más estable, debe quedar claro en qué conjunto de datos, modelo, métrica, configuración y unidad experimental se observó esa estabilidad.

## Herramientas sin protocolo de gobernanza suficiente

Herramientas como Quantus y OpenXAI han contribuido a estandarizar y facilitar la evaluación XAI [@hedstrom2023; @agarwal2022]. Quantus organiza familias de métricas y reduce fricción técnica. OpenXAI promueve comparabilidad y transparencia en la evaluación de explicaciones post-hoc. Estas contribuciones son importantes, pero no resuelven por sí solas el problema de gobernanza metodológica.

Antes de ejecutar una métrica deben definirse las reglas del experimento: qué artefactos son admisibles, cómo se congelan configuraciones, qué salidas se excluyen, cómo se armonizan esquemas, qué pruebas estadísticas son válidas, cómo se controla multiplicidad y qué límites conserva cada afirmación. Una herramienta puede ofrecer métricas; un protocolo debe gobernar cuándo esas métricas pueden transformarse en evidencia.

La contribución necesaria, por tanto, no consiste solo en ampliar el catálogo de métricas. Consiste en integrar métricas, artefactos, reproducibilidad, inferencia y trazabilidad dentro de una secuencia operativa. Ese es el punto en el que la crisis de evaluación conduce al protocolo FOM-7.

## Implicación para el capítulo

El capítulo debe presentar la evaluación XAI como un problema de admisibilidad de evidencia. No basta con generar explicaciones plausibles ni con producir tablas de métricas. Es necesario demostrar que los resultados provienen de artefactos válidos, que las comparaciones son homogéneas, que la variabilidad fue controlada, que la inferencia es apropiada y que las afirmaciones son trazables.

Esta transición prepara la función de FOM-7: convertir una evaluación fragmentada en una cadena auditable de decisiones, artefactos, métricas, pruebas y afirmaciones delimitadas.


# Protocolo FOM-7 para benchmarking auditable


## Función metodológica

FOM-7 (*Framework Operation Method*, siete puertas) se define como una secuencia operativa para convertir ejecuciones de benchmarking XAI en evidencia reproducible, comparable y trazable. Su propósito no es introducir un nuevo explicador ni una métrica aislada, sino gobernar el ciclo completo que conecta diseño experimental, ejecución controlada, calificación de artefactos, armonización analítica, inferencia estadística, reproducibilidad y reporte de afirmaciones.

El protocolo responde directamente a la crisis de evaluación descrita en la sección anterior. La existencia de métodos, métricas y herramientas no garantiza por sí misma que los resultados sean admisibles como evidencia científica. Una herramienta puede calcular métricas correctamente y, aun así, el estudio puede sobreinterpretar sus resultados si no declara qué artefactos son válidos, qué configuraciones fueron congeladas, qué pruebas estadísticas son admisibles y qué límites conserva cada afirmación.

FOM-7 opera como puente entre el diagnóstico y la práctica experimental: transforma problemas de fragmentación, reproducibilidad y trazabilidad en controles secuenciales verificables.

La Tabla 3 resume las siete puertas, sus artefactos de entrada y salida, y el tipo de fallo metodológico que cada una busca controlar.

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

FOM-7 no demuestra utilidad humana directa, verdad causal de las explicaciones ni superioridad universal de un método. Su alcance es funcionalmente fundamentado (*functionally-grounded*): produce evidencia comparativa, reproducible y trazable sobre métodos post-hoc bajo condiciones experimentales controladas. Las dimensiones centradas en humanos (*human-grounded*) o centradas en aplicación (*application-grounded*) requerirían protocolos adicionales con usuarios, tareas, escalas e instrumentos propios.


# Diseño empírico del benchmark


## Enfoque general

El diseño empírico operacionaliza la evaluación de métodos XAI agnósticos al modelo como un benchmark cuantitativo, reproducible y multi-métrico. Su finalidad es comparar LIME, SHAP, Anchors y DiCE bajo condiciones controladas, evitando que las diferencias observadas se confundan con variaciones no documentadas de modelo, semilla, muestra, configuración o artefacto.

El estudio se ubica en una lógica funcionalmente fundamentada (*functionally-grounded*): las métricas utilizadas son proxies computacionales de calidad explicativa y no evidencia directa de utilidad humana, plausibilidad semántica o causalidad. Esta delimitación es central para sostener afirmaciones prudentes y auditables.

## Fases experimentales

El diseño distingue dos cohortes de evidencia. La primera, EXP1, funciona como fase de calibración y reproducibilidad. Su propósito es verificar la implementación del pipeline, entrenar y congelar modelos, y estimar dispersión métrica bajo variación de semilla. EXP1 no se utiliza para sostener las afirmaciones confirmativas principales.

La segunda, EXP2, constituye el benchmark primario. En esta fase se ejecuta el diseño factorial completo y se producen los artefactos que alimentan las pruebas estadísticas, los perfiles por método y las afirmaciones empíricas del capítulo. La separación entre EXP1 y EXP2 reduce la contaminación entre decisiones exploratorias y evidencia confirmatoria.

## Conjunto de datos y modelos predictivos

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

![Figura 1. Cobertura analítica EXP2 por modelo y método. Fuente: figura derivada de `thesis/assets/figures/fig_cobertura_exp2_es.png`.](../../figures/exported/fig_cobertura_exp2_es.png)

## Configuración de explicadores

SHAP se ejecuta con variantes acordes al modelo base: `TreeExplainer` para modelos de árboles y `KernelExplainer` para modelos donde se requiere aproximación más general. LIME utiliza `LimeTabularExplainer` con parámetros congelados de muestreo, número de características y ancho de kernel. Anchors emplea reglas locales con umbral de precisión efectivo de 0.95. DiCE genera contrafactuales orientados a la clase opuesta, usando diferencias entre instancia original y contrafactual como base de importancia.

Estas configuraciones deben interpretarse como parte del protocolo experimental. No se evalúan nombres abstractos de métodos, sino implementaciones concretas con parámetros específicos, artefactos registrados y límites conocidos.

## Métricas primarias

El benchmark utiliza cinco métricas primarias, resumidas en la Tabla 1:

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

El diseño se gobierna mediante FOM-7, resumido en la Tabla 3. Las puertas controlan congelación del protocolo, ejecución declarativa, auditoría de artefactos, armonización de tablas, exportación inferencial, perfilado de reproducibilidad y trazabilidad de afirmaciones.

Esta estructura es necesaria porque el benchmark no solo produce resultados; produce resultados que deben ser admisibles como evidencia. Una celda con artefacto vacío, esquema incompatible o valores inválidos no puede alimentar pruebas confirmativas. Una afirmación sin trazabilidad a tabla, script, configuración o límite de alcance no debe presentarse como inferencial.

## Plan inferencial

Las diferencias globales entre métodos se evalúan mediante pruebas de Friedman y comparaciones post-hoc de Nemenyi sobre bloques completos. El análisis pareado SHAP-LIME utiliza pruebas bilaterales de Wilcoxon y corrección de multiplicidad Holm-Bonferroni. La reproducibilidad se examina mediante coeficientes de variación en configuraciones replicadas.

El objetivo del plan inferencial no es producir un ranking universal de explicadores, sino determinar qué diferencias son defendibles bajo el diseño, con qué tamaño de efecto, sobre qué unidad de análisis y dentro de qué alcance empírico.


# Resultados principales: frontera calidad-coste


## Alcance de los resultados

Los resultados proceden del benchmark EXP2 sobre UCI Adult Income. El diseño planificado comprendía 300 celdas, resultantes de cinco modelos, cuatro métodos XAI, cinco semillas y tres tamaños de muestra. Tras la auditoría de artefactos de FOM-7, se obtuvieron 275 celdas calificadas. Las celdas no calificadas fueron excluidas antes de la inferencia confirmativa.

La cobertura fue completa para SHAP y LIME, con 75 de 75 celdas cada uno. DiCE alcanzó 68 de 75 celdas y Anchors 57 de 75. Esta diferencia de cobertura no debe ocultarse: forma parte de la evidencia sobre viabilidad operativa de los métodos y condiciona la precisión de las conclusiones para Anchors y DiCE.

La Figura 1 documenta visualmente la cobertura analítica de EXP2 y debe leerse junto con la auditoría de artefactos de FOM-7.

## Diferencias globales entre métodos

El análisis global muestra diferencias estadísticamente significativas entre métodos en fidelidad y estabilidad. Para fidelidad, la prueba de Friedman produjo $\chi^2_F = 42.12$ sobre 15 bloques completos, con $p_{\mathrm{Holm}} = 1.51 \times 10^{-8}$ y $W = 0.936$. Este resultado rechaza la hipótesis nula de igualdad global entre métodos y muestra un patrón consistente: SHAP ocupa la primera posición de rango, seguido por LIME, Anchors y DiCE.

Para estabilidad, la prueba de Friedman produjo $\chi^2_F = 40.68$, con $p_{\mathrm{Holm}} = 2.29 \times 10^{-8}$ y $W = 0.904$. El patrón no replica simplemente el orden de fidelidad: SHAP mantiene el perfil más fuerte, pero DiCE aparece como método relativamente estable en comparación con LIME y Anchors. Esta diferencia confirma que fidelidad y estabilidad no son constructos equivalentes.

La implicación central es metodológica: una evaluación centrada en una única métrica habría perdido parte del fenómeno. Los métodos no se distinguen solo por cuánto se alinean con el comportamiento local del modelo, sino también por cuánto varían sus explicaciones bajo perturbaciones y por qué tipo de objeto explicativo producen.

![Figura 2. Diagrama de diferencia crítica de Nemenyi para fidelidad y estabilidad. Fuente: figura derivada de `thesis/assets/figures/fig_cd_diagram_es.png`.](../../figures/exported/fig_cd_diagram_es.png)

![Figura 3. Distribución de fidelidad y estabilidad por método. Fuente: figura derivada de `thesis/assets/figures/fig_boxplots_metricas_es.png`.](../../figures/exported/fig_boxplots_metricas_es.png)

## Comparación pareada SHAP-LIME

El contraste pareado SHAP-LIME se realizó sobre 75 celdas coincidentes $(g,s,n)$. Los resultados muestran una ventaja sistemática de SHAP en métricas de calidad explicativa, acompañada de una penalización de coste en la mayoría de contextos.

En fidelidad, SHAP supera a LIME en las 75 celdas, con diferencia media de +0.2479 y tamaño de efecto $d_z = +4.820$. En estabilidad, la ventaja también aparece en las 75 celdas, con diferencia media de +0.7176 y $d_z = +3.002$. Estos tamaños de efecto son muy grandes y respaldan la afirmación de que SHAP ofrece un perfil más fuerte cuando el objetivo principal es fidelidad y consistencia explicativa.

La parsimonia muestra el patrón inverso: SHAP es más denso y LIME más conciso. En coste, SHAP es en promedio más costoso, con diferencia media de +8047.6 ms, aunque el efecto es heterogéneo por modelo. Esto define la frontera calidad-coste: SHAP aporta mayor calidad explicativa bajo las métricas evaluadas, mientras LIME conserva atractivo operativo cuando la latencia y la concisión son prioritarias.

![Figura 4. Diferencias pareadas SHAP-LIME para fidelidad y estabilidad. Fuente: figura derivada de `thesis/assets/figures/fig_diferencias_pareadas_es.png`.](../../figures/exported/fig_diferencias_pareadas_es.png)

![Figura 5. Relación entre estabilidad y coste por método. Fuente: figura derivada de `thesis/assets/figures/fig_estabilidad_coste_es.png`.](../../figures/exported/fig_estabilidad_coste_es.png)

## Perfil de SHAP

SHAP presenta el perfil global más equilibrado en el benchmark. Sus valores consolidados reportados en la tesis son fidelidad = 0.810, estabilidad = 0.724, parsimonia = 0.234, brecha de fidelidad = 0.431 y coste = 24,804 ms sobre bloques calificados.

Este perfil lo posiciona como método fuerte para auditoría técnica cuando se requiere fidelidad y estabilidad. Sin embargo, su coste es heterogéneo: TreeSHAP puede ser eficiente en modelos de árboles, mientras que KernelSHAP puede ser costoso en modelos como SVM o MLP. Por tanto, la recomendación no debe formularse como superioridad universal, sino como preferencia condicionada por el modelo base y las restricciones operativas.

## Perfil de LIME

LIME aparece como método eficiente y parsimonioso. Su coste medio reportado es 226 ms y su fidelidad media 0.560, con parsimonia de 0.085. Estos valores sostienen su utilidad en escenarios donde se requiere explicación rápida, legible y de bajo coste.

La limitación crítica es su estabilidad casi nula bajo las condiciones evaluadas. La tesis reporta estabilidad media cercana a 0.014 y CV de estabilidad de 86.2% bajo semillas. Esto restringe su uso en auditoría, comparación entre instancias o escenarios donde dos ejecuciones razonables deberían producir explicaciones consistentes.

## Perfil de Anchors

Anchors produce reglas locales de alta precisión, cualitativamente distintas a las atribuciones numéricas de LIME y SHAP. Su fortaleza está en la legibilidad condicional: una regla puede comunicar bajo qué condiciones se mantiene una predicción.

En el benchmark, Anchors presenta cobertura incompleta, coste alto y variable, fidelidad media de 0.386 y estabilidad de 0.052. Esta lectura debe ser prudente. No implica que Anchors sea inútil, sino que sus reglas requieren criterios propios de precisión, cobertura y aplicabilidad. Su comparación directa mediante métricas diseñadas para atribuciones debe conservar esta advertencia.

## Perfil de DiCE

DiCE genera contrafactuales, no atribuciones de importancia. Por ello, su baja fidelidad bajo métricas de atribución no debe interpretarse como fallo absoluto. En la tesis, DiCE presenta fidelidad de 0.172, estabilidad intermedia de 0.366, parsimonia muy baja de 0.017 y coste moderado de 2,056 ms.

Este perfil sugiere que DiCE es más pertinente cuando el objetivo explicativo es explorar alternativas de acción o corrección, no cuando se busca auditar importancias locales. Su presencia en el benchmark ayuda a mostrar por qué FOM-7 evalúa perfiles y no rankings universales.

## Reproducibilidad del protocolo

La proposición de reproducibilidad se confirma parcialmente. En configuraciones replicadas de EXP1, SHAP-fidelidad, SHAP-estabilidad y LIME-fidelidad muestran CV inferiores al umbral del 15%, con valores principales por debajo de 3%. La excepción es LIME-estabilidad, con CV de 86.2%, explicable por una media cercana a cero.

Esta excepción no invalida el protocolo. Más bien, revela una propiedad estructural del método bajo la configuración evaluada: cuando la estabilidad media es casi nula, pequeñas variaciones absolutas producen un CV relativo alto. FOM-7 permite distinguir entre irreproducibilidad del protocolo e inestabilidad sustantiva del explicador.

## Lectura integrada

Los resultados, resumidos en la Tabla 4, sostienen tres conclusiones de alcance delimitado. Primero, existen diferencias globales significativas entre métodos bajo el diseño EXP2. Segundo, SHAP ofrece el perfil más fuerte en fidelidad y estabilidad, especialmente cuando el objetivo es auditoría técnica. Tercero, no existe un método universalmente dominante: LIME conserva ventajas de coste y parsimonia; Anchors produce reglas condicionales con límites de cobertura; DiCE aporta contrafactualidad y acción correctiva.

La frontera calidad-coste es, por tanto, el resultado interpretativo central. La selección de un método XAI debe depender del objetivo operativo: auditoría de alta fidelidad, explicación rápida, regla condicional o exploración contrafactual. FOM-7 permite que esa selección se base en evidencia trazable y no en preferencias anecdóticas.

## Figuras integradas

Las visualizaciones registradas en `figures/figure_registry.md` se usan como apoyo, no como sustituto de las pruebas estadísticas. Las figuras integradas incluyen la cobertura EXP2, el diagrama de diferencia crítica, boxplots de fidelidad/estabilidad, diferencias pareadas SHAP-LIME, la relación estabilidad-coste, la correlación entre métricas y el perfil radar por método. En particular, la Figura 7 apoya la discusión de perfiles, mientras la Figura 1 debe acompañar cualquier lectura sobre artefactos faltantes.

![Figura 6. Correlación entre métricas del benchmark. Fuente: figura derivada de `thesis/assets/figures/fig_correlacion_metricas_es.png`.](../../figures/exported/fig_correlacion_metricas_es.png)


# Discusión

## Lectura integrada de los hallazgos

Los resultados del benchmark no sostienen una jerarquía universal de métodos XAI, sino una frontera de uso condicionada por el objetivo explicativo. Esta distinción es central para interpretar el capítulo: LIME, SHAP, Anchors y DiCE no producen el mismo tipo de objeto explicativo, no fallan por las mismas razones y no deberían seleccionarse mediante una única escala de calidad.

Bajo las condiciones evaluadas en EXP2, SHAP presenta el perfil más sólido para auditoría técnica. La ventaja frente a LIME en fidelidad y estabilidad aparece en las 75 celdas pareadas, con tamaños de efecto muy grandes. Esta regularidad empírica respalda una recomendación práctica: cuando el objetivo es defender explicaciones ante revisión técnica, comparar resultados entre modelos o sostener inferencias sobre comportamiento local, SHAP ofrece la opción más robusta dentro del diseño Adult/tabular analizado.

LIME conserva, sin embargo, un lugar metodológico claro. Su coste medio bajo y su parsimonia lo hacen atractivo para escenarios de exploración rápida, baja latencia o comunicación concisa. La advertencia es igualmente clara: su estabilidad casi nula bajo las condiciones evaluadas impide tratar sus explicaciones como evidencia estable en auditoría. En este sentido, el resultado no invalida LIME como herramienta, pero sí restringe el tipo de afirmación que puede sostenerse a partir de sus salidas.

Anchors y DiCE obligan a ampliar la discusión más allá del eje atribucional. Anchors produce reglas condicionales locales; DiCE produce contrafactuales orientados a acción. Su evaluación mediante métricas de atribución sirve para caracterizar límites comparativos, pero no agota su utilidad. La baja fidelidad de DiCE, por ejemplo, no equivale a fracaso explicativo si la pregunta relevante es qué cambios podrían modificar una predicción. Del mismo modo, la cobertura incompleta de Anchors debe interpretarse como una señal operativa relevante, no como una simple anomalía experimental.

## De métricas aisladas a perfiles explicativos

El hallazgo conceptual más importante es la disociación entre fidelidad, estabilidad, coste y forma explicativa. Una evaluación que use solo fidelidad habría favorecido SHAP, pero habría invisibilizado su coste. Una evaluación centrada solo en parsimonia habría favorecido LIME, pero habría omitido su inestabilidad. Una evaluación centrada solo en interpretabilidad semántica habría destacado Anchors o DiCE, pero sin resolver la trazabilidad inferencial de sus resultados.

Por ello, el capítulo propone interpretar los métodos como perfiles. SHAP corresponde al perfil de auditoría de alta fidelidad y estabilidad; LIME al perfil de explicación rápida y económica; Anchors al perfil de regla local condicional; DiCE al perfil contrafactual y de exploración de alternativas. Esta lectura es más útil que un ranking único porque conecta la selección del método con el propósito de uso.

![Figura 7. Perfil multidimensional normalizado por método. Fuente: figura derivada de `thesis/assets/figures/fig_radar_metodos_es.png`.](../../figures/exported/fig_radar_metodos_es.png)

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


# Conclusiones

Este capítulo abordó un problema práctico y metodológico: cómo evaluar explicaciones post-hoc de aprendizaje automático sin reducir la interpretabilidad a una métrica aislada ni convertir resultados experimentales en afirmaciones más generales de lo que la evidencia permite. La respuesta propuesta combina una lectura multidimensional de los métodos XAI con FOM-7, un protocolo de siete puertas para producir evidencia reproducible, comparable y trazable.

El resultado empírico principal es que, en el benchmark Adult/tabular evaluado, SHAP ofrece el perfil más fuerte de fidelidad y estabilidad. Las pruebas globales muestran diferencias significativas entre métodos, y el contraste pareado SHAP-LIME confirma una ventaja sistemática de SHAP en las 75 celdas coincidentes. Esta ventaja tiene un coste: SHAP es más denso y, en promedio, más costoso que LIME.

LIME conserva valor cuando la prioridad es velocidad, concisión y exploración local de bajo coste. Su limitación crítica es la estabilidad: bajo las condiciones evaluadas, sus explicaciones no deben tratarse como evidencia consistente para auditoría o comparación robusta. Anchors y DiCE ocupan espacios distintos. Anchors resulta pertinente cuando se necesita una regla condicional local; DiCE, cuando la pregunta es contrafactual y orientada a alternativas de acción.

La conclusión metodológica es que no existe un método universalmente dominante. La selección debe depender del objetivo explicativo, la tolerancia al coste, la necesidad de estabilidad, la forma de explicación requerida y el nivel de riesgo del contexto. En aplicaciones donde la explicación debe ser defendible, no basta con producir una salida interpretable: se requiere saber si esa salida es fiel, estable, reproducible y trazable.

FOM-7 contribuye precisamente en ese punto. Sus puertas de congelación, ejecución, auditoría, armonización, exportación, perfilado y reporte convierten el benchmarking XAI en un proceso gobernado. El protocolo no garantiza utilidad humana ni verdad causal, pero sí reduce la ambigüedad metodológica: distingue artefactos calificados de artefactos no admisibles, inferencia confirmativa de descripción, y evidencia delimitada de sobreafirmación.

La contribución del capítulo es doble. En el plano empírico, ofrece criterios de selección para LIME, SHAP, Anchors y DiCE bajo un diseño factorial controlado. En el plano metodológico, muestra cómo FOM-7 puede ordenar métricas, resultados y límites en una cadena auditable de evidencia. Esta combinación permite pasar de explicaciones plausibles a afirmaciones defendibles.

El alcance de estas conclusiones es deliberadamente acotado. Los resultados no deben extrapolarse sin validación a otras modalidades, métricas, poblaciones o contextos de decisión. La utilidad humana, la acción contrafactual real y la validez causal exigen estudios adicionales. Aun así, el capítulo aporta una base concreta para avanzar desde la proliferación de métodos XAI hacia una cultura de evaluación más disciplinada.

En síntesis, la pregunta no es solo qué método explica mejor, sino bajo qué condiciones, para qué propósito, con qué evidencia y con qué límites. FOM-7 ofrece una forma de formular y responder esa pregunta sin perder trazabilidad. Esa es la contribución central: hacer que la evaluación de XAI sea menos dependiente de intuiciones y más dependiente de evidencia verificable.


# Referencias


Adadi, A., & Berrada, M. (2018). Peeking inside the black-box: A survey on explainable artificial intelligence (XAI). *IEEE Access, 6*, 52138-52160. https://doi.org/10.1109/access.2018.2870052

Agarwal, C., Ley, D., Krishna, S., Saxena, E., Pawelczyk, M., Johnson, N., Puri, I., Zitnik, M., & Lakkaraju, H. (2022). OpenXAI: Towards a transparent evaluation of post hoc model explanations. In *Advances in Neural Information Processing Systems (NeurIPS)*. NeurIPS.

Ali, S., Abuhmed, T., El-Sappagh, S., Muhammad, K., Alonso-Moral, J. M., Confalonieri, R., Guidotti, R., Del Ser, J., Díaz-Rodríguez, N., & Herrera, F. (2023). Explainable artificial intelligence (XAI): What we know and what is left to attain trustworthy artificial intelligence. *Information Fusion, 99*, 101805. https://doi.org/10.1016/j.inffus.2023.101805

Alvarez-Melis, D., & Jaakkola, T. S. (2018). *On the robustness of interpretability methods*. arXiv. https://arxiv.org/abs/1806.08049

Altukhi, Z. M., Pradhan, S., & Aljohani, N. (2025). A systematic literature review of the latest advancements in XAI. *Technologies, 13*(3), 93. https://doi.org/10.3390/technologies13030093

Arrieta, A. B., Díaz-Rodríguez, N., Del Ser, J., Bennetot, A., Tabik, S., Barbado, A., Garcia, S., Gil-Lopez, S., Molina, D., Benjamins, R., Chatila, R., & Herrera, F. (2019). Explainable artificial intelligence (XAI): Concepts, taxonomies, opportunities and challenges toward responsible AI. *Information Fusion, 58*, 82-115. https://doi.org/10.1016/j.inffus.2019.12.012

Bhattacharya, A., & Verbert, K. (2024). How good is your explanation? Towards a standardised evaluation approach for diverse XAI methods on multiple dimensions of explainability. In *Proceedings of the 32nd ACM Conference on User Modeling, Adaptation and Personalization (UMAP Adjunct '24)*. https://doi.org/10.1145/3631700.3664911

Burger, C., Chen, L., & Le, T. (2023). Are your explanations reliable? Investigating the stability of LIME in explaining text classifiers by marrying XAI and adversarial attack. In *Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing* (pp. 12931-12944). https://doi.org/10.18653/v1/2023.emnlp-main.792

Canha, D., Kubler, S., Främling, K., & Fagherazzi, G. (2025). A functionally-grounded benchmark framework for XAI methods: Insights and foundations from a systematic literature review. *ACM Computing Surveys, 57*(12). https://doi.org/10.1145/3737445

Doshi-Velez, F., & Kim, B. (2017). *Towards a rigorous science of interpretable machine learning*. arXiv. https://doi.org/10.48550/arXiv.1702.08608

Friedman, M. (1937). The use of ranks to avoid the assumption of normality implicit in the analysis of variance. *Journal of the American Statistical Association, 32*(200), 675-701. https://doi.org/10.1080/01621459.1937.10503522

Hedström, A., Weber, L., Bareeva, D., Krakowczyk, D., Motzkus, F., Samek, W., Lapuschkin, S., & Höhne, M. M.-C. (2023). Quantus: An explainable AI toolkit for responsible evaluation of neural network explanations and beyond. *Journal of Machine Learning Research, 24*(34), 1-11.

Lipton, Z. C. (2018). The mythos of model interpretability. *Queue, 16*(3), 31-57. https://doi.org/10.1145/3236386.3241340

Lundberg, S. M., & Lee, S. (2017). A unified approach to interpreting model predictions. *arXiv*. https://doi.org/10.48550/arXiv.1705.07874

Mothilal, R. K., Sharma, A., & Tan, C. (2020). Explaining machine learning classifiers through diverse counterfactual explanations. In *FAT* '20: Proceedings of the 2020 Conference on Fairness, Accountability, and Transparency*. https://doi.org/10.1145/3351095.3372850

Nauta, M., Trienes, J., Pathak, S., Nguyen, E., Peters, M., Schmitt, Y., Schlötterer, J., van Keulen, M., & Seifert, C. (2023). From anecdotal evidence to quantitative evaluation methods: A systematic review on evaluating explainable AI. *ACM Computing Surveys, 55*(13s), 1-42. https://doi.org/10.1145/3583558

Pawlicki, M., Pawlicka, A., Uccello, F., Szelest, S., D'Antonio, S., Kozik, R., & Choraś, M. (2024). Evaluating the necessity of the multiple metrics for assessing explainable AI: A critical examination. *Neurocomputing, 602*, 128282. https://doi.org/10.1016/j.neucom.2024.128282

Ribeiro, M. T., Singh, S., & Guestrin, C. (2016). "Why should I trust you?": Explaining the predictions of any classifier. *Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining*. https://doi.org/10.1145/2939672.2939778

Ribeiro, M. T., Singh, S., & Guestrin, C. (2018). Anchors: High-precision model-agnostic explanations. *Proceedings of the AAAI Conference on Artificial Intelligence, 32*(1). https://doi.org/10.1609/aaai.v32i1.11491

Rudin, C., Chen, C., Chen, Z., Huang, H., Semenova, L., & Zhong, C. (2022). Interpretable machine learning: Fundamental principles and 10 grand challenges. *Statistics Surveys, 16*, 1-85. https://doi.org/10.1214/21-ss133

Schwalbe, G., & Finzel, B. (2023). A comprehensive taxonomy for explainable artificial intelligence: A systematic survey of surveys on methods and concepts. *Data Mining and Knowledge Discovery, 38*(5), 3043-3101. https://doi.org/10.1007/s10618-022-00867-8

Wachter, S., Mittelstadt, B., & Russell, C. (2017). Counterfactual explanations without opening the black box: Automated decisions and the GDPR. *SSRN Electronic Journal*. https://doi.org/10.2139/ssrn.3063289

Zheng, X., Shirani, F., Chen, Z., Lin, C., Cheng, W., Guo, W., & Luo, D. (2025). F-FIDELITY: A robust framework for faithfulness evaluation of explainable AI. *ICLR 2025 Proceedings*. https://trustai4s-lab.github.io/ffidelity
