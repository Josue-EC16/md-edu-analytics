# Diccionario de Datos: EduAnalytics

## **Fuente / Dataset:** `ai_student_impact_dataset (1).csv`

## 1. Identificación y Contexto

### `Student_ID`

- **Traducción:** Identificador del estudiante.
- **Descripción:** Número único que sirve para individualizar a cada estudiante que participó en la recopilación de datos. No contiene valor analítico.
- **Tipo de dato:** `int` (Entero).
- **Relaciones:** Llave primaria del conjunto; no se relaciona analíticamente con otras variables.

### `Major_Category`

- **Traducción:** Área académica / Facultad.
- **Descripción:** Categoría principal que engloba la carrera que el estudiante está cursando (ej. _STEM, Humanities, Business, Medical, Arts_).
- **Tipo de dato:** `string` (Categórica nominal).
- **Relaciones:** Frecuentemente relacionada con `Institutional_Policy` (las políticas suelen variar por facultad) y `Primary_Use_Case` (diferentes áreas usan la IA para propósitos distintos).

### `Year_of_Study`

- **Traducción:** Año o nivel de estudios.
- **Descripción:** El progreso o año académico en el que se encuentra el estudiante (ej. _Freshman, Sophomore, Junior, Senior, Graduate_).
- **Tipo de dato:** `string` (Categórica ordinal).
- **Relaciones:** Puede tener relación con la `Prompt_Engineering_Skill` (mayor experiencia académica podría influir) y la presión reflejada en `Burnout_Risk_Level`.

---

## 2. Variables Académicas (Rendimiento y Estudio)

### `Pre_Semester_GPA`

- **Traducción:** GPA antes del semestre.
- **Descripción:** El promedio de calificaciones acumulado del estudiante antes de iniciar el periodo de estudio monitoreado. Sirve como línea base del rendimiento.
- **Tipo de dato:** `float` (Numérico decimal).
- **Relaciones:** Fuertemente relacionado con `Post_Semester_GPA` (sirve para calcular el progreso o caída del rendimiento).

### `Post_Semester_GPA`

- **Traducción:** GPA después del semestre.
- **Descripción:** El promedio de calificaciones al finalizar el periodo evaluado. En modelos predictivos suele ser la variable objetivo para tareas de regresión.
- **Tipo de dato:** `float` (Numérico decimal).
- **Relaciones:** Relacionado directamente con `Pre_Semester_GPA`, `Weekly_GenAI_Hours` y `Traditional_Study_Hours`.

### `Traditional_Study_Hours`

- **Traducción:** Horas de estudio tradicional.
- **Descripción:** Cantidad de horas a la semana que el estudiante dedica al estudio convencional (leyendo libros, repasando notas) sin asistencia automatizada.
- **Tipo de dato:** `float` (Numérico decimal).
- **Relaciones:** Relacionada inversamente (o de forma complementaria) con `Weekly_GenAI_Hours` y tiene un impacto en `Skill_Retention_Score`.

### `Skill_Retention_Score`

- **Traducción:** Puntuación de retención de habilidades.
- **Descripción:** Métrica que evalúa qué tanto conocimiento a largo plazo o habilidades prácticas retiene el estudiante.
- **Tipo de dato:** `float` (Numérico decimal, usualmente en escala 0-100).
- **Relaciones:** Se cruza mucho con `Perceived_AI_Dependency` y `Weekly_GenAI_Hours` (para verificar si el uso excesivo de IA reduce la retención real de conocimiento).

---

## 3. Hábitos de Uso de Inteligencia Artificial

### `Weekly_GenAI_Hours`

- **Traducción:** Horas semanales de uso de IA generativa.
- **Descripción:** La cantidad promedio de horas que el estudiante dedica por semana a usar herramientas de IA generativa (como ChatGPT, Claude, etc.) para tareas académicas.
- **Tipo de dato:** `float` (Numérico decimal).
- **Relaciones:** Es el predictor clave del proyecto. Se relaciona directamente con `Burnout_Risk_Level`, `Perceived_AI_Dependency` y `Post_Semester_GPA`.

