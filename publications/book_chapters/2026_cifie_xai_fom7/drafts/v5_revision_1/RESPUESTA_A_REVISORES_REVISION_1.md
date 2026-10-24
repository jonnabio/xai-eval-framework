# Carta de Respuesta a los Comentarios Editoriales (Revisión 1)

**Capítulo:** *De la explicación a la evidencia: fundamentos, aplicaciones y evaluación auditable de la inteligencia artificial explicable*  
**Autor:** Jonathan Herrera-Vásquez (Universidad Americana de Europa)  
**Editora Académica:** Dra. Irene Arostegui (Colección CIFIE / Editorial Tintazul)  
**Fecha:** 24 de octubre de 2026  

---

Estimada Dra. Irene Arostegui:

Agradezco profundamente su detallada y constructiva revisión editorial del capítulo. Sus observaciones han permitido elevar significativamente la precisión metodológica, la claridad conceptual y la honestidad epistémica del manuscrito.

A continuación, se presenta la respuesta detallada punto por punto a cada uno de sus comentarios, señalando las enmiendas específicas incorporadas en el texto revisado.

---

### Comentario 44 — Correspondencia entre las compuertas de FOM-7 y las métricas del benchmark

**Comentario de la Editora:**

> *"Haga explícita la correspondencia entre las siete compuertas que conforman FOM-7 y las métricas efectivamente operacionalizadas en el benchmark empírico. La Tabla 1 presenta cinco métricas primarias: fidelidad, estabilidad, parsimonia, brecha de fidelidad y coste computacional, mientras que el protocolo previamente definido comprende siete puertas, incluidas consistencia inter-método (G6) y equidad en la explicación (G7). Es necesario indicar cuáles de las siete puertas fueron evaluadas experimentalmente, cuáles fueron analizadas mediante indicadores equivalentes y cuáles permanecen como componentes del marco pendientes de validación empírica, a fin de evitar que el lector interprete que las siete fueron sometidas al mismo nivel de comprobación."*

**Respuesta del Autor:**

Se acepta plenamente la observación. Comparto la apreciación de que presentar las siete compuertas del marco teórico de gobernanza junto con las cinco métricas tabulares del benchmark sin un deslinde explícito podía inducir a error al lector respecto al nivel de comprobación de cada componente.

**Modificaciones realizadas:**

1. **Sección 06 (`06_protocolo_fom7.md`):** Se incorporó una subsección explícita titulada *«Correspondencia metodológica y niveles de comprobación»*, donde se formalizan tres niveles de verificación técnica:
   - **Nivel 1 (Evaluación experimental directa en el benchmark):** Fidelidad ($F$ y $\Delta_k$), Estabilidad ($S$), Parsimonia ($P$) y Coste computacional ($C$).
   - **Nivel 2 (Evaluación mediante indicadores operacionales específicos por objeto):** Validez contrafactual y cobertura de reglas ($G_4$), evaluadas a través de la cobertura empírica en Anchors y la tasa de generación factible en DiCE dentro del inventario calificado de celdas.
   - **Nivel 3 (Componentes metodológicos reservados para auditorías ampliadas):** Consistencia inter-método ($G_6$) y Equidad en la explicación ($G_7$), delimitadas como compuertas del diseño general del marco no sometidas a contrastes de hipótesis en este benchmark factorial.
2. **Sección 07 (`07_diseno_empirico.md`):** Se añadió el apartado *«Métricas primarias y correspondencia con FOM-7»*, explicitando este mapeo previo a la presentación de la Tabla 1.
3. **Tabla 1 (`tables/table_metrics.md`):** Se expandió la *Nota* metodológica al pie de la tabla detallando de forma sintética la correspondencia con las compuertas $G_1$ a $G_7$ y aclarando cuáles permanecen reservadas para auditorías ampliadas.

---

### Comentario 50 — Calibración metodológica de la reproducibilidad

**Comentario de la Editora:**

> *"Sustituir la expresión «garantizar la reproducibilidad completa» por una formulación metodológicamente más precisa. La fijación de una semilla favorece la reproducibilidad, pero no la garantiza por sí sola, pues esta depende también de las versiones de bibliotecas y dependencias, configuración del entorno, implementación de los algoritmos, hardware y disponibilidad del código y de los parámetros experimentales. Hay que indicar los mecanismos adicionales empleados para asegurar la reproducibilidad del benchmark o, en su defecto, hablar de «favorecer» o «controlar» la reproducibilidad experimental."*

**Respuesta del Autor:**

Coincido enteramente con la apreciación. La afirmación original constituía una sobrestimación metodológica, dado que el determinismo numérico en arquitecturas computacionales modernas involucra múltiples capas más allá de una semilla pseudoaleatoria de inicialización.

