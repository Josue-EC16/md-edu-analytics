# Verificación de las Fases 1, 2 y 3 de EduAnalytics

Fecha: **9 de octubre de 2026**. Evidencia estructurada: [VERIFICACION_FASES_1_2_3.json](VERIFICACION_FASES_1_2_3.json). El trabajo quedó preparado para revisión local; no se creó un commit ni se publicó al remoto.

## Problemas confirmados y correcciones

Se encontraron 26.595 archivos de `.venv` versionados, ausencia de políticas de exclusión y finales de línea, huellas de CSV/notebooks calculadas sobre CRLF incompatibles con los bytes LF publicados, lectura con separador incorrecto en el notebook complementario, fórmula Markdown dañada, categorías y tres medias por grupo discordantes, referencias de entorno obsoletas y afirmaciones causales o instrumentales sin respaldo.

Se incorporaron `.gitignore` y `.gitattributes`, se retiró `.venv` **solo del índice**, se conservaron sus archivos y el historial, y se normalizó texto en LF. Los datos locales cambiaron únicamente de finales de línea; los valores y el CSV canónico de Git permanecen iguales. Se alinearon documentación, diccionario y materiales; se corrigieron ruta/separador/codificación, fórmula, roles, correlaciones ordinales e interpretaciones del notebook de la raíz. Se eliminaron direcciones de memoria de las representaciones de tablas y se fijaron sus identificadores HTML para estabilizar las salidas. Se conserva `wrangler` como secuencia principal y la raíz como complemento.

## Entorno reconstruido y ejecución

Dos entornos **nuevos**, independientes de `.venv`, con Python **3.10.6**, instalaron satisfactoriamente los requisitos y dieron `No broken requirements found.` en `pip check`. El segundo se instaló sin red desde ruedas descargadas, usando los requisitos de la copia canónica. Ambos contienen las mismas **66 dependencias resueltas**, fijadas en `requirements-lock.txt`; el archivo específico de preparación referencia al principal. No se acredita una verificación en otra versión de Python ni en otro sistema operativo; las pruebas se realizaron en Windows.

| Dependencia | Versión comprobada |
|---|---|
| Python | 3.10.6 |
| numpy | 2.2.6 |
| pandas | 2.3.3 |
| scikit-learn | 1.7.2 |
| scipy | 1.15.3 |
| ipykernel | 7.3.0 |
| nbformat | 5.11.1 |
| nbclient | 0.11.0 |
| nbconvert | 7.17.1 |
| matplotlib | 3.10.9 |
| seaborn | 0.13.2 |
| ipython | 8.39.0 |

Se ejecutaron en orden Fase 1 → Fase 2 → Fase 3 → complemento, con un kernel nuevo por notebook y salidas guardadas en UTF-8/LF. El verificador comprueba conteos de ejecución consecutivos y ausencia de salidas de error. También se ejecutaron desde las carpetas de fases; el complemento se probó con directorio de trabajo en la carpeta de Fase 3.

| Notebook | Celdas de código | Errores | Copia limpia desde raíz | Copia limpia desde carpetas |
|---|---:|---:|---|---|
| wrangler/01_ENTENDIMIENTO_NEGOCIO/01_entendimiento_negocio.ipynb | 4 | 0 | PASS | PASS |
| wrangler/02_COMPRENSION_DATOS/02_comprension_datos_eda.ipynb | 20 | 0 | PASS | PASS |
| wrangler/03_PREPARACION_DATOS/03_preparacion_datos.ipynb | 14 | 0 | PASS | PASS |
| notebook_eduanalytics_md.ipynb | 20 | 0 | PASS | PASS |

Las huellas de los **cuatro notebooks fueron idénticas antes y después de ambas ejecuciones de la copia limpia**, y coinciden con el contenido entregado. Se revisaron visualmente los 11 gráficos de Fase 2 y los 5 del complemento; las salidas de los notebooks no contienen stderr.

