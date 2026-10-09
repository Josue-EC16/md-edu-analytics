"""Genera la estructura académica de Fase 4; no ejecuta experimentos."""
from pathlib import Path
import nbformat as nb

ROOT=Path(__file__).resolve().parents[1]
FOLDER=ROOT/'wrangler/04_MODELADO'
BOOT='''from pathlib import Path
import sys
ROOT = next(p for p in [Path.cwd(), *Path.cwd().parents]
            if (p / "wrangler/03_PREPARACION_DATOS/artefactos/manifest.json").is_file())
sys.path.insert(0, str(ROOT / "wrangler/04_MODELADO"))
from eduanalytics_modelado import core
from eduanalytics_modelado.academico import texto, metricas, matrices, presentar_modelo, presentar_comparacion
import pandas as pd
from IPython.display import display
entradas = core.verificar_entradas()
print("Python:", core.versiones()["Python"], "scikit-learn:", core.versiones()["scikit-learn"])
print("CSV:", entradas["input"]["path"], "SHA-256:", entradas["input"]["sha256"])
'''
AUTHORS='''**Universidad:** UNIFRANZ — **Materia:** Minería de Datos.

**Integrantes:** Milenka Melody Chuquimia Osco; Edson Teddy Tito Chuquimia; Carlos Daniel Valverde Mendoza; Alvaro Luis Carlos del Carpio Blanco; Marcelo Josue Escobar Chipana.

Clasificación retrospectiva de registros completos. La población corresponde a los estudiantes universitarios representados en el CSV. La etiqueta no es un diagnóstico clínico. No se demuestra causalidad, representatividad institucional ni detección anticipada. El KPI descriptivo es 24,974 % de etiquetas High; no mide calidad predictiva.
'''


def md(s): return nb.v4.new_markdown_cell(s)
def code(s): return nb.v4.new_code_cell(s)
def save(name,cells):
    book=nb.v4.new_notebook(cells=cells,metadata={'kernelspec':{'display_name':'EduAnalytics Python 3.10.6','language':'python','name':'python3'},
        'language_info':{'name':'python','version':'3.10.6'}})
    for i,c in enumerate(book.cells): c.id=f'fase4-{name[:2]}-{i:02d}'
    (FOLDER/name).write_text(nb.writes(book)+'\n',encoding='utf-8',newline='\n')


