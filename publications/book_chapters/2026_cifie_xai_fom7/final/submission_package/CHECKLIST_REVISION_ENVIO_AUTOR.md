# Lista de Verificación y Guía de Revisión para el Autor

**Destino:** Envío formal del capítulo para el Libro Colectivo del Congreso Internacional CIFIE (Editorial TintAzul).  
**Autor:** Jonathan Herrera-Vásquez (Universidad Americana de Europa - UNADE).  
**Ubicación del paquete:** `publications/book_chapters/2026_cifie_xai_fom7/final/submission_package/`

---

## Resumen Ejecutivo de Cumplimiento Técnico

Antes de realizar la revisión visual humana, el asistente editorial automatizado ha certificado las siguientes métricas en el manuscrito actual:
- **Extensión total:** **8.019 palabras** (7.594 en cuerpo de texto + 425 en tablas). Se encuentra **981 palabras por debajo** del límite estricto de 9.000 palabras fijado por la editorial.
- **Disciplina de párrafos y legibilidad:** Cero oraciones superiores a 40 palabras; longitud media por frase de 17,6 palabras; Índice Flesch-Szigriszt = 41,0; Fernández-Huerta = 58,3.
- **Axiomas de Shapley (pág. 13):** Separados en cuatro párrafos individuales y numerados con sangrado y ecuaciones display LaTeX.
- **Figuras y tablas:** 14 figuras activas y 4 tablas consecutivas, todas con llamada previa en el texto (*callout*) y nota de procedencia/fuente APA 7.
- **Archivos generados:** Versiones duales digital a color y monocromática para imprenta en `.docx` y `.pdf`.

---

## FASE 1: Revisión Visual y Técnica del Manuscrito (Autor)

Abra los archivos ubicados en `01_capitulo/` (`capitulo_cifie_xai_fom7_color.docx` y `.pdf`) y verifique los siguientes puntos críticos:

### 1.1 Portada y Datos Institucionales
- [ ] **Título del capítulo:** *De la explicación a la evidencia: fundamentos, aplicaciones y evaluación auditable de la inteligencia artificial explicable*.
- [ ] **Subtítulo:** *El protocolo FOM-7 como marco operativo para comparaciones reproducibles*.
- [ ] **Nombre del autor:** Jonathan Herrera-Vásquez.
- [ ] **Grado académico:** Candidato a Doctor / M.Sc. (según requerimiento de la plantilla oficial).
- [ ] **Afiliación institucional:** Universidad Americana de Europa (UNADE).
- [ ] **ORCID:** `https://orcid.org/0000-0002-7149-6635`.
- [ ] **Correo institucional:** Confirmar que su dirección de contacto de correspondencia esté correctamente escrita.

### 1.2 Resumen y Palabras Clave
- [ ] **Resumen:** Contiene entre 150 y 250 palabras y responde sintéticamente a: tema central, problema/necesidad, objetivo general, método/FOM-7, aportación empírica y conclusiones.
- [ ] **Palabras clave:** Contiene exactamente de 3 a 5 términos normalizados (ej.: *Inteligencia artificial explicable, Evaluación de explicaciones, Protocolo FOM-7, Métodos post-hoc, Auditoría de modelos*), sin repetir literalmente el título.

### 1.3 Maquetación y Tipografía
- [ ] **Tipografía:** Times New Roman 12 pt en cuerpo de texto.
- [ ] **Interlineado:** 1,5 líneas en todo el texto.
- [ ] **Alineación:** Texto justificado con sangría en primera línea (o según estilos de la plantilla).
- [ ] **Jerarquía de títulos:** Nivel 1 en MAYÚSCULAS NEGRITA; Niveles 2 y 3 en tipo oración negrita.
- [ ] **Salto y flujo de párrafos:** No existen líneas viudas o huérfanas aisladas al inicio o final de página.

### 1.4 Diagramación Especial (Página 13 - Axiomas de Shapley)
- [ ] Localice en la Sección 04 la exposición del teorema de Shapley (1953) / Lundberg y Lee (2017).
- [ ] Verifique que los cuatro axiomas se despliegan en cuatro párrafos estructurados y diferenciados:
  1. *Eficiencia:* $\sum_{i=1}^{M} \phi_i(f, x) = f(x) - \mathbb{E}[f(z)]$.
  2. *Simetría:* Si $v(S \cup \{i\}) = v(S \cup \{j\})$, entonces $\phi_i = \phi_j$.
  3. *Jugador nulo / Dummy:* Si $v(S \cup \{i\}) = v(S)$, entonces $\phi_i = 0$.
  4. *Aditividad:* $\phi_i(u + v) = \phi_i(u) + \phi_i(v)$.
