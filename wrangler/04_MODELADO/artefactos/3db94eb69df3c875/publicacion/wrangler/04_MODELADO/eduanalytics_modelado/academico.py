"""Tablas, figuras y explicaciones a partir de artefactos verificables."""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree
import joblib
from IPython.display import display, Markdown
from . import core

NOMBRES = {'dummy': 'Línea base mayoritaria', 'logistica': 'Regresión logística',
           'arbol': 'Árbol de decisión', 'random_forest': 'Random Forest'}


def texto(s):
    display(Markdown(s))


def guardar(fig, directory, nombre):
    folder = core.FASE / 'figuras' / directory.name
    folder.mkdir(parents=True, exist_ok=True)
    fig.savefig(folder / f'{nombre}.png', dpi=140, bbox_inches='tight',
                metadata={'Software': 'EduAnalytics Fase 4'})
    plt.show()
    plt.close(fig)


def metricas(result, split='validation'):
    m = result[split]
    frame = pd.DataFrame(m['by_class']).T.reindex(core.CLASES)
    display(frame)
    texto(f"Macro F1 = **{m['macro_f1']:.6f}**, Accuracy = **{m['accuracy']:.6f}**. "
          f"High: Precision **{m['by_class']['High']['precision']:.6f}** y Recall "
          f"**{m['by_class']['High']['recall']:.6f}**. El soporte representa registros de cada etiqueta.")
    if frame.precision_undefined.any():
        texto('Las clases marcadas con `precision_undefined=True` no reciben predicciones. '
              'Su precisión es indefinida; el cálculo usa cero mediante `zero_division=0`.')


def matrices(m, directory, nombre, titulo):
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5), constrained_layout=True)
    for ax, key, normalized in zip(axes, ['confusion','confusion_normalized'], [False,True]):
        a = np.asarray(m[key])
        ax.imshow(a, cmap='Blues', vmin=0, vmax=1 if normalized else max(1,a.max()))
        for i in range(3):
            for j in range(3):
                label = f'{a[i,j]:.1%}' if normalized else str(int(a[i,j]))
                ax.text(j,i,label,ha='center',va='center',color='white' if a[i,j] > (0.5 if normalized else a.max()/2) else 'black')
        ax.set(xticks=range(3),yticks=range(3),xticklabels=core.CLASES,yticklabels=core.CLASES,
               xlabel='Predicción',ylabel='Etiqueta real',
               title='Por clase real (%)' if normalized else 'Conteos (registros)')
    fig.suptitle(titulo)
    guardar(fig,directory,nombre)
    cm=np.asarray(m['confusion'])
    texto(f"High→Low: **{cm[2,0]}**; High→Medium: **{cm[2,1]}**. "
          f"Low→High: **{cm[0,2]}**; Medium→High: **{cm[1,2]}**. "
          'Los primeros son falsos negativos de High y los últimos falsos positivos. '
          'La normalización muestra la fracción de cada clase real. Un mayor Recall puede acompañarse '
          'de menor Precision; la matriz permite localizar ese compromiso.')


