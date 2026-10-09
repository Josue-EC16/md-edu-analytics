# EduAnalytics: Análisis de patrones de uso de IA generativa y riesgo de burnout estudiantil

## 1. Descripción general

**Acuerdo de alcance:** clasificación multiclase retrospectiva de registros completos de los estudiantes universitarios representados en el CSV. UNIFRANZ es la universidad del equipo, no una procedencia acreditada de los datos. `wrangler` es el flujo principal de las Fases 1–3; el notebook de la raíz es complementario. No se ha demostrado detección anticipada. El KPI es numérico descriptivo; `Burnout_Risk_Level` es categórica.

**EduAnalytics** es un proyecto de minería de datos orientado al análisis de patrones de uso de inteligencia artificial generativa en estudiantes y su relación con variables académicas y de bienestar.

El propósito principal del proyecto es identificar qué características y hábitos diferencian a los estudiantes clasificados con distintos niveles de riesgo de burnout, prestando especial atención a variables como:

- intensidad de uso de IA generativa;
- finalidad principal del uso de IA;
- dependencia percibida de IA;
- ansiedad durante exámenes;
- horas de estudio tradicional;
- rendimiento académico;
- retención de habilidades;
- contexto académico e institucional.

El proyecto **no busca demostrar que la IA generativa causa burnout, ansiedad o bajo rendimiento académico**. El enfoque es identificar **patrones, asociaciones y relaciones predictivas** dentro del conjunto de datos disponible.

---

## 2. Área de aplicación

El proyecto se encuentra dentro de las áreas de:

- Minería de Datos
- Machine Learning
- Analítica Académica
- Educación / EdTech
- Inteligencia Artificial aplicada a educación

---

## 3. Problema identificado

El uso de herramientas de inteligencia artificial generativa por parte de estudiantes ha aumentado de forma considerable. Sin embargo, disponer únicamente del dato de que un estudiante utiliza IA no es suficiente para comprender su comportamiento académico.

Es necesario analizar:

- cuánto utiliza IA;
- para qué la utiliza;
- qué nivel de dependencia percibe;
- cuánto tiempo dedica al estudio tradicional;
- qué nivel de ansiedad presenta durante los exámenes;
- cómo se comporta su rendimiento académico;
- cómo se relacionan estos factores con su retención de habilidades;
- qué patrones aparecen en estudiantes con distintos niveles de riesgo de burnout.

Por este motivo, el proyecto busca transformar los datos disponibles en información útil para reconocer perfiles y patrones asociados con niveles elevados de riesgo de burnout.

---

## 4. Objetivo general

**Identificar patrones de uso de IA generativa y hábitos académicos asociados con niveles elevados de riesgo de burnout, para apoyar la detección de perfiles de mayor riesgo y futuras estrategias de uso responsable de IA en estudiantes.**

---

## 5. Qué se quiere lograr

El proyecto busca generar evidencia analítica que permita:

1. Comprender cómo utilizan los estudiantes las herramientas de IA generativa.
2. Identificar variables asociadas con niveles bajos, medios y altos de riesgo de burnout.
3. Analizar la relación entre intensidad de uso de IA y dependencia percibida.
4. Analizar la relación entre uso de IA, ansiedad, hábitos de estudio y rendimiento académico.
5. Detectar perfiles de estudiantes con características similares.
6. Preparar modelos predictivos que puedan clasificar el nivel de riesgo de burnout.
7. Explorar modelos de regresión para rendimiento académico.
8. Explorar agrupamientos de estudiantes mediante clustering.
9. Generar información que, en un contexto institucional real, pueda apoyar estrategias preventivas y de uso responsable de IA.

---

## 6. Dataset principal

### Nombre del archivo

`ai_student_impact_dataset (1).csv`

### Fuente

**Kaggle**

La publicación original y su versión 1 se verificaron el 9 de octubre de 2026. Publicador: `ranaghulamnabi` (Coding expert G.N), licencia declarada CC0: Public Domain. El archivo local es semánticamente equivalente al original. La fecha original de descarga del equipo sigue pendiente. Véase [procedencia y evidencia de equivalencia](PROCEDENCIA_DATASET.md).


