**Tabla 2**

*Comparación conceptual de los métodos de explicabilidad evaluados*

| Método | Base matemática | Tipo de salida | Fortaleza principal | Limitación principal |
| ------ | --------------- | -------------- | ------------------- | -------------------- |
| LIME | Aproximación local mediante modelos sustitutos interpretables ajustados sobre perturbaciones ponderadas por proximidad. | Pesos locales de características para una predicción específica. | Bajo coste computacional relativo y facilidad de interpretación local. | Sensibilidad a las perturbaciones, al muestreo y a la configuración del vecindario local. |
| SHAP | Valores de Shapley de la teoría de juegos cooperativos, aplicados a la atribución de contribuciones marginales. | Atribuciones aditivas de características, locales y agregables globalmente. | Fundamento axiomático y alta calidad explicativa en escenarios tabulares. | Coste computacional elevado y dependencia de aproximaciones según la variante del explicador. |
| Anchors | Reglas de alta precisión que fijan condiciones suficientes para sostener una predicción local. | Reglas locales del tipo si-entonces, con cobertura y precisión estimadas. | Explicaciones discretas, legibles y orientadas a condiciones de decisión. | Cobertura limitada y sensibilidad al espacio de perturbación y al umbral de precisión. |
| DiCE | Generación de contrafactuales mediante optimización de proximidad, diversidad y validez. | Conjuntos de contrafactuales que muestran cambios mínimos capaces de alterar la predicción. | Análisis de alternativas accionables y concisión contrafactual. | La plausibilidad y la factibilidad de los contrafactuales dependen de las restricciones del dominio. |

*Nota.* Elaboración propia a partir de Ribeiro et al. (2016), Lundberg y Lee (2017), Ribeiro et al. (2018) y Mothilal et al. (2020).
