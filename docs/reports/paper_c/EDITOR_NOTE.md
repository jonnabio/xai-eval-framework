# Paper C: note to the editor

**Status (2026-10-04):** draft for the author. Not sent. It goes in the body of the
submission email to `revistatm@tec.ac.cr`, above the list of attached files. The Spanish
text is the one to send; the English text is the same note for the record.

**Checks (2026-10-04, with the claim registry; pull request #27)**

1. **Item 3 against the manuscript: done.** Rewritten for the third draft: it names what the
   analysis inside each method found. Re-read it if the last revision changes those results.
2. **Item 1, nothing shared with Paper D: checked, wording changed.** Paper D prints no
   Paper C result. Eight short decimals are printed in both (0.001, 0.002, 0.005, 0.010,
   0.030, 0.039, 0.040, 0.42); each is a different quantity in each paper, and the registry
   records them as coincidences. The sentence now says "result", not "value".
3. **Item 2, what the 32-page edition already carries: checked, corrected.** It carries the
   fourteen all-case coefficients of Table 1 (first panel, and second panel with three
   calls) and three of the 21 coefficients of Table 3 (alternative rubric: completeness;
   pooled view: completeness and audit usefulness). It does not carry the label-stated
   view, the rest of Table 3, or the test-retest shares. The thesis chapter carries the
   same values, the other five pooled coefficients, and the largest score shift under the
   stated label and under the alternative rubric (0.14 and 0.50 points).
4. **Thesis not yet deposited: for the author.** Change the sentence if that is no longer so.

Also for the author: add the telephone number the journal asks for.

**Revision of 2026-10-05 (fourth draft; `PLAN.md`, section 18).** The table of the
sensitivity views was removed, so the tables are now 1 (all cases), 2 (inside each
explainer), 3 (technical metrics) and 4 (clean condition). Of the values that the 32-page
edition carries, the text still prints three outside Table 1: completeness under the
alternative rubric and completeness and audit usefulness in the pooled view. The two score
shifts that only the thesis carries (0.14 and 0.50) are no longer printed. Items 2 and 3
below were rewritten for this in both languages. **Not rechecked with the registry:** that
Paper D prints none of the new results (positive control, SHAP and LIME taken together);
`register_paper_c.py` does that check when it is run on the `pubs/*` branch.

`PLAN.md`, section 13, decision 7 said the editor is not asked about a second submission
"for now". This note does not ask; it states the fact.

## Text to send (Spanish)

Asunto: Envío de manuscrito, número especial de Inteligencia Artificial: "Do LLM Judges
Agree on the Quality of Explanations? A Two-Panel Reliability Study"

Estimado equipo editorial de *Tecnología en Marcha*:

Envío el manuscrito "Do LLM Judges Agree on the Quality of Explanations? A Two-Panel
Reliability Study" para el número especial de Inteligencia Artificial. Soy el único autor.
El manuscrito es original, no está publicado y no está en evaluación en otra revista.

Quiero informarles de tres hechos antes de la revisión:

1. **Otro envío mío al mismo número.** El 3 de octubre de 2026 envié a este número el
   manuscrito "Are explanations less reliable when the model is wrong? ...". Los dos
   trabajos usan el mismo banco de pruebas público, pero responden preguntas distintas y no
   comparten resultados: aquel estudia métricas técnicas de las explicaciones según el
   acierto del modelo; este estudia la concordancia entre jueces LLM. Ningún cuadro, figura
   o resultado aparece en los dos.

2. **Disponibilidad previa de parte de los resultados.** Una versión anterior y más amplia
   de este trabajo (32 páginas, que unía este estudio con otro) está en un repositorio
   público y en un archivo de Zenodo. Fue enviada a dos revistas, que la rechazaron en la
   evaluación editorial inicial, sin revisión por pares; hoy no está en evaluación en
   ninguna. Esa versión contiene parte de un cuadro de este manuscrito y tres valores del texto:
   los coeficientes de concordancia sobre todos los casos de ambos paneles (primera
   columna y columna de tres llamadas del cuadro 1) y tres coeficientes de la sección 3.3
   (completitud con la rúbrica alternativa; completitud y utilidad para auditoría en la
   vista agregada). Un capítulo de mi tesis doctoral, que aún no está depositada, contiene
   esos mismos valores. Ninguna de esas versiones se publicó en
   una revista o en actas.

3. **Lo que es nuevo en este manuscrito.** El análisis dentro de cada método de
   explicación (cuadro 2 y figura 1): la concordancia sobre todos los casos refleja sobre
   todo diferencias entre métodos; en los casos de SHAP las puntuaciones casi no varían, y
   en los de LIME la concordancia depende de cinco registros cuyos pesos se imprimen como
   cero. También son nuevos los coeficientes con una sola llamada y para la media del
   panel, la concordancia bruta, la relación de las puntuaciones con las métricas técnicas
   (cuadro 3), la condición sin métricas, con 576 llamadas nuevas (cuadro 4), y un control
   positivo con 711 llamadas nuevas, en el que 79 explicaciones se empeoran de dos maneras
   conocidas (sección 3.6). Las
   conclusiones del manuscrito se apoyan en estos análisis.

El código, los datos y las respuestas de los jueces están en un archivo público con DOI. El
archivo identifica al autor; por eso la versión anónima no da su dirección. Puedo retirar
el acceso público a la versión anterior o añadir una nota en ella si la revista lo
prefiere.

Adjunto la versión anónima y la versión completa en Word y la figura en TIFF.

Teléfono: [número]

Atentamente,
Jonathan Herrera-Vásquez

## The same note in English (for the record)

Subject: Manuscript submission, special issue on Artificial Intelligence: "Do LLM Judges
Agree on the Quality of Explanations? A Two-Panel Reliability Study"

Dear editorial team of *Tecnología en Marcha*,

I submit the manuscript "Do LLM Judges Agree on the Quality of Explanations? A Two-Panel
Reliability Study" to the special issue on Artificial Intelligence. I am the only author.
The manuscript is original, is not published and is not under review at another journal.

I want to tell you three facts before the review:

1. **Another submission of mine to the same issue.** On 3 October 2026 I sent to this issue
   the manuscript "Are explanations less reliable when the model is wrong? ...". The two
   papers use the same public benchmark, but they answer different questions and share no
   result: that one studies technical metrics of explanations by the correctness of the
   model; this one studies agreement among LLM judges. No table, figure or result appears in
   both.

2. **Earlier availability of part of the results.** An earlier and longer version of this
   work (32 pages, which joined this study with another) is in a public repository and in a
   Zenodo archive. It was sent to two journals, which rejected it at the initial editorial
   assessment, without peer review; it is not under review anywhere today. That version
   contains part of one table of this manuscript and three values of the text: the
   agreement coefficients over all cases for both panels (first column and three-call
   column of Table 1) and three coefficients of section 3.3 (completeness under the
   alternative rubric; completeness and audit usefulness in the pooled view). A chapter of
   my doctoral thesis, which is not yet deposited, contains the same values.
   None of those versions was published in a journal or in proceedings.

3. **What is new in this manuscript.** The analysis inside each explanation method (Table 2
   and Figure 1): agreement over all cases mostly reflects differences between methods;
   among SHAP cases the scores hardly vary, and among LIME cases agreement depends on five
   records whose weights print as zero. Also new are the coefficients for one call and for
   the panel mean, raw agreement, the relation of the scores with the technical metrics
   (Table 3), the condition without metrics, with 576 new calls (Table 4), and a positive
   control with 711 new calls, in which 79 explanations are made worse in two known ways
   (section 3.6). The
   conclusions of the manuscript rest on these analyses.

The code, the data and the judges' responses are in a public archive with a DOI. The
archive identifies the author, so the blind version does not give its address. I can
withdraw public access to the earlier version or add a note to it if the journal prefers.

I attach the blind and the full version in Word and the figure in TIFF.

Telephone: [number]

Sincerely,
Jonathan Herrera-Vásquez