### Tamaño del dataset

- **50.000 registros**
- **16 variables**
- **50.000 identificadores únicos**
- **0 valores nulos**
- **0 filas completamente duplicadas**

### Unidad de análisis

Cada fila representa un estudiante y contiene información relacionada con:

- uso de inteligencia artificial generativa;
- hábitos académicos;
- rendimiento;
- dependencia percibida;
- ansiedad;
- retención de habilidades;
- nivel de riesgo de burnout.

### Consideración importante sobre el origen de los datos

El origen sintético o simulado es una posibilidad no confirmada por la publicación consultada. No se acredita un muestreo de estudiantes reales ni una procedencia institucional. Los resultados describen este dataset y no se generalizan automáticamente a toda la población estudiantil.

---

## 7. Variable objetivo principal

### `Burnout_Risk_Level`

**Traducción:** Nivel de riesgo de burnout.

**Tipo:** variable categórica.

**Categorías:**

- `Low` → Riesgo bajo
- `Medium` → Riesgo medio
- `High` → Riesgo alto

Esta es la variable objetivo principal del proyecto.

El problema predictivo asociado corresponde a una **clasificación multiclase**, ya que se busca diferenciar entre tres niveles de riesgo.

### Interpretación correcta

La variable **no representa un diagnóstico clínico de burnout**.

Un registro con:

`Burnout_Risk_Level = High`

debe interpretarse como:

> estudiante clasificado dentro del dataset con nivel alto de riesgo de burnout.

No debe interpretarse como:

> estudiante diagnosticado clínicamente con burnout.

---

## 8. KPI principal

### Porcentaje de estudiantes clasificados con riesgo alto de burnout

El KPI principal del proyecto es:

**Porcentaje de estudiantes clasificados con riesgo alto de burnout.**

### Fórmula

```text
KPI = (Número de estudiantes con Burnout_Risk_Level = High / Número total de estudiantes) × 100
```

### Cálculo actual

- Estudiantes en categoría `High`: **12.487**
- Total de estudiantes: **50.000**

```text
KPI = (12.487 / 50.000) × 100
KPI = 24,974 %
```

Redondeando:

**KPI = 24,97 %**

### Línea base

La línea base del proyecto es:

> **24,97 % de los estudiantes del dataset están clasificados con nivel alto de riesgo de burnout.**

Esto equivale aproximadamente a:

> **1 de cada 4 estudiantes del dataset.**

---

## 9. Mejora tentativa del KPI

La mejora propuesta no establece un valor numérico arbitrario sin respaldo institucional.

La meta general se plantea como:

> **Reducir la proporción de estudiantes clasificados con riesgo alto respecto de la línea base del 24,97 %.**

Esta reducción es una meta futura de intervención institucional, no un resultado demostrado. Reducir las predicciones `High` de un clasificador no demuestra reducir el riesgo real ni modifica la línea base de etiquetas del CSV.

El proyecto de minería de datos puede contribuir mediante:

- identificación de patrones;
- detección de perfiles de mayor riesgo;
- apoyo analítico;
- generación de evidencia;
- modelos predictivos;
- soporte para decisiones preventivas.

---

## 10. Métrica principal de negocio

La métrica principal de negocio coincide con el KPI:

### Métrica

**Porcentaje de estudiantes con riesgo alto de burnout**

### Unidad

**Porcentaje (%)**

### Valor actual

**24,97 %**

### Fuente de cálculo

Variable:

`Burnout_Risk_Level`

### Interpretación

Permite conocer qué proporción del conjunto de estudiantes pertenece a la categoría de mayor riesgo definida en el dataset.

---

## 11. Métricas futuras de Machine Learning

Estas métricas se utilizarán cuando se desarrollen los modelos predictivos.

### Para clasificación

El modelo principal buscará predecir:

`Burnout_Risk_Level`

Las métricas candidatas son:

- Accuracy
- Precision
- Recall
- F1-Score
- Macro F1-Score
- Matriz de confusión

Como referencia inicial, **Macro F1-Score** es una métrica adecuada para evaluar de forma equilibrada las tres clases: Low, Medium y High.

### Para regresión

