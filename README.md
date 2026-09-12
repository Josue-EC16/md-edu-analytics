# EduAnalytics: Análisis de Patrones de Uso de IA Generativa y Riesgo de Burnout Estudiantil

## Proyecto de Minería de Datos

**Universidad:** Universidad Privada Franz Tamayo - UNIFRANZ  
**Materia:** Minería de Datos  
**Metodología:** CRISP-DM  
**Estado actual:** Fase 1 completada y Fase 2 completada mediante Análisis Exploratorio de Datos (EDA)

### Integrantes

- Milenka Melody Chuquimia Osco
- Edson Teddy Tito Chuquimia
- Carlos Daniel Valverde Mendoza
- Alvaro Luis Carlos del Carpio Blanco
- Marcelo Josue Escobar Chipana

---

# 1. Descripción general del proyecto

**EduAnalytics** es un proyecto de Minería de Datos orientado al análisis de patrones de uso de Inteligencia Artificial Generativa en estudiantes y su relación con variables académicas y de bienestar.

El proyecto busca estudiar, a partir de un conjunto de datos obtenido de Kaggle, cómo se relacionan variables como las horas semanales de uso de IA generativa, la dependencia percibida, la ansiedad durante exámenes, las horas de estudio tradicional, el rendimiento académico y la retención de habilidades con los distintos niveles de riesgo de burnout estudiantil.

El propósito del proyecto no es demostrar que el uso de IA cause burnout, ansiedad o bajo rendimiento académico. El análisis se limita a identificar **patrones, asociaciones y relaciones estadísticas** presentes en los datos.

El proyecto también contempla, en fases posteriores de CRISP-DM, la posibilidad de construir modelos de:

- **Clasificación**, para estimar el nivel de riesgo de burnout.
- **Regresión**, para analizar el rendimiento académico y su variación.
- **Clustering**, para descubrir perfiles de estudiantes con comportamientos similares.

---

# 2. Contexto y problemática

La adopción de herramientas de Inteligencia Artificial Generativa como ChatGPT, Copilot y otros asistentes ha aumentado en los entornos educativos. Sin embargo, el uso intensivo de estas herramientas no siempre está acompañado de evidencia suficiente que permita conocer cómo se relacionan sus patrones de uso con variables académicas y de bienestar estudiantil.

Entre las principales preguntas del proyecto se encuentran:

- ¿Cuánto utilizan los estudiantes las herramientas de IA generativa?
- ¿Para qué utilizan principalmente estas herramientas?
- ¿Existe relación entre el tiempo de uso de IA y la dependencia percibida?
- ¿Cómo se comportan variables como ansiedad, estudio tradicional, GPA y retención de habilidades según el nivel de riesgo de burnout?
- ¿Existen perfiles de estudiantes con patrones claramente diferenciados?
- ¿Es posible construir modelos que ayuden a identificar niveles de riesgo de burnout a partir de características observables?

La necesidad principal del proyecto es transformar los datos disponibles en evidencia analítica útil para comprender estos comportamientos y apoyar futuras decisiones académicas.

---

# 3. Objetivo general

> **Identificar patrones de uso de IA generativa y hábitos académicos asociados con niveles elevados de riesgo de burnout, para apoyar la detección de perfiles de mayor riesgo y futuras estrategias de uso responsable de IA en estudiantes.**

---

# 4. Objetivos específicos

1. Analizar la estructura, calidad y distribución del conjunto de datos utilizado.
2. Identificar las variables más relevantes relacionadas con uso de IA, rendimiento académico y bienestar estudiantil.
3. Evaluar relaciones estadísticas entre las horas de uso de IA, dependencia percibida, ansiedad, estudio tradicional, retención de habilidades y riesgo de burnout.
4. Establecer un KPI principal que permita medir la proporción de estudiantes clasificados con riesgo alto de burnout.
5. Identificar hallazgos relevantes durante el EDA que sirvan como base para las siguientes fases de CRISP-DM.
6. Preparar posteriormente los datos para construir modelos de clasificación, regresión y clustering.
7. Evaluar en fases posteriores si los modelos construidos aportan información útil para la detección de perfiles de riesgo.

