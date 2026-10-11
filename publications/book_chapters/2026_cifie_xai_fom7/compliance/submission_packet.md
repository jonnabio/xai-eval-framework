# Paquete de envío

## Estado actual (2026-10-10)

El paquete de envío completo ha sido preparado y depositado en:
`publications/book_chapters/2026_cifie_xai_fom7/final/submission_package/`.

El manuscrito final cumple con el límite editorial (8.019 palabras < 9.000 palabras), incluye las 14 figuras activas citadas y auditadas, la separación diagramática de los axiomas de Shapley en la página 13, maquetación dual (color digital y monocromática para imprenta) y todos los formatos de TintAzul listos para revisión y firma del autor.

## Entregables exigidos por TintAzul / CIFIE

| Entregable | Base | Estado en `final/submission_package/` |
| --- | --- | --- |
| Capítulo en la plantilla oficial (Word y PDF, Color y B/N) | `01_capitulo/` | **Completado y generado** (`capitulo_cifie_xai_fom7_color.docx`, `.pdf`, `..._bn_impresion.docx`, `.pdf`) |
| Figuras independientes (Color, B/N y Vectoriales) | `02_figuras/` | **Completado** (14 figuras en `digital_color/`, `vectorial_editable/`, `impresion_bn/`) |
| Lista de verificación del autor | `03_formatos_editoriales_tintazul/CHECKLIST DEL AUTOR.docx` | **Preparado** (pendiente firma del autor; ver `CHECKLIST_REVISION_ENVIO_AUTOR.md`) |
| Declaración de autoría, originalidad y uso de IA | `03_formatos_editoriales_tintazul/DECLARACIÓN DE AUTORÍA.docx` | **Preparado** (pendiente firma del autor; ver instrucciones de decisiones E-AI, E-AUTH y E-PRIOR) |
| Licencia de publicación y cesión limitada de derechos | `03_formatos_editoriales_tintazul/LICENCIA DE PUBLICACIÓN...docx` | **Preparado** (pendiente firma del autor) |
| Guías y rúbrica oficial de evaluación | `03_formatos_editoriales_tintazul/` | **Disponibles para consulta** (`GUÍA-PLANTILLA`, `GUÍA RÁPIDA APA`, `RÚBRICA OFICIAL`) |

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
