"""Verifica las Fases 1–3; opcionalmente ejecuta los cuatro notebooks en kernels nuevos.

python tools/verificar_proyecto.py
python tools/verificar_proyecto.py --ejecutar --desde carpetas
No entrena clasificadores ni utiliza prueba para seleccionar transformaciones.
"""
from pathlib import Path
import argparse
import hashlib
import importlib.metadata as metadata
import importlib.util
import json
import os
import re
import shutil
import sys
import tempfile
import time
from decimal import Decimal

import nbformat
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.exceptions import NotFittedError
from sklearn.utils.validation import check_is_fitted

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / 'dataset/ai_student_impact_dataset (1).csv'
ART = ROOT / 'wrangler/03_PREPARACION_DATOS/artefactos'
NOTEBOOKS = [Path('wrangler/01_ENTENDIMIENTO_NEGOCIO/01_entendimiento_negocio.ipynb'),
             Path('wrangler/02_COMPRENSION_DATOS/02_comprension_datos_eda.ipynb'),
             Path('wrangler/03_PREPARACION_DATOS/03_preparacion_datos.ipynb'),
             Path('notebook_eduanalytics_md.ipynb')]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def ejecutar(desde):
    from nbclient import NotebookClient
    from jupyter_client import KernelManager
    results = []
    cache = ROOT / '.cache/verificacion'
    cache.mkdir(parents=True, exist_ok=True)
    for rel in NOTEBOOKS:
        cwd = ROOT if desde == 'raiz' else ROOT / rel.parent
        if desde == 'carpetas' and rel.parent == Path('.'):
            cwd = ROOT / 'wrangler/03_PREPARACION_DATOS'
        nb = nbformat.read(ROOT / rel, as_version=4)
        for cell in nb.cells:
            if cell.cell_type == 'code':
                cell.outputs = []
                cell.execution_count = None
                cell.metadata.pop('execution', None)
        km = KernelManager(kernel_name='python3')
        km.kernel_spec.argv = [sys.executable, '-m', 'ipykernel_launcher', '-f', '{connection_file}']
        km.kernel_spec.env = {}
        env = dict(os.environ, IPYTHONDIR=str(cache / 'ipython'),
                   MPLCONFIGDIR=str(cache / 'matplotlib'), JUPYTER_RUNTIME_DIR=str(cache / 'runtime'),
                   PYTHONDONTWRITEBYTECODE='1')
        env.pop('PYTHONPATH', None)
        client = NotebookClient(nb, km=km, timeout=300, allow_errors=False, record_timing=False,
                                resources={'metadata': {'path': str(cwd)}})
        start = time.perf_counter()
        print('Ejecutando:', rel.as_posix(), 'desde', cwd.relative_to(ROOT), flush=True)
        with client.setup_kernel(cwd=str(cwd), env=env, cleanup_kc=True):
            client.execute()
        for cell in nb.cells:
            if cell.cell_type == 'code':
                outputs = []
                for output in cell.outputs:
                    if (outputs and output.output_type == 'stream' and
                            outputs[-1].output_type == 'stream' and output.name == outputs[-1].name):
                        outputs[-1].text += output.text
                    else:
                        outputs.append(output)
                cell.outputs = outputs
        nbformat.validate(nb)
        (ROOT / rel).write_bytes(nbformat.writes(nb).replace('\r\n', '\n').encode('utf-8'))
        results.append({'notebook': rel.as_posix(), 'desde': desde,
                        'seconds': round(time.perf_counter() - start, 2), 'errors': 0})
    return results


