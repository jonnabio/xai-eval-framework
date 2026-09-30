**Tabla 4**

*Resumen de los resultados empíricos por hipótesis*

| Hipótesis | Prueba | Unidad | Resultado | Decisión |
| --------- | ------ | ------ | --------- | -------- |
| H1: los métodos difieren en fidelidad | Friedman y Nemenyi | 15 bloques $(g,n)$ | $\chi^2_F = 42.12$; $p_{\mathrm{Holm}} = 1.51 \times 10^{-8}$; $W = 0.936$ | Se rechaza $H_{0,1}$. Nemenyi separa SHAP de Anchors y DiCE, y LIME de DiCE. |
| H2: los métodos difieren en estabilidad | Friedman y Nemenyi | 15 bloques $(g,n)$ | $\chi^2_F = 40.68$; $p_{\mathrm{Holm}} = 2.29 \times 10^{-8}$; $W = 0.904$ | Se rechaza $H_{0,2}$. SHAP y DiCE forman el grupo más estable. |
| H3: SHAP y LIME difieren en calidad y coste | Wilcoxon pareado bilateral | Celdas coincidentes $(g,s,n)$ | Véase Herrera-Vásquez (2026); resultado no publicado | Según la tesis, se rechaza $H_{0,3}$: SHAP mejora la calidad explicativa y aumenta el coste medio. |
| Análisis exploratorio SHAP-LIME en fidelidad | Wilcoxon y prueba exacta de signos | 15 bloques $(g,n)$ | 15 de 15 bloques a favor de SHAP; $p_{\mathrm{Holm}} = 3.05 \times 10^{-4}$ | Misma dirección que H3 con la agregación por bloques; *post hoc*, no sustituye a H3. |
| P1: el protocolo es reproducible bajo semillas | Coeficiente de variación | Subconjunto de EXP2: bosque aleatorio, 100 instancias por estrato, cinco semillas; y conjunto completo | CV inferior al 3 % en las señales principales del subconjunto; CV agrupado de fidelidad de 11.4 % (SHAP) y 12.0 % (LIME) | Confirmación parcial: la estabilidad de LIME queda fuera por su media cercana a cero. |

*Nota.* $\chi^2_F$ = estadístico de Friedman; $W$ = coeficiente de concordancia de Kendall; $p_{\mathrm{Holm}}$ = valor *p* ajustado por Holm-Bonferroni. Los bloques son combinaciones de modelo y tamaño de muestra, con las semillas promediadas dentro de cada bloque. El análisis exploratorio de 15 bloques se realizó después del análisis principal y fuera del protocolo congelado. Resultados de H1 y H2 tomados de Herrera-Vásquez y Herrero-Uceda (2026), publicados; H3, el análisis exploratorio y P1, de la tesis doctoral no publicada de Herrera-Vásquez (2026).