Si se modela rendimiento académico, se podrán utilizar:

- MAE
- RMSE
- R²

### Para clustering

Se podrán utilizar métricas como:

- Silhouette Score
- análisis de cohesión de grupos
- análisis de separación entre clusters
- interpretabilidad de los perfiles encontrados

---

## 12. Variables del dataset

| Variable original | Traducción al español | Tipo / función |
|---|---|---|
| `Student_ID` | Identificador del estudiante | Identificador |
| `Major_Category` | Área o categoría académica | Categórica |
| `Year_of_Study` | Año o nivel de estudios | Categórica |
| `Pre_Semester_GPA` | Promedio académico antes del semestre | Numérica |
| `Weekly_GenAI_Hours` | Horas semanales de uso de IA generativa | Numérica |
| `Primary_Use_Case` | Principal finalidad de uso de IA | Categórica |
| `Prompt_Engineering_Skill` | Habilidad para formular prompts | Categórica |
| `Tool_Diversity` | Diversidad de herramientas de IA utilizadas | Numérica |
| `Paid_Subscription` | Suscripción pagada de IA | Booleana |
| `Traditional_Study_Hours` | Horas de estudio tradicional por semana | Numérica |
| `Perceived_AI_Dependency` | Dependencia percibida de IA | Numérica |
| `Institutional_Policy` | Política institucional respecto al uso de IA | Categórica |
| `Anxiety_Level_During_Exams` | Nivel de ansiedad durante los exámenes | Numérica |
| `Post_Semester_GPA` | Promedio académico después del semestre | Numérica |
| `Skill_Retention_Score` | Puntuación de retención de habilidades | Numérica |
| `Burnout_Risk_Level` | Nivel de riesgo de burnout | Categórica / objetivo principal |

---

## 13. Variables más importantes

### `Weekly_GenAI_Hours`

**Traducción:** Horas semanales de uso de IA generativa.

Representa la intensidad de utilización de herramientas de IA generativa.

### `Primary_Use_Case`

**Traducción:** Principal finalidad de uso de IA.

Categorías encontradas:

- `Debugging/Troubleshooting` → Depuración y resolución de problemas
- `Copywriting/Drafting` → Redacción y elaboración de borradores
- `Ideation` → Generación de ideas
- `Summarizing_Reading` → Resumen y apoyo a la lectura
- `Direct_Answer_Generation` → Generación directa de respuestas

### `Perceived_AI_Dependency`

**Traducción:** Dependencia percibida de IA.

Rango observado: **1 a 10**.

Promedio aproximado: **3,51**.

### `Traditional_Study_Hours`

**Traducción:** Horas de estudio tradicional por semana.

Promedio aproximado: **11,21 horas semanales**.

### `Anxiety_Level_During_Exams`

**Traducción:** Nivel de ansiedad durante los exámenes.

Rango observado: **1 a 10**.

Promedio aproximado: **4,27**.

### `Skill_Retention_Score`

**Traducción:** Puntuación de retención de habilidades.

Promedio aproximado: **75,80** (máximo observado: 100; instrumento y escala oficial no documentados).

### `Pre_Semester_GPA`

**Traducción:** Promedio académico antes del semestre.

Promedio aproximado: **3,15**.

### `Post_Semester_GPA`

**Traducción:** Promedio académico después del semestre.

Promedio aproximado: **3,35**.

### `Burnout_Risk_Level`

**Traducción:** Nivel de riesgo de burnout.

Es la variable objetivo principal del proyecto.

---

## 14. Variables secundarias o de contexto

### `Major_Category`

Área académica del estudiante.

Categorías:

- STEM
- Business
- Humanities
- Medical
- Arts

### `Year_of_Study`

Nivel de estudios.

Categorías:

- Freshman
- Sophomore
- Junior
- Senior
- Graduate

El dataset se encuentra principalmente orientado a educación superior.

### `Prompt_Engineering_Skill`

Nivel de habilidad para formular prompts.

Categorías:

- Beginner
- Intermediate
- Advanced

### `Tool_Diversity`

Cantidad o diversidad de herramientas de IA utilizadas.

Rango observado: **1 a 5**.

### `Institutional_Policy`