---

# 5. Alcance del proyecto

El alcance actual del proyecto comprende las dos primeras fases de CRISP-DM:

- **Fase 1: Entendimiento del negocio.**
- **Fase 2: Entendimiento de los datos mediante EDA.**

Dentro de este alcance se incluye:

- Definición del problema y objetivo del proyecto.
- Definición del KPI principal.
- Identificación de variables objetivo, variables principales y variables secundarias.
- Revisión de calidad de datos.
- Análisis de valores faltantes y duplicados.
- Detección estadística de posibles valores atípicos.
- Análisis univariado y bivariado.
- Cálculo de correlaciones.
- Estudio de la distribución del riesgo de burnout.
- Identificación de hallazgos relevantes.
- Definición preliminar de posibles tareas de Machine Learning.

En fases posteriores se contempla:

- Preparación de datos.
- Ingeniería de características.
- Codificación de variables categóricas.
- Escalado cuando sea necesario.
- División de datos en entrenamiento, validación y prueba.
- Construcción de modelos.
- Evaluación de modelos.
- Posible despliegue mediante dashboard o herramienta de apoyo al análisis académico.

---

# 6. Límites del proyecto

El proyecto presenta las siguientes limitaciones:

1. **No demuestra causalidad.** Las relaciones encontradas son asociaciones estadísticas y no permiten afirmar que una variable cause directamente otra.
2. **No realiza diagnóstico clínico.** `Burnout_Risk_Level` representa un nivel de riesgo, no un diagnóstico médico de burnout.
3. **El dataset parece sintético o simulado.** Por esta razón, los resultados deben interpretarse dentro del contexto del conjunto de datos y no generalizarse automáticamente a toda la población estudiantil.
4. **No se conoce con certeza la fórmula original utilizada para construir `Burnout_Risk_Level`.** El dataset proporciona las categorías `Low`, `Medium` y `High`, pero no se dispone de evidencia suficiente para reconstruir exactamente cómo se generaron originalmente.
5. **El público representado corresponde principalmente a educación superior.** La variable `Year_of_Study` contiene categorías como Freshman, Sophomore, Junior, Senior y Graduate, por lo que no representa directamente estudiantes de 1ro a 6to de secundaria.
6. **No se deben eliminar automáticamente los outliers.** Algunos valores extremos pueden ser precisamente los comportamientos más relevantes para el análisis.
7. **Las métricas de los futuros modelos todavía no están disponibles.** Actualmente no se han entrenado modelos de Machine Learning.

---

# 7. Fuente y descripción del dataset

## 7.1 Fuente

El dataset principal fue descargado de **Kaggle**.

Archivo utilizado:

```text
ai_student_impact_dataset (1).csv
```

## 7.2 Dimensiones

- **Registros:** 50.000
- **Variables:** 16
- **Identificadores únicos:** 50.000
- **Valores nulos:** 0
- **Filas duplicadas completas:** 0

## 7.3 Unidad de análisis

Cada fila representa un estudiante con características relacionadas con:

- Uso de IA generativa.
- Hábitos de estudio.
- Rendimiento académico.
- Dependencia percibida.
- Ansiedad.
- Retención de habilidades.
- Riesgo de burnout.

---

# 8. Diccionario de variables