**Modificaciones realizadas:**

1. **Sección 07 (`07_diseno_empirico.md`):** Se reformuló el apartado de entorno bajo el título *«Entorno de ejecución y control de reproducibilidad»*. Se sustituyó la locución impugnada por: *«Para favorecer y controlar la reproducibilidad experimental —reconociendo metodológicamente que la fijación de una semilla no la garantiza por sí sola sin un control exhaustivo del software, dependencias y arquitectura subyacente— se articularon cuatro mecanismos complementarios:...»*.
2. Se documentaron explícitamente las cuatro salvaguardas empleadas: (a) protocolo determinista multillave de cinco semillas (42, 123, 456, 789, 999) para medir y acotar la dispersión estocástica inter-ejecución; (b) congelación estricta de versiones de bibliotecas en entornos virtuales aislados; (c) preprocesadores deterministas ajustados sin fuga de datos; y (d) disponibilidad pública de código y artefactos con identificadores DOI persistentes.

---

### Comentario 54 — Delimitación de originalidad y precedencia respecto a RIMI y Tesis Doctoral

**Comentario de la Editora:**

> *"Dado que los resultados empíricos centrales de H1 y H2 proceden de una publicación previa y P1 de una tesis doctoral no publicada, se recomienda delimitar explícitamente la contribución original de este capítulo respecto de esos trabajos antecedentes. Conviene precisar qué resultados se reproducen o sintetizan, cuáles se reanalizan y qué componentes de FOM-7, interpretaciones, integraciones o aplicaciones se presentan aquí por primera vez."*

**Respuesta del Autor:**

Se acepta plenamente la recomendación. Es imperativo para la integridad científica y editorial distinguir con absoluta transparencia los resultados tomados de publicaciones previas frente a las aportaciones conceptuales y analíticas que se publican por primera vez en este volumen colectivo.

**Modificaciones realizadas:**

1. **Sección 02 (`02_introduccion.md`):** Se introdujo una subsección dedicada titulada *«Delimitación de aportaciones y procedencia de resultados»*, desglosando con nitidez tres niveles de precedencia:
   - *Resultados empíricos antecedentes sintetizados:* Contrastes de hipótesis H1 y H2 tomados de Herrera-Vásquez & Herrero-Uceda (2026, RIMI); descriptivos de reproducibilidad P1 del repositorio experimental de la tesis doctoral de Herrera-Vásquez (2026).
   - *Resultados reanalizados e integrados:* La convergencia y comparación cuatripartita simultánea (LIME, SHAP, Anchors, DiCE) bajo un prisma analítico unificado que concilia objetos explicativos dispares (sustitutos lineales, valores de Shapley, reglas lógicas y contrafactuales).
   - *Aportaciones originales inéditas de este capítulo:* (i) La formalización metodológica completa del protocolo secuencial FOM-7 de siete compuertas; (ii) El enfoque aplicado de ingeniería de datos y observabilidad de software; (iii) La caracterización de perfiles de compromiso operativo (*trade-offs*) para despliegue productivo; y (iv) La articulación de criterios de evaluación técnica alineados con la Ley de Inteligencia Artificial de la UE y el marco NIST AI RMF.
2. **Tabla 2 (`tables/table_results_summary.md`):** Se actualizó la *Nota* al pie de la tabla incorporando formalmente la declaración de precedencia y citación de procedencia.

---

### Comentario 69 — Matización epistémica: erradicación de «certificar» y «certificación»

**Comentario de la Editora:**

> *"Matizar el alcance de expresiones como «validación empírica», «certificar» o «certificación» cuando se refieren al protocolo FOM-7 en su conjunto. El benchmark aporta evidencia experimental relevante sobre el funcionamiento del marco en un conjunto de datos tabulares y bajo condiciones controladas, pero el propio capítulo reconoce que no evalúa directamente utilidad humana, plausibilidad semántica ni causalidad y que el estudio se restringe a datos tabulares. Sería más preciso hablar de «evaluación empírica», «validación experimental inicial» o «criterios de aceptación técnica», reservando «certificación» para contextos en los que exista un procedimiento normativo o de conformidad formalmente establecido."*

**Respuesta del Autor:**

Comparto enteramente este criterio de prudencia epistémica. El empleo de «certificación» en un trabajo de benchmarking experimental computacional puede sugerir erróneamente un procedimiento normativo de acreditación legal o regulatoria.

**Modificaciones realizadas:**

