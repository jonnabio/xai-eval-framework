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

La explicabilidad en inteligencia artificial surge de una tensión metodológica que atraviesa buena parte del aprendizaje automático contemporáneo: los modelos con alta capacidad predictiva pueden capturar relaciones complejas, no lineales y distribuidas, pero esa misma capacidad dificulta reconstruir, comunicar y auditar la lógica que conduce a una predicción concreta. En este contexto, la expresión "modelo de caja negra" no significa que el sistema carezca de estructura interna; significa que dicha estructura no se ofrece al investigador, al usuario experto o al responsable institucional en una forma directamente interpretable para justificar una decisión. Las revisiones recientes de XAI coinciden en que el problema no es solo técnico, sino también epistémico y práctico: explicar implica traducir el comportamiento de un modelo a artefactos que permitan inspección, contraste y uso responsable en un escenario determinado (Adadi & Berrada, 2018; Arrieta et al., 2019; Ali et al., 2023).

La XAI post-hoc responde a esta dificultad mediante artefactos explicativos construidos después del entrenamiento del modelo. Estos artefactos no son el modelo en sí mismo; son representaciones, aproximaciones, consultas o perturbaciones organizadas que describen una parte de su comportamiento bajo supuestos específicos. LIME aproxima localmente la decisión mediante un sustituto interpretable; SHAP asigna contribuciones aditivas a características con base en una formalización inspirada en valores de Shapley; Anchors produce reglas locales de alta precisión; DiCE genera alternativas contrafactuales orientadas a modificar la predicción (Ribeiro et al., 2016; Lundberg & Lee, 2017; Ribeiro et al., 2018; Mothilal et al., 2020). Esta diversidad impide tratar la explicabilidad como una propiedad única del sistema: una atribución, una regla y un contrafactual no responden la misma pregunta ni sostienen el mismo tipo de conclusión.

Por ello, una evaluación técnicamente defendible debe declarar qué objeto explicativo se evalúa, qué propiedad se mide y qué inferencia puede sostenerse con la evidencia disponible. La literatura distingue enfoques, objetivos y salidas explicativas con niveles distintos de granularidad, desde taxonomías conceptuales hasta revisiones centradas en métodos y ejemplos operacionales (Marcinkevičs & Vogt, 2023; Schwalbe & Finzel, 2023). Este capítulo adopta esa precaución: no evalúa "la explicabilidad" como una cualidad abstracta, sino artefactos post-hoc comparables bajo un protocolo, métricas y unidades de análisis previamente delimitadas.

## Interpretabilidad, explicabilidad y transparencia

La interpretabilidad se relaciona con la posibilidad de comprender la estructura, la lógica o el funcionamiento de un modelo en una forma significativa para una audiencia y una tarea. En modelos transparentes, como reglas simples, árboles poco profundos o modelos lineales de baja complejidad, parte de esa comprensión puede derivarse directamente del objeto predictivo. La explicabilidad, en cambio, se refiere a la producción de razones, representaciones o artefactos que hacen inteligible una predicción, una región del espacio de entrada o una tendencia del modelo para un propósito determinado. Esta diferencia es importante porque un modelo puede ser formalmente inspeccionable y, aun así, poco útil para una persona si contiene demasiadas variables, interacciones o transformaciones; del mismo modo, una explicación post-hoc puede ser clara y persuasiva sin reproducir fielmente el mecanismo decisional (Lipton, 2018; Murdoch et al., 2019).

La transparencia pertenece principalmente al modelo; la explicación pertenece al ecosistema de interpretación que rodea su uso. Ese ecosistema incluye el método explicador, la interfaz de comunicación, la persona que interpreta, la tarea analítica y el criterio de calidad empleado. Por esta razón, los trabajos sobre aprendizaje interpretable advierten contra sustituir modelos intrínsecamente comprensibles por explicaciones post-hoc cuando el contexto exige auditoría fuerte o decisiones de alto impacto, y proponen distinguir con cuidado entre modelos transparentes, explicaciones aproximadas y evidencia empírica de utilidad (Belle & Papantonis, 2021; Rudin et al., 2022). En consecuencia, este capítulo no evalúa comprensión subjetiva en abstracto; evalúa artefactos explicativos concretos bajo condiciones experimentales controladas, con métricas que solo cubren una parte del fenómeno explicativo.

## Métodos agnósticos y métodos específicos del modelo

Los métodos agnósticos al modelo tratan al predictor como una caja negra operacional: consultan entradas y salidas sin requerir acceso a parámetros internos, gradientes, pesos, arquitectura o reglas de entrenamiento. Esta propiedad favorece la portabilidad experimental, porque un mismo procedimiento puede aplicarse a clasificadores de familias distintas y permite comparar explicadores aun cuando el modelo base cambia. Sin embargo, también introduce un límite central: el explicador observa el comportamiento externo mediante consultas, perturbaciones o muestras sintéticas, no necesariamente el mecanismo interno que produjo la decisión. La promesa de generalidad, por tanto, debe leerse junto con sus supuestos de muestreo, vecindario, distribución de referencia y sensibilidad a hiperparámetros.

Los métodos específicos del modelo, en contraste, aprovechan información interna de determinadas familias predictivas. Algunas variantes de SHAP, por ejemplo, pueden explotar la estructura de modelos basados en árboles para reducir coste y mejorar eficiencia, mientras que otros enfoques se apoyan en gradientes o descomposiciones disponibles solo en arquitecturas particulares. Esta diferencia muestra que la comparación entre explicadores debe registrar no solo el nombre del método, sino su variante, acceso al modelo, conjunto de referencia, parámetros, presupuesto de cómputo y condiciones de ejecución. Dos explicaciones etiquetadas con el mismo método pueden diferir sustantivamente si cambian el fondo de comparación, el número de perturbaciones o la estrategia de discretización.

FOM-7 conserva esta distinción porque la portabilidad no equivale automáticamente a fidelidad. Un método agnóstico puede aplicarse a más modelos, pero sus resultados dependen de cómo se interroga la caja negra; un método específico puede ser más eficiente o preciso en una familia concreta, pero menos generalizable a otros escenarios. La evaluación propuesta en este capítulo, por tanto, trata la agnosticidad como una condición de diseño y no como una garantía de calidad explicativa.

## Explicaciones locales y globales

Una explicación local describe el comportamiento del modelo alrededor de una instancia, una predicción o un vecindario específico. Esta escala es especialmente relevante cuando se desea justificar una decisión individual, detectar variables influyentes para un caso concreto o explorar alternativas contrafactuales. Una explicación global, en cambio, intenta resumir patrones del modelo en una región amplia o en el conjunto de datos completo. LIME, SHAP y Anchors suelen utilizarse localmente, aunque sus salidas pueden agregarse para construir resúmenes globales, rankings promedio o perfiles de comportamiento por subgrupos (Ribeiro et al., 2016; Lundberg & Lee, 2017; Ribeiro et al., 2018).

La agregación de explicaciones locales no convierte automáticamente un conjunto de explicaciones en una teoría global del modelo. Un patrón estable en una región puede no sostenerse en otra, y una tendencia global puede ocultar heterogeneidades locales relevantes. Además, las decisiones de agregación introducen una capa analítica adicional: qué instancias se incluyen, cómo se normalizan las salidas, qué métrica resume la variación y qué umbral se considera material. Por esta razón, las afirmaciones del capítulo deben declarar su escala con precisión: instancia, bloque experimental, método, modelo, conjunto de datos o benchmark completo. Esa disciplina terminológica evita extrapolar resultados locales hacia conclusiones generales no sostenidas por el diseño.

## Plausibilidad, fidelidad y corrección

Una explicación plausible resulta intuitiva, narrativamente coherente o alineada con expectativas humanas, pero la plausibilidad no garantiza que el artefacto represente fielmente el comportamiento del modelo. Una explicación puede sonar convincente y, aun así, ser inestable, poco fiel o dependiente de una configuración arbitraria. Esta separación es central para evitar que la comunicación persuasiva sustituya a la evaluación técnica: en XAI, una explicación visualmente clara o fácil de contar puede generar confianza sin aportar evidencia suficiente sobre el vínculo entre características, perturbaciones y salida del predictor. La preocupación ya aparece en la literatura que diferencia comprensibilidad, utilidad, fidelidad y validez empírica como dimensiones relacionadas pero no equivalentes (Doshi-Velez & Kim, 2017; Nauta et al., 2023).

En este capítulo, la fidelidad se usa como constructo operacional: mide la alineación entre las importancias producidas por el explicador y los cambios observados en la salida del modelo cuando se enmascaran características relevantes. Esta definición no agota la noción más fuerte de *faithfulness*, entendida como correspondencia profunda con el proceso decisional, ni autoriza afirmaciones causales sobre el mundo representado por los datos. FOM-7 trata la fidelidad como evidencia medible y trazable, no como prueba automática de verdad causal. Esta prudencia es consistente con enfoques recientes que buscan robustecer la evaluación de fidelidad y separar la calidad del proxy computacional de conclusiones más amplias sobre comprensión o justicia del sistema (Zheng et al., 2025).

También debe distinguirse estabilidad de robustez. La estabilidad evalúa si pequeñas perturbaciones de entrada producen explicaciones similares; la robustez remite a resistencia frente a cambios más exigentes, condiciones fuera de distribución, ataques, variaciones de despliegue o cambios deliberados en el entorno experimental. Un método puede ser estable bajo ruido leve y frágil ante otros escenarios, o puede mostrar buena fidelidad promedio con alta variabilidad entre instancias. Esta distinción ayuda a interpretar por qué el benchmark usa varias métricas y evita decidir calidad explicativa desde un único indicador (Alvarez-Melis & Jaakkola, 2018; Hedström et al., 2023; Nauta et al., 2023).

## Métricas como proxies operacionales

Las métricas del benchmark no miden utilidad humana directa, comprensión subjetiva ni verdad causal. Funcionan como proxies reproducibles para comparar artefactos explicativos bajo un diseño controlado. En la tesis, las métricas primarias son fidelidad, estabilidad, parsimonia, brecha de fidelidad y coste computacional. Cada una cubre una dimensión distinta, con dirección e interpretación propias: la fidelidad aproxima alineación con la respuesta del modelo, la estabilidad observa sensibilidad de la explicación, la parsimonia controla complejidad comunicativa, la brecha de fidelidad permite comparar diferencias entre métodos y el coste registra la viabilidad práctica de ejecutar explicadores en condiciones repetibles.

Esta lectura multi-métrica es importante porque los métodos post-hoc producen objetos heterogéneos. Una atribución SHAP puede evaluarse naturalmente por fidelidad y estabilidad; una regla Anchors exige considerar precisión y cobertura; un contrafactual DiCE debe leerse también desde validez, proximidad, diversidad y factibilidad; un sustituto LIME requiere controlar muestreo y vecindario. La literatura de evaluación advierte que los indicadores disponibles no son intercambiables y que una conclusión sólida depende de alinear método, constructo, métrica y contexto de uso (Abdul Kadir et al., 2023; Canha et al., 2025; Pawlicki et al., 2024). Por ello, el protocolo evita formular rankings absolutos y obliga a declarar qué constructo sostiene cada conclusión.

## Alcance de la evidencia