| Variable original | Traducción al español | Tipo / Rol |
|---|---|---|
| `Student_ID` | Identificador del estudiante | Identificador, no predictor |
| `Major_Category` | Área/categoría académica | Categórica / contexto |
| `Year_of_Study` | Año/nivel de estudios | Categórica / contexto |
| `Pre_Semester_GPA` | Promedio académico antes del semestre | Numérica / principal |
| `Weekly_GenAI_Hours` | Horas semanales de uso de IA generativa | Numérica / principal |
| `Primary_Use_Case` | Principal finalidad de uso de IA | Categórica / principal |
| `Prompt_Engineering_Skill` | Habilidad para formular prompts | Categórica / secundaria |
| `Tool_Diversity` | Diversidad de herramientas de IA utilizadas | Numérica / secundaria |
| `Paid_Subscription` | Suscripción pagada | Booleana / secundaria |
| `Traditional_Study_Hours` | Horas de estudio tradicional | Numérica / principal |
| `Perceived_AI_Dependency` | Dependencia percibida de IA | Numérica / principal |
| `Institutional_Policy` | Política institucional respecto al uso de IA | Categórica / contexto |
| `Anxiety_Level_During_Exams` | Nivel de ansiedad durante exámenes | Numérica / principal |
| `Post_Semester_GPA` | Promedio académico después del semestre | Numérica / objetivo secundario |
| `Skill_Retention_Score` | Puntuación de retención de habilidades | Numérica / principal |
| `Burnout_Risk_Level` | Nivel de riesgo de burnout | Categórica / objetivo principal |

---

# 9. Variables objetivo

## 9.1 Variable objetivo principal

### `Burnout_Risk_Level`

**Traducción:** Nivel de riesgo de burnout.

**Tipo:** Categórica multiclase.

Valores:

- `Low` → Riesgo bajo.
- `Medium` → Riesgo medio.
- `High` → Riesgo alto.

Esta variable será utilizada posteriormente para una tarea de **clasificación multiclase**.

El objetivo no será diagnosticar burnout, sino identificar qué características diferencian a estudiantes clasificados en niveles bajo, medio y alto de riesgo.

---

## 9.2 Variable objetivo académica secundaria

### `Post_Semester_GPA`

**Traducción:** Promedio académico después del semestre.

Puede utilizarse como variable objetivo en una tarea de **regresión**.

Sin embargo, presenta una relación muy fuerte con `Pre_Semester_GPA`, con una correlación aproximada de:

```text
r = 0.927
```

Esto significa que el GPA previo explica una parte importante del GPA posterior, por lo que esta relación deberá ser considerada cuidadosamente durante el modelado.

---

## 9.3 Variable derivada propuesta

### `GPA_Change`

**Traducción:** Cambio en el promedio académico.

Se propone crear esta variable mediante:

```text
GPA_Change = Post_Semester_GPA - Pre_Semester_GPA
```

El cambio promedio observado es aproximadamente:

```text
+0.203
```

Esta variable puede resultar más útil para estudiar la evolución académica que simplemente predecir el GPA final.

---

# 10. Variables principales

Las variables consideradas más relevantes según el análisis realizado son:

## `Weekly_GenAI_Hours`

**Horas semanales de uso de IA generativa.**

Es una de las variables centrales del proyecto, ya que representa la intensidad del uso de IA.

## `Primary_Use_Case`

**Principal finalidad de uso de IA.**

Categorías observadas:

- Debugging/Troubleshooting → Depuración y resolución de problemas.
- Copywriting/Drafting → Redacción y elaboración de borradores.
- Ideation → Generación de ideas.
- Summarizing/Reading → Resumen y apoyo a la lectura.
- Direct Answer Generation → Generación directa de respuestas.

## `Perceived_AI_Dependency`

**Dependencia percibida de la IA.**

Escala aproximada de 1 a 10.

Es especialmente relevante porque presenta una correlación positiva importante con las horas de uso de IA.

## `Traditional_Study_Hours`

**Horas de estudio tradicional por semana.**

Permite comparar comportamientos de estudio convencional frente al uso de IA.

## `Anxiety_Level_During_Exams`

**Nivel de ansiedad durante exámenes.**

Escala aproximada de 1 a 10.

## `Skill_Retention_Score`

**Puntuación de retención de habilidades.**

Permite analizar si existen patrones entre uso de IA y retención de conocimientos o habilidades.

## `Pre_Semester_GPA`

**Promedio académico antes del semestre.**