- [ ] Confirme que las fórmulas matemáticas centradas presentan espaciado vertical armónico antes y después.

### 1.5 Tablas y Figuras
- [ ] **Tablas 1, 2, 3 y 4:** Verificar que cada tabla tiene número consecutivo, título descriptivo en cursiva, formato APA 7 (solo líneas horizontales superior, inferior y cabecera; sin rejillas verticales) y nota al pie (*Nota.*) con la fuente.
- [ ] **Figuras 1 a 14:** Verificar que cada una aparece después de haber sido citada en el texto y cuenta con pie de figura centrado con atribución metodológica y bibliográfica.
- [ ] **Versión Impresión B/N (`capitulo_cifie_xai_fom7_bn_impresion.pdf`):** Hojee esta versión y confirme que las 14 figuras monocromáticas se leen con claridad mediante tramas de rayado, grosores de línea y marcadores diferenciados sin depender del color.

### 1.6 Referencias Bibliográficas
- [ ] Verificar que la sección final **REFERENCIAS** está en orden alfabético estricto.
- [ ] Verificar sangría francesa (1,27 cm).
- [ ] Verificar que los enlaces DOI incluyan el prefijo formal `https://doi.org/...`.
- [ ] Confirmar que no queden referencias en inglés residuales (ej.: usar "En" en lugar de "In", y "Ed." en lugar de "Eds.").

---

## FASE 2: Firma de los Documentos Editoriales Oficiales TintAzul (Ya Diligenciados)

Los tres documentos requeridos en `03_formatos_editoriales_tintazul/` han sido **íntegramente completados y marcados con casillas formales (☑)** por el asistente editorial. Únicamente requieren su revisión final y firma:

### 2.1 `DECLARACIÓN DE AUTORÍA.docx` (Completado - Listo para firmar)
- **Datos generales incorporados:**
  - Título: *De la explicación a la evidencia: fundamentos, aplicaciones y evaluación auditable de la inteligencia artificial explicable*.
  - Autor y correspondencia: *Jonathan Herrera-Vásquez*.
  - Institución: *Universidad Americana de Europa (UNADE)*.
  - Correo electrónico: `jonnabio@gmail.com`.
- **Casillas marcadas (☑):**
  - Sección I (Originalidad): 4 casillas marcadas. Incorpora la nota formal declarando la procedencia y citación de los datos preliminares publicados en RIMI (CC BY-NC-SA 4.0).
  - Sección II (Autoría): 4 casillas marcadas (autoría individual de J. Herrera-Vásquez).
  - Sección III (Integridad académica): 4 casillas marcadas.
  - Sección IV (Uso auxiliar de IA): Marcado el uso auxiliar (revisión gramatical, estilo, organización preliminar y corrección lingüística) y ratificadas las 6 declaraciones de autoría intelectual humana.
  - Sección V (Derechos) y Sección VI (Sin conflicto de interés): Marcadas.
- **Acción requerida del autor:**
  - [ ] Abra el archivo, estampe su firma (escaneada o manuscrita) en la tabla final, guarde el `.docx` y genere una copia en `.pdf` (`DECLARACIÓN DE AUTORÍA_firmada.pdf`).

### 2.2 `LICENCIA DE PUBLICACIÓN Y CESIÓN LIMITADA DE DEREC.docx` (Completado - Listo para firmar)
- **Datos incorporados:** Título del capítulo, Autor (*Jonathan Herrera-Vásquez*), Institución (*UNADE*) y fecha (*10 de octubre de 2026*).
- **Acción requerida del autor:**
  - [ ] Estampe su firma en la fila del autor en la tabla de la página final, guarde el `.docx` y genere una copia en `.pdf` (`LICENCIA DE PUBLICACIÓN_firmada.pdf`).

### 2.3 `CHECKLIST DEL AUTOR.docx` (Completado - Listo para firmar)
- **Casillas marcadas (☑):** Todas las 55 casillas de verificación de las secciones I a IX se encuentran marcadas afirmativamente conforme a la auditoría técnica del capítulo.
- **Datos incorporados:** *Nombre del autor: Jonathan Herrera-Vásquez* y *Fecha: 10 de octubre de 2026*.
- **Acción requerida del autor:**
  - [ ] Estampe su firma en la línea *Firma: ________________________*, guarde el `.docx` y genere una copia en `.pdf` (`CHECKLIST DEL AUTOR_firmado.pdf`).

