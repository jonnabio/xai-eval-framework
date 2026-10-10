# Crisis de evaluación en XAI

## La crisis de confiabilidad en explicabilidad post-hoc

En la ingeniería de software, un módulo se valida mediante aserciones deterministas (`assert output == expected`). En aprendizaje supervisado, el rendimiento se comprueba contrastando predicciones con etiquetas reales (*ground truth*).

En la explicabilidad post-hoc nos encontramos ante una **crisis de evaluación estructural**: **no existe una etiqueta de referencia sobre cómo razona internamente una caja negra** (Krishna *et al.*, 2022; Nauta *et al.*, 2023; Agarwal *et al.*, 2023). Ante la ausencia de un patrón oro, los equipos han incurrido a menudo en dos prácticas metodológicamente vulnerables:
1. **La trampa de la plausibilidad intuitiva:** Asumir que una explicación es correcta si las variables destacadas confirman las expectativas previas del analista (sesgo de confirmación).
2. **La métrica endógena circular:** Evaluar un explicador utilizando las mismas métricas para las que fue optimizado algorítmicamente.

![Figura 6. Anatomía de la crisis de evaluación en explicabilidad post-hoc. Fuente: elaboración propia a partir de Krishna *et al.* (2022), Nauta *et al.* (2023) y Agarwal et al. (2023).](../figures/exported/fig_d7_cadena_evidencia_es.png)

La Figura 6 sintetiza esta crisis: desplegar un explicador sin controles cuantitativos independientes introduce un segundo componente opaco dentro de la arquitectura de supervisión.

## Taxonomía de riesgos y patologías operacionales

Para un ingeniero de datos que gestiona pipelines en producción, las fallas de los explicadores post-hoc se agrupan en cuatro patologías críticas:

### 1. El Efecto Rashomon en explicaciones
Inspirado en el fenómeno formulado por Breiman (2001), ocurre cuando múltiples modelos sustitutos obtienen un ajuste numérico equivalente respecto a la caja negra, pero presentan **jerarquías de atributos contradictorias**. Ambos sustitutos son válidos en términos de optimización cuadrática, pero uno señala a la *Edad* como variable dominante y el otro a la *Deuda*. En una auditoría regulatoria, esta discrepancia invalida la credibilidad técnica del sistema.

### 2. Inestabilidad estocástica y contratos de reproducibilidad
En ingeniería de datos, la reproducibilidad es un requisito ineludible: procesar el mismo registro con el mismo pipeline debe producir idéntico resultado. Sin embargo, al depender de muestreos de Monte Carlo, **ejecutar dos veces LIME o KernelSHAP sobre la misma instancia con diferente semilla aleatoria puede alterar el orden de los factores explicativos**. En entornos corporativos donde las explicaciones se persisten en tablas de auditoría, esta volatilidad estocástica genera inconsistencias operativas graves.

### 3. Deformación por muestreo fuera de distribución (*OOD*)
Al perturbar variables de forma independiente para estimar derivadas locales, los explicadores generan combinaciones sintéticas que violan las correlaciones del esquema relacional (por ejemplo, salarios ejecutivos con empleos no cualificados). Los modelos, al recibir estas filas anómalas, devuelven probabilidades erráticas que distorsionan los coeficientes de atribución resultantes.

### 4. Vulnerabilidad adversarial: Modelos con "andamios" (*Scaffolding Models*)
Slack *et al.* (2020) demostraron que los explicadores agnósticos pueden manipularse deliberadamente. Es posible entrenar un clasificador con una bifurcación lógica oculta:
* Aplica una lógica discriminatoria sobre consultas reales provenientes de la distribución operativa.
* Conmuta hacia un modelo neutral cuando detecta la dispersión sintética característica de las perturbaciones de LIME o SHAP.

Como resultado, el explicador emite un reporte de auditoría impecable certificando equidad, mientras el modelo discrimina activamente en producción.

![Figura 7. Taxonomía de distorsiones y traza de siete puertas FOM-7. Fuente: elaboración propia a partir de Herrera-Vásquez y Herrero-Uceda (2026).](../figures/exported/fig_d8_fom7_traza_es.png)

La Figura 7 muestra cómo cada una de las siete puertas del protocolo FOM-7 actúa como una barrera técnica de contención ante estas fallas operacionales.
