# Procedencia del dataset EduAnalytics

Consulta realizada el **9 de octubre de 2026**. La fecha de descarga original del equipo permanece desconocida; esta consulta y descarga de verificación no la sustituyen.

## Publicación comprobada

- URL: https://www.kaggle.com/datasets/ranaghulamnabi/ai-usage-and-student-academic-performance-analysis
- Título publicado: **AI Usage & Student Academic Performance Analysis**.
- Usuario publicador: **ranaghulamnabi**; nombre mostrado: **Coding expert G.N**.
- Licencia declarada por Kaggle: **CC0: Public Domain**.
- Versión consultada: **1**, única versión enumerada; nota: `Initial release`.
- Fecha de creación de esa versión según metadatos: **2026-05-15T18:10:29.143Z**. No es la fecha de descarga del equipo.
- Archivo contenido en el ZIP: `ai_student_impact_dataset (1).csv`; el ZIP contiene solamente ese CSV.

El publicador no queda acreditado por estos metadatos como autor científico, recolector o responsable de una muestra universitaria real. UNIFRANZ corresponde al equipo del proyecto.

Los controles se realizaron con los [metadatos oficiales](https://www.kaggle.com/api/v1/datasets/view/ranaghulamnabi/ai-usage-and-student-academic-performance-analysis) y la [descarga oficial de versión 1](https://www.kaggle.com/api/v1/datasets/download/ranaghulamnabi/ai-usage-and-student-academic-performance-analysis?datasetVersionNumber=1). Los notebooks utilizan el archivo local y funcionan sin consultar Kaggle durante su ejecución.

## Relación del archivo local con el original

Entrada única: `dataset/ai_student_impact_dataset (1).csv`, UTF-8, separador **punto y coma (`;`)**, finales **LF**. El original consultado tiene separador **coma (`,`)** y LF.

Ambos tienen **50.000 filas, 16 columnas**, los mismos encabezados en el mismo orden, los mismos identificadores, etiquetas, valores y orden de filas. Se compararon todos los campos: numéricos mediante `Decimal` exacto y los demás mediante igualdad de texto; además, ambos DataFrames leídos con `float_precision='round_trip'` son exactamente iguales, incluidos sus tipos.

Hay **10.369 representaciones numéricas distintas pero equivalentes** (por ejemplo, original `4.0`, local `4`). Por variable: `Pre_Semester_GPA` 34; `Weekly_GenAI_Hours` 1.087; `Traditional_Study_Hours` 1.781; `Post_Semester_GPA` 4.836; `Skill_Retention_Score` 2.631. No son diferencias de valor. No se conoce qué herramienta efectuó históricamente esa conversión de formato.

| Archivo o contenido | SHA-256 |
|---|---|
| CSV original, bytes extraídos de versión 1 | `4d911088c4b12d60a450a9acae6b606f4119ebbb48679518e427a4fc00778472` |
| CSV local anterior, CRLF | `afd5615d273f199988cf172fdb985c5d9298a018c2d386698ac4c7dc7328d694` |
| CSV local definitivo, LF | `585c433cf9b447df6812c76dbb6732d2bb663689a7b595a9a4b5d777fea991d5` |
| Contenido semántico canónico, igual para ambos | `21b6b0658b1c909045bed401a821f417f82bb9f86795ff9f346473339379d23d` |

La normalización local cambió **únicamente CRLF por LF**. Una comparación de las 50.001 filas de texto CSV, incluida la cabecera, confirmó igualdad de todos los campos antes y después. Las distintas huellas de bytes del original y del local se explican por separador y representación numérica; la huella local anterior difiere también por sus finales de línea.

La huella semántica se calcula sobre JSON compacto UTF-8 de `[cabecera, fila1, ...]`, sin ordenar filas ni columnas. En las columnas numéricas, incluido el identificador, cada campo se convierte mediante `format(Decimal(valor).normalize(), 'f')`; los demás campos se conservan literalmente. Se usa `ensure_ascii=False` y `separators=(',', ':')`. Este control complementa las huellas de bytes, que permanecen estrictas.

## Qué respalda la descripción publicada

La fuente describe información sobre estudiantes, áreas y años de estudio; hábitos de estudio; uso de IA; dependencia; GPA; retención; ansiedad y clasificación de riesgo de burnout. Define `Student_ID` como identificador único; `Tool_Diversity` como número de herramientas; `Paid_Subscription` como uso de servicios pagados y `Perceived_AI_Dependency` como dependencia autoinformada. Describe `Pre_Semester_GPA` antes del periodo de uso de IA y `Post_Semester_GPA` al completar el semestre. El diccionario separa estas definiciones de los rangos y categorías observados.

## Información pendiente y límites

La descripción, metadatos y archivos de la versión 1 **no documentan** fórmula, umbrales ni validación de `Burnout_Risk_Level`; tampoco confirman explícitamente un origen sintético o simulado. No se acredita institución, país, muestreo, participantes reales, instrumentos psicométricos, escala GPA oficial, protocolo de retención o fechas de medición de todos los campos.

La regularidad del CSV o una futura alta capacidad de clasificación no demostrarán un origen sintético ni una fórmula concreta. La posible circularidad de la etiqueta con predictores es una limitación y un análisis de sensibilidad futuro. La etiqueta no se interpreta clínicamente y las asociaciones no prueban causalidad. Los resultados describen los estudiantes universitarios representados en este CSV; su generalización institucional exige evidencia adicional.
