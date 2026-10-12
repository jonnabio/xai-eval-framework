# La Historia de la Tesis Doctoral: Evaluación Cuantitativa de Inteligencia Artificial Explicable (XAI)
*Nivel Intermedio (Estudiantes Universitarios de Informática, Ciencia de Datos e Ingeniería)*

---

## 1. Introducción y Motivación: La Opacidad de la IA y el Reto de la Evaluación

En la era del aprendizaje automático moderno, los modelos predictivos como las Redes Neuronales Profundas (MLP), las Máquinas de Vectores de Soporte (SVM) y los Ensambles de Árboles (Random Forest, XGBoost) alcanzan un rendimiento excepcional. Sin embargo, su arquitectura interna se comporta como una **"Caja Negra"** ($\mathbf{y} = f(\mathbf{x})$), donde millones de parámetros hacen imposible auditar de manera directa el proceso inferencial.

En sectores de alto impacto como las finanzas, la medicina o la justicia, el marco legal y ético exige **explicabilidad** (Sistemas de IA Explicable, XAI). Para lograrlo, la comunidad ha desarrollado explicadores post-hoc agnósticos al modelo. Estos algoritmos intentan aproximar el comportamiento de $f(\mathbf{x})$ alrededor de una instancia sin necesidad de acceder a la arquitectura interna del modelo.

Sin embargo, surgió un problema de investigación fundamental: **¿Cómo sabemos si las explicaciones producidas por estos explicadores son confiables?** 
Diferentes métodos de explicación (como LIME o SHAP) aplicados al mismo modelo y a la misma instancia frecuentemente producen explicaciones contradictorias. Sin un protocolo estandarizado de evaluación cuantitativa, los científicos y auditores corren el riesgo de caer en una "ilusión de transparencia".

Esta tesis aborda dicha brecha mediante el desarrollo, validación y benchmarking del **Protocolo FOM-7** (*Framework for Operational Metrics in 7 Gates*).

---

## 2. Los Métodos de Explicabilidad y las Métricas Cuantitativas

### A. Los Métodos de Explicabilidad Estudiados
1. **Atribución de Características (Feature Attribution):**
   * **LIME (Local Interpretable Model-agnostic Explanations):** Genera una perturbación sintética en el vecindario de la instancia $\mathbf{x}$ y entrena un modelo sustituto lineal simple ($g$) ponderado por proximidad espacial.
   * **SHAP (Shapley Additive exPlanations):** Calcula la contribución marginal de cada característica basándose en la teoría de juegos cooperativos (Valores de Shapley), garantizando propiedades axiomáticas como consistencia y eficiencia.
2. **Reglas Locales (Rule-based):**
   * **Anchors:** Construye reglas lógicas del tipo `SI condición ENTONCES predicción` con garantías estadísticas de precisión local en un vecindario de datos.
3. **Explicaciones Contrafactuales (Counterfactuals):**
   * **DiCE (Diverse Counterfactual Explanations):** Encuentra las modificaciones mínimas necesarias en las características de la entrada para cambiar la predicción del modelo hacia una clase objetivo deseada.

### B. Las 5 Métricas Cuantitativas de Evaluación
Para comparar objetivamente estos métodos, la tesis formaliza cinco métricas cuantitativas:
1. **Fidelidad (Fidelity):** Grado de acuerdo entre la predicción del modelo sustituto/explicador y el modelo caja negra original.
2. **Estabilidad (Stability):** Continuidad de la explicación ante pequeñas perturbaciones en la entrada (medida mediante distancias de repetición o coeficientes de variación).
3. **Parsimonia (Sparsity / Complexity):** Fracción de características no nulas utilizadas en la explicación (privilegiando explicaciones breves y cognitivamente manejables).
4. **Coste Computacional (Cost):** Tiempo de ejecución (*wall-clock time*) en milisegundos por instancia explicada.
5. **Brecha de Fidelidad (Faithfulness Gap):** Error cuadrático medio entre la degradación real del modelo al remover características y la expectativa teórica del explicador.

---

## 3. La Estructura de la Investigación: Artículos A a F

La tesis doctoral se desarrolla a través de 6 artículos interconectados que construyen progresivamente la evidencia científica:

```
[Opacidad de IA] ──> [Conflicto LIME vs SHAP] ──> [Necesidad de Gobernanza]
                                   │
  ┌────────────────────────────────┴────────────────────────────────┐
  │                                                                 │
  ▼                                                                 ▼
[Artículo A: Protocolo FOM-7] ──> [Artículo B: LIME vs SHAP] ──> [Artículo C: Escalabilidad]
  (Publicado - RIMI 2026)          (Enviado - CLEIej)              (Listo para envío)
                                                                    │
  ┌─────────────────────────────────────────────────────────────────┘
  │
  ▼
[Artículo D: Aplicación Empírica] ──> [Artículo E: Frontera Pareto] ──> [Artículo F: Alineación Humana]
  (Listo para envío - Tec. Marcha)      (Enviado - CyS CIC-IPN)          (En desarrollo - JCSI)
```

---

