# Configuración del Entorno del Proyecto

Este documento resume las acciones realizadas para configurar correctamente el entorno de ejecución local de los notebooks del proyecto (`notebook_eduanalytics_md.ipynb` y `H3_1_Regresion_Logistica_EduAnalytics.ipynb`).

### 1. Creación del Entorno Virtual (`.venv`)
- Se inicializó un entorno virtual aislado en la carpeta raíz del proyecto (`c:\md-edu-analytics\.venv`).
- El objetivo de esto es evitar conflictos de versiones y aislar las librerías usadas en este proyecto de la instalación global de Python.

### 2. Creación del archivo `requirements.txt`
- Se creó un archivo listando las dependencias base requeridas para ejecutar el código y visualizar los datos. Las librerías incluidas fueron:
  - `pandas`
  - `numpy`
  - `matplotlib`
  - `seaborn`
  - `statsmodels`
  - `scikit-learn`
  - `ipykernel` (necesaria para ejecutar Jupyter Notebooks dentro del editor)

### 3. Instalación de Dependencias
- Se ejecutó el comando de instalación usando `pip install -r requirements.txt` apuntando directamente al entorno `.venv` recién creado, descargando e instalando satisfactoriamente todas las herramientas de ciencia de datos.

### 4. Corrección de Ruta del Dataset
- Se detectó y recomendó solucionar un error oculto en la **Celda 4** de `notebook_eduanalytics_md.ipynb`.
- **Ruta original:** `/mnt/data/ai_student_impact_dataset (1).csv` (pensada para entornos como Google Colab).
- **Ruta corregida:** `dataset/ai_student_impact_dataset (1).csv` (ruta local dentro del proyecto).

### 5. Selección del Intérprete en el IDE
- Se indicó el último paso manual para el usuario: elegir el entorno virtual (ruta: `.venv/Scripts/python.exe`) como el intérprete / Kernel oficial de Python en el editor, eliminando así las advertencias de importación (errores "missing-import") del analizador Pyrefly.
