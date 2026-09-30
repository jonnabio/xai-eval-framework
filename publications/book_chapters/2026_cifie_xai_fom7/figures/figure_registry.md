# Registro de figuras

| Figura | Figure ID | Título final | Source material | Editable file | Exported file | Used in section | Citation/source note | Status |
| ------ | --------- | ------------ | --------------- | ------------- | ------------- | --------------- | -------------------- | ------ |
| Figura 1 | fig-cobertura-exp2 | Cobertura analítica EXP2 por modelo y método | `thesis/assets/figures/fig_cobertura_exp2_es.png`; caption in `thesis/capitulo-4-resultados.qmd` | `scripts/generate_spanish_thesis_figures.py` (tesis) | `figures/exported/fig_cobertura_exp2_es.png` | `07_diseno_empirico.md`, `08_aplicacion_empirica_perfiles_fom7.md` | Fuente interna de tesis; útil para documentar puerta 3 de FOM-7. | Copiada |
| Figura 2 | fig-cd-diagram | Diagrama de diferencia crítica de Nemenyi para fidelidad y estabilidad | `outputs/analysis/paper_a_exp2_stats/exp2_block_method_summary.csv`; `outputs/analysis/paper_a_exp2_stats/nemenyi_fidelity.csv`; `outputs/analysis/paper_a_exp2_stats/nemenyi_stability.csv` | `scripts/generate_cifie_chapter_figures.py` | `figures/exported/fig_cd_diagram_es.png` | `08_aplicacion_empirica_perfiles_fom7.md` | Elaboración propia; conserva 15 bloques, rangos y DC = 1.211 registrados. | Regenerada para legibilidad en Word |
| Figura 3 | fig-boxplots-metricas | Distribución de fidelidad y estabilidad por método | `thesis/assets/figures/fig_boxplots_metricas_es.png`; caption in `thesis/capitulo-4-resultados.qmd` | `scripts/generate_spanish_thesis_figures.py` (tesis) | `figures/exported/fig_boxplots_metricas_es.png` | `08_aplicacion_empirica_perfiles_fom7.md` | Fuente interna de tesis; muestra patrones distribucionales por bloque $(g,n)$. | Copiada |
| Figura 4 | fig-estabilidad-coste | Relación entre estabilidad y coste por método | `thesis/assets/figures/fig_estabilidad_coste_es.png`; caption in `thesis/capitulo-4-resultados.qmd` | `scripts/generate_spanish_thesis_figures.py` (tesis) | `figures/exported/fig_estabilidad_coste_es.png` | `08_aplicacion_empirica_perfiles_fom7.md` | Fuente interna de tesis; apoya la frontera calidad-coste. | Copiada |
| Figura 5 | fig-correlacion-metricas | Correlación entre métricas del benchmark | `thesis/assets/figures/fig_correlacion_metricas_es.png`; caption in `thesis/capitulo-4-resultados.qmd` | `scripts/generate_spanish_thesis_figures.py` (tesis) | `figures/exported/fig_correlacion_metricas_es.png` | `08_aplicacion_empirica_perfiles_fom7.md` | Fuente interna de tesis; apoya lectura multi-métrica, no sustituye pruebas estadísticas. | Copiada |
| Figura 6 | fig-radar-metodos | Perfil multidimensional normalizado por método | `thesis/assets/figures/fig_radar_metodos_es.png`; caption in `thesis/capitulo-4-resultados.qmd` | `scripts/generate_spanish_thesis_figures.py` (tesis) | `figures/exported/fig_radar_metodos_es.png` | `09_implicaciones_evaluacion_auditable_xai.md` | Fuente interna de tesis; útil para argumentar ausencia de método universalmente dominante. | Copiada |


## Figuras didácticas (creadas el 2026-09-30; pendientes de ubicación)

Generador: `scripts/generate_cifie_didactic_figures.py` (Cambria, escala de grises,
600 ppp; editables en PDF y SVG en `figures/editable/`). Reformulan conceptos ya
escritos en el capítulo y no aportan resultados nuevos. Los valores de D3 y D4 son
ilustrativos y así se indica dentro de la figura; las únicas cifras de diseño (300, 275 y
15) coinciden con las de la sección 07. Al insertarlas, las figuras empíricas se
renumeran después de las didácticas y cada figura debe mencionarse en el texto antes de
aparecer (plantilla CIFIE).

| ID | Archivo exportado | Contenido | Sección propuesta | Fuente para la nota APA | Estado |
| --- | --- | --- | --- | --- | --- |
| D1 | `figures/exported/fig_d1_conceptos_es.png` | Transparencia, interpretabilidad y explicabilidad: pregunta, definición y límite de cada una | 03, "Interpretabilidad, explicabilidad y transparencia" | Elaboración propia a partir de Lipton (2018), Murdoch et al. (2019), Phillips et al. (2021) y Tabassi (2023) | Creada |
| D2 | `figures/exported/fig_d2_modelos_es.png` | Espectro de modelos y explicación post-hoc agnóstica o específica | 03, "Modelos interpretables por diseño y explicaciones post-hoc" | Elaboración propia a partir de Rudin et al. (2022) y Marcinkevičs y Vogt (2023) | Creada |
| D3 | `figures/exported/fig_d3_local_global_es.png` | Alcance local frente a global (datos simulados) | 03, "Alcance local y alcance global" | Elaboración propia; ilustración con datos simulados | Creada |
| D4 | `figures/exported/fig_d4_objetos_explicativos_es.png` | Un caso, cuatro objetos explicativos: atribución, regla, contrafactual y ejemplos | 03, "Objetos explicativos y preguntas diferentes" | Elaboración propia a partir de Ribeiro et al. (2016, 2018), Lundberg y Lee (2017) y Mothilal et al. (2020); valores ilustrativos | Creada |
| D5 | `figures/exported/fig_d5_ciclo_audiencias_es.png` | Funciones de la explicación en el ciclo de vida y necesidades de cada audiencia | 04, "Funciones de la explicación durante el ciclo de vida" | Elaboración propia a partir de Tabassi (2023) y Phillips et al. (2021) | Creada |
| D6 | `figures/exported/fig_d6_niveles_evaluacion_es.png` | Niveles de evaluación y posición de FOM-7 | 03, "Niveles de evaluación y alcance de FOM-7" (o 05) | Adaptada de Doshi-Velez y Kim (2017) | Creada |
| D7 | `figures/exported/fig_d7_cadena_evidencia_es.png` | Cadena de evidencia de artefacto a afirmación y fallo típico de cada eslabón | 05, "Brecha entre métrica, constructo y afirmación" | Elaboración propia | Creada |
| D8 | `figures/exported/fig_d8_fom7_traza_es.png` | Las siete puertas de FOM-7 con la traza de una afirmación publicada (H1) | 06, "Flujo operativo" | Elaboración propia; resultado de H1 publicado en Herrera-Vásquez y Herrero-Uceda (2026) | Creada |

## Figuras retiradas

- `fig-diferencias-pareadas` (antes Figura 4, diferencias pareadas SHAP-LIME): retirada el 2026-09-27.
  Muestra resultados del contraste pareado de 75 celdas, que pertenecen al artículo Paper B+C aún no
  publicado. El capítulo remite a la tesis para esos resultados (decisión del autor; ver
  `[exclusivity]` en `pub/claim_registry.toml`).