Política institucional respecto al uso de IA.

Categorías:

- `Allowed_With_Citation` → Permitido con citación
- `Actively_Encouraged` → Promovido activamente
- `Strict_Ban` → Prohibición estricta

### `Paid_Subscription`

Indica si el estudiante utiliza una suscripción pagada.

Valores:

- True
- False

---

## 15. Variable que no debe usarse como predictor

### `Student_ID`

El identificador del estudiante se conserva para trazabilidad, pero **no debe utilizarse como variable predictora**.

No representa un comportamiento, característica académica ni condición relacionada con el problema.

---

## 16. Distribución del nivel de riesgo de burnout

| Nivel | Cantidad | Porcentaje |
|---|---:|---:|
| Low | 16.369 | 32,74 % |
| Medium | 21.144 | 42,29 % |
| High | 12.487 | 24,97 % |
| **Total** | **50.000** | **100 %** |

La categoría más frecuente es **Medium**.

La categoría de mayor interés para el KPI es **High**.

---

## 17. Principales relaciones encontradas

Las cifras siguientes son **Pearson**, recalculadas sobre el CSV completo. Para dependencia y ansiedad, escalas ordenadas cuyo instrumento no está acreditado, la interpretación principal usa **Spearman**; Pearson se conserva como contraste descriptivo histórico.

| Relación | Pearson | Spearman |
|---|---:|---:|
| `Pre_Semester_GPA` / `Post_Semester_GPA` | 0,927 | 0,917 |
| `Weekly_GenAI_Hours` / `Perceived_AI_Dependency` | 0,665 | 0,555 |
| `Perceived_AI_Dependency` / `Anxiety_Level_During_Exams` | 0,308 | 0,280 |
| `Weekly_GenAI_Hours` / `Anxiety_Level_During_Exams` | 0,269 | 0,221 |
| `Weekly_GenAI_Hours` / `Skill_Retention_Score` | -0,118 | -0,039 |

### GPA inicial y GPA final

Correlación aproximada: **0,927**.

Existe una relación positiva muy fuerte entre el rendimiento académico previo y posterior.

### Horas de IA y dependencia percibida

Correlación aproximada: **0,665**.

Es una de las relaciones más importantes del proyecto. Dentro del dataset, una mayor cantidad de horas de uso de IA tiende a estar asociada con una mayor dependencia percibida.

### Dependencia de IA y ansiedad

Correlación aproximada: **0,308**.

Existe una relación positiva moderada.

### Horas de IA y ansiedad

Correlación aproximada: **0,269**.

Existe una relación positiva débil a moderada.

### Horas de IA y retención de habilidades

Correlación aproximada: **-0,118**.

Existe una relación negativa débil.

---

## 18. Hallazgo descriptivo principal

Al comparar los estudiantes según el nivel de riesgo de burnout se observan diferencias claras:

| Variable | Low | Medium | High |
|---|---:|---:|---:|
| Horas de IA por semana | 4,64 | 7,35 | 15,21 |
| Dependencia percibida de IA | 2,82 | 3,36 | 4,64 |
| Ansiedad durante exámenes | 3,93 | 4,17 | 4,89 |
| Horas de estudio tradicional | 11,97 | 11,29 | 10,08 |
| GPA final | 3,40 | 3,35 | 3,28 |
| Retención de habilidades | 76,40 | 76,24 | 74,25 |

El grupo `High` presenta, en promedio:

- mayor cantidad de horas semanales de IA;
- mayor dependencia percibida;
- mayor ansiedad;
- menos horas de estudio tradicional;
- ligeramente menor GPA final;
- menor retención de habilidades.

Estas diferencias deben interpretarse como **asociaciones descriptivas** y no como evidencia de causalidad.

---

## 19. Variable derivada propuesta

### `GPA_Change`

Se plantea crear una variable derivada denominada **Cambio en el promedio académico**.

Fórmula:

```text
GPA_Change = Post_Semester_GPA - Pre_Semester_GPA
```

Promedio observado aproximado: **+0,203**.

Puede ser útil para modelos de regresión y para analizar la evolución académica del estudiante durante el periodo.

---

## 20. Líneas de modelado propuestas

