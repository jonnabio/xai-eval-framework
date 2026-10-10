# Aplicación empírica: Perfiles FOM-7

## Resultados consolidados del benchmark empírico

A continuación se presentan los resultados cuantitativos consolidados del benchmark empírico tras someter a los cuatro explicadores agnósticos (LIME, KernelSHAP, Anchors y DiCE) a las pruebas del protocolo **FOM-7** sobre las cinco familias de modelos entrenadas en *UCI Adult Income*.

<!-- TABLA: table_results_summary.md -->

La Tabla 2 reúne los promedios observados en las compuertas principales. A partir de esta evidencia numérica, examinamos en detalle los hallazgos operacionales más determinantes para un equipo de ingeniería.

## Análisis empírico detallado por Puertas FOM-7

### 1. Fidelidad Local (G1) y Diagrama de Diferencia Crítica de Nemenyi

Los resultados experimentales ratifican que **KernelSHAP** alcanza los niveles de fidelidad local ponderada más altos en todos los clasificadores evaluados ($\text{Fidelidad} = 0.942$ en XGBoost y $0.938$ en Random Forest), superando sistemáticamente a LIME ($\text{Fidelidad} = 0.871$ en XGBoost).

![Figura 9. Diagrama de diferencia crítica (CD) de Nemenyi para ranking de fidelidad post-hoc. Fuente: elaboración propia.](../figures/exported/fig_cd_diagram_es.png)

#### Cómo leer el Diagrama de Diferencia Crítica (Figura 9)
Para un ingeniero no familiarizado con esta representación, el **Diagrama de Diferencia Crítica (CD) de Nemenyi** sintetiza la jerarquía estadística de los algoritmos:
* El eje horizontal muestra los rangos promedio asignados a cada método (donde los valores más a la izquierda representan mejor desempeño).
* La barra horizontal en la parte superior indica la longitud del umbral crítico $CD$.
* **Regla de interpretación:** Dos algoritmos conectados por una barra negra horizontal no presentan diferencias estadísticamente significativas. Si dos métodos no están unidos por una barra continua, la diferencia en su rendimiento es estadísticamente demostrable con un $95\%$ de confianza.

La Figura 9 confirma que KernelSHAP ocupa el primer lugar en el ranking de fidelidad sin conexión de indiferencia con LIME, demostrando con significancia estadística su mayor precisión para modelar la frontera de decisión local del clasificador.

### 2. Estabilidad Local (G2) frente a Costo Computacional (G5): La Frontera de Pareto

Uno de los hallazgos de ingeniería más trascendentes del estudio radica en la demostración empírica del compromiso estructural entre la **estabilidad de las atribuciones ante perturbaciones** y la **latencia computacional requerida**.

![Figura 10. Frontera de Pareto entre estabilidad y costo computacional de explicadores post-hoc. Fuente: elaboración propia.](../figures/exported/fig_estabilidad_coste_es.png)

#### Interpretación de la Frontera de Pareto (Figura 10)
La Figura 10 ilustra la compensación directa entre dos objetivos contrapuestos en la arquitectura de sistemas:
* **LIME** se ubica en el cuadrante de alta velocidad de inferencia: consume únicamente $\bar{T}_{exp} = 45\text{ ms}$ por registro, pero exhibe la menor estabilidad del benchmark ($\text{Estabilidad} = 0.724$), mostrando fluctuaciones en el orden de factores ante variaciones leves de los datos.
* **KernelSHAP** se sitúa en el extremo opuesto de máxima robustez: alcanza una estabilidad cuasi-óptima ($\text{Estabilidad} = 0.951$), pero impone un costo computacional 25 veces superior ($\bar{T}_{exp} = 1,180\text{ ms}$ por registro).
* **Anchors y DiCE** ocupan zonas intermedias y especializadas de la frontera eficiente, reflejando su vocación hacia objetos explicativos basados en reglas lógicas y prescripciones contrafactuales.

### 3. Cobertura Empírica frente a Precisión de Reglas (G4 - EXP2)

Para evaluar **Anchors**, se analizó la relación entre la exigencia de precisión probabilística impuesta a la regla y la fracción de registros que dicha regla logra gobernar en el conjunto de prueba (EXP2).

![Figura 8. Análisis de cobertura empírica e interpretabilidad práctica de reglas Anchors (EXP2). Fuente: elaboración propia.](../figures/exported/fig_cobertura_exp2_es.png)

La Figura 8 grafica esta curva de cobertura poblacional. Se comprueba que cuando se exige una precisión muy rigurosa ($\text{prec} \ge 0.95$), la cobertura empírica de las reglas se reduce drásticamente, cubriendo apenas entre el $12\%$ y el $28\%$ de los casos evaluados. Este hallazgo confirma que las reglas de Anchors actúan en producción como "islas de certidumbre absoluta": ofrecen garantías lógicas indiscutibles dentro de su radio de cobertura, pero dejan fuera a la gran mayoría de las instancias de la base de datos.

## Matriz de Decisión para Ingenieros de Despliegue

A partir de los perfiles cuantitativos medidos por FOM-7, sintetizamos una guía práctica para orientar la selección del explicador en arquitecturas de producción según las restricciones operacionales del sistema:

1. **Auditoría Regulatoria y Cumplimiento Legal Ex-Post (Banca, Seguros, Salud):**
   - *Restricción de arquitectura:* Máxima fidelidad matemática, reproducibilidad e inalterabilidad jurídica ante inspecciones de supervisores.
   - *Explicador recomendado:* **KernelSHAP**.
   - *Fundamento empírico:* Máxima fidelidad local ($0.942$) y estabilidad entre remuestreos ($0.951$). La latencia de $1,180\text{ ms}$ es perfectamente admisible en procesos por lotes (*batch*) o revisiones fuera de línea.

2. **Inferencia Interactiva y Microservicios en Tiempo Real (E-commerce, Detección de Fraude):**
   - *Restricción de arquitectura:* Latencia estricta por debajo de $100\text{ ms}$ por llamada y presupuesto mínimo de CPU/GPU.
   - *Explicador recomendado:* **LIME** (o TreeSHAP si el modelo es un ensamble de árboles).
   - *Fundamento empírico:* Latencia media reducida de $45\text{ ms}$ y alta parsimonia de salida, aceptando una moderada variabilidad estocástica que debe mitigarse fijando semillas globales o calibrando el ancho de banda del núcleo.

3. **Verificación de Políticas Corporativas y Reglas de Negocio (Recursos Humanos, Admisiones):**
   - *Restricción de arquitectura:* Reglas deterministas en lenguaje formal (`SI-ENTONCES`) fácilmente auditables por personal no técnico.
   - *Explicador recomendado:* **Anchors**.
   - *Fundamento empírico:* Garantías formales PAC con precisión $\ge 95\%$, asumiendo una cobertura poblacional acotada ($12\%$--$28\%$) que exige derivar las instancias no cubiertas a comités humanos.

4. **Portales de Autoservicio y Mecanismos de Apelación para Clientes (Sujetos de Decisión):**
   - *Restricción de arquitectura:* Prescripciones accionables y factibilidad física de intervención correctiva directa.
   - *Explicador recomendado:* **DiCE**.
   - *Fundamento empírico:* Generación de escenarios contrafactuales que optimizan la distancia y diversidad matemática mientras protegen la inmutabilidad de variables sensibles (como edad o lugar de nacimiento), empoderando al usuario final con caminos de acción realistas.
