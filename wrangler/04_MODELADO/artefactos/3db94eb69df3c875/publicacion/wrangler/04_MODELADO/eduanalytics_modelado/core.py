"""Protocolo único utilizado por consola y notebooks. No modifica Fases 1–3."""
from pathlib import Path
import hashlib
import importlib.metadata as metadata
import importlib.util
import json
import platform
import time
import warnings
from datetime import datetime, timezone

import joblib
import numpy as np
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.exceptions import ConvergenceWarning
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, confusion_matrix, f1_score,
                             precision_recall_fscore_support, make_scorer)
from sklearn.model_selection import (GridSearchCV, RandomizedSearchCV, ParameterGrid,
                                    ParameterSampler, StratifiedKFold, cross_validate)
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier, export_text
from threadpoolctl import threadpool_limits

ROOT = Path(__file__).resolve().parents[3]
FASE = ROOT / 'wrangler/04_MODELADO'
PREP = ROOT / 'wrangler/03_PREPARACION_DATOS/artefactos'
ART = FASE / 'artefactos'
spec = importlib.util.spec_from_file_location('eduanalytics_preparacion', PREP / 'preprocesamiento.py')
prep = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prep)
CLASES = list(prep.CLASES)
MODELOS = ['logistica', 'arbol', 'random_forest']
ESCENARIOS = ['principal', 'reducido']
SEED = 42
EXCLUIDAS = ['Post_Semester_GPA', 'Skill_Retention_Score']
# pos_label no cambia el promedio macro, pero debe ser textual para la API de respuesta 1.7.2.
SCORER = make_scorer(f1_score, average='macro', labels=CLASES, zero_division=0, pos_label='High')
ESPACIOS = {
    'logistica': {'clasificador__C': [0.01, 0.1, 1, 10, 100],
                  'clasificador__class_weight': [None, 'balanced']},
    'arbol': {'clasificador__max_depth': [3, 5, 8, 12, None],
              'clasificador__min_samples_leaf': [1, 10, 50, 100],
              'clasificador__min_samples_split': [2, 10, 50],
              'clasificador__ccp_alpha': [0.0, 0.0001, 0.001],
              'clasificador__class_weight': [None, 'balanced']},
    'random_forest': {'clasificador__n_estimators': [150, 300],
                      'clasificador__max_depth': [8, 16, None],
                      'clasificador__min_samples_leaf': [1, 5, 20],
                      'clasificador__max_features': ['sqrt', 0.5],
                      'clasificador__class_weight': [None, 'balanced']},
}
PRESUPUESTOS = {'logistica': 10, 'arbol': 16, 'random_forest': 12}


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def canon(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(',', ':'),
                      allow_nan=False, default=lambda x: x.item() if isinstance(x, np.generic) else str(x))


def escribir_json(path, obj):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(json.loads(canon(obj)), ensure_ascii=False, indent=2) + '\n',
                    encoding='utf-8', newline='\n')