Representa el nivel académico inicial.

## `Post_Semester_GPA`

**Promedio académico después del semestre.**

Representa el resultado académico posterior.

## `Burnout_Risk_Level`

**Nivel de riesgo de burnout.**

Es la principal variable objetivo del proyecto.

---

# 11. Variables secundarias o de contexto

## `Major_Category`

Área académica del estudiante.

Valores principales:

- STEM
- Business
- Humanities
- Medical
- Arts

## `Year_of_Study`

Nivel de estudios:

- Freshman
- Sophomore
- Junior
- Senior
- Graduate

## `Prompt_Engineering_Skill`

Nivel de habilidad para formular prompts:

- Beginner
- Intermediate
- Advanced

## `Tool_Diversity`

Cantidad/diversidad de herramientas de IA utilizadas.

## `Institutional_Policy`

Política institucional sobre uso de IA:

- Allowed_With_Citation → Permitido con citación.
- Actively_Encouraged → Promovido activamente.
- Strict_Ban → Prohibición estricta.

## `Paid_Subscription`

Indica si el estudiante utiliza una suscripción pagada de herramientas de IA.

## `Student_ID`

Se conservará solo para trazabilidad y no será utilizado como predictor.

---

# 12. KPI principal

## Porcentaje de estudiantes clasificados con riesgo alto de burnout

Este es el principal KPI del proyecto.

### Variable utilizada

```text
Burnout_Risk_Level
```

### Unidad de medida

```text
Porcentaje (%)
```

### Fórmula

```text
KPI = (Número de estudiantes con Burnout_Risk_Level = High / Número total de estudiantes) * 100
```

### Cálculo

```text
KPI = (12.487 / 50.000) * 100
KPI = 24,974 %
```

Redondeado:

```text
24,97 %
```

### Interpretación

Aproximadamente **1 de cada 4 estudiantes** del dataset está clasificado dentro del nivel `High` de riesgo de burnout.

Esto no significa que esos estudiantes tengan burnout clínicamente, sino que pertenecen a la categoría de riesgo alto definida en el dataset.

---

# 13. Distribución del riesgo de burnout

| Nivel | Estudiantes | Porcentaje |
|---|---:|---:|
| Low | 16.369 | 32,74 % |
| Medium | 21.144 | 42,29 % |
| High | 12.487 | 24,97 % |
| **Total** | **50.000** | **100 %** |

La categoría más frecuente es `Medium`, mientras que aproximadamente una cuarta parte del dataset está clasificada como `High`.

---

# 14. Mejora tentativa del KPI

La mejora definida para el proyecto es:

> **Reducir la proporción de estudiantes clasificados con riesgo alto respecto de la línea base actual del 24,97 %.**

No se define todavía una meta numérica específica, ya que no existe suficiente fundamento institucional para justificar un valor arbitrario como 20 % o 15 %.

Esta mejora debe interpretarse como una **meta futura o escenario de mejora**, no como un resultado ya alcanzado.

El proyecto actual busca aportar información que permita, en el futuro, diseñar estrategias de prevención o acompañamiento basadas en evidencia.

---

# 15. Diferencia entre burnout, estrés y ansiedad

El proyecto no utiliza burnout como sinónimo de estrés.

- `Anxiety_Level_During_Exams` representa el nivel de ansiedad durante exámenes.
- `Burnout_Risk_Level` representa el nivel de riesgo de burnout.

Por tanto, ambas variables se analizan de manera independiente.

El proyecto debe evitar expresiones como:

```text
"El estudiante tiene burnout"
```

Y utilizar formulaciones como:

```text
"El estudiante está clasificado con un nivel alto de riesgo de burnout dentro del dataset"
```

---

# 16. Metodología CRISP-DM

El proyecto utiliza **CRISP-DM (Cross Industry Standard Process for Data Mining)**.

Las seis fases son:

1. Entendimiento del negocio.
2. Entendimiento de los datos.
3. Preparación de los datos.
4. Modelado.
5. Evaluación.
6. Despliegue.

