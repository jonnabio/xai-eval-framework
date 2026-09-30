# Auditoría de citas

## Estado vigente de la bibliografía de producción

- Fuente base: `thesis/references.bib`.
- Alcance actual: referencias fundacionales para LIME, SHAP, Anchors, DiCE,
  evaluación XAI, benchmarking reproducible, robustez/fidelidad, taxonomías y
  pruebas estadísticas.
- Estado al 2026-09-28: 41 obras en la bibliografía de producción y 41 obras citadas
  en el manuscrito actual. La sincronización del 2026-09-27 comprobó la resolución de
  los 35 DOI presentes. Sigue pendiente la revisión editorial APA 7 final antes del
  envío.
- Política para la revisión científica: las fuentes nuevas permanecen primero en
  `candidate_literature_2026-09-28.md` y entran a la bibliografía de producción solo
  cuando una sección revisada las cite.

## Inventario histórico de entradas auditadas

La lista siguiente conserva el registro de trabajo de las entradas de la base actual.
El rótulo original “pendientes de verificar” quedó obsoleto después de las pasadas OA,
la revisión de fundamentos y la sincronización del 2026-09-27; las excepciones aún
abiertas se enumeran en las secciones de DOI y URL al final de este archivo.

- `@ribeiro2016` — LIME / modelos sustitutos locales.
- `@adadi2018` — revisión XAI y problema de caja negra.
- `@ali2023` — estado de XAI y requisitos de IA confiable.
- `@arrieta2019` — conceptos, taxonomías y retos de XAI responsable.
- `@belle2021` — principios y práctica de aprendizaje automático explicable.
- `@carvalho2019` — revisión de métodos y métricas de interpretabilidad.
- `@breiman2001` — bosque aleatorio como familia de modelo predictivo.
- `@guidotti2018` — revisión de métodos para explicar modelos de caja negra.
- `@karimi2022` — recourse algorítmico, recomendaciones consecuenciales y contrafactuales.
- `@kohavi1996` — conjunto UCI Adult Income.
- `@lakens2013` — reporte e interpretación de tamaños de efecto.
- `@laugel2019` — riesgos de contrafactuales post-hoc injustificados.
- `@lundberg2017` — SHAP / valores de Shapley.
- `@lipton2018` — crítica conceptual a la interpretabilidad.
- `@marcinkevics2023` — panorama metodológico de interpretabilidad y explicabilidad.
- `@ribeiro2018` — Anchors / reglas locales de alta precisión.
- `@mothilal2020` — DiCE / explicaciones contrafactuales diversas.
- `@murdoch2019` — definiciones, métodos y aplicaciones de aprendizaje interpretable.
- `@miller2019` — explicación como fenómeno contrastivo y social; verificada en pasada fundamentos XAI 2026-07-04 mediante Semantic Scholar, OpenAlex, Crossref y arXiv.
- `@poyiadzi2020` — FACE y contrafactuales factibles/accionables.
- `@slack2020` — ataques adversariales a explicaciones post-hoc LIME/SHAP.
- `@vandenbroeck2022` — tractabilidad de explicaciones SHAP.
- `@wachter2017` — contrafactuales y decisiones automatizadas.
- `@doshi-velez2017` — evaluación rigurosa de interpretabilidad; verificada en pasada OA 2026-07-04 mediante OpenAlex/arXiv.
- `@alvarezmelis2018` — robustez de métodos de interpretabilidad.
- `@canha2025` — benchmark functionally-grounded para XAI; verificada en pasada OA 2026-07-04 mediante OpenAlex y Crossref.
- `@abdulkadir2023` — revisión/taxonomía de métricas XAI.
- `@hedstrom2023` — Quantus y evaluación responsable de explicaciones; verificada en pasada OA 2026-07-04 mediante Semantic Scholar, OpenAlex/arXiv y JMLR.
- `@agarwal2022` — OpenXAI y evaluación transparente; verificada en pasada OA 2026-07-04 mediante Semantic Scholar y OpenAlex/arXiv.
- `@zheng2025` — F-FIDELITY y evaluación de fidelidad.
- `@nauta2023` — revisión sistemática de evaluación cuantitativa XAI; verificada en pasada OA 2026-07-04 mediante Semantic Scholar, OpenAlex y Crossref.
- `@rudin2022` — principios y retos de aprendizaje automático interpretable.
- `@friedman1937` — prueba de Friedman para comparación por rangos.
- `@demsar2006` — comparación estadística no paramétrica de clasificadores/métodos.
- `@nemenyi1963` — comparaciones múltiples post-hoc de Nemenyi.
- `@wilcoxon1945` — prueba pareada de rangos con signo.
- `@altukhi2025` — revisión reciente de avances XAI.
- `@schwalbe2023` — taxonomía de conceptos y métodos XAI.
- `@pawlicki2024` — necesidad de múltiples métricas en evaluación XAI; verificada en pasada OA 2026-07-04 mediante Semantic Scholar, OpenAlex y Crossref.
- `@bhattacharya2024` — evaluación multidimensional de explicaciones; verificada en pasada OA 2026-07-04 mediante OpenAlex y Crossref.
- `@burger2023` — estabilidad de LIME.