def leer(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def csv(path, frame):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(path, index=False, sep=';', encoding='utf-8', lineterminator='\n',
                 float_format='%.17g')


def versiones():
    return {'Python': platform.python_version(), **{n: metadata.version(n) for n in
            ['scikit-learn', 'numpy', 'pandas', 'scipy', 'joblib', 'threadpoolctl',
             'matplotlib', 'seaborn', 'nbclient', 'nbformat', 'ipykernel']}}


def verificar_entradas():
    """Controla bytes de prueba para integridad, sin cargar sus etiquetas para selección."""
    if platform.python_version() != '3.10.6' or metadata.version('scikit-learn') != '1.7.2':
        raise RuntimeError('Este experimento exige Python 3.10.6 y scikit-learn 1.7.2.')
    m = leer(PREP / 'manifest.json')
    assert sha(ROOT / m['input']['path']) == m['input']['sha256']
    for rel, info in m['references'].items():
        assert sha(ROOT / rel) == (info['sha256'] if isinstance(info, dict) else info), f'Referencia de Fase 3 alterada: {rel}'
    for rel, info in m['artifacts'].items():
        assert sha(PREP / rel) == info['sha256'], f'Artefacto de Fase 3 alterado: {rel}'
    return m


def predictores(escenario):
    if escenario not in ESCENARIOS:
        raise ValueError('Escenario desconocido.')
    return [c for c in prep.PREDICTORES if escenario == 'principal' or c not in EXCLUIDAS]


def cargar(nombre, escenario='principal', autorizacion_prueba=None):
    if nombre == 'test':
        if autorizacion_prueba is None:
            raise RuntimeError('Prueba bloqueada: usar únicamente la etapa final congelada.')
        _seleccion_valida(autorizacion_prueba)
    X, y, t = prep.cargar_particion(nombre, PREP)
    X = X[predictores(escenario)]
    assert not set(X.columns) & {prep.OBJETIVO, 'Student_ID', '_row_id'}
    assert X.index.equals(y.index) and X.index.equals(t.index)
    return X, y, t


def crear_pipeline(modelo, escenario='principal', parametros=None):
    if modelo == 'dummy':
        return Pipeline([('clasificador', DummyClassifier(strategy='most_frequent'))])
    pp = prep.crear_preprocesador('logistica' if modelo == 'logistica' else 'arbol')
    if escenario == 'reducido':
        blocks = pp.named_steps['columnas'].transformers
        pp.set_params(columnas__transformers=[
            (n, transformer, [c for c in cols if c in predictores(escenario)])
            for n, transformer, cols in blocks])
    estimadores = {
        'logistica': LogisticRegression(solver='lbfgs', penalty='l2', max_iter=5000,
                                       tol=1e-4, random_state=SEED),
        'arbol': DecisionTreeClassifier(criterion='gini', random_state=SEED),
        'random_forest': RandomForestClassifier(criterion='gini', random_state=SEED,
                                               n_jobs=1),
    }
    pipe = Pipeline([('preprocesamiento', pp), ('clasificador', estimadores[modelo])])
    if parametros:
        pipe.set_params(**parametros)
    return pipe


def _configuracion():
    m = verificar_entradas()
    combinations = {n: list(ParameterGrid(s)) if n == 'logistica' else
                    list(ParameterSampler(s, n_iter=PRESUPUESTOS[n], random_state=SEED))
                    for n, s in ESPACIOS.items()}
    sources = [FASE / 'eduanalytics_modelado/core.py', ROOT / 'tools/ejecutar_modelado.py']
    return {'schema_version': 1, 'seed': SEED, 'classes': CLASES,
            'versions': versiones(), 'input_sha256': m['input']['sha256'],
            'phase3_manifest_sha256': sha(PREP / 'manifest.json'),
            'partition_sha256': {n: sha(PREP / f'{n}.csv') for n in ['train', 'validation', 'test']},
            'membership_sha256': m['split']['membership_sha256'],
            'code_sha256': {str(p.relative_to(ROOT).as_posix()): sha(p) for p in sources},
            'requirements_lock_sha256': sha(ROOT / 'requirements-lock.txt'),
            'predictors': {s: predictores(s) for s in ESCENARIOS},
            'cv': {'n_splits': 5, 'shuffle': True, 'random_state': SEED},
            'spaces': ESPACIOS, 'configurations': combinations, 'budgets': PRESUPUESTOS,
            'parallelism': {'search_n_jobs': 1, 'forest_n_jobs': 1, 'numerical_threads': 1},
            'logistic_fixed': {'solver': 'lbfgs', 'penalty': 'l2', 'max_iter': 5000, 'tol': 1e-4},
            'permutation': {'n_repeats': 5, 'random_state': SEED, 'scoring': 'macro_f1'},
            'selection': {'scenario': 'principal', 'candidates': MODELOS,
                          'metric': 'validation_macro_f1', 'tie_atol': 1e-12,
                          'tie_breakers': ['recall_High', 'logistica < arbol < random_forest',
                                           'structural_cost'],
                          'baseline': 'reference; report lack of improvement explicitly'},
            'fit_budget': {'search_cv': 380, 'candidate_refits': 6, 'dummy_cv_and_refit': 6,
                           'final_refit': 1, 'total': 393},
            'scope': 'retrospective; non-causal; non-clinical; label formula unknown',
            'test_policy': 'load labels only after selection receipt; no retuning after test'}


def preparar():
    cfg = _configuracion()
    ident = hashlib.sha256(canon(cfg).encode('utf-8')).hexdigest()[:16]
    directory = ART / ident
    if (directory / 'protocolo.json').exists():
        assert canon(leer(directory / 'protocolo.json')) == canon(cfg)
    else:
        escribir_json(directory / 'protocolo.json', cfg)
        X, y, trace = cargar('train')
        assignment = np.full(len(X), -1, dtype=np.int64)
        for k, (a, b) in enumerate(StratifiedKFold(**cfg['cv']).split(X, y)):
            assert not set(a) & set(b)
            assert (assignment[b] == -1).all()
            assignment[b] = k
        assert (assignment >= 0).all()
        frame = trace.reset_index(drop=True).copy()
        frame.insert(0, 'train_position', np.arange(len(X)))
        frame['fold'] = assignment
        frame['label'] = y.to_numpy()
        csv(directory / 'pliegues.csv', frame)
        escribir_json(directory / 'pliegues_sha256.json', {'sha256': sha(directory / 'pliegues.csv')})
    _pliegues(directory)
    escribir_json(ART / 'experimento_actual.json', {'experiment_id': ident,
                                                   'protocol_sha256': sha(directory / 'protocolo.json')})
    return directory


def experimento_actual():
    pointer = leer(ART / 'experimento_actual.json')
    directory = ART / pointer['experiment_id']
    assert sha(directory / 'protocolo.json') == pointer['protocol_sha256']
    assert canon(leer(directory / 'protocolo.json')) == canon(_configuracion()), 'Protocolo/código cambiado: preparar otro experimento.'
    return directory


def _pliegues(directory):
    path = directory / 'pliegues.csv'
    assert sha(path) == leer(directory / 'pliegues_sha256.json')['sha256']
    frame = pd.read_csv(path, sep=';')
    _, y, trace = cargar('train')
    assert np.array_equal(frame.train_position, np.arange(len(y)))
    assert np.array_equal(frame[prep.TRAZABILIDAD], trace[prep.TRAZABILIDAD])
    assert np.array_equal(frame.label, y)
    cv = []
    for k in range(5):
        a, b = np.flatnonzero(frame.fold.to_numpy() != k), np.flatnonzero(frame.fold.to_numpy() == k)
        assert len(a) == 28000 and len(b) == 7000
        assert set(y.iloc[a]) == set(CLASES) == set(y.iloc[b])
        cv.append((a, b))
    regenerated = list(StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED).split(trace, y))
    assert all(np.array_equal(a, c) and np.array_equal(b, d)
               for (a, b), (c, d) in zip(cv, regenerated))
    return cv


