# La crisis de evaluación en XAI

Fuente inicial: `planning/section06_gaps_brief_2026-09-30.md`; `thesis/capitulo-1-marco-teorico.qmd`, `thesis/capitulo-2-fundamentos.qmd` y `pub/fragments/paper_c_abstract_en.tex`.

## De las métricas a la evidencia

La XAI dispone de métodos, métricas y herramientas maduras, pero calcular indicadores no basta para producir evidencia comparable y acumulable. Persisten diferencias en definiciones métricas, criterios de inclusión, configuraciones y agregación, además de confusión entre resultados exploratorios y confirmatorios (Doshi-Velez & Kim, 2017; Kadir et al., 2023; Canha et al., 2025; Pawlicki et al., 2024; Bhattacharya & Verbert, 2024). Por ello, nombres como LIME o SHAP no son unidades experimentales suficientes: la comparación debe identificar configuración, artefacto, métrica, prueba y alcance de la afirmación. FOM-7 organiza esa cadena de evidencia.

**Fidelidad.** Comparar objetos distintos requiere más que una sola métrica. La fidelidad estima correspondencia con el comportamiento del modelo, pero no capta estabilidad, parsimonia, coste o adecuación al objeto explicativo. Depende de perturbaciones, enmascaramiento, referencias y supuestos sobre características ausentes; no equivale a causalidad ni a calidad universal (Alvarez-Melis & Jaakkola, 2018; Zheng et al., 2025). La evaluación debe combinar dimensiones y leer perfiles condicionados por la tarea (Nauta et al., 2023; Pawlicki et al., 2024).

**Métrica y afirmación.** Una métrica no respalda afirmaciones más amplias que su constructo: fidelidad local no demuestra utilidad humana; estabilidad no prueba causalidad; precisión de una regla no garantiza cobertura; y validez contrafactual para el modelo no implica factibilidad personal. Véase la Figura 6.

Como los métodos producen sustitutos, atribuciones, reglas y contrafactuales, una escala común puede confundir desalineación métrica con falta de valor explicativo. Una afirmación comparativa debe identificar objeto, métrica, diseño, unidad y alcance; FOM-7 exige trazabilidad al artefacto (Kadir et al., 2023; Nauta et al., 2023; Bhattacharya & Verbert, 2024).

![Figura 6. Cadena de evidencia de una afirmación sobre explicaciones y fallo típico de cada eslabón. Fuente: elaboración propia.](../figures/exported/fig_d7_cadena_evidencia_es.png)

**Reproducibilidad.** Deben versionarse datos, modelos, semillas, parámetros, métricas, agregación, análisis y exclusiones. Sin esos registros, no se distinguen efectos del modelo de los del explicador. El benchmarking funcional documenta el ciclo desde configuración y artefactos hasta inferencia y reporte (Hedström et al., 2023; Agarwal et al., 2022; Canha et al., 2025).

**Herramientas y gobernanza.** Quantus y OpenXAI facilitan el cálculo y la comparación de métricas, pero no definen admisibilidad, separación de calibración y confirmación, ni el alcance de las conclusiones. FOM-7 complementa estas herramientas con reglas de evidencia (Hedström et al., 2023; Agarwal et al., 2022).

## Brechas de validez y alcance de FOM-7

### Validez técnica y de constructo

**Técnica.** Fidelidad y estabilidad dependen de perturbaciones y configuración; un explicador también puede manipularse para ocultar el comportamiento del modelo (Alvarez-Melis & Jaakkola, 2018; Slack et al., 2020; Zheng et al., 2025). FOM-7 evalúa bajo condiciones declaradas, pero no prueba robustez adversarial. **Constructo.** Una etiqueta métrica no garantiza medir la propiedad de interés; la evaluación sigue siendo multidimensional y dependiente de tarea (Nauta et al., 2023; Pawlicki et al., 2024; Bhattacharya & Verbert, 2024). FOM-7 explicita constructos y unidades, pero no valida cada proxy.

### Validez humana, causal y de acción

**Humana.** Comprensión, confianza calibrada y desempeño son distintos; las explicaciones no mejoran necesariamente decisiones en las tareas estudiadas (Kim et al., 2024; Alufaisan et al., 2021; Poursabzi-Sangdeh et al., 2021). FOM-7 no evalúa impacto humano. **Causal y de acción.** Una atribución no es un efecto causal; un contrafactual puede ser inviable o injusto aunque cambie la predicción (Wachter et al., 2017; Laugel et al., 2019; Karimi et al., 2022). FOM-7 no establece causalidad ni factibilidad personal.

### Validez operativa y de gobernanza

**Operativa.** Reproducibilidad, coste y cambio de distribución afectan el uso durante el ciclo de vida (Hedström et al., 2023; Lakkaraju et al., 2020; Tabassi, 2023). FOM-7 registra configuración, variación y coste, pero no monitoriza despliegues. **Gobernanza.** Transparencia y supervisión no constituyen por sí mismas un estándar de evidencia; FOM-7 aporta trazabilidad, no certificación regulatoria (Phillips et al., 2021; European Parliament & Council of the European Union, 2024). **Modelos emergentes.** La fidelidad de razonamientos generados depende de la prueba; la evidencia multimodal es limitada (Zhao et al., 2024; Turpin et al., 2023; Zaman & Srivastava, 2026), por lo que FOM-7 requiere adaptación.

La brecha común es conectar artefacto, constructo, audiencia y decisión. FOM-7 organiza evidencia funcional y cubre parcialmente las validez técnica, de constructo, operativa y de gobernanza; no sustituye evaluación humana, causal ni de despliegue. La sección siguiente desarrolla sus siete puertas.
