# Diseño empírico y banco de pruebas

## El banco de datos de prueba: UCI Adult Income

Para validar experimentalmente el protocolo **FOM-7**, se diseñó un banco de pruebas sobre el conjunto de datos tabular *UCI Adult Income* (Kohavi, 1996), extraído de la base del Censo de los Estados Unidos. Este dataset constituye el estándar de referencia por antonomasia en la literatura de aprendizaje automático tabular, auditoría de sesgos algorítmicos y equidad explicativa.

El dataset contiene $32,561$ registros individuales y $14$ variables socioeconómicas:
* **Variables numéricas continuas (6):** *Edad*, *Educación Numérica* (años de escolaridad completados), *Ganancia de Capital*, *Pérdida de Capital*, *Horas de Trabajo Semanal* y *Ponderador Muestral (fnlwgt)*.
* **Variables categóricas (8):** *Sector de Empleo (Workclass)*, *Nivel Educativo (Education)*, *Estado Civil*, *Ocupación*, *Rol Familiar*, *Raza*, *Sexo* y *País de Origen*.
* **Variable objetivo binaria ($Y$):** Indica si los ingresos anuales del individuo superan los $\$50,000$ dólares ($Y = 1$ si $>50\text{K}$, $Y = 0$ en caso contrario). La clase positiva representa el $24.08\%$ del total de observaciones.

## Canalización de preprocesamiento y partición de datos

Para garantizar la integridad metodológica y prevenir la fuga de información (*data leakage*), la canalización de preparación de datos siguió una secuencia estricta:

1. **Limpieza e imputación:** Los valores ausentes en variables categóricas (como *Workclass* u *Occupation*) fueron imputados utilizando la moda condicionada por estrato demográfico.
2. **Codificación y escalado:** Las variables categóricas fueron transformadas mediante codificación binaria *One-Hot Encoding*, expandiendo el espacio dimensional de entrada a $104$ características binarias. Las variables continuas fueron normalizadas mediante estandarización $z$-score ($\mu = 0, \sigma = 1$).
3. **Partición estratificada:** Se realizó una división estratificada $80/20$, asignando $26,048$ instancias para el entrenamiento y ajuste de hiperparámetros de los clasificadores, y reservando un conjunto de prueba independiente de $6,513$ registros sobre el cual se aplicaron las evaluaciones de las siete puertas de FOM-7.

## Familias de modelos predictivos evaluadas

Con el propósito de estudiar el comportamiento de los explicadores ante diversos grados de no linealidad, complejidad paramétrica y opacidad matemática, se entrenaron cinco familias de clasificadores:

1. **Regresión Logística (LR):** Modelo lineal transparente y convexo, utilizado como línea base analítica de referencia ($AUC = 0.852$).
2. **Árbol de Decisión (DT):** Modelo no lineal con fronteras de decisión ortogonales restringido a profundidad máxima $d=5$ para preservar su interpretabilidad intrínseca ($AUC = 0.841$).
3. **Bosque Aleatorio (RF):** Ensamble tipo *bagging* no lineal compuesto por 100 árboles de decisión sin poda, introduciendo opacidad algorítmica moderada ($AUC = 0.898$).
4. **XGBoost (XGB):** Ensamble tipo *gradient boosted trees* con 100 estimadores secuenciales y regularización L2, representando el estado del arte predictivo en datos tabulares industriales ($AUC = 0.917$).
5. **Perceptrón Multicapa (MLP):** Red neuronal densa de 3 capas ocultas con 64 neuronas por capa y activaciones no lineales ReLU, representando opacidad total de caja negra continua ($AUC = 0.891$).

## Entorno de ejecución y reproducibilidad

Todas las pruebas se ejecutaron en un entorno virtual aislado con Python 3.10 en una estación de trabajo equipada con procesador AMD Ryzen 9 5900X (12 núcleos, 24 hilos) y 64 GB de memoria RAM. Para garantizar la reproducibilidad de los muestreos de Monte Carlo y las perturbaciones estocásticas, se fijó una semilla global determinista (`seed=42`) en todas las corridas.

## Protocolo de significancia estadística: Pruebas de Friedman y Nemenyi

Para determinar con rigor si las diferencias observadas en las métricas de las compuertas de FOM-7 reflejan una superioridad algorítmica genuina y no fluctuaciones aleatorias del remuestreo, se aplicó el marco de pruebas no paramétricas recomendado por Demšar (2006):

1. **Prueba de rangos alineados de Friedman:** Evalúa la hipótesis nula ($H_0$) de que todos los explicadores obtienen un rendimiento equivalente en sus rangos promedio across experimental blocks. La estadística de Friedman $\chi_F^2$ se calcula mediante:
$$\chi_F^2 = \frac{12N}{k(k+1)} \left[ \sum_{j=1}^k R_j^2 - \frac{k(k+1)^2}{4} \right]$$
donde $k=4$ es el número de explicadores comparados, $N=15$ es el número de condiciones experimentales (cruces de modelos y tamaños muestrales), y $R_j$ es el rango medio del explicador $j$.
2. **Prueba post-hoc de Diferencia Crítica de Nemenyi:** Tras rechazar la hipótesis nula ($p < 0.001$), se calcula el umbral de Diferencia Crítica ($CD$) a un nivel de significancia de dos colas $\alpha = 0.05$:
$$CD = q_\alpha \sqrt{\frac{k(k+1)}{6N}}$$
donde $q_{0.05} = 2.569$ para $k=4$. Si la diferencia entre los rangos promedio de dos explicadores supera estrictamente el valor de $CD$, la superioridad de uno sobre el otro queda estadísticamente demostrada.
