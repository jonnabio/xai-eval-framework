# Implicaciones para la evaluación auditable de XAI

## Selección de métodos y gobernanza de evidencia

La selección de métodos no admite una jerarquía universal: LIME, SHAP, Anchors y DiCE producen objetos distintos y compromisos distintos entre calidad, coste y cobertura. La pregunta es qué método responde a la tarea y qué evidencia hace admisible cada afirmación. El benchmark presenta perfiles condicionados, no una competencia cerrada.

FOM-7 hace trazable el paso de resultados a afirmaciones al separar auditoría, armonización, inferencia, reproducibilidad y reporte. Exige conservar unidad de análisis, configuración y alcance. Así, las conclusiones se acotan a EXP2, Adult Income, celdas calificadas y métricas y pruebas definidas, en vez de generalizar desde una comparación particular.

## Uso del protocolo y desarrollo del campo

La elección depende de tarea y riesgo: SHAP puede servir para auditoría si su coste y variante son viables; LIME, para exploración si su inestabilidad no se trata como evidencia robusta; Anchors, si se informan precisión y cobertura; DiCE, si se evalúan validez, proximidad, diversidad y factibilidad. En contextos de alto impacto, claridad y bajo coste no sustituyen validación ni restricciones de dominio.

OpenXAI, Quantus y las revisiones recientes amplían las herramientas y métricas disponibles; FOM-7 no las sustituye, sino que organiza su uso con criterios de admisibilidad, alcance inferencial y trazabilidad (Agarwal et al., 2022; Hedström et al., 2023; Nauta et al., 2023; Pawlicki et al., 2024; Canha et al., 2025). La madurez del campo requiere distinguir evidencia confirmativa, descripción y observaciones no generalizables.