El capítulo se ubica principalmente en evaluación funcionalmente fundamentada (*functionally-grounded*): utiliza proxies computacionales y artefactos verificables en lugar de estudios directos con usuarios. Esta elección permite reproducibilidad, comparación sistemática y control estadístico, pero no autoriza conclusiones sobre utilidad humana, satisfacción, confianza calibrada o desempeño en tareas reales. En la terminología de Doshi-Velez y Kim (2017), esas afirmaciones requerirían diseños centrados en humanos (*human-grounded*) o centrados en aplicación (*application-grounded*), con tareas, participantes, criterios de éxito y condiciones de uso explícitamente definidos.

Por tanto, el lenguaje inferencial debe conservar el alcance de la evidencia. No debe afirmarse que un método "explica mejor" en términos universales ni que una métrica aislada captura la calidad total de una explicación. Debe afirmarse, cuando proceda, que un método presenta mayor fidelidad, estabilidad, parsimonia o eficiencia bajo un conjunto de datos, modelo, métrica, configuración y unidad de análisis determinados. Esta regla de escritura es también una regla de validez: protege al capítulo de convertir resultados experimentales acotados en promesas generales sobre confianza, transparencia o responsabilidad algorítmica.


# Métodos post-hoc evaluados: LIME, SHAP, Anchors y DiCE


## Panorama comparativo

Los cuatro métodos analizados representan familias distintas de explicación post-hoc agnóstica o parcialmente agnóstica al modelo. LIME produce sustitutos locales; SHAP genera atribuciones aditivas de características; Anchors formula reglas locales de alta precisión; DiCE construye ejemplos contrafactuales diversos. Esta heterogeneidad es metodológicamente decisiva porque cada método produce un objeto explicativo diferente y, por tanto, no debe evaluarse como si todos respondieran exactamente la misma pregunta. Una atribución responde cuánto contribuye una característica bajo una definición operacional de referencia; una regla responde bajo qué condiciones se conserva una predicción; un contrafactual responde qué cambios podrían alterar el resultado. Las revisiones sobre modelos de caja negra y métodos interpretables subrayan esta diversidad de salidas y advierten que la evaluación debe alinear método, artefacto, métrica y propósito antes de comparar resultados (Guidotti et al., 2018; Carvalho et al., 2019; Marcinkevičs & Vogt, 2023).

La Tabla 2 sintetiza la base matemática, el tipo de salida, las fortalezas y las limitaciones que orientan la comparación empírica. Su función no es reducir los métodos a una jerarquía única, sino fijar el vocabulario con el que se leerán los resultados. FOM-7 exige que cada conclusión conserve unido el método, el objeto explicativo, la métrica, el contexto experimental y el alcance de la afirmación. Por ello, la comparación del capítulo debe entenderse como evaluación de perfiles: SHAP puede ser fuerte en fidelidad y estabilidad bajo las condiciones estudiadas; LIME puede ser eficiente y conciso, pero frágil ante perturbaciones; Anchors puede aportar reglas comunicables con restricciones de cobertura; DiCE puede producir alternativas contrafactuales útiles aunque no sea un método de atribución. La Tabla 4 permite conectar esta distinción conceptual con evidencia empírica: no todos los métodos tuvieron la misma cobertura de celdas, no todos optimizan el mismo constructo y no todos deben leerse con el mismo estándar de comparación.

## LIME: sustitutos locales e inestabilidad potencial

LIME (*Local Interpretable Model-agnostic Explanations*) explica predicciones individuales mediante una aproximación local del modelo de caja negra. El procedimiento genera perturbaciones alrededor de una instancia, consulta el modelo original y ajusta un modelo interpretable, usualmente lineal, ponderando las observaciones según su proximidad a la instancia explicada (Ribeiro et al., 2016). Su intuición es atractiva: aunque el modelo global sea demasiado complejo para inspeccionarse directamente, una región cercana a una observación específica podría aproximarse con una frontera más simple. La explicación resultante identifica características con pesos positivos o negativos que describen la influencia local estimada en la predicción.

La fortaleza de LIME reside en su flexibilidad y en su bajo umbral comunicativo. Puede aplicarse a clasificadores diversos sin acceder a parámetros internos, produce salidas relativamente legibles y suele tener menor coste computacional que explicadores más exhaustivos. Sin embargo, esa misma flexibilidad introduce riesgos que no deben quedar ocultos bajo la etiqueta de "modelo agnóstico". La explicación depende del esquema de muestreo, de la definición del vecindario, del kernel de proximidad, del número de perturbaciones, de la selección de variables y del sustituto interpretable elegido. Si esos elementos cambian, la explicación puede variar de forma sustancial aun cuando la instancia y el modelo base sean los mismos. Por ello, no basta con afirmar que una explicación LIME es interpretable porque utiliza un modelo lineal; debe verificarse si ese sustituto aproxima de manera adecuada el comportamiento local bajo condiciones documentadas (Ribeiro et al., 2016; Guidotti et al., 2018).

Esta sensibilidad conecta con una preocupación más amplia sobre confiabilidad de explicaciones post-hoc. Estudios recientes muestran que LIME puede producir narrativas plausibles y, aun así, ser inestable ante cambios razonables de perturbación o vulnerable a manipulaciones del proceso explicativo (Burger et al., 2023; Slack et al., 2020). Para FOM-7, LIME representa un caso ejemplar de método útil para exploración rápida y comunicación inicial, pero que exige controles explícitos de estabilidad, trazabilidad de parámetros y alcance local. En el benchmark de la tesis, LIME aparece como una alternativa de bajo coste y alta parsimonia: mantiene cobertura completa de celdas, coste medio de 226 ms, fidelidad moderada de 0.560 y parsimonia de 0.085. Sin embargo, su estabilidad media queda prácticamente anulada (0.014) y presenta una variación elevada bajo semillas. Esa combinación lo vuelve útil en escenarios de latencia o explicación preliminar, pero problemático para auditoría, comparación entre instancias o decisiones de alto riesgo cuando se requiere consistencia explicativa.

El valor de LIME dentro del capítulo, por tanto, no consiste en ser el método "débil" frente a SHAP, sino en mostrar un compromiso metodológico muy frecuente en XAI aplicada: rapidez y legibilidad no equivalen a reproducibilidad. Si el objetivo operativo es obtener una explicación local rápida para inspección exploratoria, LIME puede ser razonable siempre que se documenten sus parámetros y se evite generalizar la explicación fuera del vecindario evaluado. Si el objetivo es auditoría confirmatoria, la estabilidad casi nula observada en la tesis obliga a tratar sus salidas como evidencia preliminar, no como base suficiente para afirmar consistencia del comportamiento explicativo.

## SHAP: atribución aditiva basada en valores de Shapley

SHAP (*SHapley Additive exPlanations*) interpreta una predicción como suma de contribuciones atribuibles a las características. Su fundamento proviene del valor de Shapley en teoría de juegos cooperativos, adaptado al problema de distribuir la salida de un modelo entre variables explicativas (Lundberg & Lee, 2017). La salida típica de SHAP es un vector de atribuciones local para una instancia, aunque esas atribuciones pueden agregarse para construir resúmenes globales, comparar subgrupos o analizar tendencias de importancia. Su influencia se debe a que ofrece un marco formal unificado para explicaciones aditivas, con propiedades axiomáticas que facilitan la lectura comparativa de contribuciones.

Esa formalización, sin embargo, no elimina las decisiones operativas. El conjunto de referencia, la forma de simular ausencia de características, la dependencia entre variables y la variante concreta del explicador condicionan el significado de las atribuciones. KernelSHAP conserva una orientación más general y agnóstica, pero puede requerir numerosas consultas al modelo; TreeSHAP aprovecha la estructura de modelos basados en árboles para calcular atribuciones de forma más eficiente. La literatura sobre tractabilidad recuerda que calcular explicaciones SHAP exactas puede ser difícil o inviable para clases amplias de modelos, lo que obliga a registrar cuándo se trabaja con aproximaciones y qué compromisos introducen (Van den Broeck et al., 2022). Por tanto, "usar SHAP" no describe por sí solo una configuración experimental suficiente: deben especificarse variante, modelo base, conjunto de referencia, estrategia de aproximación y coste de cómputo.

El carácter formal de SHAP también puede inducir una lectura excesivamente fuerte si se confunden atribuciones operacionales con causalidad. Los valores SHAP distribuyen una salida del modelo bajo supuestos definidos; no prueban por sí mismos que una característica cause un resultado en el mundo ni que una intervención sobre ella produzca el cambio esperado. En este capítulo, SHAP se trata como una herramienta de atribución técnicamente robusta, pero su evidencia se mantiene dentro del alcance del benchmark. En los resultados extraídos de la tesis, SHAP presenta el perfil global más fuerte: fidelidad media cercana a 0.810, estabilidad media de 0.724, cobertura completa y ventaja pareada sobre LIME en las 75 celdas coincidentes. Su límite principal es el coste: el promedio reportado alcanza 24,804 ms y la diferencia media SHAP-LIME en coste es de +8,047.6 ms, con heterogeneidad por familia de modelo.

Esta frontera calidad-coste es central para la lectura del capítulo. SHAP es especialmente defendible cuando la prioridad es evidencia explicativa de alta calidad, cuando la ejecución puede realizarse fuera de línea o cuando el coste adicional se justifica por necesidades de auditoría. En cambio, si el sistema exige baja latencia, explicación interactiva o repetición masiva sobre muchas instancias, el perfil de SHAP debe evaluarse junto con presupuesto computacional, variante del explicador y familia de modelo. FOM-7 convierte esta tensión en una afirmación acotada: SHAP domina en calidad explicativa bajo las métricas del benchmark, pero no elimina la necesidad de evaluar factibilidad operacional.

## Anchors: reglas locales de alta precisión

Anchors explica una predicción mediante reglas locales tipo si-entonces. La idea central es encontrar condiciones suficientes bajo las cuales el modelo mantiene la misma predicción con alta probabilidad (Ribeiro et al., 2018). A diferencia de LIME o SHAP, Anchors no produce principalmente pesos de características, sino reglas que delimitan una región de decisión. Esta diferencia cambia la pregunta explicativa: ya no se pregunta qué variable aporta más a una predicción, sino qué conjunto de condiciones ancla esa predicción dentro de un espacio local.

La fortaleza de Anchors es comunicativa. Una regla local puede resultar más legible que una lista de atribuciones, especialmente cuando la explicación se comunica a personas que razonan mediante condiciones, excepciones o umbrales. Sin embargo, la precisión de una regla debe interpretarse junto con su cobertura. Una regla extremadamente específica puede alcanzar alta precisión porque aplica a muy pocos casos; una regla más general puede cubrir una región más amplia, pero perder precisión. Esta tensión convierte a Anchors en un método que exige evaluación cuidadosa: precisión, cobertura, complejidad de regla y reproducibilidad deben reportarse de manera conjunta, porque ninguna de esas dimensiones equivale por sí sola a calidad explicativa (Ribeiro et al., 2018; Guidotti et al., 2018).

Anchors también muestra por qué la evaluación debe atender al formato de salida. Una regla tiene cardinalidad, condiciones, umbrales y cobertura; una atribución tiene pesos; un contrafactual tiene distancia, factibilidad y validez. Si el benchmark traduce todos esos objetos a una sola escala, corre el riesgo de medir más la conveniencia de la métrica que la calidad del método. Por ello, FOM-7 debe presentar Anchors como evidencia condicional: útil cuando precisión y cobertura se reportan juntas, pero limitada cuando se compara directamente contra métodos de atribución. En los resultados de la tesis, Anchors alcanza solo 57 de 75 celdas calificadas (76.0%), con faltantes concentrados en combinaciones como `logreg_anchors` y `mlp_anchors`; además, presenta fidelidad media de 0.386, estabilidad de 0.052 y coste alto o variable. Estos resultados no prueban que Anchors sea irrelevante, sino que su objeto explicativo queda parcialmente desalineado con métricas diseñadas para atribuciones continuas.

