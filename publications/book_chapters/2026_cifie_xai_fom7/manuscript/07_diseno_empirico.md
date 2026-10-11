# Diseño empírico y banco de pruebas

## El banco de datos de prueba: UCI Adult Income

Para validar experimentalmente el protocolo **FOM-7**, se diseñó un banco de pruebas sobre el conjunto tabular *UCI Adult Income* (Kohavi, 1996), estándar de referencia en aprendizaje automático tabular y equidad algorítmica.

El corpus reúne $32,561$ registros y $14$ variables socioeconómicas:

* **Variables continuas (6):** *Edad*, *Educación Numérica*, *Ganancia de Capital*, *Pérdida de Capital*, *Horas Semanales* y *Ponderador Muestral (fnlwgt)*.
* **Variables categóricas (8):** *Sector de Empleo*, *Nivel Educativo*, *Estado Civil*, *Ocupación*, *Rol Familiar*, *Raza*, *Sexo* y *País de Origen*.
* **Variable objetivo binaria ($Y$):** Ingresos superiores a $\$50,000$ anuales ($Y = 1$ si $>50\text{K}$, $Y = 0$ en caso contrario), con prevalencia positiva del $24.08\%$.

## Canalización de preprocesamiento y partición

La preparación de datos siguió una canalización estricta para evitar fuga de información (*data leakage*):

1. **Limpieza e imputación:** Imputación por moda condicionada por estrato demográfico para valores ausentes en variables categóricas.
2. **Codificación y escalado:** Transformación *One-Hot Encoding* sobre variables categóricas (expandiendo el espacio a $104$ columnas binarias). Estandarización $z$-score ($\mu = 0, \sigma = 1$) sobre variables continuas.
3. **Partición estratificada:** División $80/20$, asignando $26,048$ instancias a entrenamiento y $6,513$ registros a prueba independiente para evaluar las siete compuertas en cinco bloques muestrales ($n \in \{50, 100, 200, 500, 1000\}$).

## Familias de modelos predictivos evaluadas

Se entrenaron cinco familias de clasificadores con distinta complejidad funcional:

1. **Regresión Logística (LR):** Modelo lineal convexo regularizado L2 ($C=1.0$), empleado como línea base interpretable ($AUC = 0.852$).
2. **Árbol de Decisión (DT):** Modelo no lineal ortogonal con criterio Gini y profundidad $d=5$ ($AUC = 0.841$).
3. **Bosque Aleatorio (RF):** Ensamble *bagging* de 100 árboles no podados con submuestreo de $\sqrt{p}$ variables ($AUC = 0.898$).
4. **XGBoost (XGB):** Ensamble *gradient boosting* con 100 estimadores, profundidad $d=6$, tasa $\eta = 0.1$ y penalización L2 ($AUC = 0.917$).
5. **Perceptrón Multicapa (MLP):** Red neuronal densa de 3 capas ocultas (64 neuronas cada una), activaciones ReLU y optimizador Adam ($AUC = 0.891$).

## Entorno de ejecución y reproducibilidad

Los experimentos se ejecutaron en Python 3.10 sobre una estación AMD Ryzen 9 5900X (12 núcleos, 24 hilos) con 64 GB de RAM. Se fijó una semilla global determinista (`seed=42`) para garantizar la reproducibilidad completa.

## Protocolo de significancia estadística: Pruebas de Friedman y Nemenyi

Para certificar si las divergencias en FOM-7 reflejan diferencias algorítmicas genuinas, se aplicó el protocolo no paramétrico de Demšar (2006):

1. **Prueba de rangos alineados de Friedman:** Contrasta la hipótesis nula ($H_0$) de rendimiento equivalente en rangos promedio:

$$\chi_F^2 = \frac{12N}{k(k+1)} \left[ \sum_{j=1}^k R_j^2 - \frac{k(k+1)^2}{4} \right]$$

donde $k=4$ explicadores, $N=15$ bloques experimentales y $R_j = \frac{1}{N} \sum_{i=1}^N r_i^j$ es el rango medio del explicador $j$. Si los métodos fuesen indistinguibles, sus rangos coincidirían ($R_j \approx 2.5$) y $\chi_F^2$ tendería a cero. Un valor de $\chi_F^2$ con $p < 0.001$ rechaza formalmente la equivalencia.

2. **Prueba post-hoc de Diferencia Crítica de Nemenyi:** Tras rechazar $H_0$, se calcula la Diferencia Crítica ($CD$) a dos colas con $\alpha = 0.05$:

$$CD = q_\alpha \sqrt{\frac{k(k+1)}{6N}}$$

donde $q_{0.05} = 2.569$ es el valor crítico de la distribución de rango studentizado para $k=4$. Si la separación entre los rangos promedio de dos explicadores $|R_a - R_b|$ supera $CD$, la diferencia es estadísticamente significativa al $95\%$ de confianza.