def verificar():
    assert sys.version_info[:3] == (3, 10, 6), 'La comprobación requiere Python 3.10.6.'
    manifest = json.loads((ART / 'manifest.json').read_text(encoding='utf-8'))
    assert sha(CSV) == manifest['input']['sha256']
    assert b'\r\n' not in CSV.read_bytes()
    for name, value in manifest['references'].items():
        assert sha(ROOT / name) == value, f'Referencia desactualizada: {name}'
    for name, info in manifest['artifacts'].items():
        assert sha(ART / name) == info['sha256'], f'Artefacto modificado: {name}'
        assert (ART / name).stat().st_size == info['bytes']
    assert manifest['versions']['Python'] == '3.10.6'
    for name, value in manifest['versions'].items():
        if name != 'Python':
            assert metadata.version(name) == value, f'Versión distinta: {name}'
    df = pd.read_csv(CSV, sep=';', encoding='utf-8-sig', float_precision='round_trip')
    assert df.shape == (50000, 16)
    assert df.Student_ID.is_unique and not df.isna().any().any() and not df.duplicated().any()
    classes = {'Low': 16369, 'Medium': 21144, 'High': 12487}
    assert df.Burnout_Risk_Level.value_counts().to_dict() == classes
    assert Decimal(classes['High']) * 100 / Decimal(len(df)) == Decimal('24.974')
    spec = importlib.util.spec_from_file_location('eduanalytics_verificacion', ART / 'preprocesamiento.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    all_parts, loaded, summaries = [], {}, []
    for name, size in [('train', 35000), ('validation', 7500), ('test', 7500)]:
        X, y, trace = module.cargar_particion(name, ART)
        assert X.shape == (size, 14) and X.index.equals(y.index) and X.index.equals(trace.index)
        assert list(X.columns) == module.PREDICTORES
        assert not {'Student_ID', '_row_id', 'Burnout_Risk_Level', 'GPA_Change'} & set(X.columns)
        assert set(y) == set(classes) and trace.Student_ID.is_unique and trace.index.is_unique
        original = df.iloc[trace['_row_id'].to_numpy()]
        pd.testing.assert_frame_equal(X.reset_index(drop=True), original[module.PREDICTORES].reset_index(drop=True), check_exact=True)
        pd.testing.assert_series_equal(y.reset_index(drop=True), original.Burnout_Risk_Level.reset_index(drop=True), check_exact=True)
        assert np.array_equal(trace.Student_ID.to_numpy(), original.Student_ID.to_numpy())
        part = pd.read_csv(ART / (name + '.csv'), sep=';', float_precision='round_trip')
        assert module.huella_pertenencia(part) == manifest['split']['membership_sha256'][name]
        all_parts.append(part)
        loaded[name] = (X, y, trace)
        summaries.append({'partition': name, 'rows': size, **y.value_counts().to_dict()})
    merged = pd.concat(all_parts).sort_values('_row_id')
    assert merged._row_id.tolist() == list(range(50000)) and merged.Student_ID.is_unique
    pd.testing.assert_frame_equal(merged[df.columns].reset_index(drop=True), df, check_exact=True)

    X_train = loaded['train'][0]
    transforms = {}
    for model in ['logistica', 'arbol']:
        first, second = module.crear_preprocesador(model), module.crear_preprocesador(model)
        assert first is not second and first['columnas'] is not second['columnas']
        for pipeline in [first, second, clone(first)]:
            try:
                check_is_fitted(pipeline)
            except NotFittedError:
                pass
            else:
                raise AssertionError('Una fábrica devolvió una instancia ajustada.')
        transformed = first.fit_transform(X_train)
        assert transformed.shape == (35000, 30) and np.isfinite(transformed).all()
        columns = first['columnas']
        encoder = columns.named_transformers_['categoricas']
        for col, cats in zip(module.CATEGORICAS, encoder.categories_):
            assert set(cats) == set(X_train[col])
        if model == 'logistica':
            scaler = columns.named_transformers_['numericas']['escalado']
            np.testing.assert_allclose(scaler.mean_, X_train[module.NUMERICAS].mean().to_numpy())
            assert scaler.n_samples_seen_ == 35000
            fitted_mean = scaler.mean_.copy()
        else:
            np.testing.assert_array_equal(transformed[:, :8], X_train[module.NUMERICAS].to_numpy())
        unknown = loaded['validation'][0].iloc[:3].copy()
        unknown[module.CATEGORICAS] = '__CATEGORIA_NUEVA_DE_CONTROL__'
        encoded_unknown = first.transform(unknown)
        assert np.isfinite(encoded_unknown).all() and (encoded_unknown[:, 8:29] == 0).all()
        np.testing.assert_array_equal(transformed[:, -1], X_train.Paid_Subscription.to_numpy(dtype=float))
        if model == 'logistica':
            np.testing.assert_array_equal(scaler.mean_, fitted_mean)
            fold = module.crear_preprocesador(model).fit(X_train.iloc[:1000])
            np.testing.assert_allclose(fold['columnas'].named_transformers_['numericas']['escalado'].mean_,
                                       X_train.iloc[:1000][module.NUMERICAS].mean().to_numpy())
        assert not any('Student_ID' in n or '_row_id' in n or 'Burnout_Risk_Level' in n
                       for n in first.get_feature_names_out())
        transforms[model] = {'train_shape': list(transformed.shape), 'unknown_categories': 'PASS', 'fresh_unfitted': 'PASS'}
    with tempfile.TemporaryDirectory(prefix='eduanalytics_integridad_') as folder:
        target = Path(folder)
        shutil.copyfile(ART / 'manifest.json', target / 'manifest.json')
        (target / 'train.csv').write_bytes((ART / 'train.csv').read_bytes() + b'\n')
        try:
            module.cargar_particion('train', target)
        except ValueError as exc:
            assert 'Hash incorrecto' in str(exc)
        else:
            raise AssertionError('Se aceptó un archivo alterado.')
    notebook_results = []
    for rel in NOTEBOOKS:
        nb = nbformat.read(ROOT / rel, as_version=4)
        nbformat.validate(nb)
        cells = [c for c in nb.cells if c.cell_type == 'code']
        assert [c.execution_count for c in cells] == list(range(1, len(cells) + 1))
        assert not any(o.output_type == 'error' for c in cells for o in c.outputs)
        assert b'\r\n' not in (ROOT / rel).read_bytes()
        assert all(not any(ord(x) < 32 and x not in '\r\n\t' for x in c.source) for c in nb.cells)
        notebook_results.append({'notebook': rel.as_posix(), 'code_cells': len(cells), 'errors': 0, 'sha256': sha(ROOT / rel)})
    # Numeric references from the general document: all 18 published group means.
    document = (ROOT / 'docs/INFORMACION_GENERAL_PROYECTO_EDUANALYTICS.md').read_text(encoding='utf-8')
    section = re.search(r'^## 18\..*?(?=^## \d+\.|\Z)', document, re.M | re.S).group(0)
    mapping = dict(zip(['Horas de IA por semana', 'Dependencia percibida de IA', 'Ansiedad durante exámenes',
                        'Horas de estudio tradicional', 'GPA final', 'Retención de habilidades'],
                       ['Weekly_GenAI_Hours', 'Perceived_AI_Dependency', 'Anxiety_Level_During_Exams',
                        'Traditional_Study_Hours', 'Post_Semester_GPA', 'Skill_Retention_Score']))
    means = df.groupby('Burnout_Risk_Level')[list(mapping.values())].mean()
    verified = 0
    for line in section.splitlines():
        if line.startswith('|'):
            row = [v.strip() for v in line.strip('|').split('|')]
            if row[0] in mapping:
                for label, value in zip(module.CLASES, row[1:]):
                    assert round(means.loc[label, mapping[row[0]]], 2) == float(value.replace(',', '.'))
                    verified += 1
    assert verified == 18
    assert manifest['changes']['records_modified'] == manifest['changes']['records_excluded'] == 0
    assert not manifest['preprocessing']['learned_parameters_exported']
    return {'Python': sys.version.split()[0], 'source_sha256': sha(CSV), 'rows': len(df), 'columns': df.shape[1],
            'nulls': 0, 'complete_duplicates': 0, 'id_duplicates': 0, 'classes': classes,
            'kpi_high_percent': '24.974', 'partitions': summaries, 'reconstruction': 'EXACT',
            'overlap': 0, 'predictors': 14, 'documented_means_checked': verified,
            'transforms': transforms, 'notebooks': notebook_results, 'manifest_hashes': 'PASS'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ejecutar', action='store_true')
    parser.add_argument('--desde', choices=['raiz', 'carpetas'], default='raiz')
    parser.add_argument('--salida', help='Ruta opcional del reporte JSON.')
    args = parser.parse_args()
    assert sys.version_info[:3] == (3, 10, 6), 'Seleccionar Python 3.10.6.'
    execution = ejecutar(args.desde) if args.ejecutar else []
    result = verificar()
    result['execution'] = execution
    if args.salida:
        Path(args.salida).write_bytes((json.dumps(result, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
    print(json.dumps(result, ensure_ascii=False, indent=2))
