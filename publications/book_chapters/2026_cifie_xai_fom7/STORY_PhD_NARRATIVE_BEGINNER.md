# La Historia Detrás de la Tesis: De Cajas Negras a Explicaciones Confiables
*Una narrativa sencilla sobre Inteligencia Artificial Explicable (XAI), pensada para no expertos y útil como estructura de la defensa doctoral.*

---

## Acto 1: La Pregunta Inicial — El Robot Mago y la Caja Negra

Imagina que en tu escuela contratan a un robot superinteligente para tomar decisiones importantes. Por ejemplo:
- Quién entra al equipo de fútbol.
- Quién recibe una beca de estudios.
- Quién necesita ayuda extra en matemáticas.

El robot analiza miles de datos en un segundo y anuncia su veredicto: **"Aceptado"** o **"Rechazado"**.

Cuando le preguntas al robot: *«Oye, ¿por qué me rechazaste?»*, el robot no responde nada. Se queda en silencio. Su cerebro es un laberinto gigante de millones de números que nadie puede leer a simple vista.

En el mundo real de la tecnología, a estos modelos de Inteligencia Artificial los llamamos **"Cajas Negras"**. Se usan en hospitales para detectar enfermedades, en bancos para dar préstamos y en sistemas legales. 

Pero surge un problema grave: **no podemos ni debemos confiar a ciegas en un robot mago si no sabemos cómo toma sus decisiones.** ¿Qué pasa si el robot está cometiendo un error? ¿O si está discriminando a alguien por una razón equivocada?

---

## Acto 2: El Dilema — ¿Quién Explica al Explicador?

Para resolver este problema, los científicos inventaron a los **"Detectives de IA"** (en ciencia los llamamos *métodos de explicabilidad post-hoc*, como LIME, SHAP, Anchors o DiCE).

El trabajo de un detective de IA es mirar a la caja negra por fuera, hacerle preguntas rápidas y decirle a las personas en español sencillo: 
> *«El robot te rechazó la beca por tus notas en historia, no por tu edad».*

¡Parecía la solución perfecta! Pero pronto los científicos descubrieron un nuevo dilema: **los detectives a veces se contradicen entre sí.**

Si le pides una explicación al detective **LIME**, te dice una cosa. Si le pides la explicación al detective **SHAP** sobre la misma persona, ¡te dice algo diferente!

Aquí nace la **motivación central de mi Tesis de Doctorado**:
> *Si las herramientas que nos explican la IA tampoco son perfectas y se contradicen... ¿cómo sabemos cuál dice la verdad? ¿Quién evalúa a los evaluadores?*

---

## Acto 3: Las 6 Piezas del Rompecabezas (Los Artículos A al F)

Para resolver este rompecabezas, organizamos nuestra investigación en seis etapas conectadas entre sí, como los capítulos de una historia de detectives:

```
[Mago Caja Negra] ──> [Detectives XAI] ──> [¿En quién confiar?]
                                                   │
  ┌────────────────────────────────────────────────┴────────────────────────────────┐
  │                                                                                 │
  ▼                                                                                 ▼
[Papel A: El Reglamento] ──> [Papel B: El Duelo] ──> [Papel C: Resistencia] ──> [Papel D: Caso Real]
  (Protocolo FOM-7)          (LIME vs SHAP)          (Escalabilidad)           (UCI Adult)
                                                                                    │
  ┌─────────────────────────────────────────────────────────────────────────────────┘
  │
  ▼
[Papel E: La Balanza] ──> [Papel F: Juicio Humano] ──> [¡Transparencia Defendible!]
  (Trade-offs)              (Alineación con personas)
```

---

### 1. Papel A: El Reglamento para los Detectives (Protocolo FOM-7)
* **Estado:** Publicado en *Revista de Investigación Multidisciplinaria Iberoamericana (RIMI)* (2026, DOI: 10.69850/rimi.vi3.307).
* **La idea simple:** Antes de poner a trabajar a los detectives, necesitamos un reglamento oficial de 7 pasos para asegurarnos de que las pruebas sean válidas. Lo llamamos el protocolo **FOM-7**.
* **Lo que descubrimos:** Creamos una forma justa de medir 5 propiedades clave:
  1. **Fidelidad:** ¿La explicación dice la verdad sobre lo que hizo la IA?
  2. **Estabilidad:** Si le preguntamos dos veces lo mismo, ¿mantiene su respuesta o cambia de opinión?
  3. **Parsimonia:** ¿La explicación es corta y fácil de entender?
  4. **Coste:** ¿Cuánto tiempo y cálculo le toma al detective responder?
  5. **Brecha de fidelidad:** ¿Qué tanto se equivoca al simplificar el problema?

