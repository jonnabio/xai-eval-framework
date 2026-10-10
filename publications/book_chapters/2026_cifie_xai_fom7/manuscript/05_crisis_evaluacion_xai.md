# Crisis de evaluación en XAI

## La crisis de confiabilidad en explicabilidad post-hoc

En la ingeniería de software tradicional, la validez de un módulo se verifica mediante aserciones deterministas: dadas unas entradas conocidas, se comprueba que la salida coincida exactamente con el valor esperado (`assert output == expected`). En el aprendizaje automático supervisado, el rendimiento se valida contrastando las predicciones contra un conjunto de etiquetas reales (*ground truth*).

Sin embargo, en el ámbito de la explicabilidad post-hoc nos enfrentamos a una **crisis de evaluación fundamental**: **no existe una etiqueta de referencia sobre cómo razona internamente una caja negra** (Krishna *et al.*, 2022; Nauta *et al.*, 2023; Agarwal *et al.*, 2023). Al no existir un "patrón oro" verificable, los desarrolladores han caído con frecuencia en dos trampas metodológicas:
1. **La trampa de la plausibilidad intuitiva:** Considerar que una explicación es "buena" si las variables destacadas confirman las intuiciones previas del desarrollador, lo cual incurre en sesgo de confirmación y legitima explicaciones espurias.
2. **La métrica endógena circular:** Evaluar un explicador utilizando las mismas métricas matemáticas para las que fue optimizado, impidiendo comparaciones cruzadas objetivas.

![Figura 6. Anatomía de la crisis de evaluación en explicabilidad post-hoc. Fuente: elaboración propia a partir de Krishna *et al.* (2022), Nauta *et al.* (2023) y Agarwal et al. (2023).](../figures/exported/fig_d7_cadena_evidencia_es.png)

La Figura 6 esquematiza la anatomía de esta crisis. Cuando un equipo despliega un explicador sin controles de calidad cuantitativos, corre el riesgo de introducir un segundo componente opaco dentro de su arquitectura de monitorización.

## Taxonomía de riesgos y patologías operacionales

Para un ingeniero de datos que supervisa flujos analíticos en producción, las fallas de los explicadores post-hoc se agrupan en cuatro patologías operativas críticas:

### 1. El Efecto Rashomon en explicaciones
Inspirado en el fenómeno estadístico formulado por Breiman (2001), ocurre cuando múltiples modelos sustitutos locales (por ejemplo, dos parametrizaciones distintas de LIME o la comparación entre LIME y SHAP) obtienen un ajuste numérico idéntico respecto a la caja negra, pero presentan **jerarquías de atributos diametralmente opuestas**. Ambos sustitutos son matemáticamente válidos en términos de optimización de mínimos cuadrados, pero uno afirma que el factor decisivo fue la *Edad* y el otro que fue el *Nivel de Deuda*. En una auditoría regulatoria o en un proceso judicial, esta contradicción destruye la credibilidad del sistema.

### 2. Inestabilidad estocástica y violación de contratos de reproducibilidad
En ingeniería de datos, la reproducibilidad es un contrato inquebrantable: procesar el mismo registro con el mismo pipeline debe producir exactamente el mismo resultado. Sin embargo, debido a que métodos como LIME y KernelSHAP dependen de muestreos estocásticos de Monte Carlo, **ejecutar dos veces el explicador sobre la misma instancia con diferente semilla aleatoria puede alterar el orden de los atributos más relevantes**. En un entorno corporativo donde las explicaciones se almacenan en tablas de auditoría, esta volatilidad estocástica genera inconsistencias graves entre corridas.

### 3. Deformación por muestreo fuera de distribución (*OOD*)
Al perturbar las características de forma independiente para estimar derivadas locales, los explicadores generan combinaciones sintéticas que violan las correlaciones naturales del esquema relacional (por ejemplo, filas con salarios millonarios y empleos no cualificados). Los modelos de caja negra, al recibir estos registros anómalos, devuelven probabilidades erráticas que distorsionan severamente los gradientes y coeficientes de atribución resultantes.

### 4. Vulnerabilidad adversarial: Modelos con "andamios" (*Scaffolding Models*)
Investigaciones fundamentales de Slack *et al.* (2020) demostraron que los explicadores agnósticos pueden ser engañados deliberadamente mediante una técnica denominada *adversarial scaffolding*. Es posible diseñar un modelo predictivo que contiene una compuerta condicional oculta:
* Cuando el modelo recibe una consulta real proveniente de la distribución operativa, aplica una lógica discriminatoria o basada en atributos protegidos (como el género o la etnia).
* Pero cuando detecta que la consulta proviene del muestreo perturbado característico de LIME o SHAP (identificando la dispersión sintética de los datos), el modelo conmuta automáticamente su lógica interna hacia un clasificador benigno que solo utiliza variables neutrales.

Como consecuencia, el explicador emite un reporte de auditoría impecable que certifica que el sistema es neutral y equitativo, ocultando por completo la discriminación real en producción.

![Figura 7. Taxonomía de distorsiones y traza de siete puertas FOM-7. Fuente: elaboración propia a partir de Herrera-Vásquez y Herrero-Uceda (2026).](../figures/exported/fig_d8_fom7_traza_es.png)

La Figura 7 muestra la trazabilidad entre estas cuatro distorsiones y las siete puertas de verificación del protocolo FOM-7, demostrando cómo cada puerta actúa como una barrera de contención técnica ante fallas operativas específicas.
