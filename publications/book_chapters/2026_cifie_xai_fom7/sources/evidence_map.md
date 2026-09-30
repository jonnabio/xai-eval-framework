# Mapa de evidencia para la revisión científica del capítulo CIFIE

**Estado:** reconciliado con la sincronización del 2026-09-27 y el scaffold del
2026-09-28

**Alcance:** arquitectura de afirmaciones, fuentes y límites; no sustituye el registro
de claims numéricos

Este mapa controla la transición desde el manuscrito técnico actual hacia un capítulo
general, científico y legible. Separa cuatro clases de soporte: literatura publicada,
marcos o normas oficiales, evidencia empírica protegida del proyecto y síntesis
editorial explícitamente identificada. Las fuentes candidatas verificadas se registran
en `references/candidate_literature_2026-09-28.md`; seis pasaron a la bibliografía de
producción el 2026-09-29 al ser citadas en las secciones 02-03.

## Matriz de sección, afirmación y evidencia

| Sección objetivo | Función argumental | Afirmaciones principales | Evidencia admisible | Límites obligatorios | Estado |
| --- | --- | --- | --- | --- | --- |
| 01. Resumen y palabras clave | Sintetizar problema, alcance general, FOM-7 y demostración empírica. | Producir una explicación no demuestra su validez; FOM-7 organiza evidencia funcionalmente fundamentada; el benchmark ilustra el protocolo. | Solo fuentes y resultados ya desarrollados en el cuerpo. | No introducir evidencia nueva ni rankings universales. | Diferir hasta cerrar las secciones 02-10 |
| 02. Por qué importa la XAI | Explicar funciones, audiencias y riesgos de la explicación. | Las necesidades cambian por audiencia y propósito; la XAI puede apoyar depuración, supervisión, auditoría y contestabilidad; no garantiza confiabilidad. | Phillips et al.; Tabassi; AI Act; Kim et al.; estudios humanos de Alufaisan et al. y Poursabzi-Sangdeh et al.; literatura conceptual existente. | Distinguir utilidad potencial, obligación de transparencia, confianza subjetiva y mejora real de decisiones. | Redactada y referenciada el 2026-09-29; resultados humanos limitados a sus tareas |
| 03. Qué es y qué no es la XAI | Definir el campo y sus distinciones centrales. | XAI es una familia de métodos y prácticas sociotécnicas; transparencia, interpretabilidad y explicación post-hoc no son sinónimos; local/global y modelo/datos/decisión son ejes diferentes. | Lipton; Miller; Murdoch et al.; Marcinkevičs y Vogt; Schwalbe y Finzel; Rudin et al.; Phillips et al.; Tabassi; Kim et al. | Plausibilidad no equivale a fidelidad; atribución no equivale a causalidad. | Taxonomía consolidada en prosa el 2026-09-29 |
| 04. Ámbitos de aplicación y horizontes próximos | Presentar ejemplos concretos y necesidades específicas por dominio. | Salud, finanzas, ciberseguridad, sistemas autónomos y modelos fundacionales requieren explicaciones para actores, decisiones y riesgos diferentes. | WHO y Ghassemi et al.; Weber et al.; Rjoub et al.; Kuznietsov et al.; Zhao et al.; evidencia primaria adicional donde se afirme un efecto concreto. | Cada ejemplo debe incluir decisión, actor, riesgo, evidencia útil y brecha; no presentar adopción futura como hecho. | Cinco dominios con fuente panorámica verificada; evidencia primaria selectiva aún abierta |
| 05. Familias explicativas y problema de evaluación | Relacionar preguntas con objetos explicativos y métricas. | Atribuciones, reglas, contrafactuales y modelos sustitutos responden preguntas distintas; no deben reducirse a una métrica universal. | Ribeiro et al.; Lundberg y Lee; Mothilal et al.; Wachter et al.; Karimi et al.; Nauta et al.; Quantus; OpenXAI; tabla de métodos. | Comparar constructos homogéneos y declarar qué objeto evalúa cada métrica. | Fuentes actuales suficientes; requiere compresión del catálogo técnico |
| 06. Brechas científicas de la XAI | Organizar brechas técnicas, de constructo, humanas, causales, operativas, de gobernanza y de modelos emergentes. | La evaluación es multidimensional; la validez humana está poco estandarizada; explicaciones persuasivas pueden no mejorar decisiones; distribución, seguridad y LLM amplían los problemas de fidelidad. | Doshi-Velez y Kim; Nauta et al.; Pawlicki et al.; Bhattacharya y Verbert; Kim et al.; Alufaisan et al.; Poursabzi-Sangdeh et al.; Lakkaraju et al.; Slack et al.; Zhao et al.; Turpin et al.; Zaman y Srivastava. | No generalizar un resultado humano a todos los usuarios o tareas; separar ausencia de evidencia de evidencia de ausencia; presentar la fidelidad de cadena de pensamiento como problema dependiente de métrica. | Taxonomía y evidencia primaria suficientes para el scaffold; despliegue longitudinal y multimodalidad amplia permanecen abiertos |
| 07. FOM-7 como respuesta metodológica | Presentar siete puertas y su alcance. | FOM-7 alinea diseño, artefactos, constructos, métricas, inferencia, reproducibilidad y claims. | Tesis, tabla FOM-7, registro de claims y artefactos calificados. | FOM-7 gobierna evaluación comparativa funcional; no demuestra utilidad humana, causalidad ni impacto de despliegue. | Verificado en material interno |
| 08. Caso empírico: de benchmark a evidencia auditable | Demostrar FOM-7 con Adult/tabular. | El diseño, cobertura, jerarquía de análisis y resultados protegidos muestran por qué la auditabilidad precede al ranking. | Tesis, `pub/claims.toml`, RIMI/artefactos registrados, tablas y figuras calificadas. | Mantener dataset, modelos, semillas, tamaños, unidad de análisis, cobertura y alcance; excluir resultados no publicados de Paper B+C. | Sincronizado y protegido por cobertura/exclusividad |
| 09. Implicaciones para investigación, práctica y gobernanza | Traducir los hallazgos a decisiones de selección y documentación. | No existe un método universalmente dominante; la evidencia requerida depende de objetivo, actor, riesgo y ciclo de vida. | Síntesis de secciones 02-08; NIST AI RMF; fuentes de dominio. | Presentar como síntesis razonada y no como efecto empírico universal. | Dependiente de la redacción de secciones 02-08 |
| 10. Limitaciones y agenda científica | Separar límites del caso y agenda general. | El caso es tabular y funcionalmente fundamentado; la agenda requiere validez humana, causal, operacional y multimodal. | Limitaciones verificadas de la tesis; taxonomías de evaluación; candidatos humanos y LLM. | No convertir una carencia del benchmark en carencia universal del campo sin revisión. | Base suficiente; prioridades deben cerrarse después de secciones 04 y 06 |
| 11. Conclusiones | Responder a la tesis central. | Una explicación se vuelve evidencia defendible solo cuando propósito, objeto, evaluación, trazabilidad y límite inferencial están alineados. | Síntesis completa del capítulo. | Concluir en proporción a la evidencia; FOM-7 conserva alcance acotado. | Diferir hasta cerrar el cuerpo |