def evaluar(y, pred):
    assert len(y) == len(pred) and set(pred) <= set(CLASES)
    p, r, f, s = precision_recall_fscore_support(y, pred, labels=CLASES, zero_division=0)
    by_class = {c: {'precision': float(p[i]), 'recall': float(r[i]), 'f1': float(f[i]),
                    'support': int(s[i]), 'precision_undefined': int(np.sum(np.asarray(pred) == c)) == 0}
                for i, c in enumerate(CLASES)}
    cm = confusion_matrix(y, pred, labels=CLASES)
    normalized = np.divide(cm, cm.sum(axis=1, keepdims=True),
                           out=np.zeros_like(cm, dtype=float), where=cm.sum(axis=1, keepdims=True) != 0)
    return {'macro_f1': float(f1_score(y, pred, labels=CLASES, average='macro', zero_division=0)),
            'accuracy': float(accuracy_score(y, pred)), 'by_class': by_class,
            'confusion': cm.tolist(), 'confusion_normalized': normalized.tolist(), 'classes': CLASES}


def predecir(pipe, X, y, trace):
    start = time.perf_counter()
    pred = pipe.predict(X)
    proba = pipe.predict_proba(X)
    seconds = time.perf_counter() - start
    order = list(pipe.classes_)
    assert set(order) == set(CLASES)
    assert proba.shape == (len(X), 3) and np.isfinite(proba).all()
    assert (proba >= 0).all() and (proba <= 1).all() and np.allclose(proba.sum(axis=1), 1, atol=1e-12)
    assert np.array_equal(pred, np.asarray(order)[proba.argmax(axis=1)])
    out = trace.reset_index(drop=True).copy()
    out['actual'] = np.asarray(y)
    out['predicted'] = pred
    for c in CLASES:
        out[f'prob_{c}'] = proba[:, order.index(c)]
    return evaluar(y, pred), out, seconds, order


