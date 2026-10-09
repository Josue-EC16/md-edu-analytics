from pathlib import Path
import hashlib
import io
import json

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, OneHotEncoder, StandardScaler

CLASES = ['Low', 'Medium', 'High']
OBJETIVO = 'Burnout_Risk_Level'
NUMERICAS = ['Pre_Semester_GPA', 'Weekly_GenAI_Hours', 'Tool_Diversity', 'Traditional_Study_Hours',
            'Perceived_AI_Dependency', 'Anxiety_Level_During_Exams', 'Post_Semester_GPA', 'Skill_Retention_Score']
CATEGORICAS = ['Major_Category', 'Year_of_Study', 'Primary_Use_Case', 'Prompt_Engineering_Skill', 'Institutional_Policy']
BOOLEANAS = ['Paid_Subscription']
PREDICTORES = ['Major_Category', 'Year_of_Study', 'Pre_Semester_GPA', 'Weekly_GenAI_Hours',
              'Primary_Use_Case', 'Prompt_Engineering_Skill', 'Tool_Diversity', 'Paid_Subscription',
              'Traditional_Study_Hours', 'Perceived_AI_Dependency', 'Institutional_Policy',
              'Anxiety_Level_During_Exams', 'Post_Semester_GPA', 'Skill_Retention_Score']
TRAZABILIDAD = ['_row_id', 'Student_ID']

def crear_preprocesador(modelo):
    """Pipeline nuevo sin ajustar; no contiene clasificador ni usa etiquetas."""
    if modelo not in {'logistica', 'arbol'}:
        raise ValueError("Modelo debe ser 'logistica' o 'arbol'.")
    numerico = Pipeline([('escalado', StandardScaler())]) if modelo == 'logistica' else 'passthrough'
    columnas = ColumnTransformer([
        ('numericas', numerico, NUMERICAS),
        ('categoricas', OneHotEncoder(drop=None, handle_unknown='ignore', sparse_output=False), CATEGORICAS),
        ('booleanas', FunctionTransformer(np.asarray, kw_args={'dtype': np.float64},
                                         feature_names_out='one-to-one'), BOOLEANAS),
    ], remainder='drop', sparse_threshold=0)
    return Pipeline([('columnas', columnas)])

def cargar_particion(nombre, carpeta):
    """Carga una partición original y verifica hash, esquema, tipos, tamaño y clases."""
    if nombre not in {'train', 'validation', 'test'}:
        raise ValueError("Partición debe ser 'train', 'validation' o 'test'.")
    carpeta = Path(carpeta)
    manifiesto = json.loads((carpeta / 'manifest.json').read_text(encoding='utf-8'))
    if manifiesto['schema_version'] != 1 or manifiesto['schema']['predictors'] != PREDICTORES:
        raise ValueError('Manifiesto incompatible con las funciones de preparación.')
    informacion = manifiesto['partitions'][nombre]
    if informacion['file'] != f'{nombre}.csv':
        raise ValueError('Nombre de archivo de partición inesperado.')
    contenido = (carpeta / informacion['file']).read_bytes()
    if hashlib.sha256(contenido).hexdigest() != manifiesto['artifacts'][informacion['file']]['sha256']:
        raise ValueError(f'Hash incorrecto en {informacion["file"]}; no se utiliza una partición modificada.')
    tipos = dict(manifiesto['schema']['original_dtypes'])
    tipos.update({'_row_id': 'int64', 'Paid_Subscription': 'string'})
    datos = pd.read_csv(io.BytesIO(contenido), sep=';', encoding='utf-8', dtype=tipos,
                        float_precision='round_trip')
    if list(datos.columns) != manifiesto['schema']['partition_columns']:
        raise ValueError('Columnas o su orden no coinciden con el manifiesto.')
    if datos['Paid_Subscription'].isna().any() or not datos['Paid_Subscription'].isin(['True', 'False']).all():
        raise ValueError('Paid_Subscription contiene un valor distinto de True/False.')
    datos['Paid_Subscription'] = datos['Paid_Subscription'].map({'True': True, 'False': False}).astype(bool)
    if datos.isna().any().any() or not np.isfinite(datos[NUMERICAS].to_numpy()).all():
        raise ValueError('La partición no cumple la calidad sin nulos/no finitos registrada.')
    if len(datos) != informacion['rows'] or not datos['_row_id'].is_unique or not datos['Student_ID'].is_unique:
        raise ValueError('Tamaño o identificadores de la partición inconsistentes.')
    if not datos[OBJETIVO].isin(CLASES).all():
        raise ValueError('Objetivo con clases inesperadas.')
    conteos = {c: int(datos[OBJETIVO].eq(c).sum()) for c in CLASES}
    if conteos != informacion['class_counts'] or not all(conteos.values()):
        raise ValueError('Distribución o presencia de clases no coincide con el manifiesto.')
    datos.index = pd.Index(datos['_row_id'].to_numpy(), name='_row_id')
    X = datos[PREDICTORES].copy()
    y = datos[OBJETIVO].copy()
    trazabilidad = datos[TRAZABILIDAD].copy()
    assert X.index.equals(y.index) and X.index.equals(trazabilidad.index)
    return X, y, trazabilidad
