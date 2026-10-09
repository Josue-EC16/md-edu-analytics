# Fase 4 · Modelado EduAnalytics

Flujo principal de clasificación multiclase retrospectiva, posterior a las Fases 1–3 verificadas. Usa las particiones originales: 35.000 entrenamiento, 7.500 validación y 7.500 prueba; 14 predictores principales y un escenario de sensibilidad de 12. El KPI 24,974 % High describe etiquetas, no desempeño predictivo. Fase 5 permanece pendiente.

## Entorno y ejecución

Python **3.10.6**, scikit-learn **1.7.2** y las versiones de `requirements.txt`/`requirements-lock.txt` de la raíz. No se añadieron dependencias: joblib y threadpoolctl ya están fijadas en el lock. Instalar con `python -m venv .venv`, `.venv/Scripts/python.exe -m pip install -r requirements.txt` y comprobar `pip check`. Conservar entornos existentes; seleccionar ese intérprete como kernel. En Linux, el ejecutable equivalente es `.venv/bin/python`; la verificación realizada corresponde a Windows.

Desde la raíz del repositorio:

```powershell
.venv/Scripts/python.exe tools/ejecutar_modelado.py preparar
.venv/Scripts/python.exe tools/ejecutar_modelado.py entrenar --escenario ambos
.venv/Scripts/python.exe tools/ejecutar_modelado.py comparar
.venv/Scripts/python.exe tools/ejecutar_modelado.py finalizar
.venv/Scripts/python.exe tools/ejecutar_modelado.py verificar
.venv/Scripts/python.exe tools/ejecutar_modelado.py notebooks --incluir-prueba --desde raiz
.venv/Scripts/python.exe tools/ejecutar_modelado.py notebooks --incluir-prueba --desde carpetas
.venv/Scripts/python.exe tools/ejecutar_modelado.py informe
.venv/Scripts/python.exe tools/verificar_modelado.py --copia-limpia --manifest
```

Desde `wrangler/04_MODELADO`, usar el mismo intérprete con las rutas `../../.venv/Scripts/python.exe ../../tools/ejecutar_modelado.py ...`. También se admite ejecutar cada notebook desde raíz o su propia carpeta con Restart Kernel and Run All. El orden es 00 → 01 → 02 → 03 → 04 → 05 → 06. El notebook 06 requiere selección congelada; la ejecución automática lo omite si no se indica `--incluir-prueba`.

Entrenar una familia: `entrenar --modelo logistica --escenario principal` (opciones adicionales: arbol, random_forest, dummy; reducido o ambos). El código compartido ejecuta los mismos pasos desde notebooks y consola. Los notebook muestran preprocesamiento, espacios, búsquedas completas, métricas, figuras e interpretación calculada.

## Protocolo y resultados

Antes de calcular resultados se guarda `artefactos/<id>/protocolo.json`, con espacios y combinaciones efectivas, versiones, huellas y reglas. `pliegues.csv` conserva posiciones de entrenamiento, identificadores y pliegue; su SHA-256 es estricto. Cinco pliegues estratificados, mezcla y semilla 42. Mismas configuraciones para ambos escenarios. Búsquedas completas: 10 logística, 16 árbol, 12 bosque. Total inicial: 393 ajustes, incluidos Dummy y modelo final. Un trabajo de ajuste y un hilo numérico evitan paralelismo anidado.

Se selecciona entre los tres candidatos principales por Macro F1 de validación. Empate absoluto hasta 1e-12: Recall de High, simplicidad logística→árbol→bosque y coste estructural. Los tiempos complementan la comparación, sin decidir empates por fluctuaciones del equipo. Dummy sirve como referencia: si el ganador no lo supera, se informa falta de mejora. La media CV selecciona hiperparámetros; no es evaluación independiente. La DE entre pliegues no es un intervalo de confianza.

`seleccion_modelo.json` se congela y su recibo precede la carga de etiquetas de prueba. El pipeline nuevo ganador se reajusta con entrenamiento+validación, 42.500 registros, y después evalúa prueba. Ningún resultado de prueba cambia la selección. La carga ordinaria de prueba está bloqueada en el paquete de Fase 4. Los controles de integridad pueden calcular su hash sin usar sus etiquetas para decidir.

La API de scoring 1.7.2 exige una etiqueta textual válida en la respuesta del estimador: el scorer declara `pos_label="High"`. En el promedio macro este parámetro se ignora, como indica su aviso; se mantienen las tres clases explícitas y el valor coincide con el cálculo directo de F1 macro. Los avisos no indican una evaluación binaria ni un fallo de convergencia. Los fallos reales y ConvergenceWarning detienen ajustes.