def _recibo(directory):
    files = {p.name: sha(p) for p in sorted(directory.iterdir())
             if p.is_file() and p.name != 'recibo.json'}
    escribir_json(directory / 'recibo.json', {'files': files})


def _verificar_recibo(directory):
    receipt = leer(directory / 'recibo.json')
    assert receipt['files']
    for name, value in receipt['files'].items():
        assert Path(name).name == name and sha(directory / name) == value, f'Artefacto alterado: {name}'


def cargar_resultado(modelo, escenario='principal', directory=None):
    directory = directory or experimento_actual()
    path = directory / escenario / modelo
    _verificar_recibo(path)
    result = leer(path / 'resultado.json')
    assert result['experiment_id'] == directory.name and result['scenario'] == escenario
    assert result['model'] == modelo
    _, y, trace = cargar('validation', escenario)
    predictions = pd.read_csv(path / 'predicciones_validacion.csv', sep=';', float_precision='round_trip')
    assert np.array_equal(predictions[prep.TRAZABILIDAD], trace[prep.TRAZABILIDAD])
    assert np.array_equal(predictions.actual, y)
    assert canon(evaluar(y, predictions.predicted)) == canon(result['validation'])
    _validar_probabilidades(predictions)
    return result


def _validar_probabilidades(frame):
    probs = frame[[f'prob_{c}' for c in CLASES]].to_numpy()
    assert np.isfinite(probs).all() and (probs >= 0).all() and (probs <= 1).all()
    assert np.allclose(probs.sum(axis=1), 1, atol=1e-12)
    # Empates de probabilidades se resuelven por el orden real del estimador (alfabético).
    order = sorted(CLASES)
    expected = np.array(order)[frame[[f'prob_{c}' for c in order]].to_numpy().argmax(axis=1)]
    assert np.array_equal(expected, frame.predicted)


def _interpretar(pipe, modelo, Xval, yval, directory):
    clf = pipe.named_steps['clasificador']
    if modelo == 'dummy':
        return {'majority_class': str(clf.classes_[np.argmax(clf.class_prior_)])}
    names = pipe.named_steps['preprocesamiento'].get_feature_names_out()
    if modelo == 'logistica':
        rows = [{'class': c, 'feature': n, 'coefficient': float(v)}
                for c, coefs in zip(clf.classes_, clf.coef_) for n, v in zip(names, coefs)]
        csv(directory / 'coeficientes.csv', pd.DataFrame(rows))
        return {'iterations': clf.n_iter_.tolist(), 'max_iter': clf.max_iter,
                'converged': bool(np.max(clf.n_iter_) < clf.max_iter),
                'coefficients': int(clf.coef_.size), 'transformed_features': len(names)}
    csv(directory / 'importancia_impureza.csv', pd.DataFrame({'feature': names, 'importance': clf.feature_importances_}))
    with threadpool_limits(limits=1):
        perm = permutation_importance(pipe, Xval, yval, scoring=SCORER,
                                      n_repeats=5, random_state=SEED, n_jobs=1)
    table = pd.DataFrame({'feature': Xval.columns, 'mean': perm.importances_mean,
                          'std': perm.importances_std})
    for j in range(5):
        table[f'repeat_{j}'] = perm.importances[:, j]
    csv(directory / 'importancia_permutacion.csv', table)
    if modelo == 'arbol':
        rules = export_text(clf, feature_names=list(names), decimals=4, max_depth=clf.get_depth()+1)
        (directory / 'reglas.txt').write_text(rules, encoding='utf-8', newline='\n')
        # Guardar un árbol para dibujar sin depender de la caché del pipeline completo.
        joblib.dump(clf, directory / 'arbol_interpretacion.joblib', compress=3)
        return {'depth': clf.get_depth(), 'nodes': clf.tree_.node_count,
                'leaves': clf.get_n_leaves(), 'transformed_features': len(names),
                'feature_names': list(names), 'estimator_classes': list(clf.classes_)}
    return {'trees': len(clf.estimators_),
            'total_nodes': sum(t.tree_.node_count for t in clf.estimators_),
            'mean_depth': float(np.mean([t.get_depth() for t in clf.estimators_])),
            'transformed_features': len(names)}