## Integridad, calidad y particiones

Entrada única: `dataset/ai_student_impact_dataset (1).csv`. Se preservaron las 50.000 filas, las 16 columnas, todos los valores, identificadores y etiquetas, con comparación exacta de todos los campos después de sustituir CRLF por LF. SHA-256 definitivo: `585c433cf9b447df6812c76dbb6732d2bb663689a7b595a9a4b5d777fea991d5`.

| Control | Resultado |
|---|---:|
| Filas / columnas originales | 50.000 / 16 |
| Nulos / campos vacíos | 0 / 0 |
| Duplicados completos / de identificador | 0 / 0 |
| Categorías internamente inconsistentes | 0 |
| Incidencias en rangos plausibles declarados | 0 |
| Etiquetas ausentes o inesperadas | 0 |
| Registros modificados o excluidos | 0 |
| KPI High exacto | 24,974 % |

Los rangos plausibles son criterios provisionales de auditoría, no instrumentos acreditados. Los **3.269 registros distintos** señalados por IQR en Fase 2 se conservan; ningún extremo se eliminó ni recortó.

| Partición | Registros | Low | Medium | High |
|---|---:|---:|---:|---:|
| Entrenamiento | 35.000 | 11.458 | 14.801 | 8.741 |
| Validación | 7.500 | 2.455 | 3.172 | 1.873 |
| Prueba | 7.500 | 2.456 | 3.171 | 1.873 |
| Total | 50.000 | 16.369 | 21.144 | 12.487 |

Se verificaron cero intersecciones por fila y estudiante, cobertura completa, reconstrucción exacta en el orden original, alineación X/y/trazabilidad y presencia de las tres clases. **Los tres CSV de particiones son idénticos byte a byte a los existentes antes de la corrección**, incluida la pertenencia y el orden de cada estudiante. La Fase 3 y el cargador bloquean cualquier divergencia mediante huellas congeladas de `(_row_id, Student_ID)`.

Los 14 predictores son las cinco categóricas (`Major_Category`, `Year_of_Study`, `Primary_Use_Case`, `Prompt_Engineering_Skill`, `Institutional_Policy`), ocho numéricas (`Pre_Semester_GPA`, `Weekly_GenAI_Hours`, `Tool_Diversity`, `Traditional_Study_Hours`, `Perceived_AI_Dependency`, `Anxiety_Level_During_Exams`, `Post_Semester_GPA`, `Skill_Retention_Score`) y `Paid_Subscription`. El objetivo y los campos `Student_ID`/`_row_id` permanecen fuera de X. `GPA_Change` no se añadió; las etiquetas siguen siendo texto Low/Medium/High.

## Artefactos y traspaso

Carpeta: `wrangler/03_PREPARACION_DATOS/artefactos/`. Las particiones conservan datos sin transformaciones aprendidas y contienen 17 columnas por `_row_id`; X contiene 14. El módulo exportado procede literalmente de la celda visible de Fase 3. Todas las huellas de entrada, referencias y artefactos del manifiesto coinciden.

| Artefacto | SHA-256 verificado |
|---|---|
| `train.csv` | `ad1350d1a98ea6cbb8f52d572c930257f5f3010033a0ca9969109d32e15e15fc` |
| `validation.csv` | `218af598fa78428fddafd4b530d3563d985a7ada0a2b4ffe758ea2cff3369e0e` |
| `test.csv` | `380f4be4f1d48fed8b44a688bdfc9990654238b9ecb9943f18c2651ecc1fc4b8` |
| `variables.csv` | `33e43397c774e5b474137b338e6e65634573c71b4a35a93164c069d14de12e89` |
| `decisiones_limpieza.csv` | `315eb7368fb3606479952015673b71d301d62a2fc647dd8d3f94fdca324ca062` |
| `preprocesamiento.py` | `c4f370181164f711cb6fa10c36c67e6d7ca082b7be852d9d6958c1efdbf873d5` |
| `INSTRUCCIONES_FASE4.md` | `f2c90303cda08bfb29f962b30620da68bc406a032a84b28989745ea9074aba0e` |
| `requirements_preparacion.txt` | `db94247c199f1e71c7503451c573551df039fbf65cb817603ffc2d7757da8a7f` |

