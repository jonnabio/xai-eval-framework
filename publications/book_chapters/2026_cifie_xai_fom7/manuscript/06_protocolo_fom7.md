# Protocolo FOM-7 para benchmarking auditable

Fuente inicial: `thesis/capitulo-1-marco-teorico.qmd`, `thesis/capitulo-2-fundamentos.qmd`, `thesis/capitulo-3-diseno-experimental.qmd` y `thesis/capitulo-6-conclusiones.qmd`.

## Función metodológica

FOM-7 (*Framework Operation Method*) es una secuencia de siete puertas que convierte ejecuciones de benchmarking XAI en evidencia reproducible, comparable y trazable. No añade un explicador ni una métrica: gobierna el paso del diseño y los artefactos a la inferencia y las afirmaciones. Su alcance es funcionalmente fundamentado; produce evidencia computacional, no demuestra comprensión humana ni causalidad (Doshi-Velez & Kim, 2017; Hedström et al., 2023; Nauta et al., 2023).

El protocolo fija condiciones de admisibilidad para cada etapa y vincula cada conclusión con sus artefactos. La Figura 7 resume las puertas, sus salidas y la traza de una afirmación publicada.


## Regla secuencial de admisibilidad

Las puertas son secuenciales: si una falla, los resultados afectados pueden describirse, pero no sostener inferencia confirmativa. La regla evita deriva post hoc, artefactos inválidos, comparaciones incompatibles y sobreafirmación. Distinguir medidas por instancia, resúmenes por ejecución y bloques inferenciales evita pseudorreplicación; una comparación solo es admisible si usa artefactos calificados, unidades compatibles y una prueba coherente con el diseño.

El flujo es: congelar, ejecutar, auditar, armonizar, inferir, perfilar reproducibilidad y reportar. Ninguna etapa posterior repara una falla anterior.

![Figura 7. Puertas del protocolo FOM-7 y traza de una afirmación publicada. Fuente: elaboración propia; resultado publicado en Herrera-Vásquez y Herrero-Uceda (2026).](../figures/exported/fig_d8_fom7_traza_es.png)

## Puertas del protocolo

**Puerta 1, congelación.** Antes de la ejecución confirmativa se fijan código, configuración, factores, métodos, métricas e inferencia en un manifiesto versionado. EXP1 calibra; EXP2 sostiene la inferencia (Agarwal et al., 2022; Canha et al., 2025; Zheng et al., 2025).

**Puerta 2, ejecución controlada.** Se ejecutan manifiestos con semillas y entorno registrados, sin cambios manuales durante la corrida confirmativa. Cada fallo queda asociado a una configuración y artefacto identificables.

**Puerta 3, auditoría de artefactos.** Se detectan archivos vacíos, esquemas incompatibles y valores inválidos. Lo no calificado se excluye sin reconstrucciones sintéticas y se registra; la cobertura forma parte de los resultados.

**Puerta 4, armonización.** Claves, métricas y agregaciones se estandarizan sin equiparar atribuciones, reglas y contrafactuales. Las tablas conservan método, modelo, semilla, tamaño, unidad y estado de calificación.

**Puerta 5, inferencia.** Las tablas se generan de forma determinista solo desde entradas calificadas y toda excepción se documenta. Friedman/Nemenyi requieren bloques comparables; Wilcoxon, pares; las comparaciones múltiples, el ajuste previsto.

**Puerta 6, reproducibilidad.** Se perfila dispersión entre ejecuciones y variación por semillas, protocolo o coste; la Tabla 2 resume P1. EXP1 calibra; EXP2 sostiene H1 y H2.

**Puerta 7, reporte trazable.** Cada afirmación se vincula con resultados, tablas, scripts, configuración y límites; sin esa traza, se presenta como descriptiva. Las conclusiones conservan el contexto EXP2 y no generalizan más allá del benchmark.

## Límites explícitos

FOM-7 ofrece evidencia funcional comparativa y trazable bajo condiciones controladas; no demuestra utilidad humana, causalidad ni superioridad universal. No sustituye estudios con usuarios, auditorías regulatorias o evaluación en despliegue: establece una base reproducible para esas extensiones.