## Afirmaciones empíricas protegidas

Estas afirmaciones ya están sincronizadas con el registro del proyecto. Cualquier
cambio numérico o de alcance exige actualizar primero el registro correspondiente y
ejecutar los verificadores.

| Afirmación admisible | Fuente de control | Límite de redacción | Estado |
| --- | --- | --- | --- |
| EXP2 compara LIME, SHAP, Anchors y DiCE sobre UCI Adult Income bajo el diseño declarado en el manuscrito. | Tesis, `pub/claims.toml`, `07_diseno_empirico.md` | No extrapolar a otras modalidades, datasets o implementaciones. | Verificada y cubierta |
| La auditoría distingue celdas planificadas, calificadas y excluidas antes de la inferencia. | Registro de claims, tabla de resultados, figura de cobertura | Conservar la definición de celda y la razón de exclusión. | Verificada y cubierta |
| En la operacionalización del capítulo existen diferencias globales entre métodos en fidelidad y estabilidad. | Tesis, tabla de resultados, `08_aplicacion_empirica_perfiles_fom7.md` | Reportar bloques, prueba, ajuste y alcance; evitar “superioridad general”. | Verificada y cubierta |
| SHAP presenta el perfil más fuerte de fidelidad y estabilidad dentro del benchmark declarado. | Tesis, registro de claims, tablas/figuras calificadas | Restringir a este benchmark, métricas y agregación. | Verificada y cubierta |
| LIME conserva una ventaja relativa de coste, con menor estabilidad bajo la operacionalización utilizada. | Tesis, registro de claims, figura calidad-coste | Evitar la etiqueta no acotada “inestabilidad estructural”. | Verificada y cubierta |
| Anchors y DiCE producen objetos distintos de una atribución de características y requieren métricas compatibles con reglas y contrafactuales. | Fuentes fundacionales, diseño del benchmark, resultados calificados | No interpretar una métrica de atribución como juicio total sobre reglas o contrafactuales. | Verificada; límite de constructo obligatorio |
| FOM-7 transforma resultados en claims trazables mediante siete puertas operativas. | Tabla FOM-7, tesis y pipeline registrado | Presentarlo como protocolo del capítulo, no como estándar universal validado externamente. | Verificada en extracción |

## Matriz de evidencia nueva prioritaria