La lectura correcta es doble. Primero, Anchors aporta una forma de evidencia que puede ser muy útil cuando el usuario necesita condiciones suficientes y comunicables: "si se cumplen estas premisas, la predicción se mantiene". Segundo, esa utilidad exige reportar cobertura, precisión y complejidad de regla junto con cualquier métrica agregada. Una regla estrecha puede parecer excelente si solo se observa precisión, pero su valor práctico cambia si cubre una fracción mínima de casos. FOM-7 conserva esta tensión al impedir que la cobertura incompleta se oculte en promedios globales y al exigir que las afirmaciones sobre reglas se formulen como evidencia condicional, no como superioridad general del método.

## DiCE: contrafactuales diversos y acción correctiva

DiCE (*Diverse Counterfactual Explanations*) genera ejemplos contrafactuales: instancias alternativas que, con cambios mínimos o controlados, producirían una predicción diferente (Mothilal et al., 2020). Su pregunta principal no es qué característica contribuyó más a la predicción actual, sino qué tendría que cambiar para obtener otro resultado. Esta orientación ubica a DiCE en una familia distinta de explicaciones, especialmente relevante para escenarios donde el usuario necesita explorar alternativas de acción, posibilidades de corrección o rutas de *recourse* frente a una decisión automatizada (Wachter et al., 2017; Karimi et al., 2022).

La evaluación de contrafactuales exige criterios adicionales. Un contrafactual debe ser válido respecto al modelo, cercano a la instancia original, diverso respecto a otras alternativas y, en muchos dominios, factible o accionable. La accionabilidad impone restricciones semánticas: no todas las características pueden modificarse, y no todos los cambios matemáticamente cercanos son realistas. Un aumento de edad, una modificación de origen familiar o una combinación incompatible de atributos pueden invertir una etiqueta en el modelo sin constituir una recomendación plausible para una persona. Por ello, una métrica de fidelidad tradicional puede ser insuficiente para evaluar DiCE si no se acompaña de criterios de proximidad, diversidad, plausibilidad y coherencia con el dominio (Mothilal et al., 2020; Karimi et al., 2022).

La tradición contrafactual también advierte que una explicación puede ser injustificada si se apoya en regiones poco plausibles del espacio de datos o si no respeta la estructura local del problema. FACE, por ejemplo, enfatiza contrafactuales factibles y accionables en regiones conectadas por datos observados, mientras que otras críticas señalan los peligros de contrafactuales post-hoc que satisfacen una condición formal pero no una condición práctica de uso (Poyiadzi et al., 2020; Laugel et al., 2019). Para FOM-7, esta tensión exige que DiCE no sea evaluado como si fuera simplemente un método de atribución. En la tesis, DiCE conserva 68 de 75 celdas calificadas (90.7%), presenta fidelidad baja bajo métricas de atribución (0.172), estabilidad intermedia (0.366), parsimonia muy baja como señal de concisión contrafactual (0.017) y coste moderado de 2,056 ms. Esta combinación lo vuelve relevante para discutir la ausencia de un método universalmente dominante: puede ser menos adecuado para auditar importancias locales, pero más alineado con escenarios donde interesa explorar alternativas de acción.

El capítulo debe cuidar especialmente el lenguaje al interpretar DiCE. Un contrafactual válido para el modelo no es automáticamente una recomendación justa, viable o accionable para una persona; para sostener esa afirmación se requerirían restricciones de dominio, conocimiento causal y evaluación contextual que exceden el benchmark. La contribución de DiCE aquí es más precisa: muestra que la explicabilidad también puede formularse como exploración de mundos alternativos, no solo como atribución retrospectiva de pesos. FOM-7 permite incorporar esa familia explicativa sin forzarla a competir en igualdad artificial con métodos cuyo objeto principal es la importancia de características.

## Comparación metodológica y uso dentro de FOM-7

Los cuatro métodos no producen evidencia intercambiable. LIME aproxima localmente una frontera de decisión; SHAP reparte contribuciones entre características; Anchors identifica condiciones suficientes para conservar una predicción; DiCE propone alternativas contrafactuales que cambiarían el resultado. Esta ontología de salidas organiza la lectura del benchmark y evita una conclusión simplista del tipo "un método gana". La pregunta metodológica más precisa es qué método produce qué tipo de evidencia, bajo qué configuración, con qué métrica y para qué objetivo de auditoría o comunicación.

Dentro de FOM-7, la comparación se vuelve admisible solo cuando el capítulo declara el objeto explicativo de cada método, la métrica aplicada y su pertinencia, la unidad experimental que sostiene el resultado, los artefactos y scripts que respaldan la cifra, y los límites que conserva la afirmación. Esta regla permite usar los resultados del benchmark sin sobreafirmar. SHAP puede describirse como fuerte en fidelidad y estabilidad bajo las condiciones evaluadas; LIME como eficiente pero inestable; Anchors como regla local con límites de cobertura; DiCE como método contrafactual cuya calidad no se agota en métricas de atribución. La conclusión metodológica no es que el investigador deba elegir siempre SHAP, descartar LIME, abandonar Anchors o privilegiar DiCE. La conclusión es que cada método ocupa una posición distinta en el espacio calidad-coste, fidelidad-estabilidad y atribución-acción.

Esa lectura por perfiles es la base técnica para la discusión posterior del capítulo y para la tesis central de FOM-7: la explicabilidad defendible no depende de elegir un explicador universal, sino de sostener afirmaciones trazables sobre artefactos específicos. En términos prácticos, el protocolo obliga a convertir frases genéricas en formulaciones auditables. No se dice "SHAP explica mejor", sino "SHAP obtuvo mayor fidelidad y estabilidad que los otros métodos bajo EXP2 Adult Income y las métricas definidas"; no se dice "LIME es malo", sino "LIME fue eficiente y parsimonioso, pero inestable bajo semillas"; no se dice "Anchors falla", sino "Anchors tuvo cobertura incompleta y requiere lectura conjunta de precisión y cobertura"; no se dice "DiCE no sirve por baja fidelidad", sino "DiCE responde a una lógica contrafactual que debe evaluarse con criterios de validez, proximidad, diversidad y factibilidad". Esta disciplina de formulación es el puente entre la comparación de métodos y la gobernanza de evidencia que desarrolla FOM-7.


# La crisis de evaluación en XAI


## Un campo con métodos maduros y evaluación fragmentada

La XAI ha consolidado métodos post-hoc ampliamente utilizados, entre ellos LIME, SHAP, Anchors y DiCE, y dispone además de revisiones, taxonomías y herramientas que muestran una madurez técnica creciente. Sin embargo, esa madurez no se ha traducido de manera automática en una evaluación comparativa, reproducible y estadísticamente defendible. El campo produce explicaciones con relativa facilidad, pero todavía enfrenta dificultades para decidir cuándo esas explicaciones son fieles, estables, comparables, útiles para un propósito concreto o admisibles como evidencia científica. En ese sentido, la crisis de evaluación no consiste en falta de métodos ni en ausencia de métricas; consiste en la distancia entre calcular indicadores y construir evidencia acumulable sobre la calidad de los artefactos explicativos.

Esta brecha aparece en varias capas. Primero, existe proliferación de métricas con nombres similares, definiciones distintas y supuestos operativos no siempre explícitos. Segundo, los estudios emplean criterios variables de inclusión de instancias, configuraciones de explicadores, perturbaciones, semillas, conjuntos de referencia y reglas de agregación. Tercero, no siempre se separa la evidencia exploratoria de la evidencia confirmatoria, lo que puede transformar hallazgos de calibración en afirmaciones generales. Cuarto, falta una disciplina compartida para convertir resultados numéricos en afirmaciones delimitadas por objeto explicativo, métrica, unidad de análisis y alcance. Esta preocupación atraviesa la literatura sobre evaluación rigurosa de interpretabilidad, revisión de métricas XAI, benchmarking funcional y evaluación multidimensional de explicaciones (Doshi-Velez & Kim, 2017; Abdul Kadir et al., 2023; Canha et al., 2025; Pawlicki et al., 2024; Bhattacharya & Verbert, 2024).

El resultado práctico es que muchos estudios son difíciles de comparar entre sí. Dos investigaciones pueden afirmar que evalúan "LIME" o "SHAP" y, aun así, trabajar con vecindarios, semillas, perturbaciones, variantes del explicador, fondos de referencia, modelos base y métricas incompatibles. Bajo esas condiciones, el nombre del método deja de ser una unidad experimental suficiente. La comparación defendible requiere describir el método como una configuración completa y no como una etiqueta. Esta es una de las razones por las que FOM-7 desplaza el foco desde el ranking de explicadores hacia la gobernanza de una cadena de evidencia: artefacto, métrica, prueba, resultado y afirmación deben permanecer conectados.

## La insuficiencia de la fidelidad aislada

La fidelidad ha sido una de las métricas más utilizadas en evaluación XAI porque promete responder una pregunta intuitiva: hasta qué punto la explicación representa el comportamiento observable del modelo. Sin embargo, la fidelidad aislada no basta para caracterizar la calidad explicativa. Una explicación puede ser relativamente fiel y, al mismo tiempo, inestable ante pequeñas perturbaciones, poco parsimoniosa, costosa de producir, difícil de reproducir o inadecuada para el tipo de objeto que genera el método. En un benchmark con métodos heterogéneos, esta limitación se vuelve más visible: la fidelidad de un sustituto local, la precisión de una regla Anchor y la validez de un contrafactual DiCE no son manifestaciones idénticas de un mismo constructo.

Además, la fidelidad depende de su operacionalización. Si se evalúa mediante perturbación, enmascaramiento de características o cambio de salida del modelo, el resultado puede verse afectado por instancias fuera de distribución, dependencias entre variables, supuestos sobre ausencia o presencia de características y decisiones sobre el conjunto de referencia. En ese caso, la métrica mide simultáneamente propiedades del explicador y artefactos del procedimiento de evaluación. Por ello, las discusiones recientes sobre robustez y fidelidad enfatizan que la puntuación no debe interpretarse como verdad causal ni como garantía universal de calidad explicativa (Alvarez-Melis & Jaakkola, 2018; Zheng et al., 2025).

Esta limitación exige un enfoque multi-métrico. En el marco de la tesis, las dimensiones primarias son fidelidad, estabilidad, parsimonia, brecha de fidelidad y coste computacional. Cada una captura una propiedad distinta y ninguna sustituye a las demás. La estabilidad permite observar sensibilidad de la explicación; la parsimonia controla complejidad comunicativa; el coste informa factibilidad operacional; la brecha de fidelidad compara efectos de enmascaramiento; la fidelidad aproxima alineación con la respuesta del modelo. La evaluación defendible requiere leer perfiles de métodos, no coronar un ganador universal a partir de una única escala. Esta lectura coincide con la literatura que advierte que las explicaciones deben evaluarse como artefactos multidimensionales y dependientes del contexto de uso (Nauta et al., 2023; Pawlicki et al., 2024).

