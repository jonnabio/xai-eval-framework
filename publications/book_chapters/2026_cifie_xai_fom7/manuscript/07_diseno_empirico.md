# Diseño empírico y banco de pruebas

## El banco de datos de prueba: UCI Adult Income

Para someter al protocolo **FOM-7** a una validación empírica rigurosa, se diseñó un banco de pruebas experimental sobre el dataset *UCI Adult Income* (también conocido como *Census Income Dataset*), extraído de la base de datos de la Oficina del Censo de los Estados Unidos (Kohavi, 1996). Este conjunto de datos constituye el estándar de referencia indiscutible para la evaluación de algoritmos de clasificación tabulares, análisis de opacidad y estudios de equidad algorítmica.

El banco de datos abarca $32,561$ observaciones de personas adultas. Cada registro incluye $14$ características socioeconómicas individuales:
* **Variables numéricas continuas (6):** *Edad*, *Educación Numérica* (años de estudio), *Ganancia de Capital*, *Pérdida de Capital*, *Horas de Trabajo por Semana* y *Ponderador Poblacional (fnlwgt)*.
* **Variables categóricas nominales y ordinales (8):** *Sector de Empleo (Workclass)*, *Nivel de Estudios (Education)*, *Estado Civil*, *Ocupación*, *Relación Familiar*, *Raza*, *Sexo* y *País de Origen*.
* **Variable objetivo binaria ($Y$):** Indica si los ingresos anuales del individuo superan los $\$50,000$ dólares ($Y = 1$ si $>50\text{K}$, $Y = 0$ en caso contrario). La clase positiva representa el $24.08\%$ del total de la población.

## Preprocesamiento de datos y partición experimental

Para garantizar la integridad metodológica y evitar el sesgo por fuga de información (*data leakage*), la canalización de procesamiento de datos se diseñó bajo criterios estrictos de separación:

1. **Limpieza e imputación:** Las observaciones con valores perdidos en variables categóricas (como *Workclass* u *Occupation*) fueron imputadas empleando la moda condicionada dentro de su grupo estratificado.
2. **Codificación y escalado:** Las variables categóricas fueron transformadas mediante codificación binaria *One-Hot Encoding*, generando un espacio expandido de $104$ características binarias. Las variables numéricas continuas se normalizaron mediante escalado $z$-score ($\mu = 0, \sigma = 1$).
3. **Partición estratificada:** El dataset se dividió en una proporción estratificada $80/20$: un conjunto de entrenamiento ($n = 26,048$) para el ajuste de los clasificadores primarios y un conjunto de prueba reservado ($n = 6,513$) sobre el cual se ejecutaron de forma independiente todas las evaluaciones de las siete puertas de FOM-7.

## Familias de modelos predictivos evaluadas

Con el fin de analizar el comportamiento de las métricas de explicabilidad frente a distintos grados de complejidad matemática y profundidad no lineal, se entrenaron cinco familias de clasificadores predictivos:

1. **Regresión Logística (LR):** Modelo lineal transparente interpretable por construcción, utilizado como línea base analítica ($AUC = 0.852$).
2. **Árbol de Decisión (DT):** Modelo no lineal interpretable por diseño restringido a profundidad máxima $d=5$, con fronteras de decisión ortogonales ($AUC = 0.841$).
3. **Bosque Aleatorio (RF):** Ensamble tipo *bagging* no lineal compuesto por 100 árboles de decisión no restringidos, introduciendo opacidad moderada ($AUC = 0.898$).
4. **XGBoost (XGB):** Ensamble tipo *gradient boosting* con 100 estimadores secuenciales y regularización $\text{L2}$, representando el estado del arte predictivo en datos tabulares ($AUC = 0.917$).
5. **Perceptrón Multicapa (MLP):** Red neuronal artificial profunda compuesta por 3 capas ocultas de 64 neuronas cada una con funciones de activación ReLU, representando opacidad completa de caja negra no lineal ($AUC = 0.891$).

## Entorno de ejecución y reproducibilidad

Todas las corridas experimentales se ejecutaron en un entorno virtual aislado con Python 3.10 en una estación de trabajo Linux con procesador AMD Ryzen 9 5900X de 12 núcleos y 64 GB de RAM. Para asegurar la reproductibilidad exacta de las mediciones de estabilidad y latencia, se fijó la semilla del generador de números pseudoaleatorios en `seed=42` para todas las particiones, optimizaciones y muestreos estocásticos de los explicadores.
