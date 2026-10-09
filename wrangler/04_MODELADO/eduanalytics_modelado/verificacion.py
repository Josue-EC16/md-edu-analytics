"""Controles dirigidos, ejecución limpia y reproducción del experimento congelado."""
from pathlib import Path
import argparse
import json
import os
import subprocess
import sys
import time
import tempfile
import shutil
from datetime import datetime, timezone

import joblib
import nbformat
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.utils.validation import check_is_fitted
from sklearn.exceptions import NotFittedError
from threadpoolctl import threadpool_limits
from . import core


def worker(directory):
    selection=core._seleccion_valida(directory)
    core._verificar_recibo(directory/'final')
    pipe=joblib.load(directory/'final/pipeline_final.joblib')
    X,y,trace=core.cargar('test',autorizacion_prueba=directory)
    metrics,pred,_,order=core.predecir(pipe,X,y,trace)
    saved=pd.read_csv(directory/'final/predicciones_prueba.csv',sep=';',float_precision='round_trip')
    assert np.array_equal(pred[core.prep.TRAZABILIDAD],saved[core.prep.TRAZABILIDAD])
    assert np.array_equal(pred.predicted,saved.predicted) and np.array_equal(pred.actual,saved.actual)
    assert np.array_equal(pred[[f'prob_{c}' for c in core.CLASES]],saved[[f'prob_{c}' for c in core.CLASES]])
    assert core.canon(metrics)==core.canon(core.leer(directory/'final/resultado.json')['test'])
    assert pipe.feature_names_in_.tolist()==selection['predictors']
    pp=pipe.named_steps['preprocesamiento'].named_steps['columnas']
    if selection['model']=='logistica':
        scale=pp.named_transformers_['numericas'].named_steps['escalado']
        Xt,_,_=core.cargar('train');Xv,_,_=core.cargar('validation')
        assert scale.n_samples_seen_==42500
        assert np.allclose(scale.mean_,pd.concat([Xt,Xv])[core.prep.NUMERICAS].mean())
    return {'new_process':True,'prediction_rows':len(X),'predictions':'EXACT',
            'probabilities':'EXACT','metrics':'EXACT','classes_order':order,
            'pipeline_sha256':core.sha(directory/'final/pipeline_final.joblib')}


