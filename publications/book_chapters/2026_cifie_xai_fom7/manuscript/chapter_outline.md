# Esquema científico del capítulo

> **Orden vigente (2026-09-30, decisión del autor):** 02 Introducción; 03 Qué es y qué no
> es la XAI; 04 Por qué importa la XAI (funciones, audiencias y ámbitos); 05 La crisis de
> evaluación en XAI (brechas); 06 Protocolo FOM-7; 07 Métodos evaluados y diseño del
> benchmark; 08 Aplicación empírica; 09 Implicaciones; 10 Limitaciones; 11 Conclusiones.
> Los nombres de archivo no cambian. Este orden prevalece sobre la numeración de las
> secciones siguientes; véase `planning/science_first_revision_plan_2026-09-28.md`.

**Estado:** estructura de producción aprobada para la revisión science-first

**Título de trabajo:** *De la explicación a la evidencia: fundamentos,
aplicaciones y evaluación auditable de la inteligencia artificial explicable*

**Subtítulo de trabajo:** *El protocolo FOM-7 como marco operativo para
comparaciones reproducibles*

## Tesis central

La inteligencia artificial explicable no convierte automáticamente un modelo opaco
en un sistema comprensible o confiable. Produce objetos explicativos cuyo valor
científico depende del propósito, la audiencia, el dominio y la evidencia usada para
validarlos. Una explicación solo puede tratarse como evidencia defendible cuando su
fidelidad, estabilidad, utilidad, reproducibilidad y alcance están explícitamente
delimitados. FOM-7 operacionaliza una parte de ese problema en la evaluación
comparativa funcionalmente fundamentada.

## Alcance y extensión de trabajo

- Idioma: español.
- Registro: científico, preciso y accesible para lectores técnicos no especializados
  en XAI.
- Extensión máxima: 9.000 palabras de cuerpo, sin referencias; objetivo de trabajo:
  8.800 palabras (editor, 2026-10-01).
- Estilo estructural: pocas secciones principales con ideas desarrolladas; integrar
  nombres de dominios, métodos y puertas dentro de la prosa en lugar de crear una
  subsección para cada elemento.
- Contribución original: FOM-7 y su demostración empírica acotada.
- Función del benchmark: caso metodológico, no eje exclusivo del capítulo ni ranking
  universal de métodos.
- Aplicaciones prioritarias: salud, finanzas, ciberseguridad, sistemas autónomos y
  modelos fundacionales o de lenguaje.
- Educación y servicios públicos: ejemplos transversales, salvo que evidencia futura
  justifique una subsección independiente.

## Estructura de producción

### 01. Resumen y palabras clave

**Archivo:** `01_resumen_palabras_clave.md`

**Función:** sintetizar la necesidad general de XAI, las áreas de aplicación, las
brechas científicas, la contribución de FOM-7 y la demostración empírica.

**Contenido mínimo:**

1. Problema: generar explicaciones no equivale a validarlas.
2. Alcance: panorama conceptual, aplicaciones, brechas y evaluación.
3. Contribución: FOM-7 como protocolo de evidencia auditable.
4. Demostración: benchmark Adult/tabular bajo condiciones declaradas.
5. Conclusión acotada: la selección depende del propósito y del tipo de evidencia.

**Regla:** redactar al final y no introducir ninguna afirmación que no aparezca en el
cuerpo.

### 02. Por qué importa la inteligencia artificial explicable

**Archivo de producción:** `02_introduccion.md`

**Función:** establecer el problema científico y social antes de presentar métodos.

**Subsecciones previstas:**

1. De la predicción a la supervisión humana.
2. Funciones de una explicación durante el ciclo de vida de la IA.
3. Audiencias distintas: desarrollo, auditoría, profesión, dirección, regulación y
   personas afectadas.
4. Promesa y límite: explicación, confianza y confiabilidad no son equivalentes.
5. Objetivo, tesis y recorrido del capítulo.

**Afirmaciones necesarias:**

- una explicación puede apoyar depuración, monitoreo, comunicación, auditoría,
  supervisión y contestabilidad;
- el contenido útil cambia con la audiencia y la decisión;
- la explicabilidad es solo una dimensión de la IA confiable;
- una explicación persuasiva puede no mejorar la decisión humana.

**Ruta de evidencia:** literatura conceptual actual; candidatos C01-C08 y marcos
oficiales. Los resultados humanos deben conservar el límite de su tarea experimental.

### 03. Qué es y qué no es la XAI

**Archivo de producción:** `03_fundamentos_xai.md`

**Función:** ofrecer una definición general de XAI y fijar el vocabulario que usará el
resto del capítulo.

**Bloques de argumento:**

1. XAI como práctica sociotécnica: qué se explica, para quién y con qué propósito.
2. Conceptos, modelos y objetos explicativos: interpretabilidad, transparencia,
   métodos post-hoc, escalas local/global, atribuciones, reglas y contrafactuales.
