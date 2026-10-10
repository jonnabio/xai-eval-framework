# El protocolo operativo FOM-7

## El concepto: Un harness de pruebas automatizadas para XAI

En la ingeniería de datos moderna, la calidad de los pipelines se asegura mediante frameworks como `pytest`, `dbt test` o `Great Expectations`, que verifican aserciones concretas sobre los datos (completitud, unicidad, rangos de distribución) antes de autorizar su consumo.

El marco **FOM-7** (*Framework for Operational Metrics in 7 Gates*) traslada este principio al ámbito de la explicabilidad algorítmica. Concebido como un **harness de certificación cuantitativa estructurado en siete puertas de control secuenciales**, FOM-7 evalúa si un explicador post-hoc es matemáticamente fiel, estable, legible, eficiente y equitativo:

* **Puerta 1 (G1) - Fidelidad Local (*Fidelity Gate*):** Precisión con la que el sustituto interpretable $g$ reproduce las predicciones del clasificador primario $f$ en la vecindad del registro auditado.
* **Puerta 2 (G2) - Estabilidad y Robustez (*Stability Gate*):** Resistencia del explicador ante perturbaciones leves de entrada y ruidos sensoriales.
* **Puerta 3 (G3) - Parsimonia Cognitiva (*Parsimony Gate*):** Brevedad de la explicación ($\le 7$ características relevantes) para garantizar comprensibilidad humana sin sobrecarga.
* **Puerta 4 (G4) - Cobertura y Accionabilidad (*Coverage Gate*):** Proporción de la población cubierta por la regla (Anchors) o factibilidad física de los cambios prescritos (DiCE).
* **Puerta 5 (G5) - Eficiencia Computacional (*Efficiency Gate*):** Cumplimiento de los SLAs de infraestructura ($<100\text{ ms}$ para APIs interactivas, $<2,000\text{ ms}$ para auditorías batch).
* **Puerta 6 (G6) - Consistencia Inter-método (*Cross-Explainer Consistency Gate*):** Grado de concordancia entre distintos explicadores sobre una misma instancia.
* **Puerta 7 (G7) - Equidad en la Explicación (*Explanatory Fairness Gate*):** Homogeneidad de fidelidad y estabilidad a través de subgrupos demográficos protegidos.

## Formulaciones matemáticas de las métricas de evaluación

A continuación se presentan las formulaciones cuantitativas computables de cada compuerta:

### 1. Fidelidad Local Ponderada (G1)

Evalúa el coeficiente de determinación local entre el sustituto explicativo $g(z)$ y el modelo original $f(z)$ sobre el conjunto de perturbaciones $Z_x$, ponderado por la proximidad $\pi_x(z)$:

$$\text{Fidelidad}(g, f, x) = 1 - \frac{\sum_{z \in Z_x} \pi_x(z) \left( f(z) - g(z) \right)^2}{\sum_{z \in Z_x} \pi_x(z)}$$

Un valor de $1.0$ representa una réplica perfecta de la frontera local; valores inferiores a $0.85$ indican un desacoplamiento inaceptable respecto al clasificador real.

### 2. Estabilidad Local basada en la Constante de Lipschitz y Similitud Coseno (G2)

Teóricamente, la estabilidad se define acotando la constante de Lipschitz del operador explicativo $E(x) \in \mathbb{R}^{\vert F \vert}$ en una bola de radio $\epsilon$:

$$\text{Estabilidad}(E, x, \epsilon) = 1 - \max_{x' : \Vert x - x' \Vert_2 \le \epsilon} \frac{\Vert E(x) - E(x') \Vert_2}{\Vert x - x' \Vert_2}$$

Para viabilizar este cómputo de manera determinista y escalable en producción, FOM-7 calcula la **similitud coseno media** entre vectores de atribución obtenidos bajo perturbaciones gaussianas controladas ($\sigma_{\text{ruido}} = 0.05 \cdot \sigma_X$):

$$\text{Estabilidad}_{\text{cos}}(E, x) = \frac{1}{B} \sum_{b=1}^B \frac{E(x) \cdot E(x + \delta_b)}{\Vert E(x) \Vert_2 \, \Vert E(x + \delta_b) \Vert_2}$$

donde $B$ es el número de muestras de validación y $\delta_b \sim \mathcal{N}(0, \sigma^2 I)$. Un valor próximo a $1.0$ garantiza que ruidos menores no alterarán la jerarquía de factores reportados.

### 3. Parsimonia y Escasez de Coeficientes (G3)

Mide la fracción de variables cuya atribución absoluta cae por debajo de un umbral de significancia práctica $\tau$:

$$\text{Escasez}(E(x), \tau) = \frac{1}{\vert F \vert} \sum_{i=1}^{\vert F \vert} \mathbb{I}(\vert \phi_i(x) \vert \le \tau)$$

### 4. Cobertura Empírica de Reglas (G4)

Para métodos basados en predicados condicionales (Anchors), cuantifica la proporción de registros del conjunto de prueba $N$ que satisfacen los antecedentes del ancla $A$:

$$\text{Cobertura}(A) = \frac{1}{N} \sum_{j=1}^{N} \mathbb{I}(A(x_j) = 1)$$

### 5. Latencia Computacional Media (G5)

Tiempo medio de CPU/GPU $t(E, x_k)$ requerido para generar la explicación de una instancia sobre un lote de $M$ casos:

$$\bar{T}_{exp} = \frac{1}{M} \sum_{k=1}^{M} t(E, x_k) \quad [\text{ms/instancia}]$$

### 6. Consistencia Inter-método (G6)

Mide la correlación de rangos de Spearman entre los vectores de atribución generados por dos explicadores $E_1$ y $E_2$ sobre la misma instancia:

$$\text{Consistencia}(E_1, E_2, x) = 1 - \frac{6 \sum_{i=1}^{|F|} d_i^2}{|F| (|F|^2 - 1)}$$

donde $d_i$ es la diferencia entre los rangos asignados a la característica $i$.

### 7. Equidad en la Explicación (G7)

Evalúa la paridad en la fidelidad local media entre subgrupos demográficos protegidos (como género o etnia), aplicando el criterio regulatorio de la regla de los cuatro quintos:

$$\text{Paridad}(G_1) = \min_{a, b \in \mathcal{A}} \frac{\bar{G}_1(A = a)}{\bar{G}_1(A = b)} \ge 0.80$$

## Criterios de Aprobación para Auditoría de Producción

Para que un pipeline de inferencia sea certificado para producción bajo el protocolo FOM-7, debe satisfacer concurrentemente:

* **Umbral de Fidelidad:** $\text{Fidelidad} \ge 0.85$ (G1), impidiendo que el explicador emita aproximaciones espurias.
* **Umbral de Estabilidad:** $\text{Estabilidad} \ge 0.80$ (G2), asegurando que ruidos instrumentales no alteren el veredicto explicativo.
* **Presupuesto de Latencia:** $\bar{T}_{exp} \le 100\text{ ms}$ para microservicios interactivos, o $\bar{T}_{exp} \le 2,000\text{ ms}$ para auditorías batch.

La Tabla 1 consolida las especificaciones técnicas de cada compuerta del protocolo FOM-7.

<!-- TABLA: table_metrics.md -->
