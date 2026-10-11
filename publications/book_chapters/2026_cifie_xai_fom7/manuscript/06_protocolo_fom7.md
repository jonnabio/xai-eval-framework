# El protocolo operativo FOM-7

## El concepto: Un harness de pruebas automatizadas para XAI

En la ingeniería de datos, la calidad de los flujos se certifica mediante herramientas como `pytest`, `dbt test` o `Great Expectations`. Estos marcos validan aserciones concretas sobre los esquemas (completitud, unicidad y rangos) antes de autorizar su consumo.

El marco **FOM-7** (*Framework for Operational Metrics in 7 Gates*) traslada esta disciplina a la explicabilidad algorítmica. Diseñado como un **harness de certificación cuantitativa en siete compuertas secuenciales**, FOM-7 evalúa si un explicador post-hoc es fiel, robusto, legible, eficiente y equitativo:

* **Puerta 1 (G1) - Fidelidad Local (*Fidelity Gate*):** Precisión del sustituto $g$ al reproducir la caja negra $f$ en la vecindad del registro.
* **Puerta 2 (G2) - Estabilidad y Robustez (*Stability Gate*):** Resistencia de la explicación ante fluctuaciones y ruido sensorial.
* **Puerta 3 (G3) - Parsimonia Cognitiva (*Parsimony Gate*):** Concentración en pocas variables dominantes ($\le 7$) para evitar sobrecarga cognitiva.
* **Puerta 4 (G4) - Cobertura y Accionabilidad (*Coverage Gate*):** Alcance poblacional de las reglas (Anchors) o factibilidad física de los cambios prescritos (DiCE).
* **Puerta 5 (G5) - Eficiencia Computacional (*Efficiency Gate*):** Cumplimiento de latencias de infraestructura ($<100\text{ ms}$ en línea, $<2,000\text{ ms}$ en lote).
* **Puerta 6 (G6) - Consistencia Inter-método (*Cross-Explainer Consistency Gate*):** Concordancia de orden jerárquico entre distintos explicadores.
* **Puerta 7 (G7) - Equidad en la Explicación (*Explanatory Fairness Gate*):** Homogeneidad de fidelidad y estabilidad a través de subgrupos demográficos protegidos.

## Formulaciones matemáticas de las métricas de evaluación

A continuación se formalizan las métricas computables de cada compuerta:

### 1. Fidelidad Local Ponderada (G1)

Evalúa el coeficiente de determinación local entre el sustituto explicativo $g(z)$ y el modelo original $f(z)$ sobre el conjunto de perturbaciones $Z_x$, ponderado por la proximidad $\pi_x(z)$:

$$\text{Fidelidad}(g, f, x) = 1 - \frac{\sum_{z \in Z_x} \pi_x(z) \left( f(z) - g(z) \right)^2}{\sum_{z \in Z_x} \pi_x(z)}$$

Esta formulación opera de modo análogo a un coeficiente $R^2$ local. El numerador suma los errores cuadráticos ponderados por la proximidad $\pi_x(z)$. El denominador normaliza por la masa de ponderación. Un valor de $1.0$ representa coincidencia perfecta en la vecindad. Valores inferiores a $0.85$ evidencian que el sustituto distorsiona la frontera del modelo.

### 2. Estabilidad Local basada en la Constante de Lipschitz y Similitud Coseno (G2)

La estabilidad formal acota la constante de Lipschitz del operador explicativo $E(x) \in \mathbb{R}^{\vert F \vert}$ en una bola de radio $\epsilon$:

