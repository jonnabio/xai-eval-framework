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

Esta métrica opera análogamente a un coeficiente de determinación local $R^2$: el numerador suma las discrepancias al cuadrado entre la predicción de la caja negra $f(z)$ y la del sustituto $g(z)$ ponderadas por proximidad $\pi_x(z)$, mientras el denominador normaliza por la masa total de ponderación. Un valor de $1.0$ indica coincidencia absoluta en toda la vecindad; valores inferiores a $0.85$ evidencian que el sustituto no refleja fielmente la frontera del modelo.

### 2. Estabilidad Local basada en la Constante de Lipschitz y Similitud Coseno (G2)

Teóricamente, la estabilidad se define acotando la constante de Lipschitz máxima del operador explicativo $E(x) \in \mathbb{R}^{\vert F \vert}$ dentro de una bola de perturbación de radio $\epsilon$:

$$\text{Estabilidad}(E, x, \epsilon) = 1 - \max_{x' : \Vert x - x' \Vert_2 \le \epsilon} \frac{\Vert E(x) - E(x') \Vert_2}{\Vert x - x' \Vert_2}$$

La fracción $\frac{\|E(x) - E(x')\|_2}{\|x - x'\|_2}$ mide la tasa máxima de variación del vector de explicación frente a una variación en la entrada. Si un cambio microscópico en los datos genera un giro brusco en las atribuciones, la fracción se dispara y la estabilidad colapsa.

Para operacionalizar este cálculo de manera escalable y determinista en pipelines de producción, FOM-7 evalúa la **similitud coseno media** entre los vectores de atribución obtenidos sobre $B$ perturbaciones gaussianas controladas ($\sigma_{\text{ruido}} = 0.05 \cdot \sigma_X$):

$$\text{Estabilidad}_{\text{cos}}(E, x) = \frac{1}{B} \sum_{b=1}^B \frac{E(x) \cdot E(x + \delta_b)}{\Vert E(x) \Vert_2 \, \Vert E(x + \delta_b) \Vert_2}$$

donde el producto punto dividido por el producto de las normas euclidianas mide si las explicaciones apuntan en la misma dirección geométrica en el espacio de características. Un valor de $1.0$ certifica que los factores destacados y sus signos son idénticos bajo ruido; valores por debajo de $0.80$ alertan sobre volatilidad estocástica inaceptable.

### 3. Parsimonia y Escasez de Coeficientes (G3)

Mide la fracción de variables cuya atribución absoluta cae por debajo de un umbral de significancia práctica $\tau$ (típicamente $\tau = 0.01$):

$$\text{Escasez}(E(x), \tau) = \frac{1}{\vert F \vert} \sum_{i=1}^{\vert F \vert} \mathbb{I}(\vert \phi_i(x) \vert \le \tau)$$

donde $|F|$ es la cantidad total de columnas. Una escasez elevada (por ejemplo, $\ge 0.85$ en una tabla de 100 variables) indica que el explicador filtra el ruido de fondo y concentra la atención en pocas variables críticas.

### 4. Cobertura Empírica de Reglas (G4)

Para métodos basados en predicados condicionales (Anchors), cuantifica la proporción de registros del conjunto de prueba $N$ que satisfacen los antecedentes del ancla $A$:

$$\text{Cobertura}(A) = \frac{1}{N} \sum_{j=1}^{N} \mathbb{I}(A(x_j) = 1)$$

donde $A(x_j) = 1$ indica que el registro $j$ cumple todos los predicados de la regla.

### 5. Latencia Computacional Media (G5)

Tiempo medio de CPU/GPU $t(E, x_k)$ requerido para generar la explicación completa de una instancia sobre un lote representativo de $M$ casos:

$$\bar{T}_{exp} = \frac{1}{M} \sum_{k=1}^{M} t(E, x_k) \quad [\text{ms/instancia}]$$

### 6. Consistencia Inter-método (G6)

Mide el coeficiente de correlación de rangos de Spearman entre las jerarquías de variables ordenadas por dos explicadores $E_1$ y $E_2$ sobre la misma instancia:

$$\text{Consistencia}(E_1, E_2, x) = 1 - \frac{6 \sum_{i=1}^{|F|} d_i^2}{|F| (|F|^2 - 1)}$$

donde $d_i = \text{rango}(E_1)_i - \text{rango}(E_2)_i$ es la diferencia entre los puestos asignados a la variable $i$ por ambos métodos. Si ambos explicadores coinciden exactamente en el orden de las variables, $d_i = 0$ para toda $i$ y la consistencia es $+1.0$; si entregan órdenes invertidos, la consistencia se degrada hacia $-1.0$.

### 7. Equidad en la Explicación (G7)

Evalúa la paridad en la fidelidad local media entre subgrupos demográficos protegidos (como género o etnia), aplicando el criterio regulatorio de la regla de los cuatro quintos (*Four-Fifths Rule*):

$$\text{Paridad}(G_1) = \min_{a, b \in \mathcal{A}} \frac{\bar{G}_1(A = a)}{\bar{G}_1(A = b)} \ge 0.80$$

donde $\bar{G}_1(A = a)$ es la fidelidad media del explicador en el subgrupo protegido $a$, y $\mathcal{A}$ es el conjunto de subgrupos. La razón compara el grupo con menor fidelidad frente al grupo con mayor fidelidad: si la razón cae por debajo de $0.80$, existe una brecha discriminatoria inadmisible en la calidad de la auditoría.

## Criterios de Aprobación para Auditoría de Producción

Para que un pipeline de inferencia sea certificado para producción bajo el protocolo FOM-7, debe satisfacer concurrentemente:

* **Umbral de Fidelidad:** $\text{Fidelidad} \ge 0.85$ (G1), impidiendo que el explicador emita aproximaciones espurias.
* **Umbral de Estabilidad:** $\text{Estabilidad} \ge 0.80$ (G2), asegurando que ruidos instrumentales no alteren el veredicto explicativo.
* **Presupuesto de Latencia:** $\bar{T}_{exp} \le 100\text{ ms}$ para microservicios interactivos, o $\bar{T}_{exp} \le 2,000\text{ ms}$ para auditorías batch.

La Tabla 1 consolida las especificaciones técnicas de cada compuerta del protocolo FOM-7.

<!-- TABLA: table_metrics.md -->