def entrenar(modelo, escenario='principal', directory=None):
    directory = directory or experimento_actual()
    assert modelo in MODELOS + ['dummy'] and escenario in ESCENARIOS
    if modelo == 'dummy' and escenario != 'principal':
        raise ValueError('La línea base no depende del escenario de predictores.')
    out = directory / escenario / modelo
    if (out / 'recibo.json').exists():
        return cargar_resultado(modelo, escenario, directory)
    if (directory / 'seleccion_modelo.json').exists():
        raise RuntimeError('Selección congelada: no se añaden nuevos ajustes a este experimento.')
    out.mkdir(parents=True, exist_ok=True)
    X, y, _ = cargar('train', escenario)
    Xv, yv, tv = cargar('validation', escenario)
    cv = _pliegues(directory)
    cfg = leer(directory / 'protocolo.json')
    pipeline = crear_pipeline(modelo, escenario)
    start = time.perf_counter()
    print(f'Entrenando {modelo}/{escenario}: {PRESUPUESTOS.get(modelo, 1)} configuraciones, 5 pliegues', flush=True)
    with threadpool_limits(limits=1), warnings.catch_warnings():
        warnings.simplefilter('error', ConvergenceWarning)
        if modelo == 'dummy':
            scores = cross_validate(pipeline, X, y, cv=cv, scoring=SCORER, n_jobs=1,
                                    return_train_score=True, error_score='raise')
            cvtable = pd.DataFrame({'fold': range(5), **scores})
            pipeline.fit(X, y)
            best_params = {}
            mean, std = float(np.mean(scores['test_score'])), float(np.std(scores['test_score']))
            folds = scores['test_score'].tolist()
            fits = 6
            refit_time = None
        else:
            kwargs = dict(estimator=pipeline, cv=cv, scoring=SCORER, refit=True,
                          n_jobs=1, return_train_score=True, error_score='raise')
            if modelo == 'logistica':
                search = GridSearchCV(param_grid=ESPACIOS[modelo], **kwargs)
            else:
                search = RandomizedSearchCV(param_distributions=ESPACIOS[modelo],
                                             n_iter=PRESUPUESTOS[modelo], random_state=SEED, **kwargs)
            search.fit(X, y)
            assert canon(search.cv_results_['params']) == canon(cfg['configurations'][modelo])
            pipeline = search.best_estimator_
            best_params = search.best_params_
            mean = float(search.best_score_)
            std = float(search.cv_results_['std_test_score'][search.best_index_])
            folds = [float(search.cv_results_[f'split{k}_test_score'][search.best_index_]) for k in range(5)]
            cvtable = pd.DataFrame(search.cv_results_)
            cvtable['params'] = [canon(p) for p in cvtable['params']]
            fits = PRESUPUESTOS[modelo] * 5 + 1
            refit_time = float(search.refit_time_)
    search_seconds = time.perf_counter() - start
    csv(out / 'busqueda_cv.csv', cvtable)
    train_metrics, _, train_seconds, order = predecir(pipeline, X, y, cargar('train', escenario)[2])
    val_metrics, predictions, val_seconds, _ = predecir(pipeline, Xv, yv, tv)
    csv(out / 'predicciones_validacion.csv', predictions)
    interpretation = _interpretar(pipeline, modelo, Xv, yv, out)
    cache = ROOT / '.cache/modelado' / directory.name / escenario
    cache.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, cache / f'{modelo}.joblib', compress=3)
    result = {'experiment_id': directory.name, 'model': modelo, 'scenario': escenario,
              'predictors': list(X.columns), 'best_params': best_params, 'estimator_classes': order,
              'cv': {'macro_f1_mean': mean, 'macro_f1_std': std, 'fold_scores': folds,
                     'fits': fits, 'configurations': PRESUPUESTOS.get(modelo, 1)},
              'train': train_metrics, 'validation': val_metrics,
              'overfit_gap': train_metrics['macro_f1'] - val_metrics['macro_f1'],
              'interpretation': interpretation}
    escribir_json(out / 'resultado.json', result)
    escribir_json(out / 'ejecucion.json', {'started_utc': datetime.now(timezone.utc).isoformat(),
                   'search_and_refit_seconds': search_seconds, 'selected_refit_seconds': refit_time,
                   'train_inference_seconds': train_seconds, 'validation_inference_seconds': val_seconds,
                   'inference_includes': 'predict and predict_proba; full pipeline',
                   'fits': fits, 'candidate_cache_sha256': sha(cache / f'{modelo}.joblib')})
    _recibo(out)
    print(f'Completado {modelo}/{escenario}: CV={mean:.6f}; validación={val_metrics["macro_f1"]:.6f}', flush=True)
    return cargar_resultado(modelo, escenario, directory)