def presentar_modelo(modelo, escenario='principal', directory=None):
    directory=directory or core.experimento_actual()
    r=core.cargar_resultado(modelo,escenario,directory)
    folder=directory/escenario/modelo
    cv=pd.read_csv(folder/'busqueda_cv.csv',sep=';')
    Xt,_,_=core.cargar('train',escenario);Xv,_,_=core.cargar('validation',escenario)
    unknown={c:int((~Xv[c].isin(Xt[c].unique())).sum()) for c in core.prep.CATEGORICAS}
    texto('### Categorías desconocidas y controles de entrada')
    display(pd.DataFrame({'variable':list(unknown),'registros_desconocidos_validación':list(unknown.values())}))
    texto(f"Se observaron **{sum(unknown.values())} incidencias** de categorías de validación ausentes en entrenamiento. "
          'La política `handle_unknown="ignore"` representa una desconocida mediante ceros; su prueba dirigida utiliza un caso artificial separado.')
    texto('### Búsqueda y configuración seleccionada')
    display(cv if modelo=='dummy' else cv.assign(configuration_index=np.arange(len(cv))).sort_values('rank_test_score').reset_index(drop=True))
    display(pd.DataFrame([{'parámetro':k,'valor':str(v)} for k,v in r['best_params'].items()]))
    texto(f"Se completaron **{r['cv']['configurations']} configuraciones** y **{r['cv']['fits']} ajustes**. "
          f"CV Macro F1 = **{r['cv']['macro_f1_mean']:.6f}**, DE = **{r['cv']['macro_f1_std']:.6f}**. "
          'Esta media selecciona hiperparámetros; no evalúa independientemente al ganador. '
          'La desviación entre cinco pliegues no es un intervalo de confianza.')
    if modelo!='dummy':
        fig,ax=plt.subplots(figsize=(10,4))
        ax.plot(np.arange(len(cv)),cv.mean_test_score,'o-',label='Media CV de validación')
        ax.plot(np.arange(len(cv)),cv.mean_train_score,'x--',label='Media CV de entrenamiento')
        ax.set(title=f'{NOMBRES[modelo]} — {escenario}: configuraciones de búsqueda',
               xlabel='Índice configuration_index (orden original de búsqueda)',ylabel='Macro F1',ylim=(-.02,1.02))
        ax.legend();guardar(fig,directory,f'{escenario}_{modelo}_cv')
        best=int(cv.rank_test_score.idxmin())
        texto(f"La configuración de índice **{best}** obtiene la mejor media CV. "
              'Las curvas muestran ajuste y validación dentro de entrenamiento; el eje no es una escala de complejidad.')
    texto('### Diagnóstico en entrenamiento y comparación en validación fija')
    display(pd.DataFrame([{'partición':s,'Macro F1':r[s]['macro_f1'],'Accuracy':r[s]['accuracy']}
                          for s in ['train','validation']]))
    metricas(r)
    texto(f"Brecha Macro F1 entrenamiento−validación = **{r['overfit_gap']:.6f}**. "
          'Una brecha positiva señala un posible sobreajuste; una brecha pequeña tampoco garantiza generalización externa.')
    matrices(r['validation'],directory,f'{escenario}_{modelo}_confusion',f'{NOMBRES[modelo]} — {escenario}: validación')
    timing=core.leer(folder/'ejecucion.json')
    display(pd.DataFrame([timing]).drop(columns=['candidate_cache_sha256']))
    texto('Los tiempos incluyen el preprocesamiento. Son observaciones de esta ejecución y equipo, no constantes reproducibles.')
    texto('### Interpretabilidad')
    if modelo=='dummy':
        texto(f"La clase mayoritaria aprendida es **{r['interpretation']['majority_class']}**. "
              'Predecirla siempre sirve como referencia mínima: Accuracy puede parecer apreciable '
              'mientras Low y High tienen Recall cero. El KPI 24,974 % describe etiquetas y no este desempeño.')
    elif modelo=='logistica':
        df=pd.read_csv(folder/'coeficientes.csv',sep=';')
        display(df)
        fig,axes=plt.subplots(1,3,figsize=(20,6),constrained_layout=True,sharex=True)
        for ax,c in zip(axes,core.CLASES):
            a=df[df['class']==c].copy();a['abs']=a.coefficient.abs()
            a=a.nlargest(8,'abs').sort_values('coefficient')
            ax.barh(a.feature,a.coefficient,color=['#c75b39' if v<0 else '#287c8e' for v in a.coefficient])
            ax.axvline(0,color='black',lw=.7);ax.set(title=c,xlabel='Coeficiente (escala del logit)')
            ax.tick_params(axis='y',labelsize=7)
        fig.suptitle(f'Coeficientes de mayor magnitud — {escenario}')
        guardar(fig,directory,f'{escenario}_{modelo}_coeficientes')
        texto(f"Convergencia: **{r['interpretation']['converged']}**, iteraciones "
              f"**{r['interpretation']['iterations']}** de máximo 5000. Las numéricas están estandarizadas "
              'dentro del entrenamiento correspondiente. L2 reduce magnitudes; con todas las categorías '
              'one-hot no hay una categoría de referencia eliminada. Los coeficientes forman una decisión conjunta '
              'multinomial y no prueban efectos causales ni una comparación inequívoca aislada.')
    else:
        impurity=pd.read_csv(folder/'importancia_impureza.csv',sep=';')
        perm=pd.read_csv(folder/'importancia_permutacion.csv',sep=';').sort_values('mean')
        display(impurity.sort_values('importance',ascending=False));display(perm)
        fig,axes=plt.subplots(1,2,figsize=(15,6),constrained_layout=True)
        a=impurity.nlargest(10,'importance').sort_values('importance')
        axes[0].barh(a.feature,a.importance);axes[0].set(title='Impureza: 10 mayores',xlabel='Importancia relativa')
        axes[0].tick_params(axis='y',labelsize=7)
        axes[1].barh(perm.feature,perm['mean'],xerr=perm['std'],color='#287c8e')
        axes[1].axvline(0,color='black',lw=.7)
        axes[1].set(title='Permutación: variables originales',xlabel='Disminución de Macro F1 en validación')
        axes[1].tick_params(axis='y',labelsize=8)
        fig.suptitle(f'{NOMBRES[modelo]} — {escenario}: importancia del modelo')
        guardar(fig,directory,f'{escenario}_{modelo}_importancias')
        top=perm.iloc[-1]
        texto(f"Mayor importancia por permutación: **{top.feature}**, caída media **{top['mean']:.6f}**. "
              'Las barras de error son DE de cinco permutaciones, no intervalos de confianza. '
              'Impureza puede favorecer variables con más cortes; predictores correlacionados pueden repartirse '
              'o enmascarar importancia por permutación. Estas medidas describen el modelo, no causalidad ni la fórmula de burnout.')
        info=r['interpretation']
        if modelo=='arbol':
            clf=joblib.load(folder/'arbol_interpretacion.joblib')
            texto(f"Árbol seleccionado: profundidad **{info['depth']}**, **{info['nodes']} nodos** "
                  f"y **{info['leaves']} hojas**. La vista siguiente muestra la raíz y dos niveles descendientes; "
                  'el resto se indica truncado. Las reglas completas están en `reglas.txt` y pertenecen al ganador.')
            fig,ax=plt.subplots(figsize=(24,12))
            plot_tree(clf,max_depth=2,feature_names=info['feature_names'],class_names=list(clf.classes_),
                      filled=True,rounded=True,fontsize=8,ax=ax)
            ax.set_title(f'Árbol seleccionado — {escenario} (vista truncada a profundidad 2)')
            guardar(fig,directory,f'{escenario}_{modelo}_estructura')
            if clf.tree_.feature[0]>=0:
                root=info['feature_names'][clf.tree_.feature[0]]
                texto(f"Raíz: **{root} ≤ {clf.tree_.threshold[0]:.4f}**, Gini **{clf.tree_.impurity[0]:.4f}**, "
                      f"**{clf.tree_.n_node_samples[0]} muestras**. La rama izquierda cumple el umbral; "
                      'la derecha lo supera. `value` y Gini reflejan pesos si se seleccionó `balanced`; '
                      f"el orden real de clases es **{list(clf.classes_)}**. Cada hoja predice la clase de mayor proporción ponderada.")
        else:
            texto(f"Bosque de **{info['trees']} árboles**, **{info['total_nodes']} nodos** en total "
                  f"y profundidad media **{info['mean_depth']:.2f}**. Agrega árboles ajustados sobre muestras "
                  'bootstrap y subconjuntos de variables, pudiendo representar interacciones y reducir '
                  'variabilidad respecto de un árbol individual. Su decisión resulta menos simple de explicar.')
    texto(f"### Conclusión del experimento\nMacro F1 de validación **{r['validation']['macro_f1']:.6f}**; "
          f"Recall de High **{r['validation']['by_class']['High']['recall']:.6f}**. "
          'El resultado corresponde a etiquetas de registros completos de este CSV. Un desempeño alto '
          'podría reflejar reglas desconocidas de construcción de la etiqueta; no acredita detección anticipada ni utilidad clínica.')
    return r