## Brecha entre métrica, constructo y afirmación

Una métrica solo es útil si se mantiene conectada con el constructo que pretende medir. La crisis de evaluación aparece cuando una cifra se transforma en una afirmación más fuerte que la evidencia disponible. Una métrica de fidelidad local no demuestra utilidad humana; una métrica de estabilidad no prueba causalidad; una regla precisa no garantiza cobertura amplia; un contrafactual válido para el modelo no implica que la acción sea posible, justa o razonable para una persona. Este problema se agrava porque la forma tabular de los resultados puede dar una apariencia de objetividad mayor que la que realmente permite el diseño.

La brecha de constructo es especialmente visible porque los métodos producen objetos explicativos heterogéneos. LIME genera sustitutos locales; SHAP produce atribuciones; Anchors formula reglas; DiCE genera contrafactuales. Forzar todos esos artefactos a una misma escala puede castigar a un método por no producir el tipo de salida que la métrica espera. Una baja fidelidad de DiCE bajo métricas de atribución, por ejemplo, no prueba que los contrafactuales carezcan de valor; indica que el método responde a una pregunta distinta. Del mismo modo, una regla Anchor con alta precisión pero baja cobertura no puede leerse igual que un vector SHAP estable. Por ello, las revisiones recientes insisten en interpretar la evaluación XAI como un espacio multidimensional de propiedades, fuentes de evidencia y contextos de tarea (Abdul Kadir et al., 2023; Nauta et al., 2023; Bhattacharya & Verbert, 2024).

La consecuencia metodológica es clara: una afirmación comparativa debe declarar qué objeto se evaluó, con qué métrica, bajo qué diseño, con qué unidad de análisis y con qué límite de interpretación. Sin esa información, el resultado puede parecer cuantitativo y, sin embargo, ser débil como evidencia científica. FOM-7 convierte esta advertencia en una regla de reporte: cada afirmación debe conservar trazabilidad hacia un artefacto fuente y debe formularse con el alcance exacto que permite el diseño. No basta con decir que un método "explica mejor"; debe decirse en qué métrica, bajo qué configuración, en qué población experimental y con qué restricciones de generalización.

## Reproducibilidad y trazabilidad insuficientes

La reproducibilidad en XAI no se limita a publicar código. También requiere versionar datos, modelos, semillas, configuraciones de explicadores, parámetros de perturbación, definiciones métricas, reglas de agregación, scripts de análisis y criterios de exclusión. Las explicaciones post-hoc agregan puntos de variación que no siempre aparecen en el entrenamiento del modelo base: vecindarios artificiales, conjuntos de referencia, umbrales de reglas, generadores contrafactuales, estrategias de muestreo y aproximaciones computacionales. Si esos elementos no se registran, dos ejecuciones pueden producir explicaciones diferentes sin que el lector pueda distinguir si la diferencia proviene del modelo, del explicador, de la semilla, de la métrica o del entorno computacional.

Esta fragilidad debilita la auditabilidad de resultados y dificulta la acumulación de evidencia. Una comparación entre explicadores no debería depender de detalles invisibles del pipeline, porque entonces el resultado no es plenamente inspeccionable ni reproducible. La literatura reciente sobre benchmarking funcional y evaluación responsable de explicaciones insiste en que la reproducibilidad debe cubrir el ciclo completo: configuración experimental, artefactos explicativos, métricas calculadas, análisis estadístico y reporte de conclusiones (Hedström et al., 2023; Agarwal et al., 2022; Canha et al., 2025). En ese marco, la trazabilidad no es burocracia documental; es una condición para que una afirmación pueda ser auditada.

La trazabilidad también controla la sobreafirmación. Cada afirmación fuerte debería poder regresar a un artefacto fuente: tabla, figura, configuración, script, prueba estadística o decisión metodológica. Si se afirma que un método es más estable, debe quedar claro en qué conjunto de datos, modelo, métrica, configuración y unidad experimental se observó esa estabilidad. Si se afirma que una diferencia es estadísticamente significativa, debe identificarse la prueba, el diseño de bloques o pares, el ajuste por multiplicidad y la población de celdas admisibles. Esta disciplina es central para el capítulo porque permite conectar la discusión conceptual con los resultados empíricos sin convertir el benchmark en una narración persuasiva no verificable.

## Herramientas sin protocolo de gobernanza suficiente

Herramientas como Quantus y OpenXAI han contribuido a estandarizar y facilitar la evaluación XAI. Quantus organiza familias de métricas y reduce fricción técnica al ofrecer una infraestructura para evaluar explicaciones de manera sistemática; OpenXAI promueve comparabilidad, transparencia y evaluación de explicaciones post-hoc bajo condiciones más controladas (Hedström et al., 2023; Agarwal et al., 2022). Estas contribuciones son importantes porque corrigen parte de la dispersión técnica del campo. Sin embargo, una herramienta no resuelve por sí sola el problema de gobernanza metodológica.

Antes de ejecutar una métrica deben definirse reglas que exceden al software: qué artefactos son admisibles, cómo se congelan configuraciones, qué salidas se excluyen, cómo se armonizan esquemas, qué pruebas estadísticas son válidas, cómo se controla la multiplicidad, cómo se separa calibración de confirmación y qué límites conserva cada afirmación. Una librería puede calcular correctamente una métrica y, aun así, el estudio puede sobreinterpretar el resultado si no distingue entre constructo medido, objeto explicativo y alcance del conjunto de datos. El problema no es solamente de implementación, sino de arquitectura de evidencia.

La contribución necesaria, por tanto, no consiste solo en ampliar el catálogo de métricas. Consiste en integrar métricas, artefactos, reproducibilidad, inferencia y trazabilidad dentro de una secuencia operativa. Ese es el punto en el que la crisis de evaluación conduce al protocolo FOM-7. FOM-7 no compite con Quantus u OpenXAI como herramienta de cálculo; opera en otra capa. Su función es gobernar cuándo un resultado métrico puede considerarse admisible, cuándo una comparación es homogénea, cuándo una prueba estadística es apropiada y cuándo una afirmación conserva el alcance de la evidencia que la sostiene.

## Implicación para el capítulo

El capítulo debe presentar la evaluación XAI como un problema de admisibilidad de evidencia. No basta con generar explicaciones plausibles ni con producir tablas de métricas. Es necesario demostrar que los resultados provienen de artefactos válidos, que las comparaciones son homogéneas, que la variabilidad fue controlada, que la inferencia es apropiada y que las afirmaciones son trazables. Esta posición protege al capítulo contra dos excesos simétricos: el entusiasmo que convierte cualquier explicación en transparencia y el escepticismo que descarta toda evaluación funcional por no medir utilidad humana directa.

La transición hacia FOM-7 nace precisamente de esta tensión. Si la XAI ya dispone de métodos maduros, métricas abundantes y toolkits funcionales, el problema pendiente es ordenar la cadena que transforma ejecuciones experimentales en evidencia defendible. FOM-7 responde a esa necesidad mediante siete puertas secuenciales: congelar el protocolo, ejecutar bajo condiciones controladas, auditar artefactos, armonizar métricas, aplicar inferencia admisible, perfilar reproducibilidad y reportar afirmaciones trazables. La crisis de evaluación, entonces, no es solo un diagnóstico del campo; es la justificación metodológica del protocolo que estructura el resto del capítulo.


# Protocolo FOM-7 para benchmarking auditable


## Función metodológica

FOM-7 (*Framework Operation Method*, siete puertas) se define como una secuencia operativa para convertir ejecuciones de benchmarking XAI en evidencia reproducible, comparable y trazable. Su propósito no es introducir un nuevo explicador ni una métrica aislada, sino gobernar el ciclo completo que conecta diseño experimental, ejecución controlada, calificación de artefactos, armonización analítica, inferencia estadística, perfilado de reproducibilidad y reporte de afirmaciones. En términos metodológicos, FOM-7 ocupa la capa que suele quedar implícita entre dos momentos del trabajo empírico: por un lado, la producción de explicaciones y métricas; por otro, la formulación de conclusiones sobre fidelidad, estabilidad, coste o utilidad técnica de un método.

El protocolo responde directamente a la crisis de evaluación descrita en la sección anterior. La existencia de métodos, métricas y herramientas no garantiza por sí misma que los resultados sean admisibles como evidencia científica. Una librería puede calcular métricas correctamente y, aun así, el estudio puede sobreinterpretar sus resultados si no declara qué artefactos son válidos, qué configuraciones fueron congeladas, qué comparaciones son homogéneas, qué pruebas estadísticas son admisibles y qué límites conserva cada afirmación. Esta distinción se alinea con la literatura que separa evaluación funcional, evaluación con humanos y evaluación en aplicación: FOM-7 se ubica principalmente en el dominio *functionally-grounded*, por lo que produce evidencia computacional trazable, no evidencia directa de comprensión humana ni verdad causal de las explicaciones (Doshi-Velez & Kim, 2017; Hedström et al., 2023; Nauta et al., 2023).

FOM-7 opera como puente entre el diagnóstico y la práctica experimental. La fragmentación métrica se traduce en reglas de armonización; la fragilidad de artefactos se traduce en auditoría de integridad; la irreproducibilidad se traduce en semillas declarativas y perfilado de variación; la sobreafirmación se traduce en trazabilidad de *claims*. Por ello, el protocolo no debe leerse como una lista administrativa, sino como una arquitectura de admisibilidad. Cada puerta responde a un modo de fallo observado en benchmarking XAI y establece qué condiciones deben cumplirse antes de que un resultado pueda sostener inferencia confirmativa. La Tabla 3 resume las siete puertas, sus artefactos de entrada y salida, y el tipo de fallo metodológico que cada una busca controlar.

## Regla secuencial de admisibilidad

Las siete puertas de FOM-7 son secuenciales. Cada puerta debe satisfacerse antes de proceder a la siguiente. Si una puerta falla, los resultados afectados no desaparecen necesariamente, pero se degradan a estatus descriptivo y no pueden sostener afirmaciones inferenciales. Esta regla es importante porque separa dos funciones que con frecuencia se mezclan en estudios de XAI: explorar un fenómeno y demostrar una comparación. Un artefacto incompleto puede ser útil para diagnóstico del pipeline; una celda faltante puede informar sobre viabilidad de un método; una métrica calculada sobre una cohorte parcial puede sugerir una hipótesis. Sin embargo, ninguno de esos elementos debe convertirse en afirmación confirmativa si no atraviesa los controles previos.

La regla central puede formularse así: ninguna afirmación inferencial puede formularse si las puertas previas no están satisfechas y si la afirmación no puede trazarse a artefactos fuente verificables. Esta formulación protege el capítulo contra tres riesgos recurrentes. El primero es la deriva de protocolo: cambios post-hoc en configuraciones, hipótesis, criterios de inclusión, métricas o pruebas estadísticas. El segundo es la contaminación de artefactos: uso de salidas vacías, malformadas, incompletas o no comparables. El tercero es la sobreafirmación: conversión de resultados numéricos en conclusiones generales sin declarar alcance, unidad de análisis o límites.

En la tesis, esta regla también evita la pseudorreplicación. Las métricas pueden computarse por instancia, pero la unidad de análisis inferencial debe respetar la estructura del diseño, especialmente cuando se comparan métodos sobre modelos, semillas y tamaños de muestra. FOM-7 obliga a distinguir entre métricas de instancia, resúmenes de ejecución, bloques comparables y pruebas inferenciales. Así, una diferencia numérica solo se vuelve evidencia comparativa cuando procede de artefactos calificados, unidades homogéneas y una prueba compatible con el diseño. Esta disciplina convierte al protocolo en una defensa contra la apariencia de precisión que producen las tablas cuando el camino desde dato crudo hasta afirmación no está regulado.

