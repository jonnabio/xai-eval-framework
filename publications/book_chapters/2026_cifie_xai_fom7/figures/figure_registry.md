# Registro de figuras

## Conjunto activo (2026-10-10)

Auditoría de los archivos de sección: las 14 figuras están citadas en el texto
antes de aparecer, sus versiones en **color** (por defecto para edición digital) existen en
`figures/exported/` y sus versiones específicas en **blanco y negro** (compatibles para impresión con tramas/marcadores) existen en `figures/bw/`. Cada caption identifica una fuente externa o elaboración propia con sus datos fuente. Las referencias externas de las captions se encuentran en `references/references_apa7.md`.

| No. | ID / archivo exportado (Color por defecto) | Versión B/W (Impresión) | Sección | Uso y fuente declarada en caption | Archivo editable / regeneración |
| --- | --- | --- | --- | --- | --- |
| 1 | D1 / `fig_d1_conceptos_es.png` | `figures/bw/fig_d1_conceptos_es.png` | 03 | Distinciones conceptuales; Lipton (2018), Murdoch et al. (2019), Phillips et al. (2021) y Tabassi (2023). | `scripts/generate_cifie_didactic_figures.py` (`figures/editable/fig_d1_conceptos_es.svg`) |
| 2 | D2 / `fig_d2_modelos_es.png` | `figures/bw/fig_d2_modelos_es.png` | 03 | Modelos interpretables y explicaciones post-hoc; Rudin et al. (2022), Marcinkevičs y Vogt (2023). | `scripts/generate_cifie_didactic_figures.py` (`figures/editable/fig_d2_modelos_es.svg`) |
| 3 | D6 / `fig_d6_niveles_evaluacion_es.png` | `figures/bw/fig_d6_niveles_evaluacion_es.png` | 03 | Niveles de evaluación y FOM-7; adaptada de Doshi-Velez y Kim (2017). | `scripts/generate_cifie_didactic_figures.py` (`figures/editable/fig_d6_niveles_evaluacion_es.svg`) |
| 4 | D4 / `fig_d4_objetos_explicativos_es.png` | `figures/bw/fig_d4_objetos_explicativos_es.png` | 04 | Cuatro objetos explicativos; Ribeiro et al. (2016, 2018), Lundberg y Lee (2017), Mothilal et al. (2020); valores ilustrativos. | `scripts/generate_cifie_didactic_figures.py` (`figures/editable/fig_d4_objetos_explicativos_es.svg`) |
| 5 | D9 / `fig_d9_lime_geometria_es.png` | `figures/bw/fig_d9_lime_geometria_es.png` | 04 | Fundamento geométrico de LIME y riesgo de perturbaciones OOD; Ribeiro et al. (2016). | `scripts/generate_cifie_equation_figures.py` (`figures/editable/fig_d9_lime_geometria_es.svg`) |
| 6 | D10 / `fig_d10_shap_coaliciones_es.png` | `figures/bw/fig_d10_shap_coaliciones_es.png` | 04 | Teoría de juegos cooperativos, ponderación KernelSHAP y cascada aditiva; Lundberg y Lee (2017). | `scripts/generate_cifie_equation_figures.py` (`figures/editable/fig_d10_shap_coaliciones_es.svg`) |
| 7 | D11 / `fig_d11_anchors_dice_es.png` | `figures/bw/fig_d11_anchors_dice_es.png` | 04 | Topología de reglas PAC en Anchors y física multiobjetivo en DiCE; Ribeiro et al. (2018) y Mothilal et al. (2020). | `scripts/generate_cifie_equation_figures.py` (`figures/editable/fig_d11_anchors_dice_es.svg`) |
| 8 | D5 / `fig_d5_ciclo_audiencias_es.png` | `figures/bw/fig_d5_ciclo_audiencias_es.png` | 04 | Marco sintético de trade-offs operacionales; Tabassi (2023), Phillips et al. (2021). | `scripts/generate_cifie_didactic_figures.py` (`figures/editable/fig_d5_ciclo_audiencias_es.svg`) |
| 9 | D7 / `fig_d7_cadena_evidencia_es.png` | `figures/bw/fig_d7_cadena_evidencia_es.png` | 05 | Cadena de evidencia y fallos; elaboración propia a partir de Krishna et al. (2022), Nauta et al. (2023) y Agarwal et al. (2023). | `scripts/generate_cifie_didactic_figures.py` (`figures/editable/fig_d7_cadena_evidencia_es.svg`) |
| 10 | D8 / `fig_d8_fom7_traza_es.png` | `figures/bw/fig_d8_fom7_traza_es.png` | 05 | Taxonomía de distorsiones y traza de siete puertas FOM-7; Herrera-Vásquez y Herrero-Uceda (2026). | `scripts/generate_cifie_didactic_figures.py` (`figures/editable/fig_d8_fom7_traza_es.svg`) |
| 11 | D12 / `fig_d12_fom7_metrologia_es.png` | `figures/bw/fig_d12_fom7_metrologia_es.png` | 06 | Metrología operativa FOM-7: estabilidad angular (G2) y consistencia inter-método (G6); elaboración propia. | `scripts/generate_cifie_equation_figures.py` (`figures/editable/fig_d12_fom7_metrologia_es.svg`) |
| 12 | Nemenyi / `fig_cd_diagram_es.png` | `figures/bw/fig_cd_diagram_es.png` | 08 | Diferencias críticas en fidelidad y estabilidad; tablas de rangos y comparaciones de Nemenyi de EXP2. | `scripts/generate_cifie_chapter_figures.py`; EXP2 CSVs under `outputs/analysis/paper_a_exp2_stats/` |
| 13 | Stability-cost / `fig_estabilidad_coste_es.png` | `figures/bw/fig_estabilidad_coste_es.png` | 08 | Estabilidad y coste por método; resultados del benchmark EXP2. | `scripts/generate_spanish_thesis_figures.py`; source figure in `thesis/assets/figures/` |
| 14 | EXP2 coverage / `fig_cobertura_exp2_es.png` | `figures/bw/fig_cobertura_exp2_es.png` | 08 | Cobertura empírica e interpretabilidad práctica de reglas Anchors (EXP2). | `scripts/generate_spanish_thesis_figures.py`; source figure in `thesis/assets/figures/` |