def presentar_comparacion(directory=None, sensibilidad=False):
    directory=directory or core.experimento_actual()
    table=core.tabla_comparacion(directory)
    shown=table.copy()
    complexities=[]
    interpretations=[]
    for model,scenario in zip(shown.model,shown.scenario):
        r=core.cargar_resultado(model,scenario,directory);i=r['interpretation']
        if model=='dummy':
            complexities.append('Clase fija');interpretations.append('Regla mayoritaria')
        elif model=='logistica':
            complexities.append(f"{i['coefficients']} coeficientes")
            interpretations.append('Coeficientes regularizados; frontera conjunta')
        elif model=='arbol':
            complexities.append(f"Profundidad {i['depth']}; {i['nodes']} nodos; {i['leaves']} hojas")
            interpretations.append('Reglas de divisiones y hojas')
        else:
            complexities.append(f"{i['trees']} árboles; {i['total_nodes']} nodos")
            interpretations.append('Conjunto; importancias globales')
    shown['complexity']=complexities;shown['interpretability']=interpretations
    display(shown)
    fig,axes=plt.subplots(1,3,figsize=(16,4),constrained_layout=True)
    for ax,metric,title in zip(axes,['validation_macro_f1','recall_High','precision_High'],['Macro F1','Recall High','Precision High']):
        pivot=table.pivot(index='model',columns='scenario',values=metric)
        pivot.plot.bar(ax=ax,ylim=(0,1.05),rot=20)
        ax.set(title=title,xlabel='Modelo',ylabel='Puntuación en validación');ax.legend(title='Escenario',fontsize=8)
    guardar(fig,directory,'comparacion_sensibilidad' if sensibilidad else 'comparacion_modelos')
    pairs=table[table.model!='dummy'].pivot(index='model',columns='scenario',values=['validation_macro_f1','recall_High','precision_High'])
    delta=pd.DataFrame({m:pairs[m]['reducido']-pairs[m]['principal'] for m in ['validation_macro_f1','recall_High','precision_High']})
    display(delta.rename_axis('modelo'))
    texto('Las diferencias son reducido−principal, sobre las mismas particiones, pliegues, espacios y presupuestos. '
          'Retirar GPA final y retención analiza sensibilidad; no garantiza disponibilidad anticipada de los restantes '
          'campos ni elimina circularidad con una etiqueta de fórmula desconocida. Las figuras tienen la misma escala.')
    if not sensibilidad:
        selection=core.comparar(directory)
        texto(f"Ganador entre los tres candidatos principales: **{NOMBRES[selection['model']]}**, "
              f"Macro F1 **{selection['validation']['macro_f1']:.6f}**, mejora sobre Dummy "
              f"**{selection['improvement_over_dummy']:.6f}**. Se aplicó la regla registrada; "
              'la sensibilidad no cambia el escenario elegido. Precision, errores y costes complementan la decisión.')
        ranked=table[(table.scenario=='principal')&(table.model!='dummy')].sort_values('validation_macro_f1',ascending=False)
        margin=float(ranked.iloc[0].validation_macro_f1-ranked.iloc[1].validation_macro_f1)
        high=selection['validation']['by_class']['High']
        testo=(f"La ventaja sobre el segundo candidato es **{margin:.6f}** en Macro F1. "
               'Esta diferencia numérica no demuestra superioridad estadística. '
               f"El ganador recupera **{high['recall']:.2%}** de los registros High de validación; "
               f"queda **{1-high['recall']:.2%}** sin clasificar como High. "
               'El interés especial en High exige valorar estos errores en Fase 5, sin cambiar la regla después de ver prueba.')
        texto(testo)
        if selection['improvement_over_dummy']<=0:
            texto('**Limitación:** el ganador de candidatos no supera la línea base; no se demuestra utilidad predictiva adicional.')
        for model in ['dummy']+core.MODELOS:
            result=core.cargar_resultado(model,'principal',directory)
            matrices(result['validation'],directory,f'comparacion_{model}_confusion',f'{NOMBRES[model]}: validación principal')
    return table


