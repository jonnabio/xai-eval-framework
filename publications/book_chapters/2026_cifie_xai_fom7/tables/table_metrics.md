**Tabla 1**

*Métricas primarias del benchmark*

| Métrica | Símbolo | Definición operacional | Unidad | Dirección |
| ------- | ------- | ---------------------- | ------ | --------- |
| Fidelidad | $F$ | Correlación entre las importancias absolutas asignadas por el explicador y el cambio observado en la salida del modelo al enmascarar individualmente cada característica. | Coeficiente | Mayor es mejor |
| Estabilidad | $S$ | Similitud coseno media entre explicaciones generadas sobre perturbaciones gaussianas de una misma instancia ($T = 15$ perturbaciones, 105 pares por instancia). | Similitud coseno | Mayor es mejor |
| Parsimonia | $P$ | Proporción de características activas, es decir, con peso $\lvert w_i\rvert > 10^{-4}$, respecto del total de características transformadas. | Proporción | Menor es mejor |
| Brecha de fidelidad | $\Delta_k$ | Cambio absoluto en la probabilidad de la clase positiva al enmascarar las $k = 5$ características de mayor importancia. | Diferencia de probabilidad | Mayor es mejor |
| Coste computacional | $C$ | Tiempo de pared por instancia explicada, registrado durante la ejecución del explicador. | ms por instancia | Menor es mejor |

*Nota.* Correspondencia con las siete compuertas del protocolo FOM-7: Fidelidad ($F$) y Brecha de fidelidad ($\Delta_k$) operacionalizan la calidad local y el impacto de características; Estabilidad ($S$), la robustez estocástica local; Parsimonia ($P$), la concisión y complejidad; Coste ($C$), la latencia computacional. La validez contrafactual y cobertura de reglas se evalúan mediante indicadores específicos de objeto en el inventario calificado (cobertura empírica en Anchors y tasa de generación en DiCE, Figura 8). La consistencia inter-método y la equidad explicativa constituyen compuertas del protocolo integral no sometidas a contraste empírico de hipótesis en este benchmark, reservadas para auditorías ampliadas. Las métricas se calculan por instancia y se promedian por ejecución; la inferencia se realiza sobre bloques modelo × tamaño de muestra, no sobre instancias. Son indicadores operacionales de calidad explicativa bajo condiciones controladas, no medidas directas de utilidad humana, plausibilidad semántica ni causalidad. Otras operacionalizaciones, como ROAR o medidas locales de tipo Lipschitz, podrían producir ordenamientos distintos. Elaboración propia a partir de Herrera-Vásquez (2026).
