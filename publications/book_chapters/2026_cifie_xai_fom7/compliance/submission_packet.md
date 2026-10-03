# Paquete de envío

## Estado actual (2026-10-03)

El capítulo está en revisión científica y editorial; no está listo para envío. La
lista de trabajo es la "Consolidated pending list" de
`planning/science_first_revision_plan_2026-09-28.md`, y el diagnóstico editorial está
en `editorial/editorial_compliance_assessment_2026-09-30.md`.

## Entregables exigidos por TintAzul / CIFIE

| Entregable | Base | Estado |
| --- | --- | --- |
| Capítulo en la plantilla oficial (Word) | `editorial/GUÍA-PLANTILLA.docx`; build `scripts/build_cifie_chapter.py` | Pendiente [E-FMT, contenido pendiente] |
| Lista de verificación del autor, firmada | `editorial/CHECKLIST DEL AUTOR.docx`; estado en `compliance/author_checklist_working.md` | Pendiente [E-FORMS] |
| Declaración de autoría, originalidad y uso de IA, firmada por todos los autores | `editorial/DECLARACIÓN DE AUTORÍA.docx` | Pendiente de decisiones E-AI, E-AUTH y E-PRIOR [E-FORMS] |
| Licencia de publicación y cesión limitada de derechos, firmada | `editorial/LICENCIA DE PUBLICACIÓN Y CESIÓN LIMITADA DE DEREC.docx` | Pendiente [E-FORMS] |
| Hoja de diseño editorial | `manuscript/00_hoja_diseno_editorial.md` (no se publica) | Actualizar a los campos de la plantilla; confirmar si se entrega [E-FRONT, E-Q1] |

## Figuras actuales del capítulo

El borrador contiene diez figuras activas, todas mencionadas en el texto antes de
aparecer y con caption que declara una fuente bibliográfica o los datos internos de
elaboración propia. El mapeo y las fuentes están auditados en
`figures/figure_registry.md`.

1. `figures/exported/fig_d1_conceptos_es.png` (conceptos: interpretabilidad, explicabilidad y transparencia)
2. `figures/exported/fig_d2_modelos_es.png` (modelos interpretables y explicaciones post-hoc)
3. `figures/exported/fig_d4_objetos_explicativos_es.png` (objetos explicativos)
4. `figures/exported/fig_d6_niveles_evaluacion_es.png` (niveles de evaluación y FOM-7)
5. `figures/exported/fig_d5_ciclo_audiencias_es.png` (ciclo de vida y audiencias)
6. `figures/exported/fig_d7_cadena_evidencia_es.png` (cadena de evidencia)
7. `figures/exported/fig_d8_fom7_traza_es.png` (puertas FOM-7 y traza H1)
8. `figures/exported/fig_cobertura_exp2_es.png` (cobertura analítica EXP2)
9. `figures/exported/fig_cd_diagram_es.png` (diferencias críticas de Nemenyi)
10. `figures/exported/fig_estabilidad_coste_es.png` (estabilidad y coste)

La aptitud final para impresión y la retención en el paquete de envío siguen sujetas
a E-FIG y a los requisitos de producción del editor. Los exports históricos no
utilizados no forman parte de esta lista.

La figura de diferencias pareadas SHAP-LIME fue retirada el 2026-09-27 (resultados de
Paper B+C).

## Pasos para el paquete final

1. Resolver la pista A (decisiones y consultas al editor).
2. Completar las pistas B y C de la lista consolidada.
3. Construir el Word desde un estado confirmado de la rama y registrar el hash.
4. Revisar cada página en un render de Microsoft Word.
5. Completar y firmar los tres formularios.
6. Reunir los archivos en `final/submission_package/`.