## Flujo operativo

El flujo compacto del protocolo es:

```text
Congelación -> Ejecución -> Auditoría -> Armonización -> Exportación -> Perfilado -> Reporte
```

La secuencia resume una lógica de control acumulativo. La congelación impide que el diseño se adapte a los resultados; la ejecución controlada evita corridas ad-hoc; la auditoría filtra artefactos inválidos; la armonización transforma salidas heterogéneas en tablas comparables; la exportación inferencial fija los insumos estadísticos; el perfilado estima variación residual; y el reporte vincula cada afirmación con evidencia identificable. El valor de la secuencia está en que ninguna puerta compensa por completo la ausencia de otra. Una prueba estadística correcta no repara artefactos malformados; una tabla armonizada no corrige una configuración modificada post-hoc; una afirmación elegante no sustituye trazabilidad.

## Puertas del protocolo

### Puerta 1: Congelación del protocolo

La primera puerta bloquea versiones de código, archivos de configuración YAML, factores del diseño, métodos, métricas y plan inferencial antes de iniciar cualquier ejecución confirmativa. En la tesis, esta puerta se formaliza mediante `configs/experiments/exp2_scaled/manifest.yaml` y código versionado. Su función principal es impedir que decisiones analíticas se ajusten retrospectivamente al resultado observado. En un benchmark con múltiples métodos, semillas, modelos y tamaños de muestra, pequeñas modificaciones en parámetros de explicador, umbrales de inclusión o reglas de agregación pueden cambiar la interpretación de la evidencia. Por ello, la congelación transforma el diseño en un compromiso previo y auditable.

Esta puerta no elimina la exploración; la ubica en su lugar adecuado. La tesis distingue entre EXP1, orientado a calibración y reproducibilidad, y EXP2, orientado a inferencia confirmativa. La separación evita que aprendizajes obtenidos durante la calibración contaminen las afirmaciones confirmativas. Esta lógica es consistente con recomendaciones recientes sobre benchmarking funcional y evaluación responsable de explicaciones, que enfatizan la necesidad de declarar configuraciones, semillas y condiciones de comparación antes de extraer conclusiones (Agarwal et al., 2022; Canha et al., 2025; Zheng et al., 2025).

### Puerta 2: Ejecución por lotes controlada

La segunda puerta ejecuta las celdas experimentales desde manifiestos declarativos, con semillas fijas y registro del contexto de ejecución. Su regla central es impedir modificaciones ad-hoc de configuración durante la corrida confirmativa. La ejecución por lotes no es solo una conveniencia técnica: es una forma de garantizar que cada combinación de modelo, método, semilla y tamaño de muestra se produzca bajo el mismo régimen de control. Cuando las explicaciones post-hoc dependen de perturbaciones, vecindarios artificiales, conjuntos de referencia o generadores estocásticos, registrar la semilla y la configuración se vuelve parte de la evidencia.

En FOM-7, la ejecución controlada también delimita responsabilidades. Si una celda falla, el fallo queda asociado a una configuración y a un artefacto identificable, no a una intervención manual invisible. Esta trazabilidad permite distinguir entre errores de implementación, limitaciones del método, problemas de coste, incompatibilidades de esquema o ausencia de resultados. De ese modo, el protocolo no oculta las fallas; las convierte en información auditable sobre la viabilidad operativa del benchmark.

### Puerta 3: Auditoría de integridad de artefactos

La tercera puerta inspecciona de forma determinista cada `results.json` para detectar archivos vacíos, esquemas incompatibles o valores numéricos inválidos. Los artefactos excluidos no deben reemplazarse mediante reconstrucciones sintéticas no documentadas. En EXP2, esta puerta explica la exclusión de celdas faltantes o no calificadas antes de las pruebas confirmativas. Su función es proteger la inferencia de datos aparentemente disponibles pero metodológicamente inadmisibles.

La auditoría de integridad es especialmente importante en XAI porque los métodos evaluados no siempre fallan de manera homogénea. Un método puede completar todas sus celdas, otro puede fallar en ciertos modelos, y otro puede producir salidas válidas pero difíciles de comparar con atribuciones continuas. Si esas diferencias se ignoran, el análisis puede mezclar evidencia válida, evidencia incompleta y artefactos no comparables. La puerta 3 obliga a registrar qué celdas entran al análisis y cuáles quedan fuera. En el capítulo, esta lógica explica por qué la cobertura de SHAP y LIME, Anchors y DiCE debe reportarse como parte de los resultados, no como detalle técnico secundario.

### Puerta 4: Armonización a tablas listas para el análisis

La cuarta puerta convierte artefactos heterogéneos en tablas comparables mediante estandarización de claves, campos de métricas y niveles de agregación. Su finalidad es evitar mezclas de esquema, doble conteo o comparaciones entre unidades analíticas incompatibles. En un benchmark que integra LIME, SHAP, Anchors y DiCE, esta puerta es indispensable porque los métodos producen objetos distintos: pesos locales, atribuciones aditivas, reglas y contrafactuales. La armonización no debe borrar esa diferencia; debe construir una tabla común sin fingir que los objetos son idénticos.

Esta puerta también fija el nivel en que la evidencia será leída. Las métricas pueden existir a nivel de instancia, ejecución, método, bloque o resumen global, pero no todas esas unidades son válidas para todas las inferencias. Una comparación confirmativa debe evitar contar múltiples instancias como réplicas independientes cuando pertenecen a una misma combinación experimental. Por ello, FOM-7 convierte la armonización en una operación metodológica, no solo en una transformación de formato. La tabla lista para análisis debe preservar método, modelo, semilla, tamaño de muestra, métrica, unidad de agregación y estado de calificación.

### Puerta 5: Exportación inferencial

La quinta puerta genera de forma determinista las tablas de pruebas omnibus y pareadas exclusivamente desde entradas calificadas. En la tesis, la superposición de recuperación para `mlp_shap`/`svm_shap` mediante `outputs/batch_results.csv` se trata como una excepción documentada, no como una reconstrucción arbitraria. Esta precisión importa porque la inferencia estadística solo es defendible si sus insumos son reproducibles y si las excepciones están registradas antes de interpretar el resultado.

La exportación inferencial controla tres fallos: cálculos manuales no reproducibles, doble conteo de celdas y uso de artefactos no calificados. También obliga a alinear la prueba con el diseño. Las pruebas de Friedman y Nemenyi requieren bloques completos y comparables; las pruebas pareadas como Wilcoxon requieren celdas emparejadas; los ajustes por multiplicidad deben aplicarse cuando se realizan comparaciones múltiples. FOM-7 no decide por sí mismo qué prueba es universalmente correcta; exige que la prueba seleccionada sea compatible con la unidad de análisis, la estructura de dependencia y la pregunta inferencial.

### Puerta 6: Perfilado de reproducibilidad

La sexta puerta cuantifica la dispersión entre ejecuciones y el coeficiente de variación en configuraciones replicadas. Esta puerta fundamenta la proposición P1 y permite distinguir variabilidad atribuible al método, al protocolo, a semillas o a condiciones computacionales. Su función es crucial porque un método puede exhibir buen promedio y, aun así, ser demasiado variable para sostener una afirmación robusta. En XAI, la reproducibilidad debe abarcar no solo el modelo predictivo, sino también las explicaciones, las métricas y las conclusiones derivadas de ellas.

En el diseño de la tesis, EXP1 cumple una función específica de calibración y perfilado de dispersión. No alimenta las hipótesis confirmativas H1-H3 de EXP2, pero sí informa el rango de variación esperada bajo semillas y permite interpretar la estabilidad del pipeline. Esta separación conserva la integridad inferencial: las réplicas de calibración ayudan a entender la reproducibilidad, mientras que el benchmark primario sostiene las comparaciones confirmativas. La puerta 6, por tanto, no es un apéndice posterior; es el mecanismo que impide confundir variación de semilla con efecto real del método.

### Puerta 7: Reporte con trazabilidad de afirmaciones

La séptima puerta permite emitir afirmaciones inferenciales solo cuando todas las puertas previas están satisfechas y la afirmación se vincula con evidencia identificable: resultados, tablas, scripts, configuraciones y límites de interpretación. Las afirmaciones no trazables deben presentarse como descriptivas. Esta puerta es la culminación del protocolo porque transforma el control técnico previo en lenguaje científico disciplinado. El objetivo no es producir resultados más vistosos, sino formular conclusiones que puedan ser auditadas.

La trazabilidad exige que cada afirmación conserve sus condiciones de validez. Si se afirma que SHAP presenta mayor fidelidad y estabilidad, la frase debe conservar el contexto EXP2, el conjunto Adult Income, las métricas definidas, las celdas calificadas, las pruebas aplicadas y el alcance tabular del benchmark. Si se afirma que LIME es eficiente pero inestable, debe indicarse que esa lectura procede de coste, parsimonia y estabilidad bajo semillas. Si se discuten Anchors o DiCE, debe preservarse que sus objetos explicativos son reglas y contrafactuales, no simplemente atribuciones numéricas. Así, la puerta 7 convierte el reporte en una práctica de gobernanza de evidencia.

## Relación con el capítulo

Dentro de este capítulo, FOM-7 debe presentarse como protocolo de gobernanza metodológica para evaluación de XAI. Su valor no reside en declarar que un método domina universalmente, sino en hacer defendible el paso desde explicaciones post-hoc y métricas computadas hacia afirmaciones científicas delimitadas. La formulación recomendada para los resultados no es "este explicador es mejor", sino "este explicador exhibe mayor fidelidad, estabilidad o eficiencia bajo estas condiciones, con esta métrica, esta unidad de análisis y esta evidencia fuente".

La función de FOM-7 dentro del argumento general es doble. Primero, responde a la crisis de evaluación mostrando cómo una cadena de controles puede reducir fragmentación, irreproducibilidad y sobreafirmación. Segundo, prepara la lectura de los resultados empíricos: las diferencias entre SHAP, LIME, Anchors y DiCE no se presentarán como jerarquía universal, sino como perfiles admisibles bajo un diseño concreto. Este puente es lo que permite que el capítulo avance desde fundamentos y crisis hacia diseño experimental y resultados sin perder disciplina inferencial.

## Límites explícitos

FOM-7 no demuestra utilidad humana directa, verdad causal de las explicaciones ni superioridad universal de un método. Su alcance es funcionalmente fundamentado (*functionally-grounded*): produce evidencia comparativa, reproducible y trazable sobre métodos post-hoc bajo condiciones experimentales controladas. Las dimensiones centradas en humanos (*human-grounded*) o centradas en aplicación (*application-grounded*) requerirían protocolos adicionales con usuarios, tareas, escalas e instrumentos propios.

Estos límites no debilitan el protocolo; delimitan su contribución. FOM-7 no sustituye estudios con usuarios, análisis causal, auditorías regulatorias completas ni evaluación de impacto en despliegue. Lo que aporta es una condición previa: antes de preguntar si una explicación ayuda a una persona o mejora una decisión real, debe saberse si el artefacto explicativo es reproducible, comparable, métricamente interpretable y trazable. En esa medida, FOM-7 funciona como infraestructura metodológica para futuras extensiones human-centered o application-grounded, pero no reclama haberlas realizado.


