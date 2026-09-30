# Paquete de envío

## Estado actual (2026-09-30)

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

- `figures/exported/fig_cobertura_exp2_es.png` (Figura 1)
- `figures/exported/fig_cd_diagram_es.png` (Figura 2)
- `figures/exported/fig_boxplots_metricas_es.png` (Figura 3)
- `figures/exported/fig_estabilidad_coste_es.png` (Figura 4)
- `figures/exported/fig_correlacion_metricas_es.png` (Figura 5)
- `figures/exported/fig_radar_metodos_es.png` (Figura 6)

La figura de diferencias pareadas SHAP-LIME fue retirada el 2026-09-27 (resultados de
Paper B+C). La selección definitiva depende de E-FIG y de los requisitos de impresión
que confirme el editor.

## Pasos para el paquete final

1. Resolver la pista A (decisiones y consultas al editor).
2. Completar las pistas B y C de la lista consolidada.
3. Construir el Word desde un estado confirmado de la rama y registrar el hash.
4. Revisar cada página en un render de Microsoft Word.
5. Completar y firmar los tres formularios.
6. Reunir los archivos en `final/submission_package/`.
