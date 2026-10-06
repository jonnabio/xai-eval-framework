# El protocolo operativo FOM-7

## El marco conceptual FOM-7

El marco **FOM-7** (*Framework for Operational Metrics in 7 Gates*) se define como un protocolo estandarizado de auditoría cuantitativa diseñado para evaluar y certificar la calidad operacional de los explicadores post-hoc agnósticos. Inspirado en los procesos de certificación industrial por puertas de control (*stage-gate review processes*), FOM-7 organiza la evaluación del explicador en siete puertas secuenciales e independientes de verificación:

* **Puerta 1 (G1) - Fidelidad Local y Global (*Fidelity Gate*):** Evalúa con qué exactitud el artefacto explicativo secundario $g$ reproduce las decisiones y probabilidades emitidas por el modelo primario de caja negra $f$ en la región de interés.
* **Puerta 2 (G2) - Estabilidad y Robustez Local (*Stability Gate*):** Mide la capacidad del explicador para mantener atribuciones consistentes ante perturbaciones menores y ruido estocástico en la instancia de entrada.
* **Puerta 3 (G3) - Complejidad e Interpretabilidad Cognitiva (*Parsimony Gate*):** Cuantifica la escasez del vector de atribución o la brevedad de la regla lógica, asegurando que la carga cognitiva impuesta al ser humano sea manejable.
* **Puerta 4 (G4) - Cobertura Operacional y Accionabilidad (*Coverage Gate*):** Mide la proporción de la población de datos que satisface la estructura explicativa y la factibilidad física o legal de ejecutar las prescripciones sugeridas.
* **Puerta 5 (G5) - Eficiencia Computacional y Latencia (*Efficiency Gate*):** Determina el tiempo de ejecución, el consumo de memoria y la escalabilidad del algoritmo explicativo respecto a la dimensión del problema.
* **Puerta 6 (G6) - Consistencia Inter-método (*Cross-Explainer Consistency Gate*):** Evalúa el grado de concordancia o correlación de rangos entre las explicaciones generadas por distintos explicadores sobre el mismo caso de estudio.
* **Puerta 7 (G7) - Equidad en la Explicación (*Explanatory Fairness Gate*):** Verifica que la fidelidad y la estabilidad de las explicaciones se mantengan homogéneas a través de subgrupos demográficos protegidos (por ejemplo, etnia, género o edad), evitando sesgos de auditoría.

## Formulaciones matemáticas de las métricas de evaluación

A continuación se exponen las formulaciones cuantitativas empleadas en FOM-7 para medir con rigor matemático las dimensiones del protocolo:

### 1. Fidelidad Local Ponderada (G1)

La fidelidad local de un modelo explicativo $g$ respecto al modelo primario $f$ en el entorno de una instancia $x$ se calcula como la infidelidad cuadrática ponderada por la distancia del núcleo $\pi_x(z)$:

$$\text{Fidelidad}(g, f, x) = 1 - \frac{\sum_{z \in Z_x} \pi_x(z) \left( f(z) - g(z) \right)^2}{\sum_{z \in Z_x} \pi_x(z)}$$

Un valor de fidelidad próximo a $1.0$ certifica que la explicación reconstruye con alta precisión el comportamiento local de la caja negra.

### 2. Estabilidad Local basada en Constante de Lipschitz (G2)

La estabilidad local de un explicador $E$ que produce atribuciones $E(x) \in \mathbb{R}^{\vert F \vert}$ se mide estimando la constante empírica de Lipschitz máxima dentro de una bola de perturbación de radio $\epsilon$:

$$\text{Estabilidad}(E, x, \epsilon) = 1 - \max_{x' : \Vert x - x' \Vert_2 \le \epsilon} \frac{\Vert E(x) - E(x') \Vert_2}{\Vert x - x' \Vert_2}$$

Donde una estabilidad de $1.0$ indica absoluta inalterabilidad ante variaciones de pequeña escala en el punto de evaluación.

### 3. Escasez y Parsimonia Cognitiva (G3)

La escasez (*sparsity*) evalúa la proporción de coeficientes de atribución cuyo valor absoluto se encuentra por debajo de un umbral de relevancia $\tau$:

$$\text{Escasez}(E(x), \tau) = \frac{1}{\vert F \vert} \sum_{i=1}^{\vert F \vert} \mathbb{I}(\vert \phi_i(x) \vert \le \tau)$$

Una alta escasez reduce la sobrecarga cognitiva al filtrar el ruido de baja importancia en la presentación final al usuario.

### 4. Cobertura Empírica de Reglas (G4)

Para métodos basados en reglas lógicas (Anchors), la cobertura mide la fracción de instancias de la población total $N$ que satisfacen las condiciones del ancla $A$:

$$\text{Cobertura}(A) = \frac{1}{N} \sum_{j=1}^{N} \mathbb{I}(A(x_j) = 1)$$

### 5. Latencia Computacional Promedio (G5)

El costo computacional se cuantifica como la latencia media $\bar{T}_{exp}$ requerida para generar una explicación local completa sobre un conjunto de evaluación de $M$ muestras:

$$\bar{T}_{exp} = \frac{1}{M} \sum_{k=1}^{M} t(E, x_k) \quad [\text{ms/instancia}]$$

## Resumen formal de las métricas del protocolo

La Tabla 1 consolida las métricas operacionales del protocolo FOM-7, especificando sus símbolos, rangos de validez y criterios de interpretación para auditoría.

<!-- TABLA: table_metrics.md -->
