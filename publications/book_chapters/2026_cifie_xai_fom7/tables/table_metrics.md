**Tabla 3**

*Métricas primarias del benchmark*

| Métrica | Símbolo | Definición operacional | Unidad | Dirección |
| ------- | ------- | ---------------------- | ------ | --------- |
| Fidelidad | $F$ | Correlación entre las importancias absolutas asignadas por el explicador y el cambio observado en la salida del modelo al enmascarar individualmente cada característica. | Coeficiente | Mayor es mejor |
| Estabilidad | $S$ | Similitud coseno media entre explicaciones generadas sobre perturbaciones gaussianas de una misma instancia ($T = 15$ perturbaciones, 105 pares por instancia). | Similitud coseno | Mayor es mejor |
| Parsimonia | $P$ | Proporción de características activas, es decir, con peso $\lvert w_i\rvert > 10^{-4}$, respecto del total de características transformadas. | Proporción | Menor es mejor |
| Brecha de fidelidad | $\Delta_k$ | Cambio absoluto en la probabilidad de la clase positiva al enmascarar las $k = 5$ características de mayor importancia. | Diferencia de probabilidad | Mayor es mejor |
| Coste computacional | $C$ | Tiempo de pared por instancia explicada, registrado durante la ejecución del explicador. | ms por instancia | Menor es mejor |

*Nota.* Las métricas se calculan por instancia y se promedian por ejecución; la inferencia se realiza sobre bloques modelo × tamaño de muestra, no sobre instancias. Son indicadores operacionales de calidad explicativa bajo condiciones controladas, no medidas directas de utilidad humana, plausibilidad semántica ni causalidad. Otras operacionalizaciones, como ROAR o medidas locales de tipo Lipschitz, podrían producir ordenamientos distintos. Elaboración propia a partir de Herrera-Vásquez (2026).