def tabla_comparacion(directory=None):
    directory = directory or experimento_actual()
    rows = []
    for escenario, modelos in [('principal', ['dummy']+MODELOS), ('reducido', MODELOS)]:
        for modelo in modelos:
            r = cargar_resultado(modelo, escenario, directory)
            timing = leer(directory / escenario / modelo / 'ejecucion.json')
            row = {'model': modelo, 'scenario': escenario, 'params': canon(r['best_params']),
                   'cv_macro_f1': r['cv']['macro_f1_mean'], 'cv_std': r['cv']['macro_f1_std'],
                   'train_macro_f1': r['train']['macro_f1'], 'validation_macro_f1': r['validation']['macro_f1'],
                   'validation_accuracy': r['validation']['accuracy'], 'gap': r['overfit_gap'],
                   'search_seconds': timing['search_and_refit_seconds'],
                   'refit_seconds': timing['selected_refit_seconds'],
                   'inference_seconds': timing['validation_inference_seconds'],
                   'complexity': canon(r['interpretation'])}
            for c in CLASES:
                for metric in ['precision', 'recall', 'f1', 'support']:
                    row[f'{metric}_{c}'] = r['validation']['by_class'][c][metric]
            rows.append(row)
    return pd.DataFrame(rows)


def comparar(directory=None):
    directory = directory or experimento_actual()
    table = tabla_comparacion(directory)
    candidates = [cargar_resultado(n, 'principal', directory) for n in MODELOS]
    maximum = max(r['validation']['macro_f1'] for r in candidates)
    tied = [r for r in candidates if abs(r['validation']['macro_f1'] - maximum) <= 1e-12]
    recall = max(r['validation']['by_class']['High']['recall'] for r in tied)
    tied = [r for r in tied if abs(r['validation']['by_class']['High']['recall'] - recall) <= 1e-12]
    winner = min(tied, key=lambda r: MODELOS.index(r['model']))
    baseline = cargar_resultado('dummy', 'principal', directory)
    selection = {'schema_version': 1, 'experiment_id': directory.name,
                 'model': winner['model'], 'scenario': 'principal', 'predictors': winner['predictors'],
                 'hyperparameters': winner['best_params'],
                 'rule': leer(directory / 'protocolo.json')['selection'],
                 'reason': 'Mayor Macro F1 en validación; desempates predefinidos si corresponde.',
                 'improvement_over_dummy': winner['validation']['macro_f1'] - baseline['validation']['macro_f1'],
                 'cv': winner['cv'], 'validation': winner['validation'],
                 'seed': SEED, 'versions': versiones(),
                 'protocol_sha256': sha(directory / 'protocolo.json'),
                 'folds_sha256': sha(directory / 'pliegues.csv'),
                 'candidate_receipts': {f'{s}/{n}': sha(directory / s / n / 'recibo.json')
                                        for s,n in [('principal','dummy')]+[(s,n) for s in ESCENARIOS for n in MODELOS]},
                 'input_and_code_hashes': {k:v for k,v in leer(directory / 'protocolo.json').items()
                                          if 'sha256' in k},
                 'final_training': {'rows': 42500, 'partitions_in_order': ['train', 'validation'],
                                    'new_unfitted_pipeline': True, 'test_rows': 7500,
                                    'no_retuning_after_test': True}}
    path = directory / 'seleccion_modelo.json'
    if path.exists():
        assert canon(leer(path)) == canon(selection), 'No se sobrescribe una selección congelada.'
    else:
        csv(directory / 'comparacion.csv', table)
        pairs = table[table.model != 'dummy'].pivot(index='model', columns='scenario',
                    values=['validation_macro_f1','precision_High','recall_High','gap','search_seconds'])
        pairs.columns = ['_'.join(c) for c in pairs.columns]
        for metric in ['validation_macro_f1','precision_High','recall_High','gap','search_seconds']:
            pairs[f'{metric}_delta_reducido_menos_principal'] = pairs[f'{metric}_reducido'] - pairs[f'{metric}_principal']
        csv(directory / 'sensibilidad.csv', pairs.reset_index())
        escribir_json(path, selection)
        escribir_json(directory / 'seleccion_congelada.json', {'selection_sha256': sha(path),
                       'frozen_utc': datetime.now(timezone.utc).isoformat(), 'test_evaluation_started': False})
    return _seleccion_valida(directory)