## Primera pasada de ampliación científica: 2026-09-28

Objetivo: construir una base verificable para las nuevas secciones sobre importancia,
aplicaciones, evaluación humana, gobernanza y brechas, sin introducir referencias no
citadas en el Word actual.

### Fuentes candidatas aceptadas

- Principios y gobernanza: Phillips et al. (2021), Tabassi (2023), Reglamento (UE)
  2024/1689 y World Health Organization (2021).
- Salud y límites clínicos: Ghassemi et al. (2021).
- Evaluación humana y counterevidence: Kim et al. (2024), Alufaisan et al. (2021) y
  Poursabzi-Sangdeh et al. (2021).
- Dominios: Weber et al. (2024) para finanzas; Rjoub et al. (2023) para
  ciberseguridad; Kuznietsov et al. (2024) para conducción autónoma; Zhao et al.
  (2024) para modelos de lenguaje.

Se verificaron título, autoría, año, venue o institución, DOI o URL estable y alcance
del soporte. La matriz de admisibilidad, los límites y los registros APA 7 de staging
están en `candidate_literature_2026-09-28.md`.

### Decisiones de admisión

- Las revisiones sistemáticas y surveys sostendrán mapas de dominio o del campo, no
  efectos empíricos concretos cuando exista un estudio primario relevante.
- Alufaisan et al. y Poursabzi-Sangdeh et al. se incorporan como counterevidence
  primario: sus resultados se limitarán a las tareas estudiadas.
- Ghassemi et al. se identificará como perspectiva crítica y no como revisión
  sistemática.
- El AI Act sostendrá únicamente una afirmación acotada sobre transparencia e
  interpretación de resultados de sistemas de alto riesgo; no se presentará como
  garantía general de explicabilidad.
- Ninguna de estas doce fuentes se añadió todavía a `references.bib` o
  `references_apa7.md`, porque el manuscrito actual aún no las cita.

### Brechas identificadas para la pasada primaria dirigida

- Evidencia primaria sobre explicaciones bajo cambio de distribución y monitoreo en
  producción.
- Casos primarios de XAI operacional en ciberseguridad y validación de sistemas
  autónomos.
- Estudios primarios revisados por pares sobre fidelidad de explicaciones de LLM o
  sistemas multimodales.
- Fuente específica para educación o servicios públicos solo si ese ejemplo opcional
  se convierte en una subsección completa.

## Pasada primaria dirigida: 2026-09-28

Objetivo: cerrar o acotar los vacíos que impedían modificar el outline de producción.

### Fuentes aceptadas

- `Lakkaraju et al. (2020)` — estudio ICML/PMLR sobre explicaciones globales robustas
  y estables frente a conjuntos declarados de cambios de distribución. Admisible para
  afirmar que una explicación ajustada a una distribución puede perder adecuación
  cuando esa distribución cambia; no admisible como prueba de robustez universal en
  producción.
- `Roch et al. (2026)` — estudio de usuarios de USENIX Security sobre bloqueo de
  dominios maliciosos. Admisible como counterevidence específica: en esa tarea, las
  explicaciones no mejoraron desempeño ni confianza. No generalizar a todas las tareas
  o interfaces de ciberseguridad.
- `Kaufman et al. (2025)` — estudio CHI en conducción simulada. Admisible para mostrar
  que errores en las explicaciones pueden degradar juicios de confianza y dependencia,
  aun con conducción idéntica. No usar como medición de seguridad del vehículo.
- `Turpin et al. (2023)` — experimento NeurIPS con intervenciones de sesgo en prompts.
  Admisible para afirmar que ciertos racionales de cadena de pensamiento omiten
  factores que influyen en la respuesta y pueden racionalizar respuestas sesgadas.