$$\text{Estabilidad}(E, x, \epsilon) = 1 - \max_{x' : \Vert x - x' \Vert_2 \le \epsilon} \frac{\Vert E(x) - E(x') \Vert_2}{\Vert x - x' \Vert_2}$$

La razón entre normas mide la tasa de variación del vector de atribución frente a perturbaciones de entrada. Si un cambio microscópico altera drásticamente los pesos asignados, la fracción diverge y la estabilidad colapsa.

Para evaluar esta propiedad en producción, FOM-7 calcula la **similitud coseno media** entre atribuciones sobre $B$ perturbaciones gaussianas controladas ($\sigma_{\text{ruido}} = 0.05 \cdot \sigma_X$):

$$\text{Estabilidad}_{\text{cos}}(E, x) = \frac{1}{B} \sum_{b=1}^B \frac{E(x) \cdot E(x + \delta_b)}{\Vert E(x) \Vert_2 \, \Vert E(x + \delta_b) \Vert_2}$$

Un valor de $1.0$ certifica que las explicaciones conservan idéntica dirección angular bajo ruido. Puntuaciones menores a $0.80$ alertan sobre volatilidad estocástica inadmisible.

### 3. Parsimonia y Escasez de Coeficientes (G3)

Mide la fracción de variables cuya atribución absoluta cae por debajo de un umbral de significancia práctica $\tau$ (típicamente $\tau = 0.01$):

$$\text{Escasez}(E(x), \tau) = \frac{1}{\vert F \vert} \sum_{i=1}^{\vert F \vert} \mathbb{I}(\vert \phi_i(x) \vert \le \tau)$$

donde $|F|$ es la dimensión del vector de características. Una escasez alta ($\ge 0.85$) confirma que el método descarta el ruido instrumental y focaliza el análisis en las columnas determinantes.

### 4. Cobertura Empírica de Reglas (G4)

En métodos basados en reglas (Anchors), cuantifica la proporción de registros del conjunto de prueba $N$ que satisfacen los antecedentes del ancla $A$:

$$\text{Cobertura}(A) = \frac{1}{N} \sum_{j=1}^{N} \mathbb{I}(A(x_j) = 1)$$

donde $A(x_j) = 1$ indica que el registro cumple los predicados condicionales de la regla.

### 5. Latencia Computacional Media (G5)

Tiempo medio de CPU/GPU $t(E, x_k)$ demandado para generar la explicación de una instancia sobre un lote de $M$ casos:

$$\bar{T}_{exp} = \frac{1}{M} \sum_{k=1}^{M} t(E, x_k) \quad [\text{ms/instancia}]$$

### 6. Consistencia Inter-método (G6)

Mide la correlación de rangos de Spearman entre las jerarquías de variables generadas por dos explicadores $E_1$ y $E_2$ sobre la misma instancia:

$$\text{Consistencia}(E_1, E_2, x) = 1 - \frac{6 \sum_{i=1}^{|F|} d_i^2}{|F| (|F|^2 - 1)}$$

donde $d_i = \text{rango}(E_1)_i - \text{rango}(E_2)_i$ es la diferencia de posición de la variable $i$. Si ambos métodos ordenan idénticamente las variables, $d_i = 0$ y la métrica alcanza $+1.0$. Si invierten el orden jerárquico, la concordancia desciende hacia $-1.0$.

### 7. Equidad en la Explicación (G7)

Evalúa la paridad en la fidelidad local media entre subgrupos demográficos protegidos, adoptando la regla de los cuatro quintos:

$$\text{Paridad}(G_1) = \min_{a, b \in \mathcal{A}} \frac{\bar{G}_1(A = a)}{\bar{G}_1(A = b)} \ge 0.80$$

donde $\bar{G}_1(A = a)$ es la fidelidad media en el subgrupo $a$, y $\mathcal{A}$ el conjunto de subgrupos protegidos. Si la razón entre el grupo menos favorecido y el más favorecido cae por debajo de $0.80$, existe una brecha discriminatoria inadmisible en la auditoría.

La Figura 11 detalla la geometría de estas compuertas. En el Panel A (G2), la bola de perturbación $\epsilon$ contrasta el cono estable de KernelSHAP ($\cos \theta \ge 0.95$) frente a la dispersión errática de LIME ($\cos \theta < 0.75$). En el Panel B (G6), el diagrama de cruce de rangos expone la inversión jerárquica entre LIME y SHAP sobre variables como *Edad* y *Educación*, reduciendo la correlación de Spearman a $+0.10$.

![Figura 11. Metrología operativa del protocolo FOM-7: estabilidad angular (G2) y consistencia inter-método de rangos (G6). Panel A: bola de perturbación $\epsilon$ y cono de estabilidad angular en similitud coseno para KernelSHAP frente a la dispersión estocástica de LIME. Panel B: cruce de rangos jerárquicos entre explicadores sobre una misma instancia ($d_i$) ilustrando el desacuerdo crítico de Spearman. Fuente: elaboración propia.](../figures/exported/fig_d12_fom7_metrologia_es.png)

## Criterios de Aprobación para Auditoría de Producción

Para certificar un pipeline bajo el protocolo FOM-7, el explicador debe satisfacer concurrentemente:

* **Umbral de Fidelidad:** $\text{Fidelidad} \ge 0.85$ (G1), evitando aproximaciones locales espurias.
* **Umbral de Estabilidad:** $\text{Estabilidad} \ge 0.80$ (G2), garantizando que el ruido no altere las atribuciones.
* **Presupuesto de Latencia:** $\bar{T}_{exp} \le 100\text{ ms}$ en servicios interactivos, o $\bar{T}_{exp} \le 2,000\text{ ms}$ en auditorías por lotes.

La Tabla 1 consolida las especificaciones técnicas de cada compuerta del protocolo FOM-7.

<!-- TABLA: table_metrics.md -->
