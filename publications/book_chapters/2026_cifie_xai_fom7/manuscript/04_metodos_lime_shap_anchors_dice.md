# Métodos de explicabilidad: LIME, SHAP, Anchors y DiCE

## Diversidad de artefactos explicativos

En el desarrollo de software analítico, no todos los problemas requieren el mismo tipo de salida. Dependiendo del consumidor final —un analista de datos, un oficial de cumplimiento legal o un cliente que consulta una aplicación móvil—, los métodos agnósticos post-hoc producen diferentes **objetos explicativos**:

1. **Atribuciones numéricas continuas de características:** Vectores de números reales que indican el peso positivo o negativo que cada columna aportó a la predicción puntual (LIME, KernelSHAP).
2. **Reglas de decisión booleanas:** Condiciones lógicas en lenguaje formal (`SI x1 > 3 AND x2 = 'A' ENTONCES predicción = 1`) que delimitan una región de certeza inalterable (Anchors).
3. **Explicaciones contrafactuales prescriptivas:** Muestras sintéticas que indican cuál es la perturbación mínima sobre los datos de entrada necesaria para cambiar la predicción del modelo hacia una categoría favorable (`¿Qué atributos debe cambiar el usuario para ser aprobado?`) (DiCE).

![Figura 3. Cuatro objetos explicativos y métodos agnósticos evaluados en FOM-7. Fuente: elaboración propia a partir de Ribeiro *et al.* (2016, 2018), Lundberg y Lee (2017) y Mothilal *et al.* (2020).](../figures/exported/fig_d4_objetos_explicativos_es.png)

La Figura 3 sintetiza estos cuatro objetos explicativos y sus respectivos métodos agnósticos representativos. A continuación se detalla el funcionamiento algorítmico, las fórmulas matemáticas y los retos de ingeniería de cada uno.

## LIME: Explicaciones locales interpretables agnósticas al modelo

Propuesto por Ribeiro *et al.* (2016), **LIME** (*Local Interpretable Model-agnostic Explanations*) parte de una intuición geométrica muy potente para cualquier ingeniero: aunque una función de aprendizaje automático $f(x)$ sea extremadamente compleja, irregular y no lineal a escala global, **en la vecindad inmediata de un punto específico $x$ la frontera puede aproximarse mediante un plano tangente simple** (un modelo lineal interpretable $g \in G$).

### Mecanismo algorítmico paso a paso

