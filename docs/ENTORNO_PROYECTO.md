# Entorno reproducible de EduAnalytics

## Python y dependencias

Usar **Python 3.10.6**. Confirmar `python --version` antes de crear el entorno; otra versión no acredita la verificación solicitada. Desde la raíz de una copia nueva:

```powershell
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements.txt
.venv/Scripts/python.exe -m pip check
```

En Linux/macOS el ejecutable del entorno es `.venv/bin/python`. La instalación y verificación de cierre se realizan con Python 3.10.6 en Windows; no se atribuye una prueba a otros sistemas operativos. El entorno local no se versiona. No eliminar ni reemplazar un entorno existente para verificar: crear uno nuevo en un directorio temporal.

El archivo principal fija las dependencias directas de los cuatro notebooks y de su ejecución automática. `requirements-lock.txt` fija las 66 dependencias resueltas del entorno nuevo y se aplica como archivo de restricciones; no procede de `.venv`. `wrangler/03_PREPARACION_DATOS/artefactos/requirements_preparacion.txt` referencia ese mismo archivo principal, evitando versiones divergentes. `statsmodels` no se importa en estos notebooks y se retiró de los requisitos; regresión y clustering son propuestas secundarias.

## Selección del kernel y ejecución

En VS Code seleccionar el intérprete `.venv/Scripts/python.exe` y el kernel de ese entorno. Para Jupyter con un kernel nombrado, usar `.venv/Scripts/python.exe -m ipykernel install --user --name eduanalytics-py3106 --display-name "EduAnalytics Python 3.10.6"`. Seleccionar ese kernel; no reutilizar variables de una sesión anterior.

La secuencia principal es:

1. `wrangler/01_ENTENDIMIENTO_NEGOCIO/01_entendimiento_negocio.ipynb`.
2. `wrangler/02_COMPRENSION_DATOS/02_comprension_datos_eda.ipynb`.
3. `wrangler/03_PREPARACION_DATOS/03_preparacion_datos.ipynb`.

Después ejecutar el análisis complementario `notebook_eduanalytics_md.ipynb`. No hay clasificadores ejecutados en estas fases. El notebook complementario también puede ejecutarse desde cualquiera de las carpetas de fases: resuelve la raíz buscando README y docs entre los padres del directorio actual.

Todos leen `dataset/ai_student_impact_dataset (1).csv` con `sep=';'`, UTF-8 compatible con BOM y rutas relativas. Los notebooks de wrangler funcionan desde la raíz o su propia carpeta. Ejecutar **Restart Kernel and Run All** y guardar las salidas. Para ejecución automática se dispone de nbclient/nbconvert; seleccionar explícitamente el intérprete 3.10.6 que lanza el kernel.

## Finales de línea e integridad

`.gitattributes` fija LF para CSV, notebooks, código y documentación. Las huellas SHA-256 se calculan sobre bytes definitivos, sin tolerar diferencias en silencio. Guardar notebooks explícitamente con LF. Si cambian datos o documentación, ejecutar de nuevo las fases en orden: Fase 3 depende de las huellas guardadas de Fases 1–2 y regenera el manifiesto.

No modificar un notebook previo después de generar el manifiesto sin repetir Fase 3. La pertenencia actual de las particiones está congelada mediante huellas de identificadores; regenerar no autoriza cambiar muestras.

## Materiales HTML

La presentación es HTML local con navegación por botones/teclado. El reporte permite cargar el mismo CSV y calcula sus resúmenes en navegador. El reporte utiliza CDN de Chart.js, Tailwind y fuentes: necesita conexión para esos recursos. Esa dependencia visual es independiente de la ejecución local de los notebooks.

El reporte de cierre en `VERIFICACION_FASES_1_2_3.md` distingue controles ejecutados y verificaciones pendientes, incluida la presentación en navegador cuando no está disponible.

## Verificación ejecutable

```powershell
.venv/Scripts/python.exe tools/verificar_proyecto.py
.venv/Scripts/python.exe tools/verificar_proyecto.py --ejecutar --desde raiz
.venv/Scripts/python.exe tools/verificar_proyecto.py --ejecutar --desde carpetas
```

El verificador comprueba archivos y salidas guardadas; con `--ejecutar` inicia un kernel limpio por notebook y guarda las salidas en LF, en orden. Las copias diagnósticas de preprocesadores se ajustan solo con entrenamiento y se descartan. No se entrenan clasificadores. Las huellas de prueba se revisan solo para integridad.

Para verificar la lógica de los HTML sin navegador: `node tools/verificar_html.js` (Node 22.12.0 comprobado). Esta prueba simula DOM y Chart; no acredita diseño visual ni carga real de CDN.