1. **Barrido léxico transversal:** Se eliminaron las instancias donde «certificar» o «certificación» se aplicaban al protocolo FOM-7 o a la evaluación experimental del benchmark, sustituyéndolas por «verificación técnica computacional», «evaluación empírica controlada» o «criterios de aceptación técnica».
2. Se reservó el término «certificación» exclusivamente para discusiones de evaluación de conformidad jurídica formal (e.g., evaluación de conformidad bajo el Reglamento de IA de la UE).
3. **Sección 11 (`11_conclusiones.md`):** Se añadió una declaración explícita de deslinde: *«El protocolo FOM-7 aporta un marco estructurado de evaluación experimental y verificación técnica de artefactos explicativos bajo condiciones controladas de laboratorio; no constituye una certificación normativa formal de sistemas de IA ni sustituye los procedimientos de evaluación de conformidad regulatoria... Su alcance se circunscribe a la evaluación funcionalmente fundamentada (Nivel 3), aportando evidencia empírica controlada sin pretender medir de forma directa la utilidad cognitiva humana, la acción contrafactual real ni la validez causal»*.

---

### Comentario 71 — Estructura explícita de limitaciones del estudio antes de la agenda futura

**Comentario de la Editora:**

> *"Incorporar antes de la agenda futura una delimitación explícita de las principales limitaciones del estudio. Entre ellas podría considerar, al menos, el uso de un único conjunto de datos tabular (UCI Adult Income), la dependencia de las operacionalizaciones seleccionadas para cada métrica, el alcance funcionalmente fundamentado de la evaluación sin participación de usuarios y las restricciones de generalización hacia otros dominios, modalidades de datos y escenarios productivos. La agenda futura puede mantenerse posteriormente como respuesta a estas limitaciones."*

**Respuesta del Autor:**

Se acepta plenamente la observación. Se ha reestructurado por completo la Sección 10 bajo el epígrafe *«Alcance y limitaciones del estudio»* para otorgar a las limitaciones el espacio y la jerarquía formal que demandan los estándares de publicación científica.

**Modificaciones realizadas:**

1. **Sección 10 (`10_limitaciones_trabajo_futuro.md`):** Se organizó la sección en dos bloques nítidamente articulados:
   - **Bloque 1: «Alcance y limitaciones del estudio»**, estructurado punto por punto en los cuatro ejes señalados por la editora:
     1. *Uso de un único conjunto de datos tabular (UCI Adult Income):* Explicación de la justificación metodológica de control y reconocimiento explícito de la imposibilidad de extrapolar a visión, PLN, audio o grafos.
     2. *Dependencia de las operacionalizaciones seleccionadas para cada métrica:* Discusión de los supuestos del enmascaramiento univariado frente a ROAR y de la similitud coseno frente a métricas Lipschitz o robustez adversarial.
     3. *Alcance funcionalmente fundamentado sin participación de usuarios humanos (Nivel 3):* Delimitación formal de que no se evalúa comprensión cognitiva, confianza calibrada ni reducción de carga mental en operadores humanos (Niveles 1 y 2).
     4. *Restricciones de generalización hacia otros dominios, modalidades y escenarios productivos:* Análisis de la naturaleza estática del benchmark frente a la deriva de datos (*drift*), latencia concurrente en microservicios, restricciones regulatorias específicas de sector o fragilidad ante ataques adversariales orientados a manipular la explicación (scaffolding). Asimismo, la cobertura incompleta observada en métodos basados en búsqueda estocástica (Anchors y DiCE) revela barreras de escalabilidad y compatibilidad que condicionan su aplicabilidad productiva.
   - **Bloque 2: «Agenda de investigación futura en respuesta a las limitaciones identificadas»**, donde cada una de las cuatro líneas de investigación futuras se formula como la respuesta directa y simétrica a cada una de las cuatro limitaciones anteriores.

---

### Verificación Técnica y Salvaguardas

- **Control de Invariantes Numéricos (RCA-001):** Se ejecutó el verificador [`scripts/pubs/verify_claims.py`](file:///d:/Github/xai-eval-framework/scripts/pubs/verify_claims.py), confirmando que las 1,898 afirmaciones numéricas del repositorio continúan derivándose exactamente de los artefactos crudos sin alteración, aprobando el 100% de las comprobaciones.
- **Sincronización de Fragmentos (RCA-003):** [`scripts/pubs/verify_sync.py`](file:///d:/Github/xai-eval-framework/scripts/pubs/verify_sync.py) superado sin discrepancias.
- **Compilación Limpia:** El manuscrito fue recompilado íntegramente mediante [`scripts/build_cifie_chapter.py`](file:///d:/Github/xai-eval-framework/scripts/build_cifie_chapter.py), generando tanto la edición digital en color como la edición monocromática para impresión.

Quedo a su entera disposición en caso de que requiera cualquier ajuste adicional antes de la maquetación final.

Atentamente,

**Jonathan Herrera-Vásquez**  
Autor  
Universidad Americana de Europa (UNADE)  
24 de octubre de 2026
