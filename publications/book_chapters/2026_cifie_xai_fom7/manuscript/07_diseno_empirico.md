# Diseño empírico y banco de pruebas

## El banco de datos de prueba: UCI Adult Income

Para validar experimentalmente el protocolo **FOM-7**, se diseñó un banco de pruebas sobre el conjunto de datos tabular *UCI Adult Income* (Kohavi, 1996), estándar de referencia en la literatura de aprendizaje automático tabular y equidad algorítmica.

El dataset contiene $32,561$ registros y $14$ variables socioeconómicas:
* **Variables numéricas continuas (6):** *Edad*, *Educación Numérica* (años completados), *Ganancia de Capital*, *Pérdida de Capital*, *Horas Semanales* y *Ponderador Muestral (fnlwgt)*.
* **Variables categóricas (8):** *Sector de Empleo (Workclass)*, *Nivel Educativo (Education)*, *Estado Civil*, *Ocupación*, *Rol Familiar*, *Raza*, *Sexo* y *País de Origen*.
* **Variable objetivo binaria ($Y$):** Ingresos anuales superiores a $\$50,000$ dólares ($Y = 1$ si $>50\text{K}$, $Y = 0$ en caso contrario), con una prevalencia positiva del $24.08\%$.

## Canalización de preprocesamiento y partición

La preparación de datos siguió una canalización rigurosa para prevenir fuga de información (*data leakage*):
1. **Limpieza e imputación:** Valores ausentes en variables categóricas fueron imputados utilizando la moda condicionada por estrato demográfico.
2. **Codificación y escalado:** Variables categóricas transformadas mediante *One-Hot Encoding*, expandiendo el espacio dimensional a $104$ columnas binarias. Variables continuas estandarizadas mediante $z$-score ($\mu = 0, \sigma = 1$).
3. **Partición estratificada:** División estratificada $80/20$, asignando $26,048$ instancias para entrenamiento y reservando un conjunto de prueba independiente de $6,513$ registros para evaluar las siete puertas de FOM-7 en cinco bloques de tamaño muestral ($n \in \{50, 100, 200, 500, 1000\}$).

## Familias de modelos predictivos evaluadas

Se entrenaron cinco familias de clasificadores con distintos niveles de no linealidad y opacidad:
1. **Regresión Logística (LR):** Modelo lineal convexo con regularización L2 ($C=1.0$), utilizado como línea base interpretable ($AUC = 0.852$).
2. **Árbol de Decisión (DT):** Modelo no lineal ortogonal con criterio Gini restringido a profundidad $d=5$ ($AUC = 0.841$).
3. **Bosque Aleatorio (RF):** Ensamble *bagging* no lineal de 100 árboles de decisión no podados con submuestreo de $\sqrt{p}$ variables ($AUC = 0.898$).
4. **XGBoost (XGB):** Ensamble *gradient boosting* con 100 estimadores secuenciales, profundidad $d=6$, tasa $\eta = 0.1$ y regularización L2 ($AUC = 0.917$).
5. **Perceptrón Multicapa (MLP):** Red neuronal densa de 3 capas ocultas (64 neuronas cada una) con activaciones ReLU y optimizador Adam ($AUC = 0.891$).

## Entorno de ejecución y reproducibilidad

Las pruebas se ejecutaron en Python 3.10 sobre una estación de trabajo AMD Ryzen 9 5900X (12 núcleos, 24 hilos) con 64 GB de RAM, fijando una semilla global determinista (`seed=42`) para garantizar la reproducibilidad exacta de los muestreos.

## Protocolo de significancia estadística: Pruebas de Friedman y Nemenyi

Para determinar si las diferencias observadas en las métricas de FOM-7 reflejan superioridad algorítmica real y no fluctuaciones muestrales, se aplicó el protocolo no paramétrico de Demšar (2006):

1. **Prueba de rangos alineados de Friedman:** Evalúa la hipótesis nula ($H_0$) de que todos los explicadores presentan un rendimiento equivalente en sus rangos promedio a través de las condiciones experimentales:

$$\chi_F^2 = \frac{12N}{k(k+1)} \left[ \sum_{j=1}^k R_j^2 - \frac{k(k+1)^2}{4} \right]$$

donde $k=4$ es el número de explicadores comparados, $N=15$ es el número de bloques experimentales (cruces de modelos y tamaños de muestra), y $R_j = \frac{1}{N} \sum_{i=1}^N r_i^j$ es el rango promedio obtenido por el explicador $j$. Si todos los métodos tuviesen un rendimiento indistinguible, sus rangos promedio serían idénticos ($R_j \approx \frac{k+1}{2} = 2.5$) y el estadístico $\chi_F^2$ sería cercano a cero. Un valor elevado de $\chi_F^2$ con $p < 0.001$ rechaza formalmente la equivalencia entre métodos.

2. **Prueba post-hoc de Diferencia Crítica de Nemenyi:** Tras rechazar $H_0$, se calcula el umbral de Diferencia Crítica ($CD$) a un nivel de significancia de dos colas $\alpha = 0.05$:

$$CD = q_\alpha \sqrt{\frac{k(k+1)}{6N}}$$

donde $q_{0.05} = 2.569$ es el valor crítico de la distribución de rango studentizado para $k=4$ algoritmos. Geométricamente, $CD$ define la distancia mínima requerida entre los rangos promedio de dos explicadores $|R_a - R_b|$: si la diferencia supera estrictamente el valor $CD$, se concluye con un $95\%$ de certeza estadística que el explicador con mejor rango supera al otro.
