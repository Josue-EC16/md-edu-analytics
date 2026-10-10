# Evaluación grupal del proyecto de minería de datos

## Instrucciones

Esta evaluación revisa el avance del proyecto hasta la fase 4 de CRISP-DM: entendimiento del negocio, entendimiento de los datos, preparación de los datos y modelado. El grupo debe responder las diez preguntas con resultados de su propio proyecto; no se evalúan respuestas memorizadas ni propuestas presentadas como si fueran resultados obtenidos.

- Respondan de forma breve, precisa y con evidencia visible en la presentación o en el notebook.
- Cada integrante debe conocer el trabajo completo. El docente puede dirigir preguntas a cualquier integrante.
- El grupo debe entregar y abrir su notebook `.ipynb` ejecutado, con código y salidas visibles. Los resultados mostrados deben coincidir con los del documento o la presentación.
- Incluyan títulos, etiquetas, unidades y fuentes en tablas y gráficos. Expliquen los resultados con redacción clara y cuiden ortografía y consistencia.
- Para clasificación, trabajen con regresión logística y/o árbol de decisión, que son los modelos revisados en clase. Si presentan otro modelo, identifíquenlo y no lo usen para sustituir la evidencia de los modelos estudiados.
- Distingan los resultados medidos de las metas futuras. No afirmen que una métrica mejoró si no muestran una comparación reproducible.

## Rúbrica

Asigne a cada criterio un nivel de 1 a 4 y calcule los puntos como `peso × nivel / 4`. Si no hay evidencia suficiente para evaluar un criterio, asígnele 0. La calificación final es la suma sobre 100 puntos.

| Criterio | Peso | 4 - Sólido | 3 - Adecuado | 2 - En desarrollo | 1 - Insuficiente |
|---|---:|---|---|---|---|
| Entendimiento del negocio y métrica | 15 | Problema, decisión y métrica están alineados; fórmula, resultado y plan de mejora están justificados. | Explica problema y métrica con resultado, con alguna justificación incompleta. | Objetivo o métrica es ambiguo; faltan elementos del cálculo o su interpretación. | No identifica un problema claro ni una métrica verificable. |
| Entendimiento y calidad de los datos | 10 | Fuente, unidad de análisis, dimensiones y calidad se describen con evidencia y contexto. | Describe los datos y sus dimensiones; la revisión de calidad es parcial. | Omite elementos importantes o presenta cifras sin evidencia. | No puede describir el conjunto de datos utilizado. |
| Preparación de los datos | 15 | Explica y reproduce tratamientos, justificando decisiones y evitando fuga de información. | Documenta los principales tratamientos, aunque alguna decisión queda poco justificada. | Tratamientos incompletos, débilmente justificados o difíciles de reproducir. | No explica qué preparación realizó o el procedimiento compromete la evaluación. |
| Exploración y hallazgo | 10 | Gráfico legible y pertinente; interpreta un hallazgo relevante sin exceder lo que permiten los datos. | Presenta e interpreta un gráfico pertinente, con análisis limitado. | El gráfico o su interpretación es poco claro o débilmente conectado al objetivo. | No presenta evidencia gráfica o el hallazgo no se sustenta en los datos. |
| Diseño del modelado y partición | 10 | Justifica modelo y partición entrenamiento/prueba; describe el procedimiento y previene fuga de información. | Indica modelo y proporciones de partición, con justificación parcial. | La partición o selección del modelo se explica de forma incompleta. | No puede describir el modelo ni cómo separó entrenamiento y prueba. |
| Variables importantes e interpretación | 10 | Identifica variables con un método apropiado y explica su interpretación y límites. | Presenta variables importantes y una interpretación básica. | Muestra variables o importancias sin explicar cómo se obtuvieron o qué significan. | No presenta evidencia de variables importantes. |
| Evaluación del modelo y mejora | 10 | Reporta métricas pertinentes sobre prueba, interpreta errores y propone una mejora comprobable. | Reporta exactitud y otra métrica pertinente; interpreta parcialmente los resultados. | Métricas incompletas, sin contexto o calculadas de forma poco clara. | No presenta métricas verificables o confunde entrenamiento con prueba. |
| Comunicación y redacción | 5 | Presentación y documentos son claros, coherentes, correctos y fáciles de seguir. | Comunicación comprensible, con errores menores de redacción u organización. | La redacción u organización dificulta seguir algunos resultados. | La presentación o documentación impide comprender el trabajo. |
| Notebook, código y reproducibilidad | 15 | Notebook organizado y ejecutable; resultados reproducibles, código legible y salidas coherentes con lo expuesto. | Notebook ejecutado y entendible; hay detalles menores de orden o reproducibilidad. | Código o salidas incompletos; cuesta verificar parte de los resultados. | Notebook ausente, no ejecutable o sin evidencia que respalde los resultados. |
| **Total** | **100** |  |  |  |  |

## Preguntas

### Entendimiento del negocio

1. **¿Qué problema concreto aborda su proyecto, qué decisión o acción busca apoyar y cuál es su criterio de éxito de negocio?** Indiquen a quién afecta y cómo se conecta el análisis con esa necesidad.

2. **¿Cuál es la métrica principal del proyecto y cómo se calcula?** Presenten su fórmula, las variables y unidades involucradas, el valor observado hasta ahora y una acción concreta para mejorarla. Aclaren si es una métrica de negocio o de desempeño del modelo.

### Entendimiento y preparación de los datos

3. **¿Cuál es la unidad de análisis, de dónde provienen los datos y cuántos registros y variables tiene el conjunto utilizado?** Indiquen qué representa una fila y, si hubo filtros, cuántos registros quedaron después de aplicarlos.

4. **¿Qué problemas de calidad encontraron y qué preparación aplicaron?** Informen la cantidad y las columnas con valores faltantes; mencionen también duplicados o inconsistencias relevantes y expliquen qué hicieron y por qué.

### Exploración de los datos

5. **¿Qué resultado interesante encontraron en la exploración y qué gráfico lo demuestra?** Muéstrenlo con título y etiquetas, describan el patrón observado y expliquen por qué importa para el objetivo del proyecto.

### Modelado

6. **¿Cuál es su variable objetivo para la clasificación, qué clases tiene y qué modelo revisado en clase utilizaron: regresión logística, árbol de decisión o ambos?** Expliquen brevemente por qué ese modelo es pertinente para su problema.

7. **¿Qué proporción de los datos usaron para entrenamiento y para prueba, y cómo hicieron la separación?** Indiquen el método o semilla si corresponde y cómo evitaron que información de prueba influyera en el entrenamiento o la preparación.

8. **¿Cuáles son las variables más importantes según su modelo y cómo determinaron su importancia?** Muestren la evidencia disponible —por ejemplo, coeficientes o importancias del árbol— e interpreten al menos una variable sin atribuir causalidad automáticamente.

9. **¿Qué desempeño obtuvo el modelo en el conjunto de prueba?** Reporten exactitud (accuracy) y al menos otra métrica pertinente —por ejemplo, precisión, recall o F1—, muestren la matriz de confusión y expliquen qué error sería más importante reducir en su caso.

10. **¿Qué visualización permite entender cómo toma decisiones su modelo?** Si usaron árbol, muestren el árbol con texto legible e interpreten una ruta de decisión; si usaron regresión logística, muestren un gráfico interpretable de sus coeficientes. Expliquen brevemente qué aporta la visualización.
