# Registro de figuras

## Conjunto activo (2026-10-03)

Auditoría de los archivos de sección: las diez figuras están citadas en el texto
antes de aparecer, sus PNG existen y cada caption identifica una fuente externa o
elaboración propia con sus datos fuente. Las referencias externas de las captions
se encuentran en `references/references_apa7.md`.

| No. | ID / archivo exportado | Sección | Uso y fuente declarada en caption | Archivo editable / regeneración |
| --- | --- | --- | --- | --- |
| 1 | D1 / `fig_d1_conceptos_es.png` | 03 | Distinciones conceptuales; Lipton (2018), Murdoch et al. (2019), Phillips et al. (2021) y Tabassi (2023). | `figures/editable/fig_d1_conceptos_es.svg` |
| 2 | D2 / `fig_d2_modelos_es.png` | 03 | Modelos interpretables y explicaciones post-hoc; Rudin et al. (2022), Marcinkevičs y Vogt (2023). | `figures/editable/fig_d2_modelos_es.svg` |
| 3 | D4 / `fig_d4_objetos_explicativos_es.png` | 03 | Cuatro objetos explicativos; Ribeiro et al. (2016, 2018), Lundberg y Lee (2017), Mothilal et al. (2020); valores ilustrativos. | `figures/editable/fig_d4_objetos_explicativos_es.svg` |
| 4 | D6 / `fig_d6_niveles_evaluacion_es.png` | 03 | Niveles de evaluación y FOM-7; adaptada de Doshi-Velez y Kim (2017). | `figures/editable/fig_d6_niveles_evaluacion_es.svg` |
| 5 | D5 / `fig_d5_ciclo_audiencias_es.png` | 04 | Funciones y audiencias; Tabassi (2023), Phillips et al. (2021). | `figures/editable/fig_d5_ciclo_audiencias_es.svg` |
| 6 | D7 / `fig_d7_cadena_evidencia_es.png` | 05 | Cadena de evidencia y fallos; elaboración propia. | `figures/editable/fig_d7_cadena_evidencia_es.svg` |
| 7 | D8 / `fig_d8_fom7_traza_es.png` | 06 | Siete puertas y traza H1; elaboración propia; resultado publicado en Herrera-Vásquez y Herrero-Uceda (2026). | `figures/editable/fig_d8_fom7_traza_es.svg` |
| 8 | EXP2 coverage / `fig_cobertura_exp2_es.png` | 07 | Cobertura analítica por modelo y método; inventario de celdas calificadas de EXP2. | `scripts/generate_spanish_thesis_figures.py`; source figure in `thesis/assets/figures/` |
| 9 | Nemenyi / `fig_cd_diagram_es.png` | 08 | Diferencias críticas en fidelidad y estabilidad; tablas de rangos y comparaciones de Nemenyi de EXP2. | `scripts/generate_cifie_chapter_figures.py`; EXP2 CSVs under `outputs/analysis/paper_a_exp2_stats/` |
| 10 | Stability-cost / `fig_estabilidad_coste_es.png` | 08 | Estabilidad y coste por método; resultados del benchmark EXP2. | `scripts/generate_spanish_thesis_figures.py`; source figure in `thesis/assets/figures/` |

Las figuras 1-7 son diagramas conceptuales; 8-10 visualizan evidencia empírica.
Todas aparecen en el orden de numeración vigente y tienen un callout anterior al
caption. Los diagramas conceptuales atribuyen las fuentes adaptadas; las figuras
empíricas declaran elaboración propia e identifican el conjunto de datos o resultados
del que se derivan.

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