| ID del scaffold | Afirmación prevista | Fuente candidata principal | Fuente de contraste o límite | Estado de primera pasada |
| --- | --- | --- | --- | --- |
| G02 | XAI puede apoyar depuración, supervisión, auditoría y contestabilidad. | Phillips et al. (2021); Tabassi (2023) | AI Act para un requisito jurídico estrecho | Incorporada en sección 02; ejemplos concretos quedan para los dominios |
| G03 | La explicabilidad no basta para una IA confiable. | Tabassi (2023); WHO (2021) | Ghassemi et al. (2021) | Incorporada en secciones 02-03; WHO y Ghassemi se reservan para salud |
| G04 | La evaluación humana carece de estandarización consistente. | Kim et al. (2024) | Doshi-Velez y Kim (2017) | Incorporada sin extrapolar recuentos del corpus revisado |
| G05 | Una explicación puede no mejorar la decisión o la corrección del error. | Alufaisan et al. (2021); Poursabzi-Sangdeh et al. (2021) | Kim et al. (2024) | Incorporada en sección 02 con límites explícitos de tarea y diseño |
| G06 | Una explicación ajustada a una distribución puede perder fidelidad o estabilidad bajo cambios relevantes. | Lakkaraju et al. (2020) | NIST AI RMF para monitoreo de ciclo de vida | Verificada para perturbaciones y familias explicativas declaradas; impacto longitudinal abierto |
| A01 | En salud, XAI puede apoyar interrogación del modelo sin validar una decisión clínica. | WHO (2021) | Ghassemi et al. (2021) | Verificada; añadir estudio primario solo si se reporta un efecto clínico concreto |
| A02 | Finanzas incluye crédito, riesgo, mercados, cartera y AML con cobertura desigual. | Weber et al. (2024) | AI Act solo para transparencia de alto riesgo cuando aplique | Verificada |
| A03 | En ciberseguridad, la utilidad de la explicación depende de la tarea y del conocimiento del analista. | Rjoub et al. (2023) | Roch et al. (2026); Slack et al. (2020) | Verificada con resultado humano acotado; no afirmar mejora general de desempeño o confianza |
| A04 | En sistemas autónomos, XAI contribuye a monitoreo y validación sin constituir por sí sola un caso de seguridad. | Kuznietsov et al. (2024) | Kaufman et al. (2025) sobre errores explicativos y juicio humano | Verificada para panorama y riesgo humano; seguridad operacional directa no demostrada |
| A05 | Los racionales de LLM pueden ser plausibles sin revelar todos los factores que influyen en la respuesta, y su fidelidad depende de cómo se mida. | Zhao et al. (2024); Turpin et al. (2023) | Zaman y Srivastava (2026) | Verificada como debate empírico; evitar “cadena de pensamiento siempre infiel” y extrapolación multimodal |

## Figuras, tablas y bibliografía

| Artefacto | Función futura | Estado reconciliado |
| --- | --- | --- |
| `tables/table_methods_comparison.md` | Resumir pregunta, salida, fortaleza y fallo por familia explicativa. | Existente; revisar durante la compresión de la sección 05 |
| `tables/table_fom7_gates.md` | Presentar las siete puertas y sus controles. | Existente y verificada contra el manuscrito actual |
| `tables/table_metrics.md` | Definir métricas del caso empírico. | Existente; conservar en la sección 08, no como taxonomía universal |
| `tables/table_results_summary.md` | Reportar resultados protegidos y sus límites. | Sincronizada el 2026-09-27 y cubierta por guards |
| `figures/exported/` y `figures/figure_registry.md` | Ilustrar cobertura y perfiles empíricos sin redundancia. | Seis figuras registradas; una figura pareada fue retirada por exclusividad |
| `references/references.bib` | Registros de obras citadas. | 48 referencias de producción; seis fuentes promovidas con la unidad 02-03 |
| `references/references_apa7.md` | Lista APA 7 incorporada por el build. | 48 obras de producción; revisión editorial final pendiente |
| `references/candidate_literature_2026-09-28.md` | Staging verificable para fuentes nuevas. | 17 candidatos verificados; seis promovidos y once todavía en staging |

## Secuencia de uso

1. Redactar cada nueva afirmación a partir de esta matriz y de la fuente completa, no
   a partir del título o del resumen aislado.
2. Transferir solo las fuentes efectivamente citadas a ambas representaciones
   bibliográficas y registrar la decisión en `citation_audit.md`.
3. Mantener juntos, en la misma unidad de cambio, claim, cita, límite y referencia.
4. Ejecutar `verify_claims.py` después de cualquier movimiento o edición de números
   protegidos y comprobar `[exclusivity]`.
5. Construir y revisar visualmente el Word al terminar cada unidad estructural.

## Controles de calidad

- Toda cifra debe conservar fuente, unidad de análisis, agregación y alcance.
- Una revisión sistemática puede sostener un mapa de campo, pero no sustituye el
  estudio primario cuando se afirma un efecto concreto.
- Una norma o regulación sostiene obligaciones o principios, no la eficacia de un
  método XAI.
- Una explicación plausible, legible o persuasiva no se describirá como fiel sin
  evidencia específica de fidelidad.
- Ningún resultado no publicado de Paper B+C puede entrar al capítulo.
- Toda referencia final debe aparecer citada y toda cita debe tener registro APA 7.