def pruebas_dirigidas(directory):
    cv=core._pliegues(directory)
    X,y,trace=core.cargar('train')
    for modelo in core.MODELOS:
        for scenario in core.ESCENARIOS:
            a=core.crear_pipeline(modelo,scenario);b=core.crear_pipeline(modelo,scenario)
            assert a is not b and a.named_steps['preprocesamiento'] is not b.named_steps['preprocesamiento']
            assert not hasattr(a.named_steps['clasificador'],'classes_')
            assert not hasattr(a.named_steps['preprocesamiento'].named_steps['columnas'],'transformers_')
            pp=clone(a.named_steps['preprocesamiento'])
            cols=core.predictores(scenario)
            train_positions,val_positions=cv[0]
            pp.fit(X.iloc[train_positions][cols])
            ct=pp.named_steps['columnas']
            num=[c for c in core.prep.NUMERICAS if c in cols]
            if modelo=='logistica':
                scale=ct.named_transformers_['numericas'].named_steps['escalado']
                assert scale.n_samples_seen_==28000
                assert np.allclose(scale.mean_,X.iloc[train_positions][num].mean())
            else:
                assert ct.named_transformers_['numericas']=='passthrough' or (
                    hasattr(ct.named_transformers_['numericas'],'func') and
                    ct.named_transformers_['numericas'].func is None)
            enc=ct.named_transformers_['categoricas']
            for c,categories in zip(core.prep.CATEGORICAS,enc.categories_):
                assert set(categories)==set(X.iloc[train_positions][c])
            unknown=X.iloc[val_positions[:1]][cols].copy()
            for c in core.prep.CATEGORICAS: unknown[c]='__unknown_test_only__'
            matrix=pp.transform(unknown)
            assert np.isfinite(matrix).all()
            assert np.count_nonzero(matrix[:,len(num):len(num)+sum(len(v) for v in enc.categories_)])==0
            assert set(np.unique(matrix[:,-1])).issubset({0.,1.})
    # Casos pequeños verifican orientación de matriz, orden textual y métrica indefinida.
    check=core.evaluar(['Low','Medium','High'],['High','Medium','High'])
    assert check['confusion']==[[0,0,1],[0,1,0],[0,0,1]]
    assert check['by_class']['Low']['precision_undefined']
    assert check['by_class']['High']['precision']==0.5 and check['by_class']['High']['recall']==1
    try: core.cargar('test')
    except RuntimeError: pass
    else: raise AssertionError('La carga ordinaria permitió acceder a prueba.')
    with tempfile.TemporaryDirectory() as tmp:
        folder=Path(tmp);file=folder/'dato.txt';file.write_text('original',encoding='utf-8')
        core._recibo(folder);file.write_text('alterado',encoding='utf-8')
        try: core._verificar_recibo(folder)
        except AssertionError: pass
        else: raise AssertionError('Se aceptó un artefacto alterado.')
    from unittest.mock import patch
    altered=core._configuracion();altered['seed']=99
    with patch.object(core,'_configuracion',return_value=altered):
        try: core.experimento_actual()
        except AssertionError: pass
        else: raise AssertionError('Se aceptó una configuración distinta en el mismo experimento.')
    return {'fresh_instances':'PASS','fold_only_scaler_and_categories':'PASS',
            'unknown_categories':'PASS','boolean_conversion':'PASS','metrics_order_and_orientation':'PASS',
            'test_guard':'PASS','corrupt_artifact_rejected':'PASS','changed_protocol_rejected':'PASS',
            'scenarios':[14,12]}


def verificar(directory=None):
    directory=directory or core.experimento_actual()
    m=core.verificar_entradas()
    selection=core._seleccion_valida(directory)
    splits={n:core.cargar(n,autorizacion_prueba=directory if n=='test' else None)
            for n in ['train','validation','test']}
    frames=[];counts=[]
    for n,(X,y,t) in splits.items():
        assert list(X)==core.prep.PREDICTORES and len(X.columns)==14
        assert not set(X)&{'Student_ID','_row_id',core.prep.OBJETIVO}
        counts.append({'partition':n,'rows':len(X),**{c:int(y.eq(c).sum()) for c in core.CLASES}})
        frames.append(pd.concat([t,X,y],axis=1))
    allrows=pd.concat(frames)
    assert len(allrows)==50000 and allrows.index.is_unique and allrows.Student_ID.is_unique
    assert set(allrows.index)==set(range(50000))
    original=pd.read_csv(core.ROOT/m['input']['path'],sep=';',encoding='utf-8-sig',float_precision='round_trip')
    restored=allrows.sort_index()[original.columns].reset_index(drop=True)
    pd.testing.assert_frame_equal(restored,original)
    table=core.tabla_comparacion(directory)
    assert len(table)==7
    fits=sum(core.cargar_resultado(n,s,directory)['cv']['fits'] for s in core.ESCENARIOS for n in core.MODELOS)
    fits+=core.cargar_resultado('dummy',directory=directory)['cv']['fits']+1
    assert fits==393
    for s in core.ESCENARIOS:
        for n in core.MODELOS:
            r=core.cargar_resultado(n,s,directory)
            path=directory/s/n/'busqueda_cv.csv'
            cv=pd.read_csv(path,sep=';',float_precision='round_trip')
            assert len(cv)==core.PRESUPUESTOS[n]
            assert [json.loads(p) for p in cv.params]==core.leer(directory/'protocolo.json')['configurations'][n]
            assert np.isclose(cv.mean_test_score.max(),r['cv']['macro_f1_mean'])
            if n=='logistica': assert r['interpretation']['converged']
    final=core.leer(directory/'final/resultado.json')
    assert final['selection_sha256']==core.sha(directory/'seleccion_modelo.json')
    event=core.leer(directory/'inicio_prueba.json');freeze=core.leer(directory/'seleccion_congelada.json')
    assert event['selection_sha256']==freeze['selection_sha256']
    assert datetime.fromisoformat(freeze['frozen_utc'])<=datetime.fromisoformat(event['started_utc'])
    assert event['model_sha256_before_test']==core.sha(directory/'final/pipeline_final.joblib')
    cp=subprocess.run([sys.executable,'-B','-X','utf8','-m','eduanalytics_modelado.verificacion',
                       '--worker',directory.name],cwd=core.FASE,capture_output=True,text=True,encoding='utf-8',check=True)
    independent=json.loads(cp.stdout)
    evidence={'experiment_id':directory.name,'input_hashes':'PASS','partitions':counts,
              'membership_order_and_coverage':'EXACT','reconstruction':'EXACT','row_and_student_overlap':0,
              'shared_folds':'PASS','full_protocol_fits':fits,'results_receipts':'PASS',
              'selection_before_test':'PASS','frozen_selection':'PASS',
              'directed_tests':pruebas_dirigidas(directory),'independent_load':independent,
              'phase3_manifest_sha256':core.sha(core.PREP/'manifest.json')}
    core.escribir_json(directory/'verificacion.json',evidence)
    return evidence


