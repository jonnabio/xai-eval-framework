# El protocolo operativo FOM-7

## El concepto: Un harness de pruebas automatizadas para XAI

En la ingeniería de datos moderna, la calidad de las tablas y pipelines se asegura mediante frameworks de pruebas automatizadas como `pytest`, `dbt test` o `Great Expectations`, los cuales verifican aserciones concretas sobre los datos (completitud, unicidad, rangos de distribución) antes de permitir que una tabla pase a consumo analítico.

El marco **FOM-7** (*Framework for Operational Metrics in 7 Gates*) traslada este mismo principio de ingeniería al dominio de la explicabilidad algorítmica. Concebido como un **harness de certificación cuantitativa estructurado en siete puertas de control secuenciales**, FOM-7 evalúa si un explicador post-hoc es matemáticamente fiel, estable, legible, eficiente y equitativo antes de autorizar su despliegue en un entorno operativo:

* **Puerta 1 (G1) - Fidelidad Local (*Fidelity Gate*):** ¿Con qué precisión el sustituto interpretable $g$ reproduce las predicciones del clasificador primario $f$ en la vecindad del registro auditado?
* **Puerta 2 (G2) - Estabilidad y Robustez (*Stability Gate*):** ¿Se mantienen las explicaciones coherentes ante perturbaciones leves de entrada y ruidos sensoriales, o colapsan estocásticamente?
* **Puerta 3 (G3) - Parsimonia Cognitiva (*Parsimony Gate*):** ¿Es la explicación suficientemente compacta ($\le 7$ características relevantes) para ser comprendida por un operador humano sin sobrecarga cognitiva?
* **Puerta 4 (G4) - Cobertura y Accionabilidad (*Coverage Gate*):** ¿Qué porcentaje de la población queda cubierto por la regla de decisión (Anchors), o qué tan realizables son los cambios requeridos (DiCE)?
* **Puerta 5 (G5) - Eficiencia Computacional (*Efficiency Gate*):** ¿Cumple la latencia del explicador con los Acuerdos de Nivel de Servicio (*SLAs*) de la arquitectura de inferencia ($<100\text{ ms}$ para APIs interactivas, $<2,000\text{ ms}$ para auditorías batch)?
* **Puerta 6 (G6) - Consistencia Inter-método (*Cross-Explainer Consistency Gate*):** ¿Coinciden distintos explicadores en los factores determinantes para el mismo registro, o discrepan en sus conclusiones?
* **Puerta 7 (G7) - Equidad en la Explicación (*Explanatory Fairness Gate*):** ¿Mantiene el explicador una fidelidad y estabilidad homogéneas entre diferentes subgrupos demográficos protegidos, evitando zonas oscuras en la auditoría?

## Formulaciones matemáticas de las métricas de evaluación

A continuación se presentan las formulaciones cuantitativas computables que sustentan cada una de las puertas del protocolo FOM-7:

### 1. Fidelidad Local Ponderada (G1)

La fidelidad evalúa el coeficiente de determinación local entre el sustituto explicativo $g(z)$ y el modelo original $f(z)$ sobre el conjunto de perturbaciones $Z_x$, ponderado por la proximidad $\pi_x(z)$:

$$\text{Fidelidad}(g, f, x) = 1 - \frac{\sum_{z \in Z_x} \pi_x(z) \left( f(z) - g(z) \right)^2}{\sum_{z \in Z_x} \pi_x(z)}$$

Un valor de fidelidad de $1.0$ representa una réplica perfecta de la superficie de decisión local, mientras que valores inferiores a $0.85$ indican que el explicador está inventando una aproximación desacoplada del clasificador real.

### 2. Estabilidad Local basada en la Constante de Lipschitz y Similitud Coseno (G2)

Teóricamente, la estabilidad se define acotando la constante de Lipschitz del operador explicativo $E(x) \in \mathbb{R}^{\vert F \vert}$ dentro de una bola de perturbación de radio $\epsilon$:

$$\text{Estabilidad}(E, x, \epsilon) = 1 - \max_{x' : \Vert x - x' \Vert_2 \le \epsilon} \frac{\Vert E(x) - E(x') \Vert_2}{\Vert x - x' \Vert_2}$$

Para viabilizar este cómputo de manera determinista y escalable en pipelines industriales de producción, FOM-7 operacionaliza esta métrica calculando la **similitud coseno media** entre los vectores de atribución obtenidos al aplicar perturbaciones gaussianas controladas de pequeña escala ($\sigma_{\text{ruido}} = 0.05 \cdot \sigma_X$):

$$\text{Estabilidad}_{\text{cos}}(E, x) = \frac{1}{B} \sum_{b=1}^B \frac{E(x) \cdot E(x + \delta_b)}{\Vert E(x) \Vert_2 \, \Vert E(x + \delta_b) \Vert_2}$$

donde $B$ es el número de muestras de validación y $\delta_b \sim \mathcal{N}(0, \sigma^2 I)$. Un valor próximo a $1.0$ garantiza que ruidos menores en los sensores o en los datos no invertirán la jerarquía de factores reportados.

### 3. Parsimonia y Escasez de Coeficientes (G3)

Mide la fracción de variables cuya atribución absoluta cae por debajo de un umbral de significancia práctica $\tau$ (filtrando el ruido de fondo):

$$\text{Escasez}(E(x), \tau) = \frac{1}{\vert F \vert} \sum_{i=1}^{\vert F \vert} \mathbb{I}(\vert \phi_i(x) \vert \le \tau)$$

Una alta escasez asegura que el artefacto presentado al analista humano no contenga decenas de coeficientes residuales que dificulten la interpretación.

### 4. Cobertura Empírica de Reglas (G4)

Para explicadores basados en predicados condicionales (Anchors), la cobertura cuantifica la proporción de registros en el conjunto de prueba $N$ que satisfacen los antecedentes del ancla $A$:

$$\text{Cobertura}(A) = \frac{1}{N} \sum_{j=1}^{N} \mathbb{I}(A(x_j) = 1)$$

### 5. Latencia Computacional Media (G5)

Calcula el tiempo medio de CPU/GPU $t(E, x_k)$ consumido para generar la explicación completa de una instancia sobre un lote de prueba de $M$ casos:

$$\bar{T}_{exp} = \frac{1}{M} \sum_{k=1}^{M} t(E, x_k) \quad [\text{ms/instancia}]$$

## Criterios de Aprobación para Auditoría de Producción

Para que un pipeline de inferencia con explicabilidad sea homologado para producción en sistemas de alto impacto bajo el protocolo FOM-7, debe satisfacer de forma concurrente los siguientes umbrales numéricos de corte:

* **Umbral de Fidelidad:** $\text{Fidelidad} \ge 0.85$ (G1), impidiendo que el explicador emita aproximaciones infieles a la caja negra.
* **Umbral de Estabilidad:** $\text{Estabilidad} \ge 0.80$ (G2), asegurando que ruidos instrumentales no alteren el veredicto explicativo.
* **Presupuesto de Latencia:** $\bar{T}_{exp} \le 100\text{ ms}$ para microservicios de decisión interactiva en tiempo real, o $\bar{T}_{exp} \le 2,000\text{ ms}$ para auditorías regulatorias por lotes fuera de línea.

La Tabla 1 consolida las especificaciones técnicas y rangos de referencia de cada una de las compuertas del protocolo FOM-7.

<!-- TABLA: table_metrics.md -->
