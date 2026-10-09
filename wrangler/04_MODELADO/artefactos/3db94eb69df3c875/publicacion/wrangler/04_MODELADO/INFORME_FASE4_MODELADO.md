# Informe Fase 4: Modelado EduAnalytics

Experimento `3db94eb69df3c875`. Python 3.10.6; scikit-learn 1.7.2.

## Objetivo y continuidad

Clasificación multiclase retrospectiva de `Burnout_Risk_Level` en estudiantes universitarios representados en el CSV. UNIFRANZ corresponde al equipo. Se preservan 50.000 registros, valores, orden y particiones. El KPI **24,974 % High** describe etiquetas; las métricas siguientes evalúan predicciones y no demuestran reducirlo.

## Diseño y presupuesto

Entrenamiento 35.000, validación 7.500 y prueba 7.500. Cinco pliegues estratificados compartidos, mezcla y semilla 42. Principal 14 predictores; reducido 12, sin GPA final ni retención. Sin identificadores, objetivo, GPA_Change, imputación, recortes o SMOTE. Pipeline nuevo por ajuste; escalado solo para logística y one-hot nominal con desconocidas ignoradas. Logística: 10 combinaciones; árbol: 16 de 360; bosque: 12 de 72. Se repiten los mismos espacios y combinaciones en sensibilidad. 380 ajustes CV + 6 reajustes de candidatos + 6 Dummy + 1 final = **393 ajustes**. Ejecución secuencial, un hilo; no se redujo el presupuesto. Configuraciones completas: `protocolo.json`; resultados completos: `busqueda_cv.csv` de cada experimento. CV selecciona hiperparámetros: su media no es una evaluación independiente y su DE no es un intervalo de confianza.

### Compatibilidad verificada

Un intento inicial falló al puntuar el primer pliegue Dummy por `pos_label=1` con etiquetas textuales. Se corrigió declarando High en el scorer y se registró otro identificador antes de las búsquedas reales. En promedio macro se ignora pos_label y se utilizan explícitamente las tres clases. La incidencia y un ajuste inicial Dummy sin evaluación completa están registrados en `incidencias_implementacion.json`; no forman parte de los 393 ajustes del experimento completo. No hubo reducción de búsquedas ni resultados estimados.

## Algoritmos y línea base

Logística multinomial L2 ofrece una referencia regularizada interpretable. El árbol representa reglas e interacciones; Random Forest agrega árboles bootstrap con subconjuntos de variables y tiene mayor complejidad. Dummy aprende **Medium**: validación Macro F1 **0.198151**, Accuracy **0.422933**. No predice Low ni High, que tienen Recall cero; su precisión indefinida se registra y se calcula como cero.

## CV y validación

| model | scenario | cv_macro_f1 | cv_std | train_macro_f1 | validation_macro_f1 | validation_accuracy | precision_High | recall_High | f1_High | gap | search_seconds |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| dummy | principal | 0.198135 | 0.000019 | 0.198135 | 0.198151 | 0.422933 | 0.000000 | 0.000000 | 0.000000 | -0.000016 | 0.394543 |
| logistica | principal | 0.539575 | 0.003304 | 0.540808 | 0.534845 | 0.533733 | 0.663941 | 0.476775 | 0.555003 | 0.005963 | 16.719550 |
| arbol | principal | 0.524107 | 0.005165 | 0.533612 | 0.533385 | 0.525733 | 0.622404 | 0.528030 | 0.571346 | 0.000227 | 27.546804 |
| random_forest | principal | 0.537131 | 0.004798 | 0.562972 | 0.534054 | 0.531467 | 0.663762 | 0.487987 | 0.562462 | 0.028918 | 745.917773 |
| logistica | reducido | 0.539967 | 0.003701 | 0.540851 | 0.535526 | 0.534400 | 0.666915 | 0.477843 | 0.556765 | 0.005325 | 14.735367 |
| arbol | reducido | 0.526106 | 0.007276 | 0.533612 | 0.533385 | 0.525733 | 0.622404 | 0.528030 | 0.571346 | 0.000227 | 24.968810 |
| random_forest | reducido | 0.537119 | 0.005011 | 0.561689 | 0.536140 | 0.533067 | 0.664978 | 0.490657 | 0.564670 | 0.025549 | 573.759455 |