def main():
    save('00_diseno_experimental_y_linea_base.ipynb',[
        md('# Fase 4 · Diseño experimental y línea base\n\n'+AUTHORS),
        md('## Problema, objetivo y protocolo previo\n\nPredecir `Burnout_Risk_Level` (Low, Medium, High), con especial atención a High. Es clasificación multiclase: '
           'el objetivo es categórico y los códigos no representan distancias. Los 14 predictores y las particiones congeladas se heredan de Fase 3. '
           'No se vuelven a dividir, limpiar ni transformar previamente. El protocolo se guarda antes de obtener resultados.'),
        code(BOOT+'directory = core.preparar()\nconfig = core.leer(directory / "protocolo.json")\nprint("Experimento:", directory.name)\nprint("Protocolo SHA-256:", core.sha(directory / "protocolo.json"))'),
        md('## Datos y particiones\n\nEntrenamiento 35.000; validación 7.500; prueba 7.500. Los conteos de prueba siguientes proceden del manifiesto previo. '
           'Las etiquetas de prueba no se cargan aquí para evaluar candidatos. Student_ID, _row_id y objetivo quedan fuera de X. GPA final y retención se incluyen bajo el alcance retrospectivo.'),
        code('display(pd.DataFrame([{ "partición": n, "registros": v["rows"], **v["class_counts"] } for n,v in entradas["partitions"].items()]))\n'
             'X, y, trace = core.cargar("train")\nprint("X:", X.shape, "y:", y.shape)\ndisplay(pd.DataFrame({"predictor": X.columns, "tipo": X.dtypes.astype(str).values}))'),
        md('## Pliegues, algoritmos y búsqueda\n\n`StratifiedKFold(n_splits=5, shuffle=True, random_state=42)` compartido por todas las familias y escenarios. '
           'Cada pipeline ajusta escalado/categorías dentro del pliegue; logística usa L2 multinomial, árbol reglas y bosque interacciones mediante un conjunto de árboles. '
           'La logística evalúa 10 configuraciones; árbol 16 aleatorias; bosque 12 aleatorias. Semilla 42 y mismas combinaciones en sensibilidad. '
           'Ejecución secuencial, un hilo: 380 ajustes CV, 6 reajustes de candidatos, 6 de Dummy y uno final, total 393.'),
        code('folds = core._pliegues(directory)\nf = pd.read_csv(directory / "pliegues.csv", sep=";")\ndisplay(pd.crosstab(f.fold, f.label).reindex(columns=core.CLASES))\ndisplay(f.head())\n'
             'print("Huella pliegues:", core.sha(directory / "pliegues.csv"))\ndisplay(config["spaces"])\ndisplay(config["configurations"])'),
        md('## Métricas y selección predefinida\n\nMacro F1 es principal; Accuracy complementa. Se informa Precision/Recall/F1/Support por clase, especialmente High. '
           'Cada F1 combina precisión y recall; Macro F1 promedia las tres clases con el mismo peso, independientemente de su soporte. '
           'Accuracy es la proporción total de aciertos; puede ocultar errores de clases menos frecuentes. '
           'Los hiperparámetros se eligen por media CV de entrenamiento; esa media no es una evaluación independiente y la DE no es un intervalo de confianza. '
           'La selección entre tres candidatos del escenario principal usa mayor Macro F1 de validación; empates hasta 1e-12 se resuelven con Recall de High y simplicidad '
           '(logística, árbol, bosque). Se contrastará con Dummy. La sensibilidad no cambia el escenario final. '
           'Después de congelar selección se reajusta un pipeline nuevo con entrenamiento+validación (42.500) y luego se consulta prueba. No se retoca tras prueba.\n\n'+
           r'$$\mathrm{Macro\ F1}=\frac{F1_{Low}+F1_{Medium}+F1_{High}}{3}$$'+ '\n\n'+
           r'$$P_{High}=\frac{TP_{High}}{TP_{High}+FP_{High}},\qquad R_{High}=\frac{TP_{High}}{TP_{High}+FN_{High}}$$'),
        code('display(config["selection"])\ndisplay(config["versions"])\ndisplay(config["fit_budget"])'),
        md('## Línea base real\n\n`DummyClassifier(strategy="most_frequent")` aprende la clase mayoritaria de entrenamiento. '
           'Se ajusta con los mismos cinco pliegues y se evalúa en entrenamiento y validación. Sirve para comprobar cuánto aportan los predictores.'),
        code('baseline = core.entrenar("dummy", directory=directory)\npresentar_modelo("dummy", directory=directory)'),
        md('## Límites y referencias\n\nPosible circularidad con la etiqueta de fórmula desconocida; origen sintético no confirmado. '
           'Fase 2 exploró todo el CSV: prueba es interna y reservada, no una cohorte externa nunca inspeccionada. '
           '[Validación cruzada](https://scikit-learn.org/1.7/modules/cross_validation.html) y '
           '[métricas](https://scikit-learn.org/1.7/modules/model_evaluation.html).')])

    descriptions={
        'logistica': ('01_regresion_logistica.ipynb','Regresión logística multinomial',
            'Hipótesis: una frontera multinomial regularizada ofrece una referencia útil e interpretable. Optimiza una pérdida logística conjunta y probabilidades para tres clases. '
            'L2 controla magnitudes; C invierte la fuerza de regularización. No exige normalidad de predictores; sí limita la forma de la frontera en el espacio transformado. '
            'Supone registros independientes para la interpretación usual; la muestra no acredita generalización externa.',
            'La fábrica "logistica" estandariza ocho numéricas, convierte booleanos a 0/1 y aplica one-hot a cinco categóricas. '
            'solver lbfgs, L2, max_iter 5000, tol 1e-4. C: 0.01, 0.1, 1, 10, 100; pesos None/balanced. '
            'No se establece multi_class, obsoleto en 1.7.2. Se verifica convergencia y se detiene ante ConvergenceWarning.'),
        'arbol': ('02_arbol_decision.ipynb','Árbol de decisión',
            'Hipótesis: reglas no lineales e interacciones pueden mejorar la referencia lineal. CART divide recursivamente por reducción de Gini. '
            'No presupone fronteras lineales ni requiere escalado. Profundidad, hojas, divisiones y poda controlan complejidad. '
            'Es sensible a cambios en datos y puede sobreajustar; pesos modifican proporciones e impureza.',
            'La fábrica "arbol" conserva numéricas sin escalado y aplica one-hot nominal/booleanos. '
            'max_depth 3,5,8,12,None; min_samples_leaf 1,10,50,100; min_samples_split 2,10,50; ccp_alpha 0,0.0001,0.001; pesos None/balanced. '
            'Se evalúan 16 combinaciones aleatorias reproducibles. Gini mide mezcla de etiquetas; no es una escala clínica.'),
        'random_forest': ('03_random_forest.ipynb','Random Forest',
            'Hipótesis: agregar árboles bootstrap y subconjuntos de variables puede representar interacciones y reducir variabilidad respecto de un árbol. '
            'Promedia probabilidades de árboles; puede sobreajustar y exige más recursos. Las importancias agregadas no describen una regla única ni relaciones causales.',
            'Reutiliza la fábrica "arbol", sin escalado. n_estimators 150/300; max_depth 8/16/None; min_samples_leaf 1/5/20; '
            'max_features sqrt/0.5; pesos None/balanced. Se evalúan 12 configuraciones reproducibles y n_jobs=1 evita paralelismo anidado.')}
    for model,(name,title,hypothesis,settings) in descriptions.items():
        url={'logistica':'linear_model.LogisticRegression','arbol':'tree.DecisionTreeClassifier','random_forest':'ensemble.RandomForestClassifier'}[model]
        save(name,[md(f'# Fase 4 · {title}\n\n'+AUTHORS),md('## Objetivo, hipótesis, algoritmo y límites\n\n'+hypothesis),
            code(BOOT+'directory = core.experimento_actual()\nX, y, trace = core.cargar("train")\nXv, yv, tracev = core.cargar("validation")\n'
                 'print("Entrenamiento", X.shape, "Validación", Xv.shape)\nassert X.index.equals(y.index)\nassert not {"Student_ID", "_row_id", "Burnout_Risk_Level"} & set(X.columns)'),
            md('## Preprocesamiento y configuración inicial\n\n'+settings+' Cada búsqueda recibe un pipeline nuevo, sin ajustar. '
               'Balanced se calcula dentro de cada ajuste, no antes de dividir. No se usa SMOTE, imputación ni recortes. Las desconocidas generan bloques one-hot de ceros.'),
            code(f'pipeline = core.crear_pipeline("{model}")\ndisplay(pipeline)\ndisplay(core.ESPACIOS["{model}"])'),
            md('## Búsqueda, resultados y explicación\n\nEl código compartido ejecuta o verifica la búsqueda completa, guarda parámetros de todas las configuraciones '
               'y evalúa el ganador en entrenamiento y validación. Las tablas y comentarios siguientes proceden de esos cálculos. '
               'La ejecución repetida reutiliza recibos válidos, sin ejecutar nuevamente la búsqueda.'),
            code(f'resultado = core.entrenar("{model}", directory=directory)\npresentar_modelo("{model}", directory=directory)'),
            md(f'## Referencia y cierre\n\n[API scikit-learn 1.7.2](https://scikit-learn.org/1.7/modules/generated/sklearn.{url}.html). '
               'La comparación definitiva se realiza en el notebook 05 y la prueba en el 06. Una métrica alta describe concordancia con etiquetas disponibles; '
               'no descubre su fórmula original ni acredita un resultado de negocio.')])

    save('04_analisis_sensibilidad.ipynb',[
        md('# Fase 4 · Análisis de sensibilidad\n\n'+AUTHORS),
        md('## Objetivo y diseño comparable\n\nComparar los tres clasificadores retirando Post_Semester_GPA y Skill_Retention_Score. '
           'Se mantienen filas, orden, pliegues, espacios, combinaciones y presupuestos. Se adapta un preprocesador nuevo dentro de Fase 4, sin editar Fase 3. '
           'Este escenario de 12 predictores no participa en la selección principal. No demuestra detección anticipada: otros campos también tienen tiempos de medición desconocidos.'),
        code(BOOT+'directory = core.experimento_actual()\nX, y, trace = core.cargar("train", "reducido")\nprint("Escenario reducido:", X.shape)\ndisplay(list(X.columns))\ndisplay(core.crear_pipeline("logistica", "reducido"))'),
        md('## Ejecución de los tres experimentos reducidos\n\nCada búsqueda recibe un pipeline completo; escalado y categorías se aprenden dentro de CV. '
           'La mejora o caída respecto del principal no prueba que esas dos variables formen parte de la construcción de la etiqueta.'),
        code('for modelo in core.MODELOS:\n    core.entrenar(modelo, "reducido", directory)\npresentar_comparacion(directory, sensibilidad=True)'),
        md('## Resultados detallados por familia\n\nSe incluyen búsquedas, matrices, métricas, brechas e interpretación del escenario reducido.'),
        code('for modelo in core.MODELOS:\n    presentar_modelo(modelo, "reducido", directory)'),
        md('## Límite del contraste\n\nUna caída pequeña no elimina circularidad; una caída grande tampoco identifica la fórmula de burnout. '
           'No se cambia el protocolo principal ni se usan resultados de prueba.')])
    save('05_comparacion_y_seleccion.ipynb',[
        md('# Fase 4 · Comparación y selección\n\n'+AUTHORS),
        md('## Regla y entradas verificadas\n\nConsumir los resultados de seis búsquedas y la línea base. Seleccionar entre los tres modelos con 14 predictores '
           'por Macro F1 de validación, Recall de High en empate y simplicidad logística→árbol→bosque. La DE de CV no es un intervalo de confianza. '
           'Los tiempos y la interpretabilidad complementan el criterio; no se utilizan resultados de prueba.'),
        code(BOOT+'directory = core.experimento_actual()\nselection = core.comparar(directory)\npresentar_comparacion(directory)'),
        md('## Congelación antes de prueba\n\nSe guardan ganador, predictores, parámetros, métricas CV/validación, semillas, versiones y hashes de código, '
           'entradas y pliegues. Una selección congelada no se sobrescribe. El modelo final usará un pipeline nuevo con entrenamiento y validación.'),
        code('display(selection)\nprint("Selección SHA-256:", core.sha(directory / "seleccion_modelo.json"))\ndisplay(core.leer(directory / "seleccion_congelada.json"))'),
        md('## Traspaso\n\nEl siguiente notebook realiza la evaluación técnica final. Un resultado de prueba inferior se informará conservando selección. '
           'No equivale a completar la evaluación de negocio de Fase 5.')])
    save('06_modelo_final_y_prueba.ipynb',[
        md('# Fase 4 · Modelo final y prueba reservada\n\n'+AUTHORS),
        md('## Condición de entrada y procedimiento congelado\n\nEste notebook requiere selección válida. Crea un pipeline nuevo con hiperparámetros ganadores y '
           '14 predictores, aprende preprocesamiento y clasificador con 42.500 registros y después carga prueba. '
           'Las ejecuciones posteriores verifican y muestran resultados guardados. No se seleccionan otros modelos ni parámetros tras prueba.'),
        code(BOOT+'directory = core.experimento_actual()\nselection = core._seleccion_valida(directory)\ndisplay(selection["final_training"])\nfinal = core.finalizar(directory)'),
        md('## Resultados finales reales\n\nEl modelo final se entrenó con más registros que los candidatos comparados en validación. '
           'Prueba evalúa el modelo congelado, no sirve para escoger candidatos. Las probabilidades estiman etiquetas y no representan calibración clínica.'),
        code('metricas(final, "test")\nmatrices(final["test"], directory, "final_prueba_confusion", "Modelo final: prueba reservada")\n'
             'display(core.leer(directory / "final/ejecucion.json"))\n'
             'pred = pd.read_csv(directory / "final/predicciones_prueba.csv", sep=";")\ndisplay(pred.head())\ndisplay(final)'),
        md('## Persistencia y comprobación independiente\n\nEl archivo joblib contiene el pipeline completo. El verificador inicia un proceso nuevo, carga el modelo '
           'y reproduce todas las etiquetas y probabilidades de prueba. Los hashes y controles constan en la evidencia generada.'),
        code('from eduanalytics_modelado.verificacion import verificar\nevidencia = verificar(directory)\ndisplay(evidencia)\n'
             'from eduanalytics_modelado.academico import generar_informe\nprint(generar_informe(directory).relative_to(ROOT))'),
        md('## Límites y Fase 5 pendiente\n\nFase 2 exploró el CSV completo; prueba es una partición interna reservada, no una cohorte externa nunca inspeccionada. '
           'Un alto rendimiento puede reflejar reglas desconocidas de la etiqueta. No demuestra causalidad, utilidad clínica, origen sintético ni detección anticipada. '
           'No demuestra reducir el KPI de etiquetas High. La evaluación de negocio y decisiones institucionales corresponden a Fase 5.')])


if __name__=='__main__': main()