## Estado actual

| Fase | Estado |
|---|---|
| 1. Entendimiento del negocio | ✅ Completada |
| 2. Entendimiento de los datos / EDA | ✅ Completada |
| 3. Preparación de los datos | ⏳ Siguiente fase |
| 4. Modelado | ❌ Pendiente |
| 5. Evaluación | ❌ Pendiente |
| 6. Despliegue | ❌ Pendiente |

---

# 17. Fase 1 - Entendimiento del negocio

## 17.1 Problema

Existe desconocimiento sobre los patrones de uso de Inteligencia Artificial Generativa en estudiantes y sobre cómo estos patrones se relacionan con variables de bienestar y desempeño académico.

El proyecto se enfoca especialmente en comprender las características de los estudiantes clasificados con distintos niveles de riesgo de burnout.

## 17.2 Objetivo de negocio

> **Identificar patrones de uso de IA generativa y hábitos académicos asociados con niveles elevados de riesgo de burnout, para apoyar la detección de perfiles de mayor riesgo y futuras estrategias de uso responsable de IA en estudiantes.**

## 17.3 Decisión que se espera apoyar

Los resultados del proyecto podrían servir para apoyar decisiones relacionadas con:

- Identificación de perfiles de estudiantes con mayor riesgo.
- Diseño de estrategias de uso responsable de IA.
- Monitoreo de patrones de dependencia percibida.
- Diseño de acciones preventivas o de acompañamiento académico.
- Priorización de grupos que requieran mayor atención.

## 17.4 KPI de negocio

**Porcentaje de estudiantes clasificados con riesgo alto de burnout.**

Línea base actual:

```text
24,97 %
```

## 17.5 Criterio de mejora

Reducir progresivamente la proporción de estudiantes clasificados en el nivel `High` respecto de la línea base actual.

---

# 18. Fase 2 - Entendimiento de los datos y EDA

El Análisis Exploratorio de Datos permitió comprender la estructura, calidad, distribución y relaciones presentes en el dataset.

---

## 18.1 ¿Qué datos tengo?

El dataset contiene:

- 50.000 registros.
- 16 variables.
- Variables numéricas, categóricas y booleanas.
- 50.000 identificadores únicos.

Las variables cubren principalmente:

- Uso de IA.
- Hábitos académicos.
- Rendimiento académico.
- Dependencia percibida.
- Ansiedad.
- Retención de habilidades.
- Riesgo de burnout.

---

## 18.2 ¿Hay datos faltantes?

No.

El dataset presenta:

```text
0 valores nulos
```

Por esta razón, no fue necesario aplicar técnicas de imputación en esta etapa.

---

## 18.3 ¿Hay duplicados?

No se encontraron filas completamente duplicadas.

```text
Duplicados completos = 0
```

Además, `Student_ID` presenta 50.000 valores únicos.

---

## 18.4 ¿Existen valores atípicos?

Sí, se detectaron posibles valores atípicos mediante el criterio IQR.

| Variable | Posibles outliers |
|---|---:|
| `Weekly_GenAI_Hours` | 2.583 |
| `Pre_Semester_GPA` | 328 |
| `Post_Semester_GPA` | 346 |
| `Traditional_Study_Hours` | 161 |
| `Perceived_AI_Dependency` | 190 |
| `Skill_Retention_Score` | 216 |

Sin embargo, no se deben eliminar automáticamente.

Por ejemplo, un estudiante con 40 horas semanales de uso de IA puede ser un caso extremo, pero al mismo tiempo puede representar precisamente el tipo de comportamiento relevante para el estudio.

---

## 18.5 Estadística descriptiva principal

### `Pre_Semester_GPA`

- Media: 3.1461
- Desviación estándar: 0.4789
- Mínimo: 1.183
- Mediana: 3.21
- Máximo: 3.998

### `Weekly_GenAI_Hours`

