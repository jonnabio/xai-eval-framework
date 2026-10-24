# Introducción

## De predecir a responder por decisiones

La expansión de la inteligencia artificial en actividades científicas,
profesionales y administrativas ha trasladado parte del problema desde la capacidad
de predecir hacia la capacidad de responder por una predicción. En una tarea de bajo
impacto puede bastar con que el sistema funcione de manera adecuada. Cuando su salida
orienta un diagnóstico, una asignación de crédito, una alerta de seguridad, una
decisión laboral o una intervención automatizada, también importa conocer qué
información utilizó, bajo qué condiciones puede fallar, quién debe supervisarlo y qué
evidencia permite cuestionar su resultado. La inteligencia artificial explicable
(*explainable artificial intelligence*, XAI) adquiere relevancia en ese tránsito: no
como ornamento comunicativo añadido a un modelo, sino como conjunto de recursos para
investigar, justificar y delimitar su comportamiento en un contexto de uso (Barredo Arrieta
et al., 2020; Ali et al., 2023).

Esta función no se reduce a “abrir” una caja negra. Un sistema puede documentar su
arquitectura y seguir siendo difícil de comprender para quien toma una decisión; a la
inversa, una explicación sencilla puede ser intuitiva y, sin embargo, describir de
forma inexacta el proceso que produjo la salida. Los principios propuestos por
Phillips et al. (2021) separan precisamente la existencia de una explicación, su
significado para una persona concreta, su correspondencia con el proceso del sistema
y el reconocimiento de los límites de conocimiento. La separación es crucial: que
una explicación exista o resulte legible no establece todavía que sea correcta,
útil o suficiente.

Por ello, el problema científico de la XAI no consiste únicamente en generar
representaciones comprensibles. Consiste en determinar cuándo un artefacto
explicativo aporta evidencia para una finalidad definida. Una explicación dirigida a
depurar un modelo responde una pregunta distinta de otra destinada a apoyar una
decisión profesional, documentar una auditoría o permitir que una persona afectada
comprenda y cuestione un resultado. Su calidad depende de la relación entre modelo,
objeto explicativo, audiencia, tarea, riesgo y criterio de evaluación.

## Objetivo, tesis y recorrido del capítulo

Este capítulo ofrece una síntesis científica y legible de los fundamentos, las
aplicaciones emergentes y las principales brechas de la XAI, y presenta FOM-7 como
una respuesta metodológica acotada al problema de evaluar comparativamente
explicaciones post-hoc. Su pregunta rectora es: ¿bajo qué condiciones una explicación
de un sistema de IA puede considerarse evidencia útil, reproducible y defendible para
una audiencia y un propósito concretos?

La tesis central es que una explicación no se convierte en evidencia por ser clara o
convincente. Debe existir correspondencia entre la pregunta formulada, el objeto
explicativo, el constructo evaluado, la audiencia, el diseño de prueba y el alcance de
la afirmación. Desde esa tesis, el capítulo define primero qué es y qué no es XAI;
examina después áreas de aplicación mediante ejemplos y límites; organiza las
brechas técnicas, humanas, causales, operativas y de gobernanza; y finalmente presenta
FOM-7 y el caso Adult/tabular como demostración de una evaluación funcionalmente
fundamentada. El caso no establece un ranking universal de explicadores. Su función
es mostrar cómo la trazabilidad y el control del diseño permiten distinguir una
salida plausible de una afirmación empírica defendible.

## Delimitación de aportaciones y procedencia de resultados

Para garantizar la debida transparencia académica y precisar la novedad de esta obra respecto de investigaciones previas de los autores, se delimitan tres planos de contribución:

1. **Resultados empíricos antecedentes:** Los contrastes inferenciales globales de las hipótesis H1 (diferencias de fidelidad) y H2 (diferencias de estabilidad) proceden de Herrera-Vásquez y Herrero-Uceda (2026), publicados en *Revista de Investigación Multidisciplinaria Iberoamericana* (RIMI); la evaluación de reproducibilidad inter-semilla (P1) y las medidas de parsimonia y coste proceden del repositorio experimental de la tesis doctoral de Herrera-Vásquez (2026).
2. **Resultados reanalizados e integrados en este capítulo:** La convergencia simultánea de los cuatro métodos (LIME, SHAP, Anchors y DiCE) bajo un prisma analítico común que contrasta objetos explicativos heterogéneos (sustitutos locales, atribuciones aditivas, reglas y contrafactuales) que en los trabajos previos se abordaban de forma aislada.
3. **Aportaciones originales inéditas presentadas por primera vez en esta obra:**
   - La formalización conceptual completa y secuencial del **Protocolo FOM-7 de siete compuertas** como estándar metodológico de aseguramiento de calidad y trazabilidad de evidencia en XAI.
   - La estructuración de las directrices desde la **perspectiva de la ingeniería de datos y la observabilidad de software**, formulando analogías de pipelines y arneses de pruebas computacionales.
   - El análisis multidimensional de **perfiles de compromiso operativo (*trade-offs*)** entre fidelidad, estabilidad, parsimonia y coste computacional para la selección justificada de métodos en producción.
   - La articulación de criterios de evaluación técnica orientados al cumplimiento de marcos regulatorios emergentes (Ley de Inteligencia Artificial de la UE y marco NIST AI RMF).