## Archivos y reutilización

`artefactos/experimento_actual.json` apunta a un experimento identificado por hashes de entradas, código de entrenamiento, configuración y versiones. Dentro de cada experimento:

- `principal/<modelo>/` y `reducido/<modelo>/`: búsqueda completa, resultados, predicciones de validación, metadatos de ejecución y recibo de integridad; coeficientes o importancias/reglas según algoritmo.
- `comparacion.csv`, `sensibilidad.csv`, selección y recibo congelado.
- `final/`: pipeline completo comprimido, predicciones/probabilidades de prueba, métricas, metadatos y recibo.
- `verificacion.json`, evidencias de ejecución de notebooks y `manifest.json`, sin autorreferencias.
- `publicacion/`: copia de código, notebooks y documentos de esa identidad; conserva la evidencia cuando una nueva identidad actualiza la vista principal.
- Figuras en `figuras/<id>/`; reporte consolidado en `INFORME_FASE4_MODELADO.md`.

Se versionan esos resultados, notebooks, código, documentos y pipeline final. Las cachés de pipelines candidatos quedan en `.cache/modelado/<id>/` y se ignoran; no son entradas de CV ni una dependencia para mostrar resultados guardados. El pequeño árbol exportado permite dibujar su estructura sin dichas cachés. Los archivos de texto usan UTF-8/LF y los joblib son binarios.

Las repeticiones comprueban recibos y reutilizan resultados; no vuelven a buscar hiperparámetros. Cambiar entradas, protocolo o código de entrenamiento produce otro identificador. Una selección congelada y la evidencia de prueba no se sobrescriben. Si se interrumpe una evaluación después de comenzar prueba, el flujo falla explícitamente para conservar evidencia.

El control `--copia-limpia` exporta los archivos actuales destinados a Git, comprueba los filtros reales de finales de línea y ejecuta verificación y siete notebooks sin copiar entornos ni cachés. Usa el intérprete verificado que lo lanza. No clona un commit antiguo ni modifica el índice; conserva la evidencia en `copia_limpia.json`. `--manifest` actualiza las huellas después de los controles.

Para reproducir exclusivamente el mismo entrenamiento final congelado, tras una evaluación completa:

```powershell
.venv/Scripts/python.exe tools/ejecutar_modelado.py reproducir-final
```

Esta operación hace un ajuste adicional, conserva el modelo original y comprueba sus métricas y predicciones; no forma parte de los 393 ajustes iniciales. El verificador ordinario carga el modelo en un proceso nuevo sin volver a entrenarlo.

## Cargar el modelo final

Ejemplo desde raíz (en otro directorio, resolver primero la raíz):

```python
from pathlib import Path
import sys
import joblib
ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / "wrangler/04_MODELADO"))
from eduanalytics_modelado import core
directory = core.experimento_actual()
core._seleccion_valida(directory)
core._verificar_recibo(directory / "final")
pipeline = joblib.load(directory / "final/pipeline_final.joblib")
X, y, trace = core.cargar("validation")
predicciones = pipeline.predict(X)
probabilidades = pipeline.predict_proba(X)
orden_probabilidades = pipeline.classes_
```

Cargar solamente artefactos propios/verificados: joblib usa persistencia de objetos Python. Mantener las versiones documentadas. Las columnas de probabilidad se obtienen desde `classes_`; no asumir el orden Low, Medium, High. Las probabilidades estiman etiquetas y no acreditan calibración clínica.

## Límites y referencias

GPA final y retención son retrospectivos. Excluirlos en sensibilidad no acredita disponibilidad anticipada de los demás campos. La fórmula de burnout y el origen sintético no están confirmados. Fase 2 exploró todo el CSV: prueba es interna reservada, no una cohorte externa nunca inspeccionada. Un desempeño alto puede reflejar reglas desconocidas de construcción de la etiqueta. No demuestra causalidad, utilidad clínica, representatividad institucional ni reducción del KPI.

[CV](https://scikit-learn.org/1.7/modules/cross_validation.html), [métricas](https://scikit-learn.org/1.7/modules/model_evaluation.html), [logística](https://scikit-learn.org/1.7/modules/generated/sklearn.linear_model.LogisticRegression.html), [árbol](https://scikit-learn.org/1.7/modules/generated/sklearn.tree.DecisionTreeClassifier.html), [bosque](https://scikit-learn.org/1.7/modules/generated/sklearn.ensemble.RandomForestClassifier.html), [permutación](https://scikit-learn.org/1.7/modules/permutation_importance.html), [persistencia](https://scikit-learn.org/1.7/model_persistence.html).