## Errores por clase

Las matrices usan filas reales y columnas predichas en orden Low, Medium, High. Se exportan conteos y proporciones por clase real en los JSON y figuras. Cada candidato conserva predicciones con trazabilidad. Precision de High penaliza falsos positivos; Recall de High penaliza High confundidos con Low/Medium. Las brechas entrenamiento−validación son diagnósticas; no prueban por sí solas generalización externa.

### Regresión logística

Parámetros: `{"clasificador__C":100,"clasificador__class_weight":null}`. Convergencia True; iteraciones [22]; 90 coeficientes.

| Real | Low | Medium | High |
| --- | --- | --- | --- |
| Low | 1185 | 1210 | 60 |
| Medium | 855 | 1925 | 392 |
| High | 154 | 826 | 893 |

Brecha entrenamiento−validación 0.005963. High→Low 154; High→Medium 826; falsos positivos de High 452. [Matrices con normalización](figuras/3db94eb69df3c875/principal_logistica_confusion.png).

### Árbol de decisión

Parámetros: `{"clasificador__ccp_alpha":0.0,"clasificador__class_weight":null,"clasificador__max_depth":5,"clasificador__min_samples_leaf":10,"clasificador__min_samples_split":2}`. Profundidad 5; 63 nodos; 32 hojas.

| Real | Low | Medium | High |
| --- | --- | --- | --- |
| Low | 1448 | 911 | 96 |
| Medium | 1162 | 1506 | 504 |
| High | 253 | 631 | 989 |

Brecha entrenamiento−validación 0.000227. High→Low 253; High→Medium 631; falsos positivos de High 600. [Matrices con normalización](figuras/3db94eb69df3c875/principal_arbol_confusion.png).

### Random Forest

Parámetros: `{"clasificador__class_weight":null,"clasificador__max_depth":8,"clasificador__max_features":0.5,"clasificador__min_samples_leaf":20,"clasificador__n_estimators":150}`. 150 árboles; 51370 nodos; profundidad media 8.00.

| Real | Low | Medium | High |
| --- | --- | --- | --- |
| Low | 1181 | 1205 | 69 |
| Medium | 887 | 1891 | 394 |
| High | 155 | 804 | 914 |

Brecha entrenamiento−validación 0.028918. High→Low 155; High→Medium 804; falsos positivos de High 463. [Matrices con normalización](figuras/3db94eb69df3c875/principal_random_forest_confusion.png).

## Interpretabilidad

Coeficientes logísticos por clase en `coeficientes.csv`, con numéricas estandarizadas y todas las categorías one-hot. No equivalen a efectos causales ni a contrastes aislados contra una categoría omitida. Árbol: reglas completas y vista truncada a profundidad 2, con orden real de clases y cantidades ponderadas si se usa balanced. Bosque: número de árboles, nodos y profundidad. Impureza puede favorecer variables con muchos cortes; permutación sobre validación mide caídas de Macro F1 en variables originales con cinco repeticiones. Correlación entre predictores puede enmascarar o repartir importancia. No se infiere la fórmula de la etiqueta.

## Sensibilidad

| model | validation_macro_f1_delta_reducido_menos_principal | precision_High_delta_reducido_menos_principal | recall_High_delta_reducido_menos_principal | gap_delta_reducido_menos_principal | search_seconds_delta_reducido_menos_principal |
| --- | --- | --- | --- | --- | --- |
| arbol | 0.000000 | 0.000000 | 0.000000 | 0.000000 | -2.577994 |
| logistica | 0.000681 | 0.002975 | 0.001068 | -0.000637 | -1.984183 |
| random_forest | 0.002086 | 0.001216 | 0.002670 | -0.003369 | -172.158318 |

