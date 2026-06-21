# Pase editorial v2

Fecha: 2026-06-20

Archivo principal revisado: `cifie_xai_fom7_v2_technical_draft.md`

## Estado general

- Versión técnica v2 ensamblada desde los archivos seccionales `manuscript/01_*.md` a `manuscript/11_*.md`.
- Extensión aproximada: 10,542 palabras, incluyendo referencias.
- Figuras: 7 figuras copiadas y referenciadas con rutas relativas válidas desde `drafts/v2_technical_draft/`.
- Tablas: 4 tablas de trabajo numeradas como Tabla 1 a Tabla 4.
- Referencias: lista APA 7 de trabajo poblada en `references/references_apa7.md`.

## Revisión de ancho de tablas

| Tabla | Riesgo editorial | Acción recomendada |
| ----- | ---------------- | ------------------ |
| Tabla 1. Métricas primarias del benchmark | Alta anchura por 7 columnas y definiciones extensas. | En plantilla Word, usar orientación horizontal o dividir en definición operacional + implementación/uso. |
| Tabla 2. Comparación de métodos XAI | Alta anchura por 6 columnas con celdas narrativas. | Dividir en dos tablas si CIFIE exige página vertical: base/salida y fortalezas/límites/uso. |
| Tabla 3. Puertas del protocolo FOM-7 | Alta anchura por 6 columnas y artefactos largos. | Priorizar como tabla horizontal; alternativa: convertir a lista numerada con subcampos. |
| Tabla 4. Resumen de resultados empíricos | Riesgo alto por varias subtablas con 7-8 columnas. | Mantener como tabla de trabajo; en versión final seleccionar solo subtablas esenciales o mover trazabilidad a anexo. |

Corrección aplicada: la fórmula de parsimonia en la Tabla 1 usa `\lvert w_i\rvert` para evitar que los delimitadores verticales rompan el parseo Markdown de columnas.

## Revisión APA 7

- `references/references_apa7.md` contiene una lista de trabajo basada en `references/references.bib`.
- Se conservaron DOI o URL cuando estaban disponibles en la bibliografía del capítulo.
- Pendiente de revisión final: cursivas, sangría francesa, capitalización exacta de títulos y datos editoriales de proceedings.
- Pandoc no está disponible en este entorno, por lo que no se generó una bibliografía renderizada automáticamente desde CSL.

## Revisión de formato CIFIE

- Título, autoría, afiliación y ORCID incluidos en el borrador técnico.
- Resumen y palabras clave incluidos al inicio.
- Estructura argumental completa: introducción, fundamentos, métodos, crisis de evaluación, FOM-7, diseño, resultados, discusión, limitaciones y conclusiones.
- Figuras numeradas en orden de primera aparición.
- Tablas numeradas y listas para adaptación a plantilla editorial.

## Pendientes antes de envío

- Confirmar límite real de palabras de CIFIE; la versión técnica v2 supera la recomendación inicial de 7,000-8,500 palabras.
- Convertir tablas anchas al formato de la plantilla oficial cuando esté disponible.
- Revisar si las citas deben permanecer como claves Markdown (`[@clave]`) o convertirse a formato narrativo APA en el manuscrito final.
- Validar DOI/URL faltantes o dudosos en la lista APA 7.
- Generar versión final en `drafts/v3_editorial_review/` después de la reducción de extensión y adaptación a plantilla.