def tabla_md(df):
    def val(x):
        return f'{x:.6f}' if isinstance(x,(float,np.floating)) else str(x).replace('|','/')
    return '\n'.join(['| '+' | '.join(map(str,df.columns))+' |',
                     '| '+' | '.join(['---']*len(df.columns))+' |']+
                    ['| '+' | '.join(val(x) for x in row)+' |' for row in df.itertuples(index=False,name=None)])


def generar_informe(directory=None):
    directory=directory or core.experimento_actual()
    selection=core._seleccion_valida(directory)
    final=core.finalizar(directory)
    t=core.tabla_comparacion(directory)
    baseline=core.cargar_resultado('dummy',directory=directory)
    compact=t[['model','scenario','cv_macro_f1','cv_std','train_macro_f1','validation_macro_f1',
               'validation_accuracy','precision_High','recall_High','f1_High','gap','search_seconds']]
    byclass=pd.DataFrame(final['test']['by_class']).T.reindex(core.CLASES).reset_index(names='clase')
    m=final['test'];cm=np.asarray(m['confusion'])
    diagnostics=[]
    for name in core.MODELOS:
        r=core.cargar_resultado(name,directory=directory)
        matrix=pd.DataFrame(r['validation']['confusion'],columns=core.CLASES).rename_axis('Real').reset_index()
        matrix['Real']=core.CLASES
        info=r['interpretation']
        if name=='logistica':
            detail=f"Convergencia {info['converged']}; iteraciones {info['iterations']}; {info['coefficients']} coeficientes."
        elif name=='arbol':
            detail=f"Profundidad {info['depth']}; {info['nodes']} nodos; {info['leaves']} hojas."
        else:
            detail=f"{info['trees']} árboles; {info['total_nodes']} nodos; profundidad media {info['mean_depth']:.2f}."
        params=core.canon(r['best_params'])
        diagnostics.append(f"### {NOMBRES[name]}\n\nParámetros: `{params}`. {detail}\n\n"+tabla_md(matrix)+
            f"\n\nBrecha entrenamiento−validación {r['overfit_gap']:.6f}. High→Low {matrix.iloc[2]['Low']}; "
            f"High→Medium {matrix.iloc[2]['Medium']}; falsos positivos de High {matrix.iloc[0]['High']+matrix.iloc[1]['High']}. "
            f"[Matrices con normalización](figuras/{directory.name}/principal_{name}_confusion.png).")
    sensitivity=pd.read_csv(directory/'sensibilidad.csv',sep=';')
    sensitivity=sensitivity[['model']+[f'{v}_delta_reducido_menos_principal' for v in
                    ['validation_macro_f1','precision_High','recall_High','gap','search_seconds']]]
    main=t[(t.scenario=='principal')&(t.model!='dummy')].sort_values('validation_macro_f1',ascending=False)
    margin=float(main.iloc[0].validation_macro_f1-main.iloc[1].validation_macro_f1)
    highval=selection['validation']['by_class']['High']
    sections=[f'# Informe Fase 4: Modelado EduAnalytics\n\nExperimento `{directory.name}`. Python 3.10.6; scikit-learn 1.7.2.',
        '## Objetivo y continuidad\n\nClasificación multiclase retrospectiva de `Burnout_Risk_Level` en estudiantes universitarios representados en el CSV. '
        'UNIFRANZ corresponde al equipo. Se preservan 50.000 registros, valores, orden y particiones. '
        'El KPI **24,974 % High** describe etiquetas; las métricas siguientes evalúan predicciones y no demuestran reducirlo.',
        '## Diseño y presupuesto\n\nEntrenamiento 35.000, validación 7.500 y prueba 7.500. Cinco pliegues estratificados compartidos, mezcla y semilla 42. '
        'Principal 14 predictores; reducido 12, sin GPA final ni retención. Sin identificadores, objetivo, GPA_Change, imputación, recortes o SMOTE. '
        'Pipeline nuevo por ajuste; escalado solo para logística y one-hot nominal con desconocidas ignoradas. '
        'Logística: 10 combinaciones; árbol: 16 de 360; bosque: 12 de 72. Se repiten los mismos espacios y combinaciones en sensibilidad. '
        '380 ajustes CV + 6 reajustes de candidatos + 6 Dummy + 1 final = **393 ajustes**. Ejecución secuencial, un hilo; no se redujo el presupuesto. '
        'Configuraciones completas: `protocolo.json`; resultados completos: `busqueda_cv.csv` de cada experimento. '
        'CV selecciona hiperparámetros: su media no es una evaluación independiente y su DE no es un intervalo de confianza.',
        '### Compatibilidad verificada\n\nUn intento inicial falló al puntuar el primer pliegue Dummy por `pos_label=1` con etiquetas textuales. '
        'Se corrigió declarando High en el scorer y se registró otro identificador antes de las búsquedas reales. '
        'En promedio macro se ignora pos_label y se utilizan explícitamente las tres clases. '
        'La incidencia y un ajuste inicial Dummy sin evaluación completa están registrados en `incidencias_implementacion.json`; '
        'no forman parte de los 393 ajustes del experimento completo. No hubo reducción de búsquedas ni resultados estimados.',
        '## Algoritmos y línea base\n\nLogística multinomial L2 ofrece una referencia regularizada interpretable. El árbol representa reglas e interacciones; '
        'Random Forest agrega árboles bootstrap con subconjuntos de variables y tiene mayor complejidad. '
        f'Dummy aprende **{baseline["interpretation"]["majority_class"]}**: validación Macro F1 **{baseline["validation"]["macro_f1"]:.6f}**, '
        f'Accuracy **{baseline["validation"]["accuracy"]:.6f}**. No predice Low ni High, que tienen Recall cero; su precisión indefinida se registra y se calcula como cero.',
        '## CV y validación\n\n'+tabla_md(compact),
        '## Errores por clase\n\nLas matrices usan filas reales y columnas predichas en orden Low, Medium, High. '
        'Se exportan conteos y proporciones por clase real en los JSON y figuras. Cada candidato conserva predicciones con trazabilidad. '
        'Precision de High penaliza falsos positivos; Recall de High penaliza High confundidos con Low/Medium. '
        'Las brechas entrenamiento−validación son diagnósticas; no prueban por sí solas generalización externa.',
        '\n\n'.join(diagnostics),
        '## Interpretabilidad\n\nCoeficientes logísticos por clase en `coeficientes.csv`, con numéricas estandarizadas y todas las categorías one-hot. '
        'No equivalen a efectos causales ni a contrastes aislados contra una categoría omitida. Árbol: reglas completas y vista truncada a profundidad 2, '
        'con orden real de clases y cantidades ponderadas si se usa balanced. Bosque: número de árboles, nodos y profundidad. '
        'Impureza puede favorecer variables con muchos cortes; permutación sobre validación mide caídas de Macro F1 en variables originales '
        'con cinco repeticiones. Correlación entre predictores puede enmascarar o repartir importancia. No se infiere la fórmula de la etiqueta.',
        '## Sensibilidad\n\n'+tabla_md(sensitivity)+
        '\n\nLas diferencias son reducido−principal. El escenario reducido conserva particiones, pliegues, combinaciones y presupuesto. '
        'Es una alternativa descriptiva; no acredita detección anticipada ni elimina posible circularidad.',
        f'## Selección congelada\n\nGanador principal: **{NOMBRES[selection["model"]]}**, Macro F1 de validación '
        f'**{selection["validation"]["macro_f1"]:.6f}**. Mejora frente a Dummy: **{selection["improvement_over_dummy"]:.6f}**. '
        'Regla: mayor Macro F1, empate hasta 1e-12, Recall de High y simplicidad logística→árbol→bosque. '
        'La decisión, parámetros, huellas y procedimiento final están en `seleccion_modelo.json`; su recibo se guardó antes de cargar prueba.',
        f'La ventaja sobre el segundo candidato es **{margin:.6f}** de Macro F1; no demuestra superioridad estadística. '
        f'El ganador recupera **{highval["recall"]:.2%}** de los High de validación y omite **{1-highval["recall"]:.2%}**. '
        'El árbol puede ofrecer otro compromiso Precision/Recall de High, visible en la tabla, pero no ganó el criterio principal. '
        'La estabilidad CV, brecha, interpretación y coste complementan la selección. Las consecuencias de omitir High deben valorarse en Fase 5.',
        f'## Modelo final y prueba\n\nPipeline nuevo reajustado con **42.500 registros**, más que los candidatos de validación. '
        f'Prueba: **7.500 registros**, Macro F1 **{m["macro_f1"]:.6f}**, Accuracy **{m["accuracy"]:.6f}**.\n\n'+tabla_md(byclass)+
        f'\n\nHigh→Low **{cm[2,0]}**, High→Medium **{cm[2,1]}**; Low→High **{cm[0,2]}**, Medium→High **{cm[1,2]}**. '
        'La selección se conserva tras prueba; no se hicieron nuevos ajustes para mejorarla.',
        '## Reproducibilidad\n\nEl README documenta comandos de etapas independientes y ejecución con kernels nuevos. '
        'Los hashes identifican datos, protocolo, código, pliegues, selección y artefactos, sin referencias circulares. '
        'Las fechas y duraciones se guardan aparte; los resultados verificables se reutilizan sin nuevas búsquedas. '
        'El pipeline final comprimido incluye preprocesamiento y clasificador. Se prueba en un proceso independiente '
        'contra todas las predicciones y probabilidades guardadas. Consulte `verificacion.json` para los controles efectivamente ejecutados.',
        '## Límites y traspaso a Fase 5\n\nLa fórmula de burnout y el origen sintético siguen sin confirmarse. Un desempeño extraordinario podría reflejar '
        'reglas desconocidas de construcción de la etiqueta; no demuestra fuga directa ni aplicación clínica. '
        'GPA final y retención pertenecen al alcance retrospectivo. Fase 2 exploró el CSV completo: prueba es una partición interna reservada, '
        'no una cohorte externa nunca inspeccionada. Se mantiene fuera de ajustes posteriores. '
        'No se demuestra causalidad, detección anticipada, representatividad institucional ni reducción real del riesgo. '
        'Fase 5 debe valorar cumplimiento de negocio, consecuencias de errores, procedencia y validación externa; permanece pendiente.',
        '## Referencias oficiales\n\n[Validación cruzada](https://scikit-learn.org/1.7/modules/cross_validation.html), '
        '[métricas](https://scikit-learn.org/1.7/modules/model_evaluation.html), '
        '[logística](https://scikit-learn.org/1.7/modules/generated/sklearn.linear_model.LogisticRegression.html), '
        '[árbol](https://scikit-learn.org/1.7/modules/generated/sklearn.tree.DecisionTreeClassifier.html), '
        '[bosque](https://scikit-learn.org/1.7/modules/generated/sklearn.ensemble.RandomForestClassifier.html), '
        '[permutación](https://scikit-learn.org/1.7/modules/permutation_importance.html).']
    (core.FASE/'INFORME_FASE4_MODELADO.md').write_text('\n\n'.join(sections)+'\n',encoding='utf-8',newline='\n')
    return core.FASE/'INFORME_FASE4_MODELADO.md'
