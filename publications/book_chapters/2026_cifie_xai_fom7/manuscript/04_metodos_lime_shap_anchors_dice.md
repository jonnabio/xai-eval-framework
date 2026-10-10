# Métodos de explicabilidad: LIME, SHAP, Anchors y DiCE

## Diversidad de artefactos explicativos

En el desarrollo de software analítico, los métodos agnósticos post-hoc producen diferentes **objetos explicativos** según las necesidades del destinatario:

1. **Atribuciones numéricas continuas de características:** Vectores de números reales que ponderan la contribución positiva o negativa de cada variable a la predicción puntual (LIME, KernelSHAP).
2. **Reglas de decisión booleanas:** Condiciones condicionales (`SI x1 > 3 AND x2 = 'A' ENTONCES predicción = 1`) que delimitan una región de certeza inalterable (Anchors).
3. **Explicaciones contrafactuales prescriptivas:** Muestras sintéticas que indican la alteración mínima en los datos de entrada requerida para conmutar la predicción del modelo hacia una categoría deseada (DiCE).

![Figura 3. Cuatro objetos explicativos y métodos agnósticos evaluados en FOM-7. Fuente: elaboración propia a partir de Ribeiro *et al.* (2016, 2018), Lundberg y Lee (2017) y Mothilal *et al.* (2020).](../figures/exported/fig_d4_objetos_explicativos_es.png)

La Figura 3 sintetiza estos cuatro objetos explicativos y sus algoritmos representativos. A continuación se detallan sus mecanismos, ecuaciones y consideraciones de ingeniería.

## LIME: Explicaciones locales interpretables agnósticas al modelo

Propuesto por Ribeiro *et al.* (2016), **LIME** (*Local Interpretable Model-agnostic Explanations*) asume que, aunque una función de aprendizaje automático $f(x)$ sea no lineal a escala global, **en la vecindad inmediata de un punto $x$ la frontera de decisión puede aproximarse mediante un plano tangente lineal simple** ($g \in G$).

### Mecanismo algorítmico