def _seleccion_valida(directory):
    directory = Path(directory)
    assert directory == experimento_actual()
    receipt = leer(directory / 'seleccion_congelada.json')
    assert sha(directory / 'seleccion_modelo.json') == receipt['selection_sha256']
    selection = leer(directory / 'seleccion_modelo.json')
    assert selection['experiment_id'] == directory.name and selection['scenario'] == 'principal'
    assert selection['predictors'] == prep.PREDICTORES
    assert selection['protocol_sha256'] == sha(directory / 'protocolo.json')
    assert selection['folds_sha256'] == sha(directory / 'pliegues.csv')
    for rel, h in selection['candidate_receipts'].items():
        assert sha(directory / rel / 'recibo.json') == h
        _verificar_recibo(directory / rel)
    return selection


def finalizar(directory=None):
    directory = directory or experimento_actual()
    selection = _seleccion_valida(directory)
    out = directory / 'final'
    if (out / 'recibo.json').exists():
        _verificar_recibo(out)
        return leer(out / 'resultado.json')
    if (directory / 'inicio_prueba.json').exists():
        raise RuntimeError('Evaluación de prueba interrumpida: conservar evidencia; usar reproducción congelada, no reiniciar selección.')
    Xt, yt, _ = cargar('train')
    Xv, yv, _ = cargar('validation')
    X, y = pd.concat([Xt, Xv]), pd.concat([yt, yv])
    assert len(X) == 42500 and X.index.is_unique and X.index.equals(y.index)
    pipeline = crear_pipeline(selection['model'], parametros=selection['hyperparameters'])
    started = time.perf_counter()
    with threadpool_limits(limits=1), warnings.catch_warnings():
        warnings.simplefilter('error', ConvergenceWarning)
        pipeline.fit(X, y)
    fit_seconds = time.perf_counter()-started
    out.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, out / 'pipeline_final.joblib', compress=3)
    escribir_json(directory / 'inicio_prueba.json', {'selection_sha256': sha(directory / 'seleccion_modelo.json'),
                   'started_utc': datetime.now(timezone.utc).isoformat(),
                   'model_sha256_before_test': sha(out / 'pipeline_final.joblib')})
    Xp, yp, tp = cargar('test', autorizacion_prueba=directory)
    metrics, predictions, seconds, order = predecir(pipeline, Xp, yp, tp)
    csv(out / 'predicciones_prueba.csv', predictions)
    result = {'experiment_id': directory.name, 'model': selection['model'], 'scenario': 'principal',
              'training_rows': len(X), 'test_rows': len(Xp), 'test': metrics,
              'classes': CLASES, 'estimator_classes': order, 'predictors': list(X.columns),
              'versions': versiones(), 'hyperparameters': selection['hyperparameters'],
              'selection_sha256': sha(directory / 'seleccion_modelo.json')}
    escribir_json(out / 'resultado.json', result)
    escribir_json(out / 'ejecucion.json', {'final_fit_seconds': fit_seconds,
                   'test_inference_seconds': seconds, 'finished_utc': datetime.now(timezone.utc).isoformat()})
    _recibo(out)
    print(f'Final {selection["model"]}: prueba Macro F1={metrics["macro_f1"]:.6f}', flush=True)
    return result