# Diseño empírico del benchmark


## Enfoque general

El diseño empírico operacionaliza la evaluación de métodos XAI agnósticos al modelo como un benchmark cuantitativo, reproducible y multi-métrico. Su finalidad es comparar LIME, SHAP, Anchors y DiCE bajo condiciones controladas, evitando que las diferencias observadas se confundan con variaciones no documentadas de modelo, semilla, muestra, configuración o artefacto. En lugar de tratar las explicaciones como productos aislados, el diseño las inserta en una cadena experimental completa: modelos predictivos congelados, explicadores configurados, artefactos auditados, métricas operacionalizadas y pruebas estadísticas aplicadas sobre unidades de análisis explícitas.

El estudio se ubica en una lógica funcionalmente fundamentada (*functionally-grounded*): las métricas utilizadas son proxies computacionales de calidad explicativa y no evidencia directa de utilidad humana, plausibilidad semántica o causalidad. Esta delimitación es central para sostener afirmaciones prudentes y auditables. En la taxonomía de Doshi-Velez y Kim (2017), el capítulo no evalúa si una explicación mejora decisiones humanas en una tarea real; evalúa si un conjunto de métodos produce artefactos comparables bajo métricas reproducibles. Esa elección permite control experimental, pero exige que cada conclusión conserve su alcance: datos tabulares, UCI Adult Income, configuraciones declaradas y explicadores post-hoc.

El diseño traduce la discusión conceptual de las secciones anteriores en decisiones operativas. La crisis de evaluación se responde mediante separación de cohortes, congelamiento de modelos, muestreo estratificado, métricas primarias, auditoría FOM-7 y pruebas no paramétricas. La unidad central de la sección no es una cifra de resultado, sino la arquitectura que hace admisible esa cifra. Por ello, las decisiones de partición, preprocesamiento, muestreo, ejecución y análisis se presentan como controles metodológicos y no como detalles secundarios de implementación.

## Fases experimentales

El diseño distingue dos cohortes de evidencia con funciones diferenciadas. La primera, EXP1, funciona como fase de calibración y reproducibilidad. Su propósito es verificar la implementación del pipeline, entrenar y congelar los artefactos de modelo compartidos por todos los explicadores en EXP2, y estimar la dispersión métrica bajo variación de semilla. EXP1 opera como una fase de control: permite observar si las métricas principales son suficientemente estables y si los modelos cumplen umbrales mínimos de desempeño, pero no sostiene las afirmaciones confirmativas principales.

La segunda cohorte, EXP2, constituye el benchmark primario. En esta fase se ejecuta el diseño factorial completo y se producen los artefactos que alimentan las pruebas estadísticas, los perfiles por método y las afirmaciones empíricas del capítulo. La separación entre EXP1 y EXP2 reduce la contaminación entre decisiones exploratorias y evidencia confirmatoria. Esta separación es importante porque, en evaluación XAI, los ajustes de configuración después de observar resultados pueden cambiar tanto las métricas como la interpretación de los métodos. FOM-7 convierte esta separación en una regla de admisibilidad: la calibración informa el diseño, pero la inferencia se formula sobre la cohorte confirmativa.

La función de EXP1 también es reproducible. En la tesis, esta fase establece que las métricas de calidad presentan coeficientes de variación inferiores al 9% bajo variación de semilla, mientras que el coste computacional exhibe mayor variabilidad, especialmente en configuraciones con KernelSHAP. Esta diferencia anticipa una tensión que recorre todo el capítulo: la calidad explicativa puede ser más estable que la latencia, y por tanto el coste debe reportarse como dimensión propia del perfil de método, no como simple dato de ingeniería.

## Conjunto de datos y modelos predictivos

El benchmark utiliza el conjunto UCI Adult Income, un problema tabular de clasificación binaria ampliamente utilizado en aprendizaje automático y evaluación XAI por su estructura heterogénea, su variable objetivo clara y la existencia de comparaciones externas. El conjunto contiene variables numéricas y categóricas asociadas con características demográficas, laborales y educativas, y la tarea consiste en predecir si el ingreso anual supera un umbral de 50,000 dólares (Kohavi & Becker, 1996). Su uso es pertinente para este capítulo porque permite evaluar explicadores post-hoc sobre un escenario tabular con transformaciones de preprocesamiento, variables correlacionadas y clases desbalanceadas de forma moderada.

El pipeline de preprocesamiento se aplica de forma determinista: partición estratificada, normalización de valores faltantes, codificación de variables categóricas, escalado de variables numéricas y persistencia del preprocesador ajustado. Las transformaciones se ajustan exclusivamente sobre el conjunto de entrenamiento para evitar fuga de datos. Este control es esencial porque los explicadores operan sobre el espacio transformado que consumen los modelos; si el preprocesamiento variara entre métodos, una diferencia atribuida al explicador podría provenir de diferencias de representación. Por ello, el preprocesador se trata como artefacto compartido y congelado.

Se consideran cinco familias de modelos: regresión logística (`logreg`), bosque aleatorio (`rf`), XGBoost (`xgb`), máquina de vectores soporte (`svm`) y perceptrón multicapa (`mlp`). Esta selección permite observar explicadores sobre fronteras de decisión lineales, basadas en árboles, con kernel y neuronales. La inclusión de bosque aleatorio sigue la tradición de modelos de ensamblado introducida por Breiman (2001), mientras que XGBoost y los modelos no lineales amplían la diversidad de mecanismos predictivos. El objetivo no es evaluar qué modelo predictivo es superior, sino someter los explicadores a familias de decisión con estructuras distintas y verificar si los perfiles XAI se mantienen bajo esa heterogeneidad.

## Diseño factorial EXP2

El benchmark primario adopta un diseño cruzado:

```text
modelo x método XAI x semilla x tamaño de muestra
```

Formalmente, el diseño planificado corresponde a:

```text
5 modelos x 4 métodos x 5 semillas x 3 tamaños de muestra = 300 celdas
```

Los factores son: modelos (`logreg`, `rf`, `xgb`, `svm`, `mlp`), métodos (`shap`, `lime`, `anchors`, `dice`), semillas (42, 123, 456, 789, 999) y tamaños de muestra por estrato (50, 100 y 200). Cada celda produce un artefacto independiente de resultados. La variación de semilla permite analizar reproducibilidad, mientras que la variación de tamaño de muestra permite examinar la estabilidad de patrones bajo distintos volúmenes de evidencia local. Esta estructura cruzada evita que una comparación entre explicadores dependa de un único modelo, una única semilla o una única escala de muestra.

El diseño planificado produce 300 celdas, pero el análisis confirmativo utiliza 275 celdas calificadas tras la auditoría FOM-7. Esta distinción entre diseño planificado y cobertura analítica es deliberada. Los artefactos faltantes o no armonizables no se reemplazan de forma sintética ni se ocultan en promedios globales; se registran como parte de la evidencia. SHAP y LIME alcanzan cobertura completa, DiCE conserva 68 de 75 celdas y Anchors 57 de 75, con impacto interpretativo específico para reglas y contrafactuales. La Figura 1 presenta esta cobertura analítica por modelo y método.

## Muestreo de instancias

Las instancias se seleccionan mediante muestreo estratificado por cuadrante de error: verdaderos positivos, verdaderos negativos, falsos positivos y falsos negativos. Esta estrategia evita evaluar los explicadores únicamente sobre aciertos del modelo y obliga a observar su comportamiento en regiones de decisión correctas e incorrectas. En un benchmark de explicabilidad, esta decisión es importante porque una explicación puede parecer razonable cuando el modelo acierta y resultar más difícil de interpretar cuando el modelo falla. Incluir falsos positivos y falsos negativos aproxima el diseño a escenarios de auditoría, donde los errores del modelo suelen ser tan relevantes como sus aciertos.

El tamaño nominal de una ejecución depende del número de instancias por cuadrante, aunque la disponibilidad real puede variar por modelo y estrato. En la tesis, el rango observado va de 27 a 800 instancias por ejecución, con mediana de 400. Esta variación no invalida el diseño porque la inferencia se realiza sobre agregados controlados, no sobre instancias tratadas como réplicas independientes. Además, la estratificación por cuadrante de error permite que cada explicador sea examinado en condiciones de decisión más ricas que una muestra aleatoria simple del conjunto de prueba.

![Figura 1. Cobertura analítica EXP2 por modelo y método. Fuente: figura derivada de `thesis/assets/figures/fig_cobertura_exp2_es.png`.](../../figures/exported/fig_cobertura_exp2_es.png)

## Configuración de explicadores

SHAP se ejecuta con variantes acordes al modelo base: `TreeExplainer` para modelos de árboles y `KernelExplainer` para modelos donde se requiere aproximación más general. LIME utiliza `LimeTabularExplainer` con parámetros congelados de muestreo, número de características y ancho de kernel. Anchors emplea reglas locales con umbral de precisión efectivo de 0.95. DiCE genera contrafactuales orientados a la clase opuesta, usando diferencias entre instancia original y contrafactual como base de importancia. Estas configuraciones deben interpretarse como parte del protocolo experimental. No se evalúan nombres abstractos de métodos, sino implementaciones concretas con parámetros específicos, artefactos registrados y límites conocidos.

La decisión de registrar configuraciones efectivas es crucial porque el nombre de un explicador no determina por sí solo la evidencia que produce. KernelSHAP y TreeSHAP difieren en coste y supuestos; LIME depende de perturbaciones y vecindario; Anchors depende de condiciones de búsqueda y umbral; DiCE depende de restricciones contrafactuales y del modo de generación. Por ello, el diseño empírico no compara etiquetas, sino ejecuciones protocolizadas. Cualquier conclusión posterior debe conservar esta configuración como parte de su alcance.

## Métricas primarias

El benchmark utiliza cinco métricas primarias, resumidas en la Tabla 1: fidelidad, estabilidad, parsimonia, brecha de fidelidad y coste computacional. La fidelidad mide la alineación entre importancias y efecto predictivo observado; la estabilidad mide similitud entre explicaciones bajo perturbaciones controladas; la parsimonia aproxima concisión mediante proporción de características activas; la brecha de fidelidad estima el cambio en la salida del modelo al enmascarar características principales; y el coste registra tiempo de ejecución por instancia explicada.

Estas métricas se computan por instancia y se agregan a nivel de ejecución mediante media aritmética. La unidad inferencial no es la instancia aislada, sino la ejecución agregada y, para las pruebas globales, el bloque experimental. Esta jerarquía evita pseudorreplicación y mantiene coherencia entre el nivel donde se calcula una métrica y el nivel donde se sostiene una afirmación. Además, cada métrica conserva dirección e interpretación propias: fidelidad, estabilidad y brecha buscan valores mayores; parsimonia y coste se leen en sentido inverso. Una lectura multi-métrica evita confundir calidad explicativa con una única escala.

## Unidades de análisis

El análisis adopta una jerarquía explícita. A nivel de instancia se calculan métricas individuales. A nivel de ejecución se obtiene el promedio para una combinación de modelo, método, semilla y tamaño. A nivel de bloque, las pruebas Friedman consideran pares modelo-tamaño $(g,n)$, generando 15 bloques completos. Esta jerarquía es el control principal contra la pseudorreplicación: muchas instancias explicadas dentro de una misma celda no equivalen a muchas réplicas independientes del método.