---

### 2. Papel B: El Gran Duelo — LIME vs SHAP a Escala
* **Estado:** Enviado a *CLEI Electronic Journal (CLEIej)* (2026-10-04, Subm. #1196).
* **La idea simple:** Pusimos a competir frente a frente a los dos detectives más famosos del mundo en cientos de situaciones diferentes.
* **Lo que descubrimos:**
  * **SHAP** es como *Sherlock Holmes*: es extremadamente cuidadoso, nunca cambia de opinión (muy estable) y da respuestas muy precisas, pero es muy lento y costoso.
  * **LIME** es como un *detective veloz*: responde rapidísimo y da explicaciones muy breves, pero si el viento sopla (pequeños cambios en los datos), a veces cambia un poco su versión.

---

### 3. Papel C: La Prueba de Resistencia y Escalabilidad
* **Estado:** Listo para envío a *Tecnología en Marcha* (Edición Especial IA, borrador de 15 pág., Zenodo v0.12.0).
* **La idea simple:** ¿Qué pasa cuando el problema se vuelve 10 veces más grande o los datos tienen ruido? ¿Los detectives resisten la presión?
* **Lo que descubrimos:** Evaluamos cómo se comportan los explicadores cuando aumentamos el tamaño de la muestra y la complejidad de los modelos. Identificamos los puntos exactos donde las explicaciones dejan de ser confiables si no se controlan los parámetros.

---

### 4. Papel D: El Examen en el Mundo Real (Benchmark UCI Adult)
* **Estado:** Listo para envío a *Tecnología en Marcha* (Edición Especial IA, solicitud de cuenta pendiente).
* **La idea simple:** Vamos a probar a todos los detectives en un caso real importante: predecir los ingresos de las personas con el conjunto de datos *UCI Adult Income*.
* **Lo que descubrimos:** Evaluamos 5 familias de modelos (árboles, redes neuronales, regresión logística, etc.) cruzados con 4 tipos de explicadores. Demostramos en la práctica cómo se aplican las 7 puertas del protocolo FOM-7 para obtener evidencia auditable en lugar de suposiciones.

---

### 5. Papel E: La Balanza de las Decisiones (Trade-offs y Gobernanza)
* **Estado:** Enviado a *Computación y Sistemas (CIC-IPN)* (2026-10-04, Subm. #6783).
* **La idea simple:** Ningún detective es perfecto en todo. Elegir un explicador es como elegir un vehículo: un auto deportivo es veloz pero caro; una bicicleta es barata pero lenta.
* **Lo que descubrimos:** Construimos la "Frontera de Selección". Le enseñamos a las organizaciones y auditores cómo elegir la mejor herramienta según su necesidad:
  * Si estás en un **hospital** o un **juicio**, usa **SHAP** (máxima estabilidad y fidelidad).
  * Si estás en una **app móvil** que necesita responder en milisegundos, usa **LIME** (rapidez y brevedad).

---

### 6. Papel F: ¿Los Humanos y los Robots Entienden lo Mismo?
* **Estado:** En desarrollo inicial (*Journal of Computer Sciences Institute*).
* **La idea simple:** Al final del día, las explicaciones son para personas de carne y hueso. ¿Realmente los humanos entienden lo mismo que las métricas matemáticas?
* **Lo que exploramos:** Diseñamos un plan para comparar si los juicios de las personas (y de modelos de lenguaje usados como jueces) coinciden con las mediciones computacionales del benchmark.

---

## Acto 4: El Gran Final — La Narrativa para la Defensa Doctoral

Esta historia une todo el trabajo de investigación en un mensaje claro y motivador para la presentación de la tesis:

1. **El Problema:** La Inteligencia Artificial es poderosa pero opaca. Necesitamos explicaciones.
2. **La Complicación:** Las herramientas de explicación existen, pero sin evaluación rigurosa pueden dar falsas ilusiones de transparencia.
3. **La Solución (FOM-7):** Creamos un protocolo estandarizado de 7 puertas para auditar las explicaciones de forma reproducible.
4. **La Evidencia (Papeles A-E):** Probamos, comparamos y medimos los límites reales de herramientas como LIME, SHAP, Anchors y DiCE.
5. **El Impacto (Papel F y Capítulos):** Le damos a la sociedad y a los científicos un mapa claro para pasar de la **confianza ciega en los algoritmos** a una **supervisión transparente, responsable y centrada en las personas**.

---
*Nota: Este documento sirve como mapa narrativo conceptual para la presentación doctoral y para enriquecer la divulgación del trabajo de investigación, mantenido de manera independiente al capítulo de libro.*