3. Propiedades, límites y niveles de evaluación: fidelidad, estabilidad, robustez,
   utilidad humana y alcance funcionalmente fundamentado de FOM-7.

**Regla conceptual:** cada término se define una vez; las secciones posteriores deben
remitir a esta taxonomía en lugar de redefinirlo.

### 04. Ámbitos de aplicación y horizontes próximos

**Archivo de producción:** `04_metodos_lime_shap_anchors_dice.md`

**Función:** conectar XAI con decisiones y riesgos concretos. El catálogo técnico que
actualmente ocupa este archivo se trasladará y comprimirá en la sección 05.

Los cinco dominios se integran bajo un bloque común, con su nombre como entrada en
prosa y sin una subsección separada por dominio. Cada uno conserva:

1. decisión o tarea apoyada por IA;
2. actor que necesita la explicación;
3. ejemplo concreto;
4. daño posible de una explicación errónea o insuficiente;
5. objeto explicativo y evidencia que podrían ayudar; y
6. brecha científica todavía abierta.

**Salud y biomedicina.**

- Ejemplo: un equipo clínico investiga si un predictor de riesgo depende de señal
  clínicamente pertinente o de un artefacto de adquisición.
- Límite: una atribución o mapa de calor no valida un diagnóstico ni demuestra
  relevancia causal.
- Evidencia prevista: C04-C06.

**Finanzas y asignación de oportunidades.**

- Ejemplo: una institución audita una decisión de crédito mientras la persona afectada
  necesita una explicación comprensible y una vía de contestación o recourse.
- Límite: variables correlacionadas, proxies y contrafactuales inviables pueden inducir
  una explicación engañosa.
- Evidencia prevista: C03, C09 y literatura actual sobre recourse.

**Ciberseguridad e infraestructura crítica.**

- Ejemplo: un analista determina por qué se marcó un dominio o flujo y si la
  explicación aporta contexto accionable para la respuesta.
- Límite: mostrar una explicación no garantiza mejor desempeño ni confianza; el
  adversario también puede atacar la explicación.
- Evidencia prevista: C10, C14 y literatura actual sobre ataques a explicaciones.

**Sistemas autónomos e industriales.**

- Ejemplo: un ingeniero o pasajero examina por qué un sistema tomó una acción y si la
  explicación es coherente con sensores, contexto y comportamiento observado.
- Límite: una explicación legible no constituye un caso de seguridad; una explicación
  errónea puede degradar confianza y dependencia aun cuando la conducta sea idéntica.
- Evidencia prevista: C11 y C15.

**Modelos fundacionales, generativos y de lenguaje.**

- Ejemplo: un equipo investiga si una respuesta se apoya en la evidencia suministrada
  o si el racional verbaliza una justificación posterior.
- Límite: la cadena de pensamiento no debe tratarse como acceso directo al cómputo
  interno; su fidelidad depende de la definición y de la prueba empleada.
- Evidencia prevista: C12, C16 y C17.
- Multimodalidad: presentar como extensión de agenda salvo que se añada evidencia
  específica antes de redactar.

### 05. La crisis de evaluación y las brechas de validez

**Archivo de producción:** `05_crisis_evaluacion_xai.md`

**Función:** conectar madurez técnica con la falta de evidencia comparable; explicar
por qué métricas y objetos distintos requieren afirmaciones acotadas; introducir las
siete brechas en grupos amplios antes de FOM-7.

**Bloques de argumento:**

1. Crisis de medición, fidelidad aislada, reproducibilidad y gobernanza.
2. Brechas agrupadas: técnica/constructo; humana/causal; operativa/gobernanza/modelos
  emergentes. Nombrar cada brecha en la prosa, no como siete subtítulos.
3. Alcance parcial de FOM-7 y transición al protocolo.

### 06. FOM-7 como respuesta metodológica acotada

**Archivo de producción:** `06_protocolo_fom7.md`

**Función:** presentar la secuencia de admisibilidad y sus límites funcionales.
Mantener las siete puertas identificables con etiquetas en línea dentro de un solo
bloque de protocolo, no con un subtítulo independiente para cada puerta.

### 07. Métodos evaluados y diseño del benchmark

**Archivo de producción:** `07_diseno_empirico.md`

**Función:** describir los cuatro objetos explicativos y el diseño reproducible de EXP1
y EXP2. Presentar LIME, SHAP, Anchors y DiCE como entradas en prosa, y agrupar factores,
muestreo, métricas, unidades e inferencia en un bloque de diseño.

**Secuencia de FOM-7 (en sección 06):**

1. Congelamiento del protocolo.
2. Ejecución controlada por lotes.
3. Auditoría de artefactos.
4. Armonización inferencial.
5. Exportación determinista de artefactos pareados.
6. Perfilado de dispersión entre ejecuciones.
7. Reporte de afirmaciones trazables a evidencia fuente.

