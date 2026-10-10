# Aplicación empírica: Perfiles FOM-7

## Resultados consolidados del benchmark empírico

A continuación se presentan los resultados consolidados tras someter a LIME, KernelSHAP, Anchors y DiCE a las pruebas de **FOM-7** sobre las cinco familias de modelos entrenadas en *UCI Adult Income*.

<!-- TABLA: table_results_summary.md -->

La Tabla 2 reúne los promedios observados en las compuertas principales. Se observa que la complejidad arquitectónica del clasificador afecta de manera dispar a cada explicador: mientras que KernelSHAP sostiene niveles elevados de fidelidad en todas las familias ($0.942$ en XGBoost, $0.938$ en Random Forest, $0.929$ en MLP), LIME experimenta una degradación notable al transicionar desde modelos lineales ($0.912$ en LR) hacia redes no lineales ($0.854$ en MLP).

## Análisis empírico detallado por Puertas FOM-7

### 1. Fidelidad Local (G1) y Diagrama de Diferencia Crítica de Nemenyi

**KernelSHAP** alcanza los niveles de fidelidad local ponderada más altos en todos los clasificadores evaluados, superando sistemáticamente a LIME.

![Figura 9. Diagrama de diferencia crítica (CD) de Nemenyi para ranking de fidelidad post-hoc. Fuente: elaboración propia.](../figures/exported/fig_cd_diagram_es.png)

#### Interpretación del Diagrama de Diferencia Crítica (Figura 9)
* El eje horizontal muestra los rangos promedio asignados a cada método (valores más a la izquierda indican mejor desempeño).
* La barra horizontal superior marca la longitud del umbral crítico $CD$.
* **Regla de lectura:** Dos algoritmos conectados por una barra negra horizontal no presentan diferencias estadísticamente significativas. Si no están unidos, la diferencia en su rendimiento es estadísticamente demostrable con un $95\%$ de confianza.

La Figura 9 ratifica que KernelSHAP ocupa el primer lugar en fidelidad sin conexión de indiferencia con LIME, demostrando con significancia estadística su superioridad para reconstruir la frontera de decisión local del clasificador.

### 2. Estabilidad Local (G2) frente a Costo Computacional (G5): La Frontera de Pareto

El estudio demuestra empíricamente el compromiso estructural entre la **estabilidad de las atribuciones** y la **latencia computacional requerida**.

![Figura 10. Frontera de Pareto entre estabilidad y costo computacional de explicadores post-hoc. Fuente: elaboración propia.](../figures/exported/fig_estabilidad_coste_es.png)

#### Interpretación de la Frontera de Pareto (Figura 10)
* **LIME** se ubica en el cuadrante de alta velocidad: consume $\bar{T}_{exp} = 45\text{ ms}$ por registro, pero exhibe la menor estabilidad del benchmark ($\text{Estabilidad} = 0.724$), mostrando fluctuaciones ante ruidos leves.
* **KernelSHAP** se sitúa en el extremo de máxima robustez: alcanza estabilidad cuasi-óptima ($\text{Estabilidad} = 0.951$), pero impone un costo computacional 25 veces superior ($\bar{T}_{exp} = 1,180\text{ ms}$).
* **Anchors y DiCE** ocupan zonas intermedias y especializadas de la frontera eficiente, orientadas a reglas lógicas y contrafactuales.

### 3. Cobertura Empírica frente a Precisión de Reglas (G4 - EXP2)

Para **Anchors**, se analizó la relación entre la exigencia de precisión probabilística y la cobertura de registros en el conjunto de prueba (EXP2).

![Figura 8. Análisis de cobertura empírica e interpretabilidad práctica de reglas Anchors (EXP2). Fuente: elaboración propia.](../figures/exported/fig_cobertura_exp2_es.png)

La Figura 8 grafica esta curva: al exigir precisión rigurosa ($\text{prec} \ge 0.95$), la cobertura empírica de las reglas se contrae, cubriendo entre el $12\%$ y el $28\%$ de los registros. Las reglas de Anchors actúan como "islas de certidumbre absoluta": ofrecen garantías lógicas indiscutibles dentro de su radio, pero dejan sin cobertura a la mayoría de las instancias.

## Matriz de Decisión para Ingenieros de Despliegue

Sintetizamos una guía para orientar la selección del explicador en arquitecturas de producción:

1. **Auditoría Regulatoria Ex-Post (Banca, Seguros, Salud):**
   - *Restricción:* Máxima fidelidad matemática, reproducibilidad e inalterabilidad jurídica.
   - *Recomendación:* **KernelSHAP** (Fidelidad $0.942$, Estabilidad $0.951$). La latencia de $1,180\text{ ms}$ es admisible en procesos por lotes (*batch*).
2. **Inferencia Interactiva y Microservicios en Tiempo Real (E-commerce, Detección de Fraude):**
   - *Restricción:* Latencia $<100\text{ ms}$ por llamada y presupuesto mínimo de CPU/GPU.
   - *Recomendación:* **LIME** (o TreeSHAP si el modelo es un ensamble de árboles). Latencia de $45\text{ ms}$ y alta parsimonia, mitigando su variabilidad con semillas fijas.
3. **Control de Políticas Corporativas y Cumplimiento (Recursos Humanos, Admisiones):**
   - *Restricción:* Reglas deterministas en lenguaje formal (`SI-ENTONCES`) comprensibles por comités no técnicos.
   - *Recomendación:* **Anchors** (Garantías PAC con precisión $\ge 95\%$), derivando los casos fuera de cobertura ($>70\%$) a revisión experta.
4. **Portales de Autoservicio y Apelaciones (Sujetos de Decisión):**
   - *Restricción:* Prescripciones accionables respetando variables inmutables.
   - *Recomendación:* **DiCE** (Contrafactuales diversos con mutabilidad restringida para guiar al usuario final).