- Media: 8.4278 horas
- Desviación estándar: 8.2695
- Mínimo: 0
- Mediana: 5.8
- Máximo: 40

### `Traditional_Study_Hours`

- Media: 11.2093 horas
- Mínimo: 1
- Mediana: 11.18
- Máximo: 35.86

### `Perceived_AI_Dependency`

- Media: 3.5054
- Escala aproximada: 1 a 10

### `Anxiety_Level_During_Exams`

- Media: 4.2708
- Escala aproximada: 1 a 10

### `Post_Semester_GPA`

- Media: 3.3493
- Mediana: 3.421
- Máximo: 4

### `Skill_Retention_Score`

- Media: 75.7981
- Mínimo: 10.78
- Máximo: 100

---

# 19. Distribuciones categóricas importantes

## `Major_Category`

- STEM: 15.059
- Business: 12.538
- Humanities: 9.994
- Medical: 6.476
- Arts: 5.933

## `Year_of_Study`

- Junior: 11.045
- Freshman: 11.031
- Senior: 10.634
- Sophomore: 9.860
- Graduate: 7.430

## `Primary_Use_Case`

- Debugging/Troubleshooting: 12.295
- Copywriting/Drafting: 12.011
- Ideation: 10.721
- Summarizing/Reading: 8.633
- Direct Answer Generation: 6.340

## `Prompt_Engineering_Skill`

- Beginner: 18.495
- Intermediate: 17.696
- Advanced: 13.809

## `Institutional_Policy`

- Allowed_With_Citation: 25.224
- Actively_Encouraged: 14.988
- Strict_Ban: 9.788

---

# 20. Relaciones entre variables

Las correlaciones más relevantes encontradas durante el EDA son:

| Relación | Correlación aproximada |
|---|---:|
| `Pre_Semester_GPA` ↔ `Post_Semester_GPA` | **0.927** |
| `Weekly_GenAI_Hours` ↔ `Perceived_AI_Dependency` | **0.665** |
| `Perceived_AI_Dependency` ↔ `Anxiety_Level_During_Exams` | **0.308** |
| `Weekly_GenAI_Hours` ↔ `Anxiety_Level_During_Exams` | **0.269** |
| `Tool_Diversity` ↔ `Skill_Retention_Score` | **0.197** |
| `Traditional_Study_Hours` ↔ `Skill_Retention_Score` | **0.148** |
| `Weekly_GenAI_Hours` ↔ `Skill_Retention_Score` | **-0.118** |
| `Perceived_AI_Dependency` ↔ `Skill_Retention_Score` | **-0.084** |
| `Post_Semester_GPA` ↔ `Traditional_Study_Hours` | **0.138** |
| `Post_Semester_GPA` ↔ `Weekly_GenAI_Hours` | **-0.019** |

---

# 21. Principales hallazgos del EDA

## 21.1 Horas de IA y dependencia percibida

Se encontró una correlación aproximada de:

```text
r = 0.665
```

entre `Weekly_GenAI_Hours` y `Perceived_AI_Dependency`.

Esto representa una relación positiva importante: a medida que aumenta el tiempo de uso de IA, también tiende a aumentar la dependencia percibida.

No implica causalidad.

---

## 21.2 Perfil promedio según nivel de riesgo de burnout

| Variable | Low | Medium | High |
|---|---:|---:|---:|
| Horas IA/semana | 4,64 | 7,35 | **15,22** |
| Dependencia percibida | 2,82 | 3,37 | **4,64** |
| Ansiedad | 3,93 | 4,17 | **4,89** |
| Estudio tradicional | **11,97** | 11,29 | **10,08** |
| GPA final | **3,41** | 3,35 | **3,28** |
| Retención de habilidades | **76,40** | 76,24 | **74,25** |

El grupo `High` presenta, en promedio:

- Mayor número de horas de uso de IA.
- Mayor dependencia percibida.
- Mayor ansiedad.
- Menos horas de estudio tradicional.
- Ligeramente menor GPA final.
- Menor retención de habilidades.