**Puente con las brechas:** cada puerta se vinculará con las brechas que controla y se
identificarán explícitamente las que quedan fuera: utilidad humana, causalidad e impacto
de despliegue.

### 08. Caso empírico: de un benchmark a evidencia auditable

**Archivo de producción:** `08_aplicacion_empirica_perfiles_fom7.md`

**Función:** integrar diseño y resultados esenciales como demostración de FOM-7.

**Bloques de argumento:**

1. Diseño EXP2 y calificación de artefactos.
2. Resultados globales y perfiles por método.
3. Reproducibilidad, selección condicionada y alcance de la evidencia.

**Reglas de protección:**

- conservar cada cifra registrada, su agregación y su límite;
- excluir resultados no publicados de Paper B+C;
- no presentar SHAP como método universalmente superior;
- tratar Anchors y DiCE según la naturaleza de sus salidas; y
- ejecutar cobertura y exclusividad después de cada movimiento de texto.

### 09. Implicaciones para investigación, práctica y gobernanza

**Archivo de producción:** `09_implicaciones_evaluacion_auditable_xai.md`

**Función:** convertir el marco y el caso en decisiones prácticas sin ampliar el
alcance empírico.

**Bloques de argumento:**

1. Selección condicionada de métodos y gobernanza de la evidencia.
2. Uso de FOM-7, relación con las herramientas del campo y límites de transferencia.

### 10. Limitaciones y agenda científica

**Archivo de producción:** `10_limitaciones_trabajo_futuro.md`

**Función:** separar los límites del caso de las brechas generales del campo.

**Bloque de límites:** integrar en una discusión continua, no una subsección por límite:

- un conjunto de datos tabular;
- familias de modelos, métodos y métricas declaradas;
- evaluación funcional sin estudio directo con usuarios;
- sensibilidad a configuraciones y artefactos disponibles; y
- transferencia de FOM-7 todavía no demostrada en otros dominios.

**Agenda científica:** agrupar las líneas en párrafos desarrollados, no en subtítulos:

1. evaluación humana y confianza calibrada;
2. causalidad, factibilidad y consecuencias del recourse;
3. explicaciones bajo cambio de distribución y monitoreo longitudinal;
4. seguridad y robustez adversarial;
5. modelos de lenguaje, agentes y multimodalidad;
6. benchmarks interdominio con validez de constructo; y
7. estándares de reporte, trazabilidad y replicación.

### 11. Conclusiones

**Archivo de producción:** `11_conclusiones.md`

**Función:** responder a la tesis central en tres movimientos:

1. XAI es una familia de intervenciones dependientes de propósito y audiencia.
2. Una explicación no se convierte en evidencia sin evaluación y trazabilidad.
3. FOM-7 aporta un protocolo verificable para una parte acotada de ese problema, como
   demuestra el caso Adult/tabular.

La conclusión no repetirá el catálogo de resultados ni añadirá líneas futuras nuevas.

## Mapa de migración del manuscrito actual

| Material actual | Acción estructural | Destino |
| --- | --- | --- |
| Introducción sobre opacidad y evidencia | Conservar, ampliar audiencias y reducir repetición de FOM-7 | 02 |
| Definiciones conceptuales | Integrar conceptos, modelos, objetos y niveles bajo pocos bloques | 03 |
| Aplicaciones | Cinco dominios bajo un bloque, con entradas en prosa | 04 |
| Crisis y brechas de validez | Agrupar siete brechas en tres temas de validez | 05 |
| Protocolo FOM-7 | Mantener siete puertas con etiquetas en línea bajo un bloque | 06 |
| Métodos y diseño empírico | Métodos y componentes del diseño como entradas en prosa bajo dos bloques | 07 |
| Resultados protegidos | Conservar como demostración acotada, con tres bloques de lectura | 08 |
| Implicaciones | Dos bloques amplios sobre selección, gobernanza y transferencia | 09 |
| Limitaciones actuales | Un bloque de límites seguido de una agenda integrada | 10 |
| Resumen y conclusiones | Reescribir al final | 01 y 11 |

## Puertas antes de mover prosa

- Cada subsección nueva debe tener evidencia identificada en `sources/evidence_map.md`.
- Las fuentes candidatas pasan a las bibliografías de producción solo al ser citadas.
- Cualquier movimiento de una cifra protegida exige verificación inmediata.
- La arquitectura debe mantenerse dentro de once archivos de sección para conservar
  el contrato del build.
- Priorizar pocos subtítulos que agrupen ideas desarrolladas; usar entradas en prosa
  para métodos, dominios y puertas, y evitar un subtítulo por elemento de una lista.
- Después de completar una unidad estructural se debe construir el Word y revisar las
  páginas modificadas.