### Artículo A: Fundamentación Teórica y el Protocolo FOM-7
* **Estado:** Publicado en *Revista de Investigación Multidisciplinaria Iberoamericana (RIMI)* (2026, DOI: `10.69850/rimi.vi3.307`).
* **Objetivo:** Definir un estándar metodológico auditable para evaluar explicadores post-hoc sin incurrir en fugas de datos o sesgos de varianza.
* **Aporte:** Formalización de las **7 Puertas de FOM-7**:
  1. *Congelación:* Pre-registro determinista del diseño experimental y del plan inferencial.
  2. *Ejecución:* Generación de resultados crudos por celda experimental con semillas fijas.
  3. *Auditoría:* Verificación de integridad de artefactos (filtrado de ejecuciones nulas o corruptas).
  4. *Armonización:* Agregación de métricas por bloques homogeneizados (modelo $\times$ tamaño muestra).
  5. *Exportación:* Evaluación estadística no paramétrica (Pruebas de Friedman y Nemenyi con ajuste de Holm).
  6. *Perfilado:* Aislamiento de la varianza algorítmica (semilla) frente a los efectos principales del método.
  7. *Reporte:* Registro trazable de afirmaciones científicas delimitadas por constructo y dominio.

---

### Artículo B: El Duelo Comparativo — LIME vs SHAP a Escala
* **Estado:** Enviado a *CLEI Electronic Journal (CLEIej)* (2026-10-04, Subm. #1196).
* **Objetivo:** Ejecutar una comparación empírica masiva entre los dos estándares de la industria (LIME y SHAP).
* **Aporte:** 
  * Demostración empírica de las ventajas teóricas de SHAP en estabilidad y fidelidad.
  * Identificación de la fragilidad estocástica de LIME: al muestrear aleatoriamente perturbaciones locales, LIME exhibe alta variabilidad en los coeficientes asignados.
  * LIME compensa esta limitación mediante un menor coste computacional y una mayor parsimonia en sus explicaciones.

---

### Artículo C: Dinámica de Escalabilidad y Resistencia
* **Estado:** Listo para envío a *Tecnología en Marcha* (Edición Especial IA, Zenodo v0.12.0 DOI: `10.5281/zenodo.23165763`).
* **Objetivo:** Analizar cómo se comportan los explicadores cuando varía el tamaño de muestra del conjunto de datos y la profundidad de los modelos.
* **Aporte:** Cuantificación del punto de degradación de los sustitutos locales. Se demuestra que incrementar el tamaño del conjunto de datos de fondo mejora la estabilidad de KernelSHAP a costa de un crecimiento cuadrático en el tiempo de procesamiento.

---

### Artículo D: Benchmark Empírico Aplicado (UCI Adult Income)
* **Estado:** Listo para envío a *Tecnología en Marcha* (Edición Especial IA).
* **Objetivo:** Aplicar el protocolo FOM-7 sobre un caso de estudio de alta relevancia social y económica (clasificación de ingresos tabulares *UCI Adult Income*).
* **Aporte:** 
  * Evaluación sobre 300 celdas planificadas ($5 \text{ modelos} \times 4 \text{ métodos} \times 5 \text{ semillas} \times 3 \text{ tamaños}$), obteniendo 275 celdas calificadas tras la auditoría FOM-7.
  * Comparación de 5 familias de modelos predictivos: Logistic Regression, Random Forest, XGBoost, SVM (RBF) y MLP.
  * Confirmación de que las explicaciones estructurales (Anchors) y contrafactuales (DiCE) deben evaluarse en dimensiones distintas a la simple atribución de características.

---

### Artículo E: Fronteras de Pareto y Gobernanza de XAI
* **Estado:** Enviado a *Computación y Sistemas (CIC-IPN)* (2026-10-04, Subm. #6783).
* **Objetivo:** Resolver el problema de selección de explicadores mediante optimización multiobjetivo y análisis de frontera de eficiencia (Pareto).
* **Aporte:** 
  * Demostración de que ningún método domina simultáneamente en todas las métricas.
  * Formulación de criterios de gobernanza:
    * **Entornos de Alta Severidad (Auditoría Médica/Legal):** Selección obligatoria de **SHAP** debido a su consistencia axiomática y alta estabilidad.
    * **Entornos de Tiempo Real / Producción de Alta Velocidad:** Selección recomendada de **LIME** o **TreeSHAP** para equilibrar coste y latencia.

---

### Artículo F: Alineación Semántica y Evaluación por Humanos/LLM
* **Estado:** En desarrollo inicial (*Journal of Computer Sciences Institute*).
* **Objetivo:** Conectar las métricas computacionales objetivas con la percepción humana de explicabilidad y la evaluación mediante Modelos de Lenguaje (LLM-as-a-Judge).
* **Aporte:** Protocolo de validación cruzada para verificar si los rankings matemáticos de fidelidad y estabilidad se traducen en una mejor comprensión y confianza por parte de los usuarios finales.

---

## 4. Síntesis y Relevancia para la Defensa de Tesis

La narrativa unificada de esta tesis doctoral demuestra que la evaluación de XAI no es una búsqueda de "el mejor método único", sino la construcción de un **sistema de perfiles explicativos trazables**:

1. **Problema de Investigación:** La falta de rigor y la contradicción entre explicadores agnósticos.
2. **Solución Metodológica:** El protocolo **FOM-7** como marco de gobernanza y control de varianza.
3. **Evidencia Empírica (Papeles B, C, D):** Cuantificación precisa del comportamiento de LIME, SHAP, Anchors y DiCE.
4. **Aplicación Práctica (Papeles E, F):** Guía de selección basada en fronteras de Pareto y alineación con las necesidades del usuario.

Este trabajo transforma la explicabilidad en una evidencia científica reproducible, defendible y auditable.