def reproducir_final(directory=None):
    """Reajuste idéntico congelado; conserva íntegra la evidencia original de prueba."""
    directory=directory or core.experimento_actual()
    selection=core._seleccion_valida(directory)
    Xt,yt,_=core.cargar('train');Xv,yv,_=core.cargar('validation')
    pipe=core.crear_pipeline(selection['model'],parametros=selection['hyperparameters'])
    with threadpool_limits(limits=1): pipe.fit(pd.concat([Xt,Xv]),pd.concat([yt,yv]))
    X,y,t=core.cargar('test',autorizacion_prueba=directory)
    metrics,pred,_,_=core.predecir(pipe,X,y,t)
    saved=pd.read_csv(directory/'final/predicciones_prueba.csv',sep=';',float_precision='round_trip')
    assert np.array_equal(pred.predicted,saved.predicted)
    assert np.allclose(pred[[f'prob_{c}' for c in core.CLASES]],saved[[f'prob_{c}' for c in core.CLASES]],rtol=0,atol=1e-12)
    assert core.canon(metrics)==core.canon(core.leer(directory/'final/resultado.json')['test'])
    out=core.ROOT/'.cache/modelado'/directory.name/'reproduccion'
    out.mkdir(parents=True,exist_ok=True)
    joblib.dump(pipe,out/'pipeline_reproducido.joblib',compress=3)
    result={'reproduced_frozen_experiment':directory.name,'predictions':'EXACT','metrics':'EXACT',
            'probabilities_max_abs_difference':float(np.max(np.abs(
                pred[[f'prob_{c}' for c in core.CLASES]].to_numpy()-saved[[f'prob_{c}' for c in core.CLASES]].to_numpy()))),
            'additional_verification_fits':1,'original_evidence_preserved':True}
    core.escribir_json(directory/'reproduccion_final.json',result)
    return result