Las figuras 1-11 son diagramas conceptuales y metodológicos; 12-14 visualizan evidencia empírica.
Todas aparecen en el orden de numeración vigente y tienen un callout anterior al
caption.

## Organización de Formatos (Color vs. B/W)

- **Versiones por Defecto (Color)**: Ubicadas en `figures/exported/` (PNG) y `figures/editable/` (SVG, PDF). Se integran por defecto en la edición digital del capítulo mediante `python scripts/build_cifie_chapter.py`.
- **Versiones de Respaldo B/W (Impresión)**: Ubicadas en `figures/bw/` (PNG, SVG, PDF). No son desaturaciones simples: cuentan con tramas de rayado (*hatching*), marcadores geométricos diferenciados (`o`, `s`, `^`, `D`), grosores de línea diferenciados y contrastes tonales adaptados a impresión monocromática. Se pueden compilar en el documento Word mediante `python scripts/build_cifie_chapter.py --bw`.

## Exports no utilizados

Estos archivos se conservan como material histórico, pero no forman parte del capítulo
actual: `fig_d3_local_global_es.png`, `fig_boxplots_metricas_es.png`,
`fig_correlacion_metricas_es.png` y `fig_radar_metodos_es.png`. No deben copiarse al
paquete de envío salvo que el autor apruebe su reincorporación y se actualicen el texto,
la numeración y este registro.

## Figuras retiradas

- `fig-diferencias-pareadas` (antes Figura 4, diferencias pareadas SHAP-LIME): retirada el 2026-09-27.
  Muestra resultados del contraste pareado de 75 celdas, que pertenecen al artículo Paper B+C aún no
  publicado. El capítulo remite a la tesis para esos resultados (decisión del autor; ver
  `[exclusivity]` en `pub/claim_registry.toml`).