Para construir esta aproximación local alrededor de un registro $x$:
1. **Generación de perturbaciones:** LIME genera un conjunto de $K$ muestras sintéticas $z'$ en el entorno de $x$ aplicando ruido gaussiano sobre variables continuas y muestreo aleatorio uniforme sobre categorías.
2. **Evaluación de la caja negra:** Envía esas $K$ muestras a la función de inferencia del clasificador primario para obtener sus probabilidades predichas $f(z')$.
3. **Ponderación por proximidad:** Asigna a cada muestra sintética $z'$ un peso $\pi_x(z)$ utilizando un núcleo de decaimiento exponencial basado en la distancia $D(x, z)$ (usualmente euclidiana o coseno):
$$\pi_x(z) = \exp\left( -\frac{D(x, z)^2}{\sigma^2} \right)$$
donde $\sigma$ es el ancho de banda del núcleo (un hiperparámetro que define el radio de la "vecindad").
4. **Ajuste del modelo sustituto:** Ajusta una regresión lineal ponderada resolviendo el siguiente problema de optimización:
$$\xi(x) = \arg\min_{g \in G} \mathcal{L}(f, g, \pi_x) + \Omega(g)$$
donde $\mathcal{L}$ representa el error cuadrático medio ponderado entre las predicciones del modelo complejo $f(z)$ y las del modelo sustituto $g(z)$, y $\Omega(g)$ es un término de regularización (por ejemplo, penalización L1 tipo Lasso) que fuerza a que solo un número reducido de características mantenga coeficientes distintos de cero.

### El riesgo operacional en ingeniería: Muestras fuera de distribución (*OOD*)

Desde la perspectiva de la ingeniería de datos, el punto débil de LIME reside en su generador de perturbaciones. Al perturbar cada columna de forma independiente e ingenua, LIME puede generar filas sintéticas que violan por completo la integridad relacional de la base de datos (por ejemplo, combinando `Edad = 18` con `Años_Estudio = 22` y `Nivel_Ingresos = Alto`). El clasificador de caja negra se ve forzado a evaluar instancias situadas en regiones vacías del espacio de datos (*Out-of-Distribution*, OOD), lo que puede inducir pendientes locales engañosas en el sustituto lineal.

## SHAP: Explicaciones aditivas basadas en teoría de juegos cooperativos

Desarrollado por Lundberg y Lee (2017), **SHAP** (*SHapley Additive exPlanations*) aborda la atribución de características transformando el problema de explicabilidad en un juego cooperativo de teoría de juegos, fundamentado en los trabajos clásicos de Shapley (1953).

### La intuición para el ingeniero de datos

Imagine un equipo de ingeniería donde cuatro columnas de una tabla (`Ingresos`, `Puntuacion_Crediticia`, `Edad`, `Deuda_Total`) colaboran para producir un veredicto de probabilidad $f(x) = 0.85$, superando la probabilidad media esperada en la base de datos $\mathbb{E}[f(X)] = 0.50$. La diferencia total a explicar es de $+0.35$. ¿Cómo distribuir equitativamente ese diferencial de $+0.35$ entre las cuatro columnas?

Si evaluamos el impacto de añadir `Puntuacion_Crediticia` en solitario, su aporte marginal puede ser $+0.20$. Pero si `Ingresos` ya formaba parte del subconjunto considerado, añadir `Puntuacion_Crediticia` podría aportar solo $+0.08$, debido a la correlación y redundancia de información entre ambas.

La solución de Shapley consiste en calcular el **aporte marginal promedio de cada característica considerando todas las combinaciones o coaliciones posibles** de variables:

$$\phi_i(x) = \sum_{S \subseteq F \setminus \{i\}} \frac{\vert S \vert ! (\vert F \vert - \vert S \vert - 1)!}{\vert F \vert !} \left[ f_x(S \cup \{i\}) - f_x(S) \right]$$

donde $F$ es el conjunto de todas las características, $S$ representa un subconjunto de características (coalición) que no contiene a la variable $i$, y $f_x(S)$ denota la predicción esperada del modelo condicionada exclusivamente a los valores observados en la coalición $S$.

### Los cuatro axiomas de Shapley

La supremacía teórica de SHAP radica en que es el **único** método de atribución local que satisface simultáneamente cuatro axiomas matemáticos fundamentales:
1. **Eficiencia (Aditividad local):** La suma de los valores de Shapley de todas las características reproduce exactamente la diferencia entre la predicción local y el valor esperado poblacional: $\sum_{i=1}^{\vert F \vert} \phi_i(x) = f(x) - \mathbb{E}[f(X)]$.
2. **Simetría:** Si dos columnas contribuyen de forma idéntica a todas las coaliciones posibles, reciben exactamente el mismo valor de atribución ($\phi_i = \phi_j$).
3. **Jugador nulo (*Dummy*):** Si una columna no altera la predicción del modelo en ninguna coalición posible, su contribución asignada es estrictamente cero ($\phi_i = 0$).
4. **Monotonicidad (Consistencia):** Si el modelo se modifica de modo que la contribución marginal de una característica aumenta o se mantiene igual en todas las coaliciones, su valor atribuido no puede decrecer.

### El reto computacional en producción: La explosión combinatoria

Para un conjunto con $M$ variables, existen $2^M$ posibles coaliciones de características. En una tabla pequeña con $M=10$ columnas, esto implica $1,024$ evaluaciones. Pero en un esquema tabular realista con $M=30$ variables, el cálculo exacto requeriría evaluar más de mil millones de combinaciones ($2^{30} \approx 1.07 \times 10^9$), lo cual resulta computacionalmente intratable.

Para solventar esta barrera, **KernelSHAP** utiliza un esquema de regresión ponderada mediante un núcleo combinatorio que estima los valores de Shapley mediante muestreo estocástico. Aunque esta aproximación hace viable el cálculo sobre cajas negras arbitrarias, la latencia resultante sigue siendo de aproximadamente $1,180\text{ ms}$ por registro, convirtiéndolo en un método adecuado para auditorías periódicas por lotes (*batch*), pero prohibitivo para APIs de inferencia en tiempo real que manejan miles de peticiones por segundo.

## Anchors: Reglas condicionales con garantías matemáticas formales

Mientras que LIME y SHAP devuelven pesos continuos, **Anchors** (Ribeiro *et al.*, 2018) genera explicaciones estructuradas como reglas de decisión lógicas del tipo `SI-ENTONCES`, un formato de enorme valor para la formulación de políticas y validación de reglas de negocio en ingeniería.

Una regla $A$ (denominada "ancla") es un conjunto de predicados booleanos sobre las variables de entrada (por ejemplo, $\text{Edad} > 35 \land \text{Estado\_Civil} = \text{Casado}$). La regla es válida si garantiza que, mientras se cumplan dichos predicados, la predicción del modelo se mantendrá invariable con una certeza probabilística formal bajo el marco PAC (*Probably Approximately Correct*):

$$P\left( \text{prec}(A) \ge 1 - \gamma \right) \ge 1 - \delta$$

donde la precisión local $\text{prec}(A)$ mide la proporción de perturbaciones locales $z$ que preservan la predicción del modelo original:

$$\text{prec}(A) = \mathbb{E}_{z \sim D(z|A)} \left[ \mathbb{I}(f(x) = f(z)) \right]$$

aquí $\gamma$ es el margen de tolerancia de error (por ejemplo, $0.05$ para una precisión del $95\%$), y $\delta$ representa el nivel de significancia estadística.

El algoritmo busca maximizar la **cobertura** (*coverage*) de la regla, entendida como la proporción de la población que cumple los criterios del ancla:

$$\text{cov}(A) = P_{z \sim D}(A(z) = 1)$$

Para explorar el inmenso espacio combinatorio de reglas posibles sin saturar el clasificador con millones de inferencias, Anchors implementa una búsqueda por haces (*beam search*) guiada por algoritmos de bandidos multi-brazo (*Multi-Armed Bandits*), evaluando prioritariamente las reglas más prometedoras.

## DiCE: Explicaciones contrafactuales diversas y recurso accionable

Propuesto por Mothilal *et al.* (2020), **DiCE** (*Diverse Counterfactual Explanations*) cambia radicalmente el enfoque de la explicabilidad: en lugar de explicar qué variables impulsaron la decisión pasada, responde a la pregunta prospectiva del usuario: *¿Cuál es el conjunto mínimo de cambios en mis datos que lograría que el modelo apruebe mi solicitud?*

### Formulación matemática y restricciones de mutabilidad

En un pipeline analítico real, no todas las variables pueden modificarse. Un contrafactual debe respetar restricciones de ingeniería indispensables:
* **Variables inmutables:** Atributos como la *Edad*, la *Fecha de Nacimiento* o el *País de Origen* no pueden ser alterados.
* **Variables con dirección monótona:** La *Antigüedad Laboral* solo puede aumentar, no disminuir.
* **Rangos físicamente factibles:** No se puede sugerir a un usuario tener un saldo negativo imposible o una jornada laboral de 120 horas semanales.

Dado un punto original $x$ y una categoría objetivo deseada $y^*$, DiCE formula la búsqueda de un conjunto de $k$ contrafactuales diversos $\{c_1, \dots, c_k\}$ resolviendo una optimización con tres términos concurrentes:

$$\min_{c_1, \dots, c_k} \frac{1}{k} \sum_{i=1}^k \mathcal{L}_{loss}(f(c_i), y^*) + \frac{\lambda_1}{k} \sum_{i=1}^k \text{dist}(x, c_i) - \lambda_2 \text{dpp}(c_1, \dots, c_k)$$

donde:
* $\mathcal{L}_{loss}$ penaliza a los contrafactuales cuya predicción en el clasificador no alcance la clase deseada $y^*$.
* $\text{dist}(x, c_i)$ penaliza la distancia matemática (combinando norma L1 para numéricas y distancia de Hamming para categóricas), forzando a que las modificaciones requeridas sean mínimas y realistas.
* $\text{dpp}(c_1, \dots, c_k)$ es una función de diversidad basada en Procesos de Determinantes Puntos (*Determinantal Point Processes*), la cual asegura que los $k$ contrafactuales devueltos propongan caminos de acción cualitativamente diferentes (por ejemplo, un camino basado en elevar el ahorro frente a un camino alternativo basado en reestructurar deudas existentes).

## Compromisos operacionales entre explicadores

Ningún explicador agnóstico es óptimo en todas las dimensiones operacionales. La selección de una herramienta exige asumir compromisos estructurales (*trade-offs*):

![Figura 5. Marco sintético de trade-offs operacionales en evaluación post-hoc de XAI. Fuente: elaboración propia a partir de Tabassi (2023) y Phillips *et al.* (2021).](../figures/exported/fig_d5_ciclo_audiencias_es.png)

Como resume la Figura 5:
* **KernelSHAP:** Ofrece la máxima solidez matemática y consistencia teórica, pero impone una latencia computacional elevada ($>1\text{ s}$ por instancia).
* **LIME:** Proporciona inferencias rápidas ($<50\text{ ms}$) y alta parsimonia, pero adolece de inestabilidad estocástica y sensibilidad a muestras fuera de distribución.
* **Anchors:** Entrega reglas deterministas de certidumbre formal inalterable, pero a costa de una cobertura poblacional reducida ($12\%$--$28\%$).
* **DiCE:** Aporta el mayor valor prescriptivo para el usuario final, pero requiere optimizaciones numéricas iterativas que demandan una configuración cuidadosa de restricciones de dominio.