def ejecutar_notebooks(directory,desde='raiz',incluir_prueba=False,nombres=None):
    from nbclient import NotebookClient
    from jupyter_client import KernelManager
    books=sorted(core.FASE.glob('*.ipynb'))
    if not incluir_prueba: books=[p for p in books if not p.name.startswith('06_')]
    if nombres is not None: books=[p for p in books if p.name[:2] in nombres]
    cache=core.ROOT/'.cache/modelado'/directory.name/'notebook_runtime'
    cache.mkdir(parents=True,exist_ok=True)
    records=[]
    for path in books:
        book=nbformat.read(path,as_version=4)
        for cell in book.cells:
            if cell.cell_type=='code':
                cell.outputs=[];cell.execution_count=None;cell.metadata.pop('execution',None)
        km=KernelManager(kernel_name='python3')
        km.kernel_spec.argv=[sys.executable,'-m','ipykernel_launcher','-f','{connection_file}']
        km.kernel_spec.env={}
        env=dict(os.environ,IPYTHONDIR=str(cache/'ipython'),MPLCONFIGDIR=str(cache/'matplotlib'),
                 JUPYTER_RUNTIME_DIR=str(cache/'runtime'),PYTHONDONTWRITEBYTECODE='1')
        env.pop('PYTHONPATH',None)
        cwd=core.ROOT if desde=='raiz' else core.FASE
        client=NotebookClient(book,km=km,timeout=7200,allow_errors=False,record_timing=False,
                              resources={'metadata':{'path':str(cwd)}})
        start=time.perf_counter();print('Notebook:',path.name,'desde',desde,flush=True)
        with client.setup_kernel(cwd=str(cwd),env=env,cleanup_kc=True): client.execute()
        for cell in book.cells:
            if cell.cell_type=='code':
                outputs=[]
                for output in cell.outputs:
                    if outputs and output.output_type=='stream' and outputs[-1].output_type=='stream' and output.name==outputs[-1].name:
                        outputs[-1].text+=output.text
                    else: outputs.append(output)
                cell.outputs=outputs;cell.metadata.pop('execution',None)
        nbformat.validate(book)
        path.write_text(nbformat.writes(book)+'\n',encoding='utf-8',newline='\n')
        records.append({'notebook':path.name,'cwd':desde,'seconds':time.perf_counter()-start,
                        'code_cells':sum(c.cell_type=='code' for c in book.cells),'errors':0,
                        'sha256':core.sha(path)})
    suffix='_parcial' if nombres is not None else ''
    core.escribir_json(directory/f'ejecucion_notebooks_{desde}{suffix}.json',records)
    if incluir_prueba and nombres is None:
        manifiesto(directory)
    return records


def manifiesto(directory=None):
    directory=directory or core.experimento_actual()
    assert core.leer(directory/'verificacion.json')['independent_load']['predictions']=='EXACT'
    for path in core.FASE.glob('*.ipynb'):
        book=nbformat.read(path,as_version=4)
        codes=[c for c in book.cells if c.cell_type=='code']
        assert [c.execution_count for c in codes]==list(range(1,len(codes)+1))
        assert not any(o.output_type=='error' for c in codes for o in c.outputs)
    published=list(core.FASE.glob('*.ipynb'))+list((core.FASE/'eduanalytics_modelado').glob('*.py'))
    published+=[core.FASE/'README_FASE4.md',core.FASE/'INFORME_FASE4_MODELADO.md',
            core.ROOT/'tools/ejecutar_modelado.py',core.ROOT/'tools/crear_notebooks_modelado.py',
            core.ROOT/'tools/verificar_modelado.py']
    # Conservar informes, fuentes y notebooks de cada identidad aunque cambie la vista actual.
    for p in published:
        dst=directory/'publicacion'/p.relative_to(core.ROOT)
        dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dst)
    files=list(directory.rglob('*'))+list((core.FASE/'figuras'/directory.name).glob('*.png'))
    artifacts={str(p.relative_to(core.ROOT).as_posix()):{'sha256':core.sha(p),'bytes':p.stat().st_size}
               for p in sorted(set(files)) if p.is_file() and p.name!='manifest.json'}
    m={'schema_version':1,'experiment_id':directory.name,'protocol_sha256':core.sha(directory/'protocolo.json'),
       'phase3_manifest_sha256':core.sha(core.PREP/'manifest.json'),'artifacts':artifacts,
       'current_published_files':{str(p.relative_to(core.ROOT).as_posix()):core.sha(p) for p in published},
       'publication_snapshot':'publicacion/ preserves code, notebooks and report for this experiment identity',
       'results_reproducible':'scores, folds, predictions; timings/dates are execution metadata',
       'excluded':'manifest itself, candidate caches, environments, private local files',
       'stage':'Fase 4 complete; Fase 5 business evaluation pending'}
    core.escribir_json(directory/'manifest.json',m)
    for rel,info in m['artifacts'].items(): assert core.sha(core.ROOT/rel)==info['sha256']
    for rel,h in m['current_published_files'].items(): assert core.sha(core.ROOT/rel)==h
    return m