Las diferencias son reducido−principal. El escenario reducido conserva particiones, pliegues, combinaciones y presupuesto. Es una alternativa descriptiva; no acredita detección anticipada ni elimina posible circularidad.

## Selección congelada

Ganador principal: **Regresión logística**, Macro F1 de validación **0.534845**. Mejora frente a Dummy: **0.336694**. Regla: mayor Macro F1, empate hasta 1e-12, Recall de High y simplicidad logística→árbol→bosque. La decisión, parámetros, huellas y procedimiento final están en `seleccion_modelo.json`; su recibo se guardó antes de cargar prueba.

La ventaja sobre el segundo candidato es **0.000791** de Macro F1; no demuestra superioridad estadística. El ganador recupera **47.68%** de los High de validación y omite **52.32%**. El árbol puede ofrecer otro compromiso Precision/Recall de High, visible en la tabla, pero no ganó el criterio principal. La estabilidad CV, brecha, interpretación y coste complementan la selección. Las consecuencias de omitir High deben valorarse en Fase 5.

## Modelo final y prueba

Pipeline nuevo reajustado con **42.500 registros**, más que los candidatos de validación. Prueba: **7.500 registros**, Macro F1 **0.534332**, Accuracy **0.535200**.

| clase | f1 | precision | precision_undefined | recall | support |
| --- | --- | --- | --- | --- | --- |
| Low | 0.521313 | 0.546959 | False | 0.497964 | 2456 |
| Medium | 0.542586 | 0.486845 | False | 0.612740 | 3171 |
| High | 0.539097 | 0.666143 | False | 0.452750 | 1873 |

High→Low **157**, High→Medium **868**; Low→High **53**, Medium→High **372**. La selección se conserva tras prueba; no se hicieron nuevos ajustes para mejorarla.

## Reproducibilidad

El README documenta comandos de etapas independientes y ejecución con kernels nuevos. Los hashes identifican datos, protocolo, código, pliegues, selección y artefactos, sin referencias circulares. Las fechas y duraciones se guardan aparte; los resultados verificables se reutilizan sin nuevas búsquedas. El pipeline final comprimido incluye preprocesamiento y clasificador. Se prueba en un proceso independiente contra todas las predicciones y probabilidades guardadas. Consulte `verificacion.json` para los controles efectivamente ejecutados.

## Límites y traspaso a Fase 5

La fórmula de burnout y el origen sintético siguen sin confirmarse. Un desempeño extraordinario podría reflejar reglas desconocidas de construcción de la etiqueta; no demuestra fuga directa ni aplicación clínica. GPA final y retención pertenecen al alcance retrospectivo. Fase 2 exploró el CSV completo: prueba es una partición interna reservada, no una cohorte externa nunca inspeccionada. Se mantiene fuera de ajustes posteriores. No se demuestra causalidad, detección anticipada, representatividad institucional ni reducción real del riesgo. Fase 5 debe valorar cumplimiento de negocio, consecuencias de errores, procedencia y validación externa; permanece pendiente.

## Referencias oficiales

[Validación cruzada](https://scikit-learn.org/1.7/modules/cross_validation.html), [métricas](https://scikit-learn.org/1.7/modules/model_evaluation.html), [logística](https://scikit-learn.org/1.7/modules/generated/sklearn.linear_model.LogisticRegression.html), [árbol](https://scikit-learn.org/1.7/modules/generated/sklearn.tree.DecisionTreeClassifier.html), [bosque](https://scikit-learn.org/1.7/modules/generated/sklearn.ensemble.RandomForestClassifier.html), [permutación](https://scikit-learn.org/1.7/modules/permutation_importance.html).