---

## 21.3 Hallazgo principal para comunicación

El resultado más claro para una presentación es:

```text
Low   -> 4,64 horas de IA/semana
Medium-> 7,35 horas de IA/semana
High  -> 15,22 horas de IA/semana
```

Los estudiantes clasificados en el nivel `High` utilizan, en promedio, más de tres veces las horas semanales de IA que los estudiantes clasificados en el nivel `Low`.

Este hallazgo debe presentarse como una asociación descriptiva y no como una relación causal.

---

# 22. Hipótesis exploratorias

Las siguientes hipótesis se consideran orientativas para fases posteriores:

### H1

Un mayor número de horas semanales de uso de IA está asociado con una mayor dependencia percibida.

### H2

Una mayor dependencia percibida está asociada con mayores niveles de ansiedad durante exámenes.

### H3

Los patrones de uso de IA presentan diferencias entre estudiantes clasificados con riesgo bajo, medio y alto de burnout.

### H4

Las horas de estudio tradicional y la retención de habilidades presentan diferencias entre grupos de riesgo de burnout.

### H5

Los estudiantes pueden agruparse en perfiles de comportamiento diferenciados mediante técnicas de clustering.

Estas hipótesis no deben interpretarse todavía como conclusiones causales.

---

# 23. Tareas de Machine Learning propuestas

## 23.1 Clasificación

**Objetivo:** predecir `Burnout_Risk_Level`.

Tipo:

```text
Clasificación multiclase
```

Clases:

- Low
- Medium
- High

Métricas candidatas para fases posteriores:

- Accuracy
- Precision
- Recall
- F1-Score
- Macro F1-Score
- Matriz de confusión

La métrica técnica candidata principal será **Macro F1-Score**, debido a que existen tres clases con distribuciones diferentes.

---

## 23.2 Regresión

Posibles variables objetivo:

- `Post_Semester_GPA`
- `GPA_Change`

Métricas candidatas:

- MAE
- RMSE
- R²

---

## 23.3 Clustering

No utiliza una variable objetivo.

El propósito será descubrir grupos de estudiantes con patrones de comportamiento similares.

Posibles métricas:

- Silhouette Score
- Cohesión intra-cluster
- Separación inter-cluster
- Interpretabilidad de los grupos

---

# 24. Próxima fase: Preparación de los datos

La siguiente etapa de CRISP-DM será la Fase 3.

Las tareas previstas son:

1. Conservar el archivo original sin modificaciones.
2. Excluir `Student_ID` de los predictores.
3. Validar rangos numéricos.
4. Revisar individualmente los posibles outliers.
5. Codificar variables categóricas.
6. Crear `GPA_Change`.
7. Seleccionar variables para cada tarea.
8. Escalar datos únicamente cuando el algoritmo lo requiera.
9. Dividir el dataset en entrenamiento, validación y prueba.
10. Prevenir data leakage mediante pipelines y una separación adecuada de datos.

---

# 25. Posible despliegue futuro

En caso de completar las fases de modelado y evaluación, los resultados podrían integrarse en:

- Dashboard académico.
- Panel de indicadores.
- Herramienta de exploración de perfiles estudiantiles.
- Sistema de apoyo a decisiones académicas.
- Módulo predictivo de riesgo.

El sistema no debería utilizarse como herramienta de diagnóstico clínico ni como mecanismo automático de sanción o evaluación individual.

---

# 26. Interpretación responsable de resultados

Durante todo el proyecto se deben respetar las siguientes reglas:

## No afirmar causalidad

Evitar:

```text
"La IA causa burnout"
```

Utilizar:

```text
"Se observa una asociación entre determinados patrones de uso de IA y los niveles de riesgo de burnout"
```

## No afirmar diagnóstico

Evitar:

```text
"24,97 % de los estudiantes tienen burnout"
```

Utilizar:

```text
"24,97 % de los registros están clasificados con riesgo alto de burnout"
```

## Reconocer el contexto del dataset