### `Primary_Use_Case`

- **Traducción:** Principal finalidad de uso de IA.
- **Descripción:** El propósito principal por el que el estudiante recurre a la IA (ej. _Copywriting/Drafting, Debugging/Troubleshooting, Ideation, Summarizing_Reading, Direct_Answer_Generation_).
- **Tipo de dato:** `string` (Categórica nominal).
- **Relaciones:** Interactúa bastante con `Major_Category` (ej. los de STEM suelen usarla para debugging) y afecta la `Skill_Retention_Score`.

### `Prompt_Engineering_Skill`

- **Traducción:** Habilidad para formular prompts.
- **Descripción:** El nivel de destreza técnica percibido del estudiante para interactuar y extraer buenas respuestas de modelos de lenguaje (ej. _Beginner, Intermediate, Advanced_).
- **Tipo de dato:** `string` (Categórica ordinal).
- **Relaciones:** Relacionada con `Tool_Diversity` y el rendimiento reflejado en `Post_Semester_GPA`.

### `Tool_Diversity`

- **Traducción:** Diversidad de herramientas de IA.
- **Descripción:** Cantidad de distintas plataformas o modelos de IA diferentes que el estudiante utiliza regularmente.
- **Tipo de dato:** `int` (Entero).
- **Relaciones:** Vinculada a `Prompt_Engineering_Skill` y `Paid_Subscription`.

### `Paid_Subscription`

- **Traducción:** Suscripción pagada de IA.
- **Descripción:** Indica si el estudiante paga por versiones premium de herramientas de IA (ej. ChatGPT Plus).
- **Tipo de dato:** `bool` (Booleano: _True / False_).
- **Relaciones:** Impacta en `Weekly_GenAI_Hours` y podría estar correlacionada con mayor `Tool_Diversity`.

### `Institutional_Policy`

- **Traducción:** Política institucional sobre IA.
- **Descripción:** El nivel de permisividad de la universidad o facultad frente al uso de la IA (ej. _Strict_Ban, Allowed_With_Citation, Actively_Encouraged_).
- **Tipo de dato:** `string` (Categórica ordinal/nominal).
- **Relaciones:** Afecta fuertemente `Anxiety_Level_During_Exams` y `Weekly_GenAI_Hours` (la prohibición puede generar estrés o menor uso reportado).

---

## 4. Bienestar y Salud Mental (KPIs)

### `Perceived_AI_Dependency`

- **Traducción:** Dependencia percibida de la IA.
- **Descripción:** Nivel subjetivo (usualmente en una escala, ej. 1 al 10) que describe qué tan dependiente se siente el estudiante de la IA para lograr aprobar sus clases.
- **Tipo de dato:** `int` (Entero).
- **Relaciones:** Fuertemente correlacionada con `Weekly_GenAI_Hours` y `Anxiety_Level_During_Exams`.

### `Anxiety_Level_During_Exams`

- **Traducción:** Nivel de ansiedad durante los exámenes.
- **Descripción:** Escala autoinformada (usualmente de 1 al 10) del nivel de estrés o ansiedad que el estudiante experimenta al enfrentarse a evaluaciones.
- **Tipo de dato:** `int` (Entero).
- **Relaciones:** Altamente vinculada a `Burnout_Risk_Level` y a si la `Institutional_Policy` entra en conflicto con sus hábitos.

### `Burnout_Risk_Level`

- **Traducción:** Nivel de riesgo de burnout (agotamiento crónico).
- **Descripción:** Clasificación del riesgo de que el estudiante sufra agotamiento severo debido al estudio (ej. _Low, Medium, High_). En EduAnalytics, el porcentaje de estudiantes en "High" es nuestro **KPI principal**.
- **Tipo de dato:** `string` (Categórica ordinal).
- **Relaciones:** Variable objetivo principal para modelos de clasificación. Se ve afectada por una combinación de `Weekly_GenAI_Hours`, `Anxiety_Level_During_Exams`, y `Traditional_Study_Hours`.
