# Paquete de Envío Editorial: Libro Colectivo CIFIE / TintAzul

**Fecha de preparación:** 10 de octubre de 2026  
**Destino:** Comité Editorial del Congreso Internacional CIFIE / TintAzul – Editorial Académica y Estratégica  
**Directorio:** `publications/book_chapters/2026_cifie_xai_fom7/final/submission_package`

---

## 1. Identificación del Capítulo

- **Título completo:** *De la explicación a la evidencia: fundamentos, aplicaciones y evaluación auditable de la inteligencia artificial explicable*
- **Subtítulo:** *El protocolo FOM-7 como marco operativo para comparaciones reproducibles*
- **Autor:** Jonathan Herrera-Vásquez
- **Grado académico:** Candidato a Doctor / M.Sc.
- **Afiliación institucional:** Universidad Americana de Europa (UNADE)
- **ORCID:** [0000-0002-7149-6635](https://orcid.org/0000-0002-7149-6635)
- **Tipo de capítulo:** Síntesis científica conceptual y metodológica con demostración empírica acotada.
- **Extensión:** **8.019 palabras** totales (7.594 palabras de prosa + 425 palabras en tablas; cumple estrictamente el límite máximo editorial de 9.000 palabras fijado por la editorial).
- **Legibilidad:** Longitud media por oración = 17,6 palabras; **0 oraciones > 40 palabras**; Índice de Flesch-Szigriszt = 41,0; Fernández-Huerta = 58,3.
- **Tipografía y Maquetación:** Times New Roman 12 pt, interlineado 1,5, justificado, tablas y figuras según normas APA 7.ª edición.

---

## 2. Estructura del Paquete de Envío

```
submission_package/
│
├── 01_capitulo/
│   ├── capitulo_cifie_xai_fom7_color.docx         # Manuscrito principal en Word (Edición digital a color)
│   ├── capitulo_cifie_xai_fom7_color.pdf          # Manuscrito compilado en PDF (Edición digital a color)
│   ├── capitulo_cifie_xai_fom7_bn_impresion.docx  # Manuscrito para imprenta en Word (Figuras B/W optimizadas)
│   └── capitulo_cifie_xai_fom7_bn_impresion.pdf   # Manuscrito para imprenta en PDF (Figuras B/W optimizadas)
│
├── 02_figuras/
│   ├── digital_color/                             # 14 figuras a color de alta resolución (PNG, 300-600 DPI)
│   │   ├── fig_d1_conceptos_es.png
│   │   ├── fig_d2_modelos_es.png
│   │   ├── fig_d6_niveles_evaluacion_es.png
│   │   ├── fig_d4_objetos_explicativos_es.png
│   │   ├── fig_d9_lime_geometria_es.png
│   │   ├── fig_d10_shap_coaliciones_es.png
│   │   ├── fig_d11_anchors_dice_es.png
│   │   ├── fig_d5_ciclo_audiencias_es.png
│   │   ├── fig_d7_cadena_evidencia_es.png
│   │   ├── fig_d8_fom7_traza_es.png
│   │   ├── fig_d12_fom7_metrologia_es.png
│   │   ├── fig_cd_diagram_es.png
│   │   ├── fig_estabilidad_coste_es.png
│   │   └── fig_cobertura_exp2_es.png
│   │
│   ├── vectorial_editable/                        # Formatos vectoriales editables (SVG y PDF de diagramas 1-11)
│   │   ├── fig_d1_conceptos_es.svg / .pdf
│   │   ├── fig_d2_modelos_es.svg / .pdf
│   │   ├── fig_d4_objetos_explicativos_es.svg / .pdf
│   │   ├── fig_d5_ciclo_audiencias_es.svg / .pdf
│   │   ├── fig_d6_niveles_evaluacion_es.svg / .pdf
│   │   ├── fig_d7_cadena_evidencia_es.svg / .pdf
│   │   ├── fig_d8_fom7_traza_es.svg / .pdf
│   │   ├── fig_d9_lime_geometria_es.svg / .pdf
│   │   ├── fig_d10_shap_coaliciones_es.svg / .pdf
│   │   ├── fig_d11_anchors_dice_es.svg / .pdf
│   │   └── fig_d12_fom7_metrologia_es.svg / .pdf
│   │
│   └── impresion_bn/                              # Versiones monocromáticas con tramas de rayado y marcadores (PNG/SVG/PDF)
│       └── [14 figuras adaptadas para impresión en escala de grises y prensa litográfica]
│
├── 03_formatos_editoriales_tintazul/              # Documentos oficiales requeridos para el envío (pre-diligenciados)
│   ├── CHECKLIST DEL AUTOR.docx                   # Lista de verificación con casillas marcadas (☑), listo para firma
│   ├── DECLARACIÓN DE AUTORÍA.docx                # Declaración de autoría, originalidad y uso auxiliar de IA cumplimentada
│   └── LICENCIA DE PUBLICACIÓN Y CESIÓN LIMITADA DE DEREC.docx # Contrato de licencia patrimonial cumplimentado
│
├── README_PAQUETE_ENVIO.md                        # Manifiesto y guía general del paquete (este documento)
└── CHECKLIST_REVISION_ENVIO_AUTOR.md              # Lista exhaustiva de verificación y pasos de firma para el autor
```

---

## 3. Resumen del Registro de Figuras (14 Figuras Activas)

Todas las 14 figuras están estrictamente citadas en el texto antes de aparecer, cuentan con leyendas completas conforme a APA 7 y declaran expresamente sus fuentes de datos primarias o bibliográficas:

| No. | Archivo Exportado | Sección | Tipo | Descripción y Fuente Declarada |
| :---: | :--- | :---: | :---: | :--- |
| **1** | `fig_d1_conceptos_es.png` | 03 | Conceptual | Distinciones conceptuales entre interpretabilidad, explicabilidad y transparencia (Lipton, 2018; Murdoch et al., 2019; Phillips et al., 2021). |
| **2** | `fig_d2_modelos_es.png` | 03 | Metodológico | Modelos intrínsecamente interpretables y explicaciones post-hoc (Rudin et al., 2022; Marcinkevičs & Vogt, 2023). |
| **3** | `fig_d6_niveles_evaluacion_es.png` | 03 | Metodológico | Tres niveles de evaluación y ubicación de FOM-7 (adaptado de Doshi-Velez & Kim, 2017). |
| **4** | `fig_d4_objetos_explicativos_es.png` | 04 | Didáctico | Cuatro objetos explicativos: atribución local, global, reglas PAC y contrafactuales. |
| **5** | `fig_d9_lime_geometria_es.png` | 04 | Geométrico | Fundamento geométrico de LIME y riesgo de perturbaciones OOD (Ribeiro et al., 2016). |
| **6** | `fig_d10_shap_coaliciones_es.png` | 04 | Matemático | Teoría de juegos cooperativos, ponderación KernelSHAP y cascada aditiva (Lundberg & Lee, 2017). |
| **7** | `fig_d11_anchors_dice_es.png` | 04 | Metodológico | Topología de reglas de alta precisión en Anchors y física multiobjetivo en DiCE. |
| **8** | `fig_d5_ciclo_audiencias_es.png` | 04 | Conceptual | Marco sintético de compromisos operativos y necesidades por audiencia (Phillips et al., 2021; Tabassi, 2023). |
| **9** | `fig_d7_cadena_evidencia_es.png` | 05 | Metodológico | Cadena de evidencia y taxonomía de modos de fallo (Krishna et al., 2022; Nauta et al., 2023; Agarwal et al., 2023). |
| **10** | `fig_d8_fom7_traza_es.png` | 05 | Metodológico | Taxonomía de distorsiones y traza secuencial de siete puertas FOM-7 (Herrera-Vásquez & Herrero-Uceda, 2026). |
| **11** | `fig_d12_fom7_metrologia_es.png` | 06 | Metrológico | Metrología operativa FOM-7: estabilidad angular (G2) y consistencia inter-método (G6). |
| **12** | `fig_cd_diagram_es.png` | 08 | Empírico | Diagrama de diferencias críticas de Nemenyi en fidelidad y estabilidad (EXP2). |
| **13** | `fig_estabilidad_coste_es.png` | 08 | Empírico | Trade-off empírico entre estabilidad y coste computacional por método (EXP2). |
| **14** | `fig_cobertura_exp2_es.png` | 08 | Empírico | Cobertura empírica e interpretabilidad práctica de reglas Anchors (EXP2). |

---

## 4. Instrucciones para la Entrega

Consulte el documento complementario [`CHECKLIST_REVISION_ENVIO_AUTOR.md`](file:///D:/Github/xai-eval-framework/publications/book_chapters/2026_cifie_xai_fom7/final/submission_package/CHECKLIST_REVISION_ENVIO_AUTOR.md) para completar los pasos de revisión final, firma de formularios y despacho formal ante el Comité Editorial de CIFIE / TintAzul.