Para construir la aproximación local alrededor de un registro $x$:
1. **Generación de perturbaciones:** Genera $K$ muestras sintéticas $z'$ en el entorno de $x$ aplicando ruido gaussiano sobre variables continuas y remuestreo sobre categóricas.
2. **Evaluación de la caja negra:** Envía las muestras $z'$ al clasificador primario para obtener sus probabilidades predichas $f(z')$.
3. **Ponderación por proximidad:** Asigna a cada muestra sintética $z'$ un peso de relevancia $\pi_x(z)$ mediante un núcleo exponencial gaussiano basado en la distancia $D(x, z)$ (distancia euclidiana o de coseno en el espacio escalado):
$$\pi_x(z) = \exp\left( -\frac{D(x, z)^2}{\sigma^2} \right)$$
donde $\sigma$ es el ancho de banda del núcleo que define el radio de la vecindad local. En términos operacionales, si la muestra perturbada $z$ es idéntica a $x$ ($D=0$), su peso es máximo ($\pi=1.0$); a medida que la distancia aumenta, el peso decae exponencialmente hacia cero, asegurando que solo los puntos muy cercanos influyan en la explicación.
4. **Ajuste del modelo sustituto:** Encuentra el modelo interpretable óptimo $g \in G$ (típicamente una regresión lineal simple $g(z') = w_0 + \sum w_i z'_i$) resolviendo:
$$\xi(x) = \arg\min_{g \in G} \mathcal{L}(f, g, \pi_x) + \Omega(g)$$
donde $\mathcal{L}$ representa el error cuadrático medio ponderado por la proximidad $\pi_x$ (midiendo la discrepancia entre las predicciones del modelo complejo $f(z)$ y las del sustituto $g(z)$), y $\Omega(g) = \alpha \sum |w_i|$ es una regularización tipo Lasso que penaliza la complejidad, forzando a que la mayoría de los pesos sean cero para entregar una explicación con pocas variables dominantes.

### Riesgo operacional: Muestras fuera de distribución (*OOD*)

Desde la perspectiva de la ingeniería de datos, el punto débil de LIME reside en perturbar columnas de forma independiente. Este procedimiento genera registros sintéticos que pueden violar la integridad lógica del esquema (por ejemplo, combinando `Edad = 18` con `Años_Estudio = 22`). Al recibir instancias situadas en zonas vacías del espacio de datos (*Out-of-Distribution*, OOD), el clasificador devuelve predicciones atípicas que pueden sesgar los coeficientes del sustituto lineal.

## SHAP: Explicaciones aditivas basadas en teoría de juegos cooperativos

Desarrollado por Lundberg y Lee (2017), **SHAP** (*SHapley Additive exPlanations*) formula la atribución de características transformando el problema en un juego cooperativo de teoría de juegos (Shapley, 1953).

### Intuición para el ingeniero de datos

Imagine que cuatro columnas de una tabla (`Ingresos`, `Puntaje_Crediticio`, `Edad`, `Deuda`) colaboran para emitir una probabilidad $f(x) = 0.85$, superando la media base $\mathbb{E}[f(X)] = 0.50$. La diferencia a explicar es de $+0.35$. El aporte marginal de `Puntaje_Crediticio` en solitario puede ser $+0.20$; pero si `Ingresos` ya forma parte del subconjunto evaluado, su aporte puede reducirse a $+0.08$ debido a la redundancia informacional entre ambas.

Shapley resuelve esta asignación calculando el **aporte marginal promedio de cada variable a través de todas las posibles combinaciones o coaliciones** de características:

$$\phi_i(x) = \sum_{S \subseteq F \setminus \{i\}} \frac{\vert S \vert ! (\vert F \vert - \vert S \vert - 1)!}{\vert F \vert !} \left[ f_x(S \cup \{i\}) - f_x(S) \right]$$

Para interpretar esta formulación:
* $F$ es el conjunto total de columnas o características.
* $S$ representa un subconjunto de características (coalición) que excluye a la variable de interés $i$.
* El término entre corchetes $[f_x(S \cup \{i\}) - f_x(S)]$ mide la contribución marginal: cuánto cambia la predicción del modelo cuando la variable $i$ se incorpora a la coalición $S$.
* La fracción con factoriales $\frac{|S|!(|F|-|S|-1)!}{|F|!}$ es un factor de ponderación probabilístico que representa la probabilidad de que la variable $i$ ingrese exactamente después del subconjunto $S$ en una permutación aleatoria uniforme de todas las características. Al promediar sobre todas las coaliciones posibles, Shapley garantiza un reparto distributivo matemáticamente justo.

### Los cuatro axiomas de Shapley

SHAP es el **único** método de atribución local que satisface cuatro propiedades axiomáticas concurrentes:
1. **Eficiencia (Aditividad local):** La suma de los valores de Shapley reproduce la desviación entre la predicción local y el valor esperado poblacional: $\sum_{i=1}^{\vert F \vert} \phi_i(x) = f(x) - \mathbb{E}[f(X)]$.
2. **Simetría:** Si dos columnas aportan lo mismo a todas las coaliciones, reciben idéntico valor de atribución ($\phi_i = \phi_j$).
3. **Jugador nulo (*Dummy*):** Si una columna no modifica la predicción en ninguna coalición, su contribución es cero ($\phi_i = 0$).
4. **Monotonicidad (Consistencia):** Si la contribución marginal de una variable no disminuye en un modelo alternativo, su valor atribuido no puede decrecer.

### Costo computacional: La explosión combinatoria y KernelSHAP

Para $M$ variables existen $2^M$ posibles coaliciones. Con $M=10$ columnas se requieren $1,024$ evaluaciones; con $M=30$, el cálculo exacto exige más de mil millones de combinaciones ($2^{30} \approx 1.07 \times 10^9$), resultando intratable.

Para cajas negras genéricas, **KernelSHAP** resuelve esta barrera estimando los valores mediante regresión lineal ponderada utilizando un núcleo combinatorio específico $\pi(z')$:

$$\pi(z') = \frac{|F| - 1}{\binom{|F|}{|z'|} |z'| (|F| - |z'|)}$$

donde $|F|$ es el número total de características y $|z'|$ es el número de variables presentes en la muestra sintética evaluada. El denominador combina el coeficiente binomial $\binom{|F|}{|z'|}$ con el tamaño de la coalición: esto asigna intencionalmente los pesos más elevados a las coaliciones extremas (aquellas con una sola variable o con casi todas), ya que es precisamente en los extremos donde resulta más sencillo aislar el efecto individual de cada atributo. Aunque viabiliza el cómputo, su latencia media ronda los $1,180\text{ ms}$ por registro, siendo adecuada para lotes pero costosa para tiempo real.

## Anchors: Reglas condicionales con garantías formales

A diferencia de los vectores continuos, **Anchors** (Ribeiro *et al.*, 2018) genera explicaciones estructuradas como reglas de decisión lógicas `SI-ENTONCES`.

Una regla $A$ (el "ancla") es un conjunto de predicados booleanos sobre las variables de entrada (por ejemplo, $\text{Edad} > 35 \land \text{Estado\_Civil} = \text{Casado}$). La regla es válida si garantiza que, mientras se cumplan dichos predicados, la predicción del modelo se mantendrá invariable con una certeza probabilística formal bajo el marco PAC (*Probably Approximately Correct*):

$$P\left( \text{prec}(A) \ge 1 - \gamma \right) \ge 1 - \delta$$

donde la precisión local $\text{prec}(A)$ mide la proporción de perturbaciones locales $z$ que preservan la predicción original $f(x)$:

$$\text{prec}(A) = \mathbb{E}_{z \sim D(z|A)} \left[ \mathbb{I}(f(x) = f(z)) \right]$$

En estas ecuaciones:
* $\mathbb{I}(\cdot)$ es la función indicadora booleana (retorna $1$ si la condición se cumple y $0$ en caso contrario).
* $D(z|A)$ es la distribución de perturbaciones locales condicionada a que se cumplan las reglas de $A$.
* $\gamma$ representa el margen de error tolerable (por ejemplo, $\gamma = 0.05$ para exigir un $95\%$ de precisión).
* $\delta$ representa el riesgo de fallo estadístico admisible (por ejemplo, $\delta = 0.01$ para un $99\%$ de confianza estadística). En términos prácticos, la regla garantiza que tenemos al menos un $99\%$ de certeza de que la precisión local superará el $95\%$.

El algoritmo busca simultáneamente maximizar la **cobertura** (*coverage*) de la regla en la población:

$$\text{cov}(A) = P_{z \sim D}(A(z) = 1)$$

donde $A(z) = 1$ indica que la instancia $z$ satisface todas las condiciones del ancla. La cobertura mide el porcentaje de la base de datos que se rige por esta regla. Anchors implementa una búsqueda por haces (*beam search*) guiada por bandidos multi-brazo (*Multi-Armed Bandits*), explorando eficientemente el espacio combinatorio de reglas candidatas sin evaluar innecesariamente el clasificador.

## DiCE: Explicaciones contrafactuales diversas y recurso accionable

Propuesto por Mothilal *et al.* (2020), **DiCE** (*Diverse Counterfactual Explanations*) adopta un enfoque prescriptivo: responde a la pregunta del usuario: *¿Cuál es el cambio mínimo en mis variables que lograría que el modelo apruebe la solicitud?*

En producción, un contrafactual debe respetar restricciones de ingeniería indispensables:
* **Variables inmutables:** Atributos como la *Edad* o el *País de Origen* no pueden ser modificados.
* **Dirección monótona:** La *Antigüedad Laboral* solo puede aumentar.
* **Rangos factibles:** Evitar combinaciones imposibles (como jornadas de 120 horas semanales).

Dado un punto $x$ y una clase deseada $y^*$, DiCE optimiza un conjunto de $k$ contrafactuales $\{c_1, \dots, c_k\}$ resolviendo:

$$\min_{c_1, \dots, c_k} \frac{1}{k} \sum_{i=1}^k \mathcal{L}_{loss}(f(c_i), y^*) + \frac{\lambda_1}{k} \sum_{i=1}^k \text{dist}(x, c_i) - \lambda_2 \text{dpp}(c_1, \dots, c_k)$$

Esta función de pérdida equilibra tres objetivos mediante hiperparámetros de penalización $\lambda_1$ y $\lambda_2$:
* **Validez de clase ($\mathcal{L}_{loss}$):** Penaliza si la predicción sobre el contrafactual $f(c_i)$ no alcanza la categoría deseada $y^*$ (fuerza al modelo a cambiar de veredicto).
* **Proximidad física ($\text{dist}$):** Penaliza la distancia entre el usuario original $x$ y el contrafactual $c_i$ (combinando norma L1 para variables continuas y distancia de Hamming para categóricas), garantizando que las modificaciones requeridas sean mínimas.
* **Diversidad prescriptiva ($\text{dpp}$):** Resta el término $\text{dpp}(c_1, \dots, c_k) = \det(\mathbf{K})$, donde $\mathbf{K}$ es una matriz de similitud entre contrafactuales ($K_{i,j} = \frac{1}{1 + \text{dist}(c_i, c_j)}$). Al restar el determinante, el optimizador maximiza la separación espacial entre los $k$ contrafactuales, entregando opciones cualitativamente distintas (por ejemplo, una opción basada en elevar ingresos frente a otra basada en reducir endeudamiento).

## Compromisos operacionales entre explicadores

La selección de un explicador exige asumir compromisos de diseño (*trade-offs*):

![Figura 5. Marco sintético de trade-offs operacionales en evaluación post-hoc de XAI. Fuente: elaboración propia a partir de Tabassi (2023) y Phillips *et al.* (2021).](../figures/exported/fig_d5_ciclo_audiencias_es.png)

Como resume la Figura 5:
* **KernelSHAP:** Máxima solidez axiomática y fidelidad local, a costa de una latencia computacional elevada ($>1\text{ s}$ por instancia).
* **LIME:** Inferencias veloces ($<50\text{ ms}$) y alta parsimonia, sujeto a inestabilidad estocástica y sensibilidad a muestras OOD.
* **Anchors:** Reglas deterministas de certidumbre formal inalterable, con cobertura poblacional acotada ($12\%$--$28\%$).
* **DiCE:** Alto valor prescriptivo para el usuario final, requiriendo optimizaciones numéricas iterativas con restricciones de dominio.
