# EduAnalytics: carga y modelado posterior a Fase 3

Estos archivos corresponden a clasificación retrospectiva multiclase de Burnout_Risk_Level.
Las etiquetas no son diagnósticos clínicos. Publicación Kaggle, versión 1 y licencia CC0 verificadas; fórmula, instrumentos y origen sintético pendientes. Véase docs/PROCEDENCIA_DATASET.md.

## Archivos

- train.csv, validation.csv y test.csv: registros originales separados por ;, UTF-8, con _row_id.
- variables.csv y decisiones_limpieza.csv: selección y reglas documentadas.
- manifest.json: huella de entrada, referencias, procedimiento, esquema, clases y hashes de salidas.
- preprocesamiento.py: crear_preprocesador(modelo) y cargar_particion(nombre, carpeta).
- requirements_preparacion.txt: versiones verificadas; Python 3.10.6 en esta ejecución.

## Carga desde un notebook de Fase 4

Ejecutar desde la raíz del proyecto o una carpeta dentro de él. Instalar las versiones indicadas
en un entorno virtual compatible cuando sea necesario: python -m pip install -r
wrangler/03_PREPARACION_DATOS/artefactos/requirements_preparacion.txt.

```python
from pathlib import Path
import sys
from sklearn.pipeline import Pipeline

raiz = next(p for p in (Path.cwd(), *Path.cwd().parents)
            if (p / 'README.md').is_file() and (p / 'wrangler').is_dir())
artefactos = raiz / 'wrangler/03_PREPARACION_DATOS/artefactos'
sys.path.insert(0, str(artefactos))
from preprocesamiento import cargar_particion, crear_preprocesador

X_train, y_train, traza_train = cargar_particion('train', artefactos)
X_val, y_val, traza_val = cargar_particion('validation', artefactos)
preprocesador_logistica = crear_preprocesador('logistica')
preprocesador_arbol = crear_preprocesador('arbol')
```

X contiene los mismos 14 predictores en el mismo orden. y conserva Low, Medium y High como texto.
La trazabilidad contiene _row_id y Student_ID. No añadir esas columnas ni el objetivo a X.
El lector verifica el hash, esquema, tamaño y clases de cada partición antes de entregarla.

## Ajuste correcto dentro de Fase 4

Crear el clasificador en la Fase 4 e integrarlo en un pipeline completo:

```python
# modelo_fase4 será una regresión logística o un árbol definidos en la Fase 4.
pipeline_completo = Pipeline([
    ('preprocesamiento', crear_preprocesador('logistica')),  # 'arbol' para el árbol
    ('clasificador', modelo_fase4),
])
```

Pasar ese pipeline sin ajustar a la validación cruzada usando SOLO X_train e y_train.
Cada pliegue aprenderá su propio escalado y categorías. No reutilizar las matrices ni las
copias diagnósticas ajustadas en Fase 3. También se puede comparar candidatos con validación,
manteniendo cualquier ajuste de preprocesamiento en entrenamiento.

Prueba se carga únicamente cuando se haya cerrado la selección del modelo:

```python
X_test, y_test, traza_test = cargar_particion('test', artefactos)
```

El manifiesto y las particiones ya están fijados: no volver a dividir los datos en los notebooks
de cada modelo. Cualquier reentrenamiento final con entrenamiento + validación se decidirá en
Fase 4 antes de evaluar prueba y mantendrá prueba completamente fuera de todo ajuste.

## Límites y decisiones pendientes

- Evaluar macro F1, matriz de confusión y precision/recall/F1 por clase, especialmente High.
  El KPI High global es 24,974 % y no es una métrica predictiva.
- La validación previa usa todos los registros disponibles para una auditoría de calidad y
  continuidad, sin seleccionar modelos con prueba. La Fase 2 exploró el mismo CSV completo:
  prueba no puede considerarse una cohorte externa nunca inspeccionada. La selección de modelos
  debe respetar el bloqueo actual y una validación externa requeriría datos nuevos.
- La publicación original está verificada. Confirmar recolección, escala GPA, instrumentos, momentos de observación y fórmula de etiqueta.
- Evaluar sensibilidad sin GPA final y retención con las mismas particiones. Eso no convierte
  automáticamente al resto de variables en información disponible para detección anticipada.
- Investigar posible circularidad de horas, dependencia, ansiedad u otros predictores con la etiqueta.
- GPA_Change queda como propuesta secundaria, fuera del conjunto principal.
- No aplicar SMOTE, recortes, imputación o selección de variables por defecto. Si se evalúan,
  ajustar cada operación solo dentro de entrenamiento o del pliegue correspondiente.
- One-hot maneja categorías desconocidas con un bloque de ceros. Revisar su frecuencia y
  significado cuando se apliquen estos pipelines a nuevos datos.
