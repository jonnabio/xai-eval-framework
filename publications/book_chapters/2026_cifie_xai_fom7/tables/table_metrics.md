# Tabla 1. Métricas primarias del benchmark

Fuente inicial: `thesis/capitulo-1-marco-teorico.qmd` y `thesis/capitulo-3-diseno-experimental.qmd`.

Las métricas se computan por instancia y se agregan a nivel de ejecución mediante media aritmética. Deben leerse como proxies operacionales y reproducibles de calidad explicativa bajo condiciones experimentales controladas, no como medidas directas de utilidad humana, plausibilidad semántica o causalidad.

| Métrica | Símbolo | Definición operacional | Unidad | Dirección | Implementación fuente | Uso dentro del capítulo |
| ------- | ------- | ---------------------- | ------ | --------- | --------------------- | ----------------------- |
| Fidelidad | $F$ | Correlación entre las importancias absolutas asignadas por el explicador y el cambio observado en la salida del modelo al enmascarar individualmente cada característica. | score | Mayor es mejor | `src/metrics/fidelity.py` | Evalúa si las características señaladas por el explicador corresponden con efectos predictivos observables. |
| Estabilidad | $S$ | Similitud coseno media entre explicaciones generadas sobre perturbaciones gaussianas de una misma instancia; en la tesis se usa $T = 15$, con 105 pares por instancia. | similitud coseno | Mayor es mejor | `src/metrics/stability.py` | Evalúa consistencia local de las explicaciones ante variación controlada de entrada. |
| Parsimonia | $P$ | Proporción de características activas, definida por pesos con $\lvert w_i\rvert > 10^{-4}$ respecto del total de características transformadas. | proporción activa | Menor es mejor | `src/metrics/sparsity.py` | Evalúa concisión de la explicación y carga potencial de interpretación. |
| Brecha de fidelidad | $\Delta_k$ | Cambio absoluto en la probabilidad de la clase positiva al enmascarar las $k = 5$ características de mayor importancia. | score | Mayor es mejor | `src/metrics/faithfulness.py` | Evalúa sensibilidad del modelo ante la remoción de las características consideradas más relevantes. |
| Coste computacional | $C$ | Tiempo de pared en milisegundos por instancia explicada, registrado durante la ejecución del explicador. | ms/instancia | Menor es mejor | `ExplainerWrapper` y `ResourceGuard` | Evalúa viabilidad operativa y frontera calidad-coste de cada método. |

## Notas de interpretación

- La unidad de análisis inferencial de la tesis es la ejecución agregada a nivel de bloque $(g, n)$, no la instancia individual.
- Las métricas no son intercambiables: fidelidad alta no implica estabilidad, parsimonia, bajo coste ni utilidad humana.
- La fidelidad y la estabilidad son operacionalizaciones específicas; otros diseños, como ROAR o medidas Lipschitz/locales alternativas, podrían producir ordenamientos distintos.
- El capítulo debe conservar el alcance empírico: datos tabulares, UCI Adult Income, métodos post-hoc agnósticos, modelos y configuraciones descritos en la tesis.