- `Zaman y Srivastava (2026)` — counterevidence ACL sobre los límites de usar la
  verbalización de pistas como única métrica. Obliga a presentar la fidelidad de cadena
  de pensamiento como un problema de evaluación multidimensional y todavía debatido.

### Resultado de la pasada

- Cambio de distribución: cerrado para el claim conceptual; evidencia longitudinal de
  despliegue permanece abierta.
- Ciberseguridad: cerrado para un ejemplo humano acotado.
- Sistemas autónomos: cerrado para el riesgo de una explicación errónea sobre juicios
  humanos; no se afirmará efecto directo sobre seguridad operacional.
- LLM: cerrado como controversia empírica con evidencia y counterevidence; la
  multimodalidad amplia permanece como agenda, no como resultado demostrado.
- Total de staging: 17 fuentes verificadas, ninguna añadida todavía a las bibliografías
  de producción.

## Unidad de redacción de fundamentos: 2026-09-29

Objetivo: reescribir las secciones 02 y 03 desde la arquitectura science-first y
transferir solo las fuentes nuevas efectivamente citadas.

### Fuentes promovidas a producción

- `@phillips2021` — citado para separar existencia, significado, exactitud de la
  explicación y límites de conocimiento, y para sostener que audiencias distintas
  requieren explicaciones distintas.
- `@tabassi2023` — citado para ubicar explicabilidad e interpretabilidad dentro de un
  conjunto más amplio de características de IA confiable y del ciclo de gestión del
  riesgo.
- `@europeanparliament2024` — citado únicamente para los requisitos estrechos de los
  artículos 13 y 14 sobre interpretación por responsables del despliegue y
  supervisión humana de sistemas de alto riesgo dentro del ámbito del Reglamento. No
  se infiere un derecho universal a una explicación técnica ni eficacia de un método.
- `@kim2024` — citado para distinguir calidad de la explicación en contexto,
  interacción humano-IA y desempeño conjunto; no se extrapolan los recuentos de su
  corpus como prevalencia del campo.
- `@alufaisan2021` — citado como resultado humano acotado: en las tareas estudiadas,
  añadir información explicativa no produjo evidencia concluyente de una mejora
  adicional en la exactitud decisional.
- `@poursabzi2021` — citado como counterevidence acotada: la transparencia facilitó
  simular un modelo sencillo, pero no garantizó dependencia apropiada ni corrección de
  errores en las condiciones experimentales estudiadas.

Los seis registros se añadieron a `references.bib` y `references_apa7.md`. Los once
candidatos restantes no pasaron a producción porque todavía no aparecen en la prosa.

### Control de alcance

- La sección 02 ya no adelanta el catálogo de métodos ni los resultados del benchmark;
  establece funciones, audiencias, ciclo de vida, gobernanza y límites de evidencia
  humana.
- La sección 03 concentra el vocabulario conceptual: interpretabilidad,
  explicabilidad, transparencia, diseño interpretable, post-hoc, escala, objeto,
  fidelidad, estabilidad, robustez y utilidad.
- Las afirmaciones de Alufaisan et al. y Poursabzi-Sangdeh et al. se mantienen ligadas
  a sus tareas y manipulaciones; no se formula que las explicaciones nunca mejoren la
  decisión humana.
- El alcance de FOM-7 permanece funcionalmente fundamentado y no se amplía a utilidad
  humana, causalidad, justicia, seguridad o impacto de despliegue.

## Pasada de enriquecimiento OA: 2026-07-04

Objetivo: reforzar afirmaciones sobre evaluación multidimensional, límites de transferencia de métricas, distinción entre evaluación funcional y estudios con usuarios, y necesidad de benchmarks trazables.

### Bases consultadas

- Semantic Scholar Graph API:
  - Búsquedas temáticas intentadas: evaluación XAI, OpenXAI, Quantus, evaluación human-grounded y benchmark functionally-grounded.
  - Resultado: la búsqueda general devolvió HTTP 429 por límite del *shared rate pool* sin API key.
  - Consultas por identificador con resultado parcial:
    - `DOI:10.1145/3583558` → `@nauta2023`, Semantic Scholar paperId `7caaafd5a3ee033c98e792c7ea5b699d005753d5`, OA confirmado, PDF ACM registrado.
    - `DOI:10.1016/j.neucom.2024.128282` → `@pawlicki2024`, Semantic Scholar paperId `c44d4ef36b44e4d40861c900881e7153a2cbf958`, OA confirmado.
    - `ARXIV:2202.06861` → `@hedstrom2023`, Semantic Scholar paperId `30e776268268e84becd2863b0632247da61238b9`, identificado como Quantus/JMLR/arXiv.
    - `ARXIV:2206.11104` → `@agarwal2022`, Semantic Scholar paperId `868e35374cb9c0fc6e4cfb17f96835aefcf520cc`, identificado como OpenXAI/arXiv.