La Fase 4 abordará clasificación con regresión logística y árbol de decisión. Regresión, clustering y `GPA_Change` son propuestas secundarias, fuera del conjunto principal de 14 predictores preparado en Fase 3.

### Clasificación

Variable objetivo: `Burnout_Risk_Level`.

Objetivo: clasificar estudiantes en Low, Medium y High.

Este es el problema predictivo principal.

### Regresión

Variables objetivo posibles:

- `Post_Semester_GPA`
- `GPA_Change`

Objetivo: estimar rendimiento académico o variación del GPA.

### Clustering

No utiliza una variable objetivo.

Objetivo: descubrir perfiles de estudiantes con patrones de comportamiento similares.

Los nombres y características de los clusters deben determinarse después de aplicar los algoritmos y no deben definirse de antemano.

---

## 21. Hipótesis exploratorias

- **H1:** una mayor cantidad de horas semanales de uso de IA generativa está asociada con una mayor dependencia percibida.
- **H2:** una mayor dependencia percibida de IA está asociada con mayores niveles de ansiedad durante los exámenes.
- **H3:** la intensidad de uso de IA presenta diferencias entre los estudiantes clasificados con riesgo bajo, medio y alto de burnout.
- **H4:** los estudiantes clasificados con riesgo alto presentan patrones diferentes de estudio tradicional, dependencia y ansiedad.
- **H5:** es posible identificar grupos de estudiantes con comportamientos similares mediante técnicas de clustering.
- **H6:** los patrones de uso de IA y los hábitos académicos presentan asociaciones diferentes con el rendimiento académico.

Estas hipótesis son exploratorias y no deben interpretarse como relaciones causales.

---

## 22. Alcance del proyecto

El alcance actual incluye:

- análisis del dataset principal descargado de Kaggle;
- estudio de 50.000 registros y 16 variables;
- análisis de patrones de uso de IA;
- análisis de dependencia percibida;
- análisis de ansiedad;
- análisis de rendimiento académico;
- análisis de retención de habilidades;
- análisis del riesgo de burnout;
- definición de un KPI medible;
- construcción futura de modelos de clasificación;
- exploración futura de modelos de regresión;
- exploración futura de clustering;
- generación de hallazgos que puedan apoyar decisiones académicas.

---

## 23. Límites del proyecto

### No se demuestra causalidad

Las relaciones encontradas son asociaciones estadísticas. No puede afirmarse que:

- usar más IA cause burnout;
- usar IA cause ansiedad;
- usar IA reduzca directamente el rendimiento;
- usar IA provoque menor retención de habilidades.

### Burnout no es un diagnóstico clínico

`Burnout_Risk_Level` representa un nivel de riesgo definido por el dataset.

No debe utilizarse como diagnóstico médico o psicológico.

### Origen sintético o simulado no confirmado

Los resultados describen principalmente el comportamiento interno del conjunto de datos y no deben generalizarse automáticamente a estudiantes reales de una universidad o país determinado.

### No se conoce completamente la fórmula original de `Burnout_Risk_Level`

Actualmente no se dispone de evidencia suficiente para reconstruir de forma verificable cómo fue generada originalmente esta variable.

Esto debe declararse como una limitación metodológica.

### Población del dataset

La variable `Year_of_Study` contiene Freshman, Sophomore, Junior, Senior y Graduate. Por esta razón, el dataset está relacionado principalmente con educación superior y no representa directamente cursos de primero a sexto de secundaria.

### El KPI no implica una mejora real todavía

La línea base de 24,97 % describe el dataset. La meta de reducir ese porcentaje corresponde a un escenario futuro y necesitaría una intervención real para poder ser comprobada.

---

## 24. Consideraciones metodológicas importantes

### Correlación no implica causalidad

Una correlación alta o moderada indica asociación estadística, pero no demuestra que una variable produzca cambios en otra.

### Disponibilidad temporal y fuga de información

En el alcance retrospectivo, GPA final y retención se incluyen como predictores de registros completos. Esto no acredita su disponibilidad anticipada. La fuga directa consiste en incluir la etiqueta o sus transformaciones; es distinta de la limitación temporal y de una posible circularidad por generación de la etiqueta. La fórmula original sigue desconocida.

