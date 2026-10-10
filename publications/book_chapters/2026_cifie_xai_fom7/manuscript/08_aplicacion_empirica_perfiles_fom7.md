# Aplicación empírica: Perfiles FOM-7

## Resultados consolidados del benchmark empírico

A continuación se presentan los resultados cuantitativos consolidados del benchmark empírico tras aplicar el protocolo de auditoría **FOM-7** sobre el conjunto de prueba de *UCI Adult Income*. La evaluación cruza de manera sistemática los cuatro explicadores agnósticos (LIME, KernelSHAP, Anchors y DiCE) con las cinco familias de clasificadores predictivos descritas.

<!-- TABLA: table_results_summary.md -->

La Tabla 2 condensa los valores promedio observados en las métricas principales de FOM-7. A partir de estos resultados numéricos, se realiza un análisis profundo de los hallazgos por cada una de las puertas de verificación.

## Análisis empírico detallado por Puertas FOM-7

### 1. Fidelidad Local (G1) y Diagrama de Diferencia Crítica de Nemenyi

Los resultados del benchmark confirman que **KernelSHAP** logra los valores de fidelidad local ponderada más elevados en todas las arquitecturas de modelo evaluadas ($\text{Fidelidad} = 0.942$ en XGBoost y $0.938$ en RF), superando de manera consistente a LIME ($\text{Fidelidad} = 0.871$ en XGBoost).

![Figura 9. Diagrama de diferencia crítica (CD) de Nemenyi para ranking de fidelidad post-hoc. Fuente: elaboración propia.](../figures/exported/fig_cd_diagram_es.png)

Para evaluar la significancia estadística de los rangos de fidelidad entre explicadores, se aplicó la prueba no paramétrica de Friedman seguida de la prueba *post-hoc* de Diferencia Crítica de Nemenyi ($\alpha = 0.05$). La Figura 9 ilustra el **Diagrama de Diferencia Crítica (CD) de Nemenyi**. Los explicadores conectados por una barra continua no muestran diferencias estadísticamente significativas. El diagrama ratifica que KernelSHAP se posiciona en el primer puesto de ranking con significancia estadística frente a LIME, demostrando su mayor capacidad para reconstruir fielmente la frontera de decisión local del modelo primario.

### 2. Estabilidad Local (G2) frente a Costo Computacional (G5): La Frontera de Pareto

Un hallazgo crucial del estudio radica en la demostración empírica del *trade-off* estructural entre la estabilidad estocástica de las atribuciones y la latencia computacional requerida para su cálculo.

![Figura 10. Frontera de Pareto entre estabilidad y costo computacional de explicadores post-hoc. Fuente: elaboración propia.](../figures/exported/fig_estabilidad_coste_es.png)

La Figura 10 presenta la **Frontera de Pareto entre estabilidad local y costo computacional**. LIME se ubica en el extremo de alta velocidad ($\bar{T}_{exp} = 45\text{ ms}$ por explicación), pero exhibe la menor estabilidad ante ruido ($\text{Estabilidad} = 0.724$). En contraposición, KernelSHAP alcanza una estabilidad óptima ($\text{Estabilidad} = 0.951$), pero requiere una latencia computacional 25 veces superior ($\bar{T}_{exp} = 1,180\text{ ms}$). Anchors y DiCE se ubican en regiones especializadas de la frontera de eficiencia, ofreciendo alternativas intermedias según el tipo de objeto explicativo requerido.

### 3. Cobertura Empírica e Interpretabilidad de Reglas (G4 - EXP2)

La evaluación de **Anchors** se profundizó mediante el experimento de cobertura de reglas locales (EXP2).

![Figura 8. Análisis de cobertura empírica e interpretabilidad práctica de reglas Anchors (EXP2). Fuente: elaboración propia.](../figures/exported/fig_cobertura_exp2_es.png)

La Figura 8 grafica la relación empírica entre el umbral de precisión exigido a la regla y la cobertura poblacional resultante. Se observa que para garantizar niveles de precisión extremadamente altos ($\text{prec} \ge 0.95$), la cobertura empírica de las reglas de Anchors se contrae de forma acelerada, cubriendo únicamente entre el $12\%$ y el $28\%$ de los datos. Este resultado confirma que las reglas de Anchors funcionan como "islas de certeza local" de gran confiabilidad pero de alcance limitado.

## Matriz de Decisión Operacional para Ingenieros de Despliegue

A partir de los perfiles empíricos consolidados bajo el protocolo FOM-7, formulamos una guía de decisión sistemática para seleccionar el explicador idóneo según los requerimientos operativos y restricciones críticas del sistema en producción:

1. **Auditoría Regulatoria Ex-Post (Banca, Seguros, Salud):**
   - *Restricción crítica:* Máxima fidelidad y consistencia jurídica ante organismos supervisores.
   - *Explicador recomendado:* **KernelSHAP**.
   - *Justificación empírica FOM-7:* Ofrece la mayor fidelidad local ($0.942$) y estabilidad entre remuestreos ($0.951$). Su latencia computacional elevada ($1,180\text{ ms}$) resulta plenamente admisible en esquemas de auditoría por lotes (*batch processing*) o revisiones periciales fuera de línea.

2. **Monitoreo y Diagnóstico en Tiempo Real (Comercio Electrónico, Detección de Fraude):**
   - *Restricción crítica:* Latencia estricta sub-segundo ($<100\text{ ms}$) y consumo mínimo de CPU por inferencia.
   - *Explicador recomendado:* **LIME**.
   - *Justificación empírica FOM-7:* Exhibe una latencia reducida ($45\text{ ms}$) y alta parsimonia explicativa, permitiendo generar aproximaciones comprensibles para operadores en turnos continuos, asumiendo una variabilidad estocástica moderada que debe amortiguarse mediante fijación de semillas o perturbaciones normalizadas.

3. **Control de Cumplimiento Normativo y Políticas Corporativas (Derecho Laboral, Admisiones):**
   - *Restricción crítica:* Certidumbre lógica inalterable y reglas deterministas de corte no negociable.
   - *Explicador recomendado:* **Anchors**.
   - *Justificación empírica FOM-7:* Aporta garantías matemáticas PAC de precisión ($\ge 95\%$) estructuradas en predicados condicionales comprensibles para oficiales de cumplimiento, asumiendo una cobertura poblacional acotada ($12\%$--$28\%$) que exige derivar los casos fuera del ancla a comités expertos.

4. **Portales de Autoservicio y Mecanismos de Apelación (Sujetos de Decisión, Clientes):**
   - *Restricción crítica:* Prescripción accionable y viabilidad física de intervención directa.
   - *Explicador recomendado:* **DiCE**.
   - *Justificación empírica FOM-7:* Produce contrafactuales que optimizan la distancia y diversidad matemática mientras protegen la invariancia de variables protegidas o inmutables (como la edad o el historial crediticio consolidado), habilitando un recurso correctivo real para el usuario final.