SHA-256 del manifiesto: `50cd682633fde10258bbb8312d2f88f084077f6f537c17e47b2fe009fd2d3981`. Los hashes de notebooks y documentos están también en la evidencia JSON; los informes de auditoría no se incluyen entre sus propias referencias para evitar dependencias circulares.

`cargar_particion` devuelve X, y y trazabilidad alineados, verifica hash/esquema/tipos/clases y rechaza un CSV alterado. `crear_preprocesador` devuelve instancias nuevas sin ajustar. Se comprobaron matrices numéricas finitas de 35.000 × 30, booleanos 0/1, categorías aprendidas solo de entrenamiento y categorías desconocidas representadas por bloques de ceros. Para logística se contrastó la media y número de muestras del escalador contra entrenamiento; para árbol se comprobó que las ocho columnas numéricas pasan sin escalado. Una instancia separada ajustada a 1.000 filas verificó parámetros propios de ese subconjunto. Ninguna copia ajustada ni matriz transformada se exportó. No se entrenaron clasificadores ni se calcularon matrices de confusión o métricas predictivas.

Las instrucciones de Fase 4 indican cargar estas mismas particiones e integrar preprocesamiento y clasificador en un pipeline sin ajustar antes de validación cruzada. Prueba se reserva para evaluación final después de selección; la Fase 2 exploró el CSV completo, por lo que prueba **no es una cohorte externa nunca inspeccionada**. No hay balanceo, SMOTE, imputación ni recortes por defecto.

## Procedencia, cifras y límites

Se verificaron publicación oficial de Kaggle, publicador `ranaghulamnabi` / Coding expert G.N, versión 1 y licencia declarada CC0. El archivo original con comas tiene los mismos valores que el local con punto y coma, demostrados mediante Decimal exacto y texto en todos los campos. Hay 10.369 diferencias numéricas de representación equivalentes, como `4.0` frente a `4`; el publicador no queda acreditado como investigador o recolector. Las huellas y método se documentan en [PROCEDENCIA_DATASET.md](PROCEDENCIA_DATASET.md).

Las tres correcciones de publicación son High/horas IA **15,22 → 15,21**, Medium/dependencia **3,37 → 3,36**, Low/GPA final **3,41 → 3,40**. Se verificaron las 18 medias por grupo, las estadísticas generales, correlaciones Pearson históricas, contraste Spearman y distribución de clases mediante Fase 2. El KPI no cambió: **24,974 %**, aproximadamente 24,97 %. El grupo High tiene más horas promedio de IA que Low; es una asociación retrospectiva del dataset, no una causa ni una capacidad predictiva demostrada.

Permanecen pendientes fecha original de descarga, recolección y muestreo acreditados, instrumentos y momentos de medición. La descripción, metadatos y ZIP de versión 1 no documentan fórmula/umbrales de etiqueta ni confirman un origen sintético. Esto limita la interpretación de una futura clasificación: podría reproducir una regla desconocida. GPA final y retención se incluyen bajo registros completos, sin detección anticipada. No hay interpretación clínica ni generalización institucional acreditada; UNIFRANZ es la institución del equipo.

## Git, copia limpia y HTML

Se construyó un índice temporal del **contenido final previsto**, no una clonación de un commit anterior. Árbol comprobado antes de añadir estos dos informes de auditoría: `37f8eaf1fde0e1833c7ae96c66a895ba4d5e93f3`; **28 archivos**, sin `.venv`, cachés, `.git` ni archivos privados. Cada blob canónico y cada archivo exportado coincidieron byte a byte con los archivos de trabajo. La política LF funciona aun con `core.autocrlf=true`; se corrigió también su efecto sobre `.gitignore` y `.gitattributes`. La operación temporal conservó intacto el índice real. Los dos informes se generaron después de la prueba y no alteran sus 28 archivos ni las referencias del manifiesto.