La Fase 2 exploró el CSV completo. Prueba es una partición interna reservada, no una cohorte externa nunca inspeccionada; debe mantenerse fuera de futuras decisiones de selección.

Cuando se desarrollen modelos predictivos será necesario definir qué variables estarían disponibles realmente en el momento de realizar una predicción.

Por ejemplo, si el objetivo es detectar riesgo antes de terminar el semestre, variables como `Post_Semester_GPA` podrían no ser apropiadas como predictoras.

### Posible dependencia de la variable objetivo

Debido a que no se conoce con exactitud cómo fue construida `Burnout_Risk_Level`, será necesario revisar si algunas variables predictoras fueron utilizadas originalmente para generar esa etiqueta.

---

## 25. Resultados esperados

Se espera que el proyecto permita obtener:

- identificación de variables relevantes;
- análisis de asociaciones entre uso de IA y riesgo de burnout;
- perfiles de estudiantes;
- modelos capaces de clasificar niveles de riesgo;
- métricas de desempeño reproducibles;
- visualizaciones interpretables;
- conclusiones basadas en datos;
- recomendaciones para futuras estrategias de uso responsable de IA.

---

## 26. Interpretación correcta del proyecto

El proyecto debe entenderse como:

> **Una aplicación de minería de datos orientada a identificar patrones de uso de IA generativa y hábitos académicos asociados con diferentes niveles de riesgo de burnout estudiantil.**

No debe presentarse como un sistema de diagnóstico clínico de burnout ni como una demostración de que la inteligencia artificial genera burnout.

---

## 27. Resumen ejecutivo

EduAnalytics analiza un dataset de Kaggle compuesto por 50.000 estudiantes y 16 variables relacionadas con uso de IA generativa, hábitos académicos, rendimiento, dependencia percibida, ansiedad, retención de habilidades y riesgo de burnout.

La variable objetivo principal es `Burnout_Risk_Level`, que clasifica a los estudiantes en riesgo bajo, medio o alto.

El KPI principal del proyecto es el **porcentaje de estudiantes clasificados con riesgo alto de burnout**, cuya línea base es **24,97 %**.

El análisis realizado muestra que los estudiantes clasificados en el grupo de riesgo alto presentan, en promedio, mayor cantidad de horas de utilización de IA, mayor dependencia percibida, mayor ansiedad, menor cantidad de horas de estudio tradicional y ligeramente menor retención de habilidades.

Una de las asociaciones más relevantes es la correlación aproximada de **0,665 entre horas semanales de uso de IA y dependencia percibida**.

El proyecto busca utilizar estos patrones para desarrollar modelos de clasificación, estudiar el rendimiento académico y descubrir perfiles de estudiantes, manteniendo siempre una interpretación no causal y no clínica de los resultados.

---

## 28. Idea central del proyecto

> **Utilizar minería de datos para identificar patrones de uso de IA generativa y hábitos académicos asociados con diferentes niveles de riesgo de burnout estudiantil, tomando como línea base que el 24,97 % de los estudiantes del dataset se encuentra clasificado en nivel de riesgo alto.**


## 29. Correcciones verificadas y preparación

Las tres diferencias de la sección 18 eran de publicación: High/horas IA 15,22 → 15,21; Medium/dependencia 3,37 → 3,36; Low/GPA final 3,41 → 3,40. El CSV no cambió de valores. Se desconoce si el origen fue transcripción o redondeo intermedio. Las Fases 2 y 3 contrastan la documentación corregida con el CSV.

El dataset tiene cero nulos, duplicados completos y duplicados de identificador. Los extremos IQR se conservan; un valor señalado no es automáticamente un error. Los criterios de plausibilidad son provisionales, no instrumentos acreditados.

Particiones congeladas: 35.000 / 7.500 / 7.500, semilla 42, estratificación por objetivo, sin cruces por estudiante. Las etiquetas siguen siendo texto. No se exportan transformaciones aprendidas ni modelos. El ajuste de categorías y escalado corresponde exclusivamente al entrenamiento o al pliegue correspondiente de Fase 4.