Para el contraste SHAP-LIME, la unidad primaria es la celda pareada $(g,s,n)$. Esto permite comparar ambos métodos en 75 coordenadas experimentales coincidentes, reduciendo la confusión por modelo, semilla o tamaño de muestra. La comparación pareada es más estricta que una comparación de promedios independientes porque exige que ambos métodos existan en la misma coordenada experimental. En este caso, la cobertura completa de SHAP y LIME permite sostener una inferencia más limpia sobre la frontera calidad-coste entre ambos métodos.

## Control FOM-7

El diseño se gobierna mediante FOM-7, resumido en la Tabla 3. Las puertas controlan congelación del protocolo, ejecución declarativa, auditoría de artefactos, armonización de tablas, exportación inferencial, perfilado de reproducibilidad y trazabilidad de afirmaciones. Esta estructura es necesaria porque el benchmark no solo produce resultados; produce resultados que deben ser admisibles como evidencia. Una celda con artefacto vacío, esquema incompatible o valores inválidos no puede alimentar pruebas confirmativas. Una afirmación sin trazabilidad a tabla, script, configuración o límite de alcance no debe presentarse como inferencial.

En la práctica, FOM-7 conecta el diseño con los resultados. La puerta 3 explica por qué las 25 celdas no calificadas se excluyen de ciertas pruebas; la puerta 4 permite transformar artefactos heterogéneos en tablas comparables; la puerta 5 genera tablas de Friedman, Nemenyi y Wilcoxon desde entradas calificadas; la puerta 6 sostiene la lectura de reproducibilidad; y la puerta 7 obliga a que cada afirmación pueda regresar a un artefacto fuente. Este control evita que el capítulo dependa de una confianza informal en el pipeline y convierte la auditabilidad en parte del método.

## Plan inferencial

Las diferencias globales entre métodos se evalúan mediante pruebas de Friedman y comparaciones post-hoc de Nemenyi sobre bloques completos. Esta elección es apropiada para comparar varios tratamientos sobre bloques relacionados y se apoya en la tradición de pruebas no paramétricas para comparación de clasificadores y métodos sobre diseños repetidos (Friedman, 1937; Demšar, 2006). Cuando Friedman rechaza la hipótesis nula, Nemenyi permite localizar diferencias de rangos entre métodos sin asumir normalidad fuerte de las métricas (Nemenyi, 1963).

El análisis pareado SHAP-LIME utiliza pruebas bilaterales de Wilcoxon sobre celdas coincidentes, con corrección de multiplicidad Holm-Bonferroni y reporte de tamaños de efecto. Wilcoxon es adecuado para contrastar diferencias pareadas cuando no se desea asumir normalidad de las diferencias (Wilcoxon, 1945), mientras que el tamaño de efecto permite evaluar magnitud práctica y no solo significación estadística (Lakens, 2013). La reproducibilidad se examina mediante coeficientes de variación en configuraciones replicadas, especialmente para distinguir señales estables de variación inducida por semilla.

El objetivo del plan inferencial no es producir un ranking universal de explicadores, sino determinar qué diferencias son defendibles bajo el diseño, con qué tamaño de efecto, sobre qué unidad de análisis y dentro de qué alcance empírico. Por ello, los resultados posteriores deben leerse como afirmaciones condicionadas: diferencias entre métodos sobre Adult Income, con cinco familias de modelos, cinco semillas, tres tamaños de muestra, métricas definidas y artefactos calificados por FOM-7.


# Aplicación empírica: perfiles explicativos bajo FOM-7


## De resultados estadísticos a evidencia de capítulo

En un artículo empírico, esta sección podría presentarse como un bloque de resultados separado de la discusión. En este capítulo, su función es distinta: mostrar cómo FOM-7 transforma salidas de benchmarking en perfiles explicativos interpretables, trazables y metodológicamente delimitados. Por ello, las cifras se presentan junto con su lectura sustantiva. La pregunta no es solo qué método obtuvo el mejor valor en una métrica, sino qué enseña cada patrón sobre la evaluación auditable de explicaciones post-hoc.

Los resultados proceden del benchmark EXP2 sobre UCI Adult Income. El diseño planificado comprendía 300 celdas, resultantes de cinco modelos, cuatro métodos XAI, cinco semillas y tres tamaños de muestra. Tras la auditoría de artefactos de FOM-7, se obtuvieron 275 celdas calificadas. Las celdas no calificadas fueron excluidas antes de la inferencia confirmativa. Esta primera cifra ya es una conclusión metodológica: un benchmark auditable no empieza con la prueba estadística, sino con la calificación de qué evidencia puede entrar a la prueba.

La cobertura fue completa para SHAP y LIME, con 75 de 75 celdas cada uno. DiCE alcanzó 68 de 75 celdas y Anchors 57 de 75. Esta diferencia de cobertura no debe ocultarse ni tratarse como un pie de página técnico: forma parte de la evidencia sobre viabilidad operativa de los métodos y condiciona la precisión de las conclusiones para reglas y contrafactuales. La Figura 1 documenta visualmente la cobertura analítica de EXP2 y debe leerse junto con la auditoría de artefactos de FOM-7.

## Evidencia global: diferencias reales, no ranking universal

El análisis global muestra diferencias estadísticamente significativas entre métodos en fidelidad y estabilidad. Para fidelidad, la prueba de Friedman produjo $\chi^2_F = 42.12$ sobre 15 bloques completos, con $p_{\mathrm{Holm}} = 1.51 \times 10^{-8}$ y $W = 0.936$. Este resultado rechaza la hipótesis nula de igualdad global entre métodos y muestra un patrón consistente: SHAP ocupa la primera posición de rango, seguido por LIME, Anchors y DiCE. La lectura inmediata es que, bajo esta operacionalización de fidelidad, las atribuciones SHAP se alinean mejor con los cambios observados en la salida del modelo.

Para estabilidad, la prueba de Friedman produjo $\chi^2_F = 40.68$, con $p_{\mathrm{Holm}} = 2.29 \times 10^{-8}$ y $W = 0.904$. El patrón no replica simplemente el orden de fidelidad: SHAP mantiene el perfil más fuerte, pero DiCE aparece como método relativamente estable en comparación con LIME y Anchors. Esta diferencia confirma que fidelidad y estabilidad no son constructos equivalentes. Una evaluación centrada en una única métrica habría perdido parte del fenómeno: los métodos no se distinguen solo por cuánto se alinean con el comportamiento local del modelo, sino también por cuánto varían sus explicaciones bajo perturbaciones y por qué tipo de objeto explicativo producen.

La implicación para un capítulo de libro es conceptual. El resultado estadístico no debe convertirse en la frase "SHAP gana". Debe convertirse en una lección sobre evaluación: cuando los métodos producen artefactos heterogéneos, las diferencias globales son útiles solo si se interpretan como perfiles condicionados por métrica, objeto explicativo y alcance experimental.

![Figura 2. Diagrama de diferencia crítica de Nemenyi para fidelidad y estabilidad. Fuente: figura derivada de `thesis/assets/figures/fig_cd_diagram_es.png`.](../../figures/exported/fig_cd_diagram_es.png)

![Figura 3. Distribución de fidelidad y estabilidad por método. Fuente: figura derivada de `thesis/assets/figures/fig_boxplots_metricas_es.png`.](../../figures/exported/fig_boxplots_metricas_es.png)

## SHAP y LIME: frontera calidad-coste

El contraste pareado SHAP-LIME se realizó sobre 75 celdas coincidentes $(g,s,n)$. Esta comparación es especialmente informativa porque ambos métodos alcanzaron cobertura completa y se evaluaron en las mismas coordenadas experimentales. Los resultados muestran una ventaja sistemática de SHAP en métricas de calidad explicativa, acompañada de una penalización de coste en la mayoría de contextos.

En fidelidad, SHAP supera a LIME en las 75 celdas, con diferencia media de +0.2479 y tamaño de efecto $d_z = +4.820$. En estabilidad, la ventaja también aparece en las 75 celdas, con diferencia media de +0.7176 y $d_z = +3.002$. Estos tamaños de efecto son muy grandes y respaldan la afirmación de que SHAP ofrece un perfil más fuerte cuando el objetivo principal es fidelidad y consistencia explicativa. En términos de auditoría técnica, esta regularidad importa más que una diferencia puntual de promedio: muestra que la ventaja aparece de forma sistemática a través de modelos, semillas y tamaños de muestra.

La parsimonia muestra el patrón inverso: SHAP es más denso y LIME más conciso. En coste, SHAP es en promedio más costoso, con diferencia media de +8047.6 ms, aunque el efecto es heterogéneo por modelo. Esto define la frontera calidad-coste: SHAP aporta mayor calidad explicativa bajo las métricas evaluadas, mientras LIME conserva atractivo operativo cuando la latencia y la concisión son prioritarias. La consecuencia no es descartar LIME, sino delimitar su uso. LIME puede ser adecuado para exploración rápida o interfaces de baja latencia, pero su estabilidad casi nula bajo las condiciones evaluadas impide tratar sus salidas como evidencia robusta de auditoría.

![Figura 4. Diferencias pareadas SHAP-LIME para fidelidad y estabilidad. Fuente: figura derivada de `thesis/assets/figures/fig_diferencias_pareadas_es.png`.](../../figures/exported/fig_diferencias_pareadas_es.png)

![Figura 5. Relación entre estabilidad y coste por método. Fuente: figura derivada de `thesis/assets/figures/fig_estabilidad_coste_es.png`.](../../figures/exported/fig_estabilidad_coste_es.png)

## Cuatro perfiles explicativos

SHAP presenta el perfil global más equilibrado en el benchmark. Sus valores consolidados reportados en la tesis son fidelidad = 0.810, estabilidad = 0.724, parsimonia = 0.234, brecha de fidelidad = 0.431 y coste = 24,804 ms sobre bloques calificados. Este perfil lo posiciona como método fuerte para auditoría técnica cuando se requiere fidelidad y estabilidad. Sin embargo, su coste es heterogéneo: TreeSHAP puede ser eficiente en modelos de árboles, mientras que KernelSHAP puede ser costoso en modelos como SVM o MLP. Por tanto, la recomendación no debe formularse como superioridad universal, sino como preferencia condicionada por el modelo base y las restricciones operativas.

LIME aparece como método eficiente y parsimonioso. Su coste medio reportado es 226 ms y su fidelidad media 0.560, con parsimonia de 0.085. Estos valores sostienen su utilidad en escenarios donde se requiere explicación rápida, legible y de bajo coste. La limitación crítica es su estabilidad casi nula bajo las condiciones evaluadas: estabilidad media cercana a 0.014 y CV de estabilidad de 86.2% bajo semillas. El valor de LIME dentro del capítulo es mostrar que una explicación plausible y barata no necesariamente es una explicación reproducible.

Anchors produce reglas locales de alta precisión, cualitativamente distintas a las atribuciones numéricas de LIME y SHAP. Su fortaleza está en la legibilidad condicional: una regla puede comunicar bajo qué condiciones se mantiene una predicción. En el benchmark, Anchors presenta cobertura incompleta, coste alto y variable, fidelidad media de 0.386 y estabilidad de 0.052. Esta lectura debe ser prudente. No implica que Anchors sea inútil, sino que sus reglas requieren criterios propios de precisión, cobertura y aplicabilidad. Su comparación directa mediante métricas diseñadas para atribuciones debe conservar esta advertencia.