`.venv` quedó fuera del índice (26.595 retirados) y sigue físicamente disponible. No quedaron archivos ignorados versionados; dataset, notebooks, documentos y artefactos se conservaron. Los cambios quedan para revisión, sin publicación remota.

Node **22.12.0** verificó el JavaScript real con DOM y Chart simulados: carga de 50.000 filas/16 columnas, clases y KPI correctos, cuatro gráficos con datos finitos, recarga LF/CRLF, rechazo de otro contenido y navegación de tres diapositivas. El reporte identifica el mismo CSV mediante SHA-256 y evita pérdida silenciosa de filas. Los enlaces locales se comprobaron y no se encontraron enlaces rotos.

**Pendiente visual:** no se encontró navegador disponible en las ubicaciones habituales comprobadas. No se acredita renderizado CSS, canvas ni carga real de CDN. El reporte HTML necesita conexión para sus bibliotecas externas. La revisión visual de los gráficos de notebooks sí se realizó.

## Archivos y reproducción

Archivos modificados o creados (además de la retirada del entorno del índice):

- `README.md`
- `docs/DICCIONARIO_DATOS.md`
- `docs/ENTORNO_PROYECTO.md`
- `docs/INFORMACION_GENERAL_PROYECTO_EDUANALYTICS.md`
- `notebook_eduanalytics_md.ipynb`
- `presentacion_eduanalytics.html`
- `reportes_analisis_dataset_principal.html`
- `requirements.txt`
- `wrangler/01_ENTENDIMIENTO_NEGOCIO/01_entendimiento_negocio.ipynb`
- `wrangler/02_COMPRENSION_DATOS/02_comprension_datos_eda.ipynb`
- `wrangler/03_PREPARACION_DATOS/03_preparacion_datos.ipynb`
- `wrangler/03_PREPARACION_DATOS/artefactos/INSTRUCCIONES_FASE4.md`
- `wrangler/03_PREPARACION_DATOS/artefactos/decisiones_limpieza.csv`
- `wrangler/03_PREPARACION_DATOS/artefactos/manifest.json`
- `wrangler/03_PREPARACION_DATOS/artefactos/preprocesamiento.py`
- `wrangler/03_PREPARACION_DATOS/artefactos/requirements_preparacion.txt`
- `.gitattributes`
- `.gitignore`
- `docs/PROCEDENCIA_DATASET.md`
- `docs/VERIFICACION_FASES_1_2_3.json`
- `docs/VERIFICACION_FASES_1_2_3.md`
- `requirements-lock.txt`
- `tools/verificar_html.js`
- `tools/verificar_proyecto.py`

Los CSV de entrada y particiones se conservan; la normalización del CSV local coincide con los bytes LF ya publicados en Git. `.vscode/settings.json` se preservó. Los respaldos, ruedas y entornos de comprobación se encuentran únicamente en `.cache/`, excluida de Git.

Desde un entorno nuevo con Python 3.10.6:

```powershell
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements.txt
.venv/Scripts/python.exe -m pip check
.venv/Scripts/python.exe tools/verificar_proyecto.py
.venv/Scripts/python.exe tools/verificar_proyecto.py --ejecutar --desde raiz
.venv/Scripts/python.exe tools/verificar_proyecto.py --ejecutar --desde carpetas
node tools/verificar_html.js
```

Usar la selección de kernel y carga detalladas en [ENTORNO_PROYECTO.md](ENTORNO_PROYECTO.md) e `INSTRUCCIONES_FASE4.md`. Las entradas están preparadas para Fase 4 de clasificación retrospectiva con las limitaciones indicadas. La selección, entrenamiento y evaluación de modelos quedan pendientes de esa fase.
