# Diccionario de datos: EduAnalytics

Entrada: `dataset/ai_student_impact_dataset (1).csv`, 50.000 registros × 16 variables. Fuente, definiciones respaldadas y límites: [procedencia](PROCEDENCIA_DATASET.md). Cada fila representa un estudiante universitario del dataset; no se acredita una muestra de UNIFRANZ.

Las categorías y rangos siguientes son **observados en el CSV**. Las definiciones se ajustan a la descripción publicada; ninguna escala observada acredita por sí sola un instrumento. Dependencia y ansiedad son escalas ordenadas, aunque su almacenamiento sea entero.

| Variable | Tipo observado | Significado y respaldo | Rango o categorías observados | Papel principal |
|---|---|---|---|---|
| `Student_ID` | `int64` | Identificador único del estudiante según la fuente; 50.000 identificadores únicos observados. No acredita participantes reales. | 100001 a 150000 | Identificador, solo trazabilidad |
| `Major_Category` | `object` | Área académica o categoría de carrera. | `Arts`, `Business`, `Humanities`, `Medical`, `STEM` | Predictor retrospectivo |
| `Year_of_Study` | `object` | Nivel o año académico; Graduate no equivale necesariamente a un año adicional. | `Freshman`, `Graduate`, `Junior`, `Senior`, `Sophomore` | Predictor retrospectivo |
| `Pre_Semester_GPA` | `float64` | GPA antes del periodo de uso de IA según la fuente; promedio previo en el análisis académico. | 1.183 a 3.998 | Predictor retrospectivo |
| `Weekly_GenAI_Hours` | `float64` | Horas semanales de uso de herramientas de IA. | 0.0 a 40.0 | Predictor retrospectivo |
| `Primary_Use_Case` | `object` | Propósito principal del uso de IA. | `Copywriting/Drafting`, `Debugging/Troubleshooting`, `Direct_Answer_Generation`, `Ideation`, `Summarizing_Reading` | Predictor retrospectivo |
| `Prompt_Engineering_Skill` | `object` | Nivel de habilidad para escribir prompts; no consta instrumento de evaluación. | `Advanced`, `Beginner`, `Intermediate` | Predictor retrospectivo |
| `Tool_Diversity` | `int64` | Número de herramientas de IA diferentes utilizadas, según la fuente. | 1 a 5 | Predictor retrospectivo |
| `Paid_Subscription` | `bool` | Uso de servicios de IA pagados, según la fuente. | `False`, `True` | Predictor retrospectivo |
| `Traditional_Study_Hours` | `float64` | Horas semanales de estudio sin IA, según la fuente. | 1.0 a 35.86 | Predictor retrospectivo |
| `Perceived_AI_Dependency` | `int64` | Dependencia autoinformada de IA, según la fuente; instrumento y umbrales no documentados. | 1 a 10 | Predictor retrospectivo |
| `Institutional_Policy` | `object` | Estado de la política universitaria sobre IA; no acredita una universidad concreta. | `Actively_Encouraged`, `Allowed_With_Citation`, `Strict_Ban` | Predictor retrospectivo |
| `Anxiety_Level_During_Exams` | `int64` | Nivel de ansiedad en exámenes; método, validación clínica y carácter autoinformado no acreditados. | 1 a 10 | Predictor retrospectivo |
| `Post_Semester_GPA` | `float64` | GPA al completar el semestre según la fuente; predictor en el alcance retrospectivo. | 1.0 a 4.0 | Predictor retrospectivo; disponibilidad prospectiva pendiente |
| `Skill_Retention_Score` | `float64` | Puntuación de aprendizaje y comprensión retenidos según la fuente; protocolo y seguimiento longitudinal no documentados. | 10.78 a 100.0 | Predictor retrospectivo; disponibilidad prospectiva pendiente |
| `Burnout_Risk_Level` | `object` | Clasificación de riesgo provista por el dataset; fórmula desconocida y sin interpretación diagnóstica. | `High`, `Low`, `Medium` | Objetivo categórico; clases textuales |

## Traducciones de las categorías de uso

| Categoría exacta | Traducción |
|---|---|
| `Copywriting/Drafting` | Redacción y borradores |
| `Debugging/Troubleshooting` | Depuración y resolución de problemas |
| `Ideation` | Generación de ideas |
| `Summarizing_Reading` | Resumen y apoyo a la lectura |
| `Direct_Answer_Generation` | Generación directa de respuestas |

No se sustituyen los valores del CSV por sus traducciones.

## Relaciones y límites

La Fase 2 calcula las asociaciones y el documento general declara sus métodos. No se atribuyen efectos causales a suscripción, política, finalidad de uso o hábitos. Las relaciones no calculadas son hipótesis para análisis posterior. La fuente no documenta que la etiqueta sea una combinación de variables determinada.

`Burnout_Risk_Level` es el objetivo categórico; el KPI **numérico** es `100 × número de etiquetas High / número de registros = 24,974 %`. Las predicciones no son las etiquetas del KPI, ni reducir predicciones High demuestra una mejora real.

## Preparación y temporalidad

Se incluyen las 14 variables diferentes de identificador y objetivo en registros completos. `Student_ID` y `_row_id` son trazabilidad fuera de X. GPA final y retención no se presentan como disponibles para detección anticipada. `GPA_Change = Post_Semester_GPA - Pre_Semester_GPA` es una propuesta secundaria, no una columna añadida al conjunto principal.

Los criterios de plausibilidad de las Fases 2–3 (GPA 0–4, puntuación de retención 0–100, escalas ordenadas 1–10, herramientas 1–5, horas 0–168) son supuestos de auditoría declarados; la fuente no acredita todas esas escalas como oficiales. One-hot se usa para las cinco columnas categóricas sin imponer distancias ni un orden operativo no documentado.