DiCE genera contrafactuales, no atribuciones de importancia. Por ello, su baja fidelidad bajo métricas de atribución no debe interpretarse como fallo absoluto. En la tesis, DiCE presenta fidelidad de 0.172, estabilidad intermedia de 0.366, parsimonia muy baja de 0.017 y coste moderado de 2,056 ms. Este perfil sugiere que DiCE es más pertinente cuando el objetivo explicativo es explorar alternativas de acción o corrección, no cuando se busca auditar importancias locales. Su presencia en el benchmark ayuda a mostrar por qué FOM-7 evalúa perfiles y no rankings universales.

![Figura 6. Correlación entre métricas del benchmark. Fuente: figura derivada de `thesis/assets/figures/fig_correlacion_metricas_es.png`.](../../figures/exported/fig_correlacion_metricas_es.png)

![Figura 7. Perfil multidimensional normalizado por método. Fuente: figura derivada de `thesis/assets/figures/fig_radar_metodos_es.png`.](../../figures/exported/fig_radar_metodos_es.png)

## Reproducibilidad como hallazgo, no solo control

La proposición de reproducibilidad se confirma parcialmente. En configuraciones replicadas de EXP1, SHAP-fidelidad, SHAP-estabilidad y LIME-fidelidad muestran CV inferiores al umbral del 15%, con valores principales por debajo de 3%. La excepción es LIME-estabilidad, con CV de 86.2%, explicable por una media cercana a cero. Esta excepción no invalida el protocolo. Más bien, revela una propiedad estructural del método bajo la configuración evaluada: cuando la estabilidad media es casi nula, pequeñas variaciones absolutas producen un CV relativo alto.

Este punto es importante para el argumento del capítulo. FOM-7 no solo confirma resultados; también ayuda a distinguir entre fallas del protocolo y propiedades problemáticas del método. Si una métrica varía porque el pipeline es inestable, el estudio pierde confiabilidad. Si una métrica varía porque el explicador produce salidas intrínsecamente inestables bajo condiciones controladas, el hallazgo es sustantivo. En este caso, la reproducibilidad funciona como lente interpretativa y no solo como requisito técnico.

## Síntesis del bloque empírico

Los resultados, resumidos en la Tabla 4, sostienen tres conclusiones de alcance delimitado. Primero, existen diferencias globales significativas entre métodos bajo el diseño EXP2. Segundo, SHAP ofrece el perfil más fuerte en fidelidad y estabilidad, especialmente cuando el objetivo es auditoría técnica. Tercero, no existe un método universalmente dominante: LIME conserva ventajas de coste y parsimonia; Anchors produce reglas condicionales con límites de cobertura; DiCE aporta contrafactualidad y acción correctiva.

La frontera calidad-coste es el resultado interpretativo central. La selección de un método XAI debe depender del objetivo operativo: auditoría de alta fidelidad, explicación rápida, regla condicional o exploración contrafactual. FOM-7 permite que esa selección se base en evidencia trazable y no en preferencias anecdóticas. Para un capítulo de libro, esta es la contribución más relevante del bloque empírico: mostrar que el valor de los resultados no reside en una tabla aislada, sino en la manera en que el protocolo convierte diferencias métricas en criterios de uso.


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

Belle, V., & Papantonis, I. (2021). Principles and practice of explainable machine learning. *Frontiers in Big Data, 4*. https://doi.org/10.3389/fdata.2021.688969

Bhattacharya, A., & Verbert, K. (2024). How good is your explanation? Towards a standardised evaluation approach for diverse XAI methods on multiple dimensions of explainability. In *Proceedings of the 32nd ACM Conference on User Modeling, Adaptation and Personalization (UMAP Adjunct '24)*. https://doi.org/10.1145/3631700.3664911

Breiman, L. (2001). Random forests. *Machine Learning, 45*(1), 5-32. https://doi.org/10.1023/a:1010933404324

Burger, C., Chen, L., & Le, T. (2023). Are your explanations reliable? Investigating the stability of LIME in explaining text classifiers by marrying XAI and adversarial attack. In *Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing* (pp. 12931-12944). https://doi.org/10.18653/v1/2023.emnlp-main.792

Canha, D., Kubler, S., Främling, K., & Fagherazzi, G. (2025). A functionally-grounded benchmark framework for XAI methods: Insights and foundations from a systematic literature review. *ACM Computing Surveys, 57*(12). https://doi.org/10.1145/3737445

Carvalho, D. V., Pereira, E. M., & Cardoso, J. S. (2019). Machine learning interpretability: A survey on methods and metrics. *Electronics, 8*(8), 832. https://doi.org/10.3390/electronics8080832

Doshi-Velez, F., & Kim, B. (2017). *Towards a rigorous science of interpretable machine learning*. arXiv. https://doi.org/10.48550/arXiv.1702.08608

Demšar, J. (2006). Statistical comparisons of classifiers over multiple data sets. *Journal of Machine Learning Research, 7*, 1-30. https://www.jmlr.org/papers/v7/demsar06a.html

Friedman, M. (1937). The use of ranks to avoid the assumption of normality implicit in the analysis of variance. *Journal of the American Statistical Association, 32*(200), 675-701. https://doi.org/10.1080/01621459.1937.10503522

Guidotti, R., Monreale, A., Ruggieri, S., Turini, F., Giannotti, F., & Pedreschi, D. (2018). A survey of methods for explaining black box models. *ACM Computing Surveys, 51*(5), 1-42. https://doi.org/10.1145/3236009

Hedström, A., Weber, L., Bareeva, D., Krakowczyk, D., Motzkus, F., Samek, W., Lapuschkin, S., & Höhne, M. M.-C. (2023). Quantus: An explainable AI toolkit for responsible evaluation of neural network explanations and beyond. *Journal of Machine Learning Research, 24*(34), 1-11.

Karimi, A.-H., Barthe, G., Schölkopf, B., & Valera, I. (2022). A survey of algorithmic recourse: Contrastive explanations and consequential recommendations. *ACM Computing Surveys, 55*(5), 1-29. https://doi.org/10.1145/3527848

Kohavi, R., & Becker, B. (1996). *Adult data set*. UCI Machine Learning Repository. https://archive.ics.uci.edu/dataset/2/adult

Lakens, D. (2013). Calculating and reporting effect sizes to facilitate cumulative science: A practical primer for t-tests and ANOVAs. *Frontiers in Psychology, 4*, 863. https://doi.org/10.3389/fpsyg.2013.00863

Laugel, T., Lesot, M.-J., Marsala, C., Renard, X., & Detyniecki, M. (2019). The dangers of post-hoc interpretability: Unjustified counterfactual explanations. In *Proceedings of the Twenty-Eighth International Joint Conference on Artificial Intelligence* (pp. 2801-2807). https://doi.org/10.24963/ijcai.2019/388

Lipton, Z. C. (2018). The mythos of model interpretability. *Queue, 16*(3), 31-57. https://doi.org/10.1145/3236386.3241340

Lundberg, S. M., & Lee, S. (2017). A unified approach to interpreting model predictions. *arXiv*. https://doi.org/10.48550/arXiv.1705.07874

Marcinkevičs, R., & Vogt, J. E. (2023). Interpretable and explainable machine learning: A methods-centric overview with concrete examples. *WIREs Data Mining and Knowledge Discovery, 13*(3). https://doi.org/10.1002/widm.1493

Mothilal, R. K., Sharma, A., & Tan, C. (2020). Explaining machine learning classifiers through diverse counterfactual explanations. In *FAT* '20: Proceedings of the 2020 Conference on Fairness, Accountability, and Transparency*. https://doi.org/10.1145/3351095.3372850

Murdoch, W. J., Singh, C., Kumbier, K., Abbasi-Asl, R., & Yu, B. (2019). Definitions, methods, and applications in interpretable machine learning. *Proceedings of the National Academy of Sciences, 116*(44), 22071-22080. https://doi.org/10.1073/pnas.1900654116

Nauta, M., Trienes, J., Pathak, S., Nguyen, E., Peters, M., Schmitt, Y., Schlötterer, J., van Keulen, M., & Seifert, C. (2023). From anecdotal evidence to quantitative evaluation methods: A systematic review on evaluating explainable AI. *ACM Computing Surveys, 55*(13s), 1-42. https://doi.org/10.1145/3583558

Nemenyi, P. B. (1963). *Distribution-free multiple comparisons* [Doctoral dissertation, Princeton University]. https://catalog.princeton.edu/catalog/2081365

Pawlicki, M., Pawlicka, A., Uccello, F., Szelest, S., D'Antonio, S., Kozik, R., & Choraś, M. (2024). Evaluating the necessity of the multiple metrics for assessing explainable AI: A critical examination. *Neurocomputing, 602*, 128282. https://doi.org/10.1016/j.neucom.2024.128282

Poyiadzi, R., Sokol, K., Santos-Rodriguez, R., De Bie, T., & Flach, P. (2020). FACE: Feasible and actionable counterfactual explanations. In *Proceedings of the AAAI/ACM Conference on AI, Ethics, and Society* (pp. 344-350). https://doi.org/10.1145/3375627.3375850

Ribeiro, M. T., Singh, S., & Guestrin, C. (2016). "Why should I trust you?": Explaining the predictions of any classifier. *Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining*. https://doi.org/10.1145/2939672.2939778

Ribeiro, M. T., Singh, S., & Guestrin, C. (2018). Anchors: High-precision model-agnostic explanations. *Proceedings of the AAAI Conference on Artificial Intelligence, 32*(1). https://doi.org/10.1609/aaai.v32i1.11491

Rudin, C., Chen, C., Chen, Z., Huang, H., Semenova, L., & Zhong, C. (2022). Interpretable machine learning: Fundamental principles and 10 grand challenges. *Statistics Surveys, 16*, 1-85. https://doi.org/10.1214/21-ss133

Schwalbe, G., & Finzel, B. (2023). A comprehensive taxonomy for explainable artificial intelligence: A systematic survey of surveys on methods and concepts. *Data Mining and Knowledge Discovery, 38*(5), 3043-3101. https://doi.org/10.1007/s10618-022-00867-8

Slack, D., Hilgard, S., Jia, E., Singh, S., & Lakkaraju, H. (2020). Fooling LIME and SHAP: Adversarial attacks on post hoc explanation methods. In *Proceedings of the AAAI/ACM Conference on AI, Ethics, and Society* (pp. 180-186). https://doi.org/10.1145/3375627.3375830

Van den Broeck, G., Lykov, A., Schleich, M., & Suciu, D. (2022). On the tractability of SHAP explanations. *Journal of Artificial Intelligence Research, 74*, 851-886. https://doi.org/10.1613/jair.1.13283

Wachter, S., Mittelstadt, B., & Russell, C. (2017). Counterfactual explanations without opening the black box: Automated decisions and the GDPR. *SSRN Electronic Journal*. https://doi.org/10.2139/ssrn.3063289

Wilcoxon, F. (1945). Individual comparisons by ranking methods. *Biometrics Bulletin, 1*(6), 80-83. https://doi.org/10.2307/3001968

Zheng, X., Shirani, F., Chen, Z., Lin, C., Cheng, W., Guo, W., & Luo, D. (2025). F-FIDELITY: A robust framework for faithfulness evaluation of explainable AI. *ICLR 2025 Proceedings*. https://trustai4s-lab.github.io/ffidelity