- OpenAlex:
  - `@nauta2023` → OpenAlex `W4321786089`, DOI `10.1145/3583558`, OA híbrido, ACM Computing Surveys.
  - `@canha2025` → OpenAlex `W4410705990`, DOI `10.1145/3737445`, OA verde, ACM Computing Surveys.
  - `@pawlicki2024` → OpenAlex `W4401009060`, DOI `10.1016/j.neucom.2024.128282`, OA híbrido, Neurocomputing.
  - `@bhattacharya2024` → OpenAlex `W4400106588`, DOI `10.1145/3631700.3664911`, OA verde, UMAP Adjunct.
  - `@doshi-velez2017` → OpenAlex `W2594475271`, DOI `10.48550/arXiv.1702.08608`, OA verde, arXiv.
- Crossref:
  - DOI metadata verified for `@nauta2023`, `@canha2025`, `@pawlicki2024`, and `@bhattacharya2024`.
  - Crossref returned 404 for arXiv DOI lookups `10.48550/arXiv.1702.08608`, `10.48550/arXiv.2202.06861`, and `10.48550/arXiv.2206.11104`; these remain verified through OpenAlex/Semantic Scholar/arXiv/JMLR URLs rather than Crossref.

### Fuentes aceptadas para esta pasada

- `@nauta2023` — aceptada para respaldar que la evaluación XAI requiere métodos cuantitativos, multidimensionales y dependientes del tipo de explicación.
- `@canha2025` — aceptada para respaldar el encuadre *functionally-grounded* y los límites de generalización de benchmarks funcionales.
- `@pawlicki2024` — aceptada para respaldar la necesidad de múltiples métricas en evaluación XAI.
- `@bhattacharya2024` — aceptada para respaldar la evaluación multidimensional y la estandarización de criterios para métodos XAI diversos.
- `@doshi-velez2017` — aceptada para respaldar la distinción entre evaluación funcional, *human-grounded* y *application-grounded*.
- `@hedstrom2023` y `@agarwal2022` — conservadas como soporte de herramientas/benchmarks de evaluación; se añadieron URLs OA a las referencias de trabajo.

### Fuentes no aceptadas o no usadas

- Búsquedas generales de Semantic Scholar no produjeron candidatos adicionales por HTTP 429.
- No se añadieron fuentes nuevas solo por actualidad; las fuentes aceptadas ya tenían correspondencia directa con afirmaciones presentes en las secciones 09 y 10.

## Pasada de enriquecimiento fundamentos XAI: 2026-07-04

Objetivo: fortalecer `03_fundamentos_xai.md` con distinciones verificadas sobre interpretabilidad, explicabilidad, transparencia, artefactos post-hoc, alcance local/global, plausibilidad, fidelidad, estabilidad, robustez y evaluación funcional bajo FOM-7.

### Bases consultadas

- Semantic Scholar Graph API:
  - Consulta por DOI con resultado aceptado:
    - `DOI:10.1073/pnas.1900654116` → `@murdoch2019`, Semantic Scholar paperId `b9518627db25f05930e931f56497602363a75491`, CorpusId `204755862`, OA confirmado, PDF PNAS registrado.
    - `DOI:10.1002/widm.1493` → `@marcinkevics2023`, Semantic Scholar paperId `7297439e3d43ac95080c9a572b2a925cdc8f9765`, CorpusId `257290340`, OA confirmado, PDF Wiley registrado.
    - `DOI:10.1016/j.artint.2018.07.007` → `@miller2019`, Semantic Scholar paperId `e89dfa306723e8ef031765e9c44e5f6f94fd8fda`, CorpusId `36024272`, OA confirmado, PDF arXiv `1706.07269` registrado.
  - Consultas por DOI con HTTP 429 en el *shared rate pool*: `@lipton2018`, `@nauta2023`, `@schwalbe2023`, `@rudin2022`.
  - Búsqueda temática `explainable AI evaluation fidelity stability robustness metrics` devolvió HTTP 429; se usaron OpenAlex y Crossref para cross-check de candidatos ya identificados por DOI.