---

## FASE 3: Verificación de Archivos y Figuras Independientes

La editorial y el equipo de diseño gráfico requieren copias sueltas de todas las figuras para la diagramación litográfica:

- [ ] **Carpeta `02_figuras/digital_color/`:**
  - Contiene exactamente las **14 figuras en PNG** de alta resolución (300 a 600 DPI) para la edición electrónica interactiva.
- [ ] **Carpeta `02_figuras/impresion_bn/`:**
  - Contiene las **14 figuras en B/N** con contrastes tonales, tramas de rayado (*hatchings*) y marcadores geométricos para imprenta offset.
- [ ] **Carpeta `02_figuras/vectorial_editable/`:**
  - Contiene los archivos fuente en **SVG y PDF vectorial** de los diagramas conceptuales y metodológicos (D1 a D12) para que los diagramadores de TintAzul puedan ajustar tipografías si fuera necesario sin pérdida de calidad.

---

## FASE 4: Protocolo de Envío por Correo Electrónico

Una vez firmados los tres documentos, prepare el mensaje de envío oficial al Comité Editorial de CIFIE / TintAzul.

### Plantilla de Correo Electrónico

> **Para:** comite.editorial@cifie.org (o dirección designada en la convocatoria)  
> **Asunto:** `[CIFIE 2026 - Libro Colectivo] Envío de Manuscrito Final y Documentos Editoriales - Jonathan Herrera-Vásquez`  
>
> **Estimado Comité Editorial y Equipo de Producción de TintAzul:**
>
> Por medio de la presente, me complace remitir el manuscrito final y la documentación correspondiente para su publicación en el Libro Colectivo derivado del Congreso Internacional CIFIE.
>
> **Datos del Manuscrito:**
> - **Título:** *De la explicación a la evidencia: fundamentos, aplicaciones y evaluación auditable de la inteligencia artificial explicable*
> - **Subtítulo:** *El protocolo FOM-7 como marco operativo para comparaciones reproducibles*
> - **Autor:** Jonathan Herrera-Vásquez
> - **Afiliación:** Universidad Americana de Europa (UNADE)
> - **ORCID:** 0000-0002-7149-6635
> - **Extensión:** 8.019 palabras (dentro del límite editorial de 9.000 palabras)
>
> **Archivos Adjuntos en el Paquete:**
> 1. **Manuscrito del capítulo:**
>    - `capitulo_cifie_xai_fom7_color.docx` (versión principal maquetada con figuras a color para edición digital).
>    - `capitulo_cifie_xai_fom7_color.pdf` (renderizado de control para verificación visual).
>    - `capitulo_cifie_xai_fom7_bn_impresion.docx` y `.pdf` (versión con figuras tramadas monocromáticas para imprenta en papel).
> 2. **Documentación editorial debidamente firmada:**
>    - `DECLARACIÓN DE AUTORÍA_firmada.pdf` (originalidad, uso auxiliar de IA y datos preliminares RIMI declarados).
>    - `LICENCIA DE PUBLICACIÓN Y CESIÓN LIMITADA DE DERECHOS_firmada.pdf`.
>    - `CHECKLIST DEL AUTOR_firmado.pdf`.
> 3. **Carpeta / Archivo comprimido de Figuras en alta resolución (`figuras_cifie_xai_fom7.zip`):**
>    - Las 14 figuras en formato PNG de alta resolución (color y B/N tramado), acompañadas de sus archivos vectoriales editables (SVG y PDF).
>
> Quedo a su entera disposición para cualquier aclaración técnica o ajuste derivado de la revisión por pares ciegos y la edición de estilo.
>
> Atentamente,
>
> **Jonathan Herrera-Vásquez**  
> Candidato a Doctor / Investigador  
> Universidad Americana de Europa (UNADE)  
> [Correo electrónico]  
> [Teléfono de contacto]  

---

## Control de Cambios y Versión Final
- **Hash de referencia del repositorio:** Auditado bajo rama de trabajo `thesis/rca-001-phase-2`.
- **Estado de las 7 puertas FOM-7:** Conforme con el protocolo reproducible y validado empíricamente.
- **Fecha de cierre del paquete:** 10 de octubre de 2026.