def verificar_copia_limpia(directory=None):
    """Copia contenido actual destinado a Git, sin tocar índice ni usar cachés candidatos."""
    directory=directory or core.experimento_actual()
    cache=core.ROOT/'.cache/modelado';cache.mkdir(parents=True,exist_ok=True)
    target=Path(tempfile.mkdtemp(prefix='contenido_final_',dir=cache))
    tracked=subprocess.check_output(['git','ls-files','-z'],cwd=core.ROOT).decode('utf-8').split('\0')
    added=subprocess.check_output(['git','ls-files','--others','--exclude-standard','-z'],cwd=core.ROOT).decode('utf-8').split('\0')
    paths=sorted(set(tracked+added)-{''})
    forbidden=('.venv','venv','.cache','__pycache__','.ipynb_checkpoints','.git','.env')
    for rel in paths:
        p=Path(rel)
        assert not any(c in forbidden or c.startswith('.env.') for c in p.parts)
        src=core.ROOT/p
        assert src.is_file()
        dst=target/p;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst)
        assert core.sha(src)==core.sha(dst)
        if src.suffix in ['.py','.ipynb','.md','.csv','.json','.txt','.html','.js'] or p.name in ['.gitattributes','.gitignore']:
            assert b'\r\n' not in src.read_bytes(),f'CRLF en contenido final: {rel}'
    # Demostrar que los filtros reales de Git conservan los bytes de texto y binarios finales.
    for rel in paths:
        raw=subprocess.check_output(['git','hash-object','--no-filters','--',rel],cwd=core.ROOT).strip()
        filtered=subprocess.check_output(['git','hash-object',f'--path={rel}','--',rel],cwd=core.ROOT).strip()
        assert raw==filtered,f'La normalización Git modificaría {rel}'
    initial_files=len(paths)
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
    old=subprocess.run([sys.executable,'-B','-X','utf8','tools/verificar_proyecto.py'],cwd=target,
                        capture_output=True,text=True,encoding='utf-8',check=True,env=env)
    new=subprocess.run([sys.executable,'-B','-X','utf8','tools/ejecutar_modelado.py','verificar'],cwd=target,
                        capture_output=True,text=True,encoding='utf-8',check=True,env=env)
    books=subprocess.run([sys.executable,'-B','-X','utf8','tools/ejecutar_modelado.py','notebooks',
                          '--incluir-prueba','--desde','carpetas'],cwd=target,
                          capture_output=True,text=True,encoding='utf-8',check=True,env=env)
    final_manifest=core.leer(target/directory.relative_to(core.ROOT)/'manifest.json')
    for rel,info in final_manifest['artifacts'].items(): assert core.sha(target/rel)==info['sha256']
    assert core.sha(target/core.PREP.relative_to(core.ROOT)/'manifest.json')==core.sha(core.PREP/'manifest.json')
    result={'source':'current local content, not a clone of an earlier commit',
            'copy_relative_path':str(target.relative_to(core.ROOT).as_posix()),
            'initial_files':initial_files,'excluded_environments_and_caches':True,
            'git_filters_preserve_bytes':'PASS','phase1_2_3':json.loads(old.stdout),
            'phase4':json.loads(new.stdout),'seven_clean_notebooks':'PASS',
            'copy_manifest_hashes':'PASS','candidate_searches_repeated':0}
    core.escribir_json(directory/'copia_limpia.json',result)
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--worker',required=True)
    args=parser.parse_args();print(json.dumps(worker(core.ART/args.worker),ensure_ascii=False))