- OpenAlex:
  - `@murdoch2019` → OpenAlex `W2910705748`, DOI `10.1073/pnas.1900654116`, OA bronce, PNAS.
  - `@marcinkevics2023` → OpenAlex `W4322621694`, DOI `10.1002/widm.1493`, OA híbrido, WIREs Data Mining and Knowledge Discovery.
  - `@nauta2023` → OpenAlex `W4321786089`, DOI `10.1145/3583558`, OA híbrido, ACM Computing Surveys.
  - `@schwalbe2023` → OpenAlex `W4313650676`, DOI `10.1007/s10618-022-00867-8`, OA híbrido, Data Mining and Knowledge Discovery.
  - `@rudin2022` → OpenAlex `W3137125108`, DOI `10.1214/21-SS133`, OA diamante, Statistics Surveys.
  - `@miller2019` → OpenAlex `W2670253439`, DOI `10.1016/j.artint.2018.07.007`, OA verde, arXiv PDF `1706.07269`.
- Crossref:
  - DOI metadata verified for `@lipton2018`, `@murdoch2019`, `@marcinkevics2023`, `@nauta2023`, `@schwalbe2023`, `@rudin2022`, and `@miller2019`.
  - Crossref confirmed `@miller2019` as journal article in *Artificial Intelligence*, published 2019-02.

### Fuentes aceptadas para esta pasada

- `@miller2019` — añadida para respaldar que las explicaciones tienen una dimensión contrastiva y social, sin convertir plausibilidad para una audiencia en fidelidad técnica.
- `@murdoch2019` — reutilizada para respaldar definiciones y métodos de aprendizaje interpretable.
- `@marcinkevics2023` y `@schwalbe2023` — reutilizadas para respaldar distinciones entre familias de métodos, conceptos y salidas explicativas.
- `@nauta2023`, `@canha2025`, `@pawlicki2024`, `@bhattacharya2024`, `@hedstrom2023` y `@zheng2025` — reutilizadas para sostener evaluación cuantitativa, multidimensional, proxy-based y dependiente del constructo.
- `@lipton2018`, `@rudin2022`, `@doshi-velez2017` y `@alvarezmelis2018` — reutilizadas para sostener ambigüedad conceptual, preferencia por modelos interpretables cuando corresponde, alcance de evaluación funcional y límites de robustez.

### Fuentes no aceptadas o no usadas

- No se aceptaron candidatos nuevos a partir de búsqueda temática porque Semantic Scholar devolvió HTTP 429.
- No se añadieron fuentes adicionales sobre explicabilidad human-centered más allá de `@miller2019`, ya que el capítulo no evalúa usuarios ni comprensión subjetiva.

## Referencias sin cita en texto

Tras las pasadas de redacción controlada, las referencias fundacionales y de evaluación más relevantes ya se citan en el manuscrito. Antes del envío debe ejecutarse una revisión final para detectar entradas remanentes en `references/references.bib` que no aparezcan en `manuscript/*.md`.

## Citas sin entrada bibliográfica

- Ninguna detectada en esta pasada. Las futuras citas del manuscrito deben cotejarse contra `references/references.bib`.

## DOI pendientes

- `@alvarezmelis2018`: entrada arXiv con URL; sin DOI en la fuente de tesis.
- `@hedstrom2023`: sin DOI JMLR registrado en la entrada de trabajo; URL oficial JMLR y arXiv `2202.06861` añadidos.
- `@agarwal2022`: sin DOI NeurIPS registrado en la entrada de trabajo; URL arXiv `2206.11104` añadida.
- `@zheng2025`: entrada fuente usa URL del proyecto; verificar DOI/publicación final si existe.

## URL pendientes de validación

- `https://arxiv.org/abs/1806.08049` (`@alvarezmelis2018`).
- `https://trustai4s-lab.github.io/ffidelity` (`@zheng2025`).
- Página oficial de Quantus/JMLR para `@hedstrom2023` registrada en la pasada OA de 2026-07-04.
- Página arXiv/OpenXAI para `@agarwal2022` registrada en la pasada OA de 2026-07-04.

## Figuras/tablas que requieren fuente

- `tables/table_metrics.md`: derivada de `thesis/capitulo-1-marco-teorico.qmd` y `thesis/capitulo-3-diseno-experimental.qmd`.
- `tables/table_methods_comparison.md`: debe cotejarse con `thesis/capitulo-2-fundamentos.qmd` y las referencias fundacionales de cada método.
- Futuras figuras copiadas desde `thesis/assets/figures/` deberán registrarse en `figures/figure_registry.md` con fuente exacta.