Los resultados obtenidos describen este conjunto de datos y no deben generalizarse automáticamente a todos los estudiantes.

---

# 27. Estado actual del proyecto

Actualmente el proyecto ha completado:

### ✅ Fase 1 - Entendimiento del negocio

- Problema definido.
- Objetivo definido.
- KPI principal definido.
- Línea base calculada.
- Variables objetivo identificadas.
- Alcance y límites establecidos.

### ✅ Fase 2 - Entendimiento de los datos / EDA

- Dataset cargado y revisado.
- Dimensiones identificadas.
- Tipos de variables identificados.
- Datos faltantes revisados.
- Duplicados revisados.
- Outliers identificados.
- Estadística descriptiva calculada.
- Distribuciones analizadas.
- Correlaciones calculadas.
- Relaciones con burnout analizadas.
- Hallazgos principales documentados.

### ⏳ Próximo paso

**Fase 3 - Preparación de los datos.**

---

# 28. Resumen ejecutivo

EduAnalytics busca analizar cómo se relacionan los patrones de uso de Inteligencia Artificial Generativa con variables académicas y de bienestar estudiantil.

El proyecto utiliza un dataset obtenido de Kaggle con **50.000 estudiantes y 16 variables**.

El KPI principal es:

> **Porcentaje de estudiantes clasificados con riesgo alto de burnout.**

La línea base calculada es:

```text
24,97 %
```

El EDA muestra que los estudiantes clasificados con riesgo `High` presentan, en promedio:

- 15,22 horas semanales de uso de IA.
- Mayor dependencia percibida.
- Mayor ansiedad.
- Menos horas de estudio tradicional.
- Menor retención de habilidades.
- Ligeramente menor GPA final.

Uno de los resultados más relevantes es la correlación aproximada de:

```text
r = 0.665
```

entre las horas semanales de IA y la dependencia percibida.

El proyecto utiliza la metodología CRISP-DM. Actualmente están completadas las fases de Entendimiento del Negocio y Entendimiento de los Datos. La siguiente etapa será la Preparación de los Datos.

---

# 29. Estructura sugerida del repositorio

```text
mineria-datos-ia-estudiantes/
├── README.md
├── requirements.txt
├── data/
│   ├── raw/
│   ├── processed/
│   └── external/
├── notebooks/
│   ├── 01_entendimiento_datos/
│   ├── 02_preparacion_datos/
│   ├── 03_modelado/
│   └── 04_evaluacion/
├── src/
│   ├── data/
│   ├── preprocessing/
│   ├── models/
│   └── evaluation/
├── reports/
│   ├── 01_entendimiento_negocio/
│   ├── 02_entendimiento_datos/
│   ├── 03_preparacion_datos/
│   ├── 04_modelado/
│   ├── 05_evaluacion/
│   └── 06_despliegue/
├── results/
│   ├── figures/
│   ├── tables/
│   └── models/
└── docs/
    ├── diccionario_datos/
    ├── metodologia/
    └── referencias/
```

---

# 30. Conclusión actual

Hasta este punto, el proyecto cuenta con una definición clara del problema, un KPI verificable, variables objetivo establecidas y un EDA suficientemente desarrollado para justificar el paso hacia la preparación y modelado de los datos.

El hallazgo más importante hasta el momento es que existen diferencias claras entre los grupos de riesgo de burnout en variables relacionadas con uso de IA, dependencia percibida, ansiedad, estudio tradicional y retención de habilidades.

Estos resultados justifican continuar hacia la Fase 3 de CRISP-DM para preparar los datos y evaluar posteriormente si estas relaciones permiten construir modelos predictivos útiles y técnicamente válidos.

---

## Nota metodológica final

Este repositorio documenta un proyecto académico de Minería de Datos. Los resultados tienen fines educativos y analíticos. No deben utilizarse como diagnóstico clínico, evaluación psicológica ni como evidencia causal sobre los efectos del uso de Inteligencia Artificial Generativa.
