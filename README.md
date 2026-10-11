# EduAnalytics: Análisis de Patrones de Uso de IA Generativa y Riesgo de Burnout Estudiantil

## Presentación del proyecto

**Universidad:** Universidad Privada Franz Tamayo (UNIFRANZ)

**Materia:** Minería de Datos

### Integrantes

- Milenka Melody Chuquimia Osco
- Edson Teddy Tito Chuquimia
- Carlos Daniel Valverde Mendoza
- Alvaro Luis Carlos del Carpio Blanco
- Marcelo Josue Escobar Chipana

## Descripción general

EduAnalytics es un proyecto de minería de datos orientado al análisis de patrones de uso de inteligencia artificial generativa en estudiantes y su relación con variables académicas y de bienestar. Parte de un conjunto de datos obtenido de Kaggle que reúne información sobre uso de IA, hábitos de estudio, rendimiento académico, dependencia percibida, ansiedad, retención de habilidades y nivel de riesgo de burnout.

## Qué busca lograr

El proyecto busca identificar patrones de uso de IA generativa y hábitos académicos asociados con los niveles de riesgo de burnout, para apoyar el análisis de perfiles y futuras estrategias de uso responsable.

El proyecto analiza asociaciones presentes en el dataset; la etiqueta de riesgo de burnout no equivale a un diagnóstico clínico.

Para más detalles, consultar el [cuaderno de información general del proyecto](docs/notebook_eduanalytics_md.ipynb).

---

## Dataset del proyecto

El dataset utilizado en este proyecto se encuentra en la carpeta `dataset/` y se llama `ai_student_impact_dataset (1).csv`.

- URL: https://www.kaggle.com/datasets/ranaghulamnabi/ai-usage-and-student-academic-performance-analysis
- Título publicado: **AI Usage & Student Academic Performance Analysis**.
- Usuario publicador: **ranaghulamnabi**; nombre mostrado: **Coding expert G.N**.
- Licencia declarada por Kaggle: **CC0: Public Domain**.
- Versión consultada: **1**, única versión enumerada; nota: `Initial release`.
- Fecha de creación de esa versión según metadatos: **2026-05-15T18:10:29.143Z**. No es la fecha de descarga del equipo.
- Archivo contenido en el ZIP: `ai_student_impact_dataset (1).csv`; el ZIP contiene solamente ese CSV.

## Requisitos del Sistema e Instalación Paso a Paso

Para que cualquier persona pueda ejecutar y probar localmente cualquier notebook (`.ipynb`) o script (`.py`) del proyecto, debe seguir estos pasos:

### 1. Requisitos Previos (Software a Instalar)

- **Python:** Versión auditada y recomendada **Python 3.10.6** (compatible con Python 3.10.x). Verificar con:
  ```powershell
  python --version
  ```
- **Git:** Para clonar el repositorio y respetar los finales de línea configurados en `.gitattributes`.
- **Editor / IDE:** [Visual Studio Code](https://code.visualstudio.com/) con la extensión de **Python** y **Jupyter**, o en su defecto **JupyterLab** / **Jupyter Notebook**.

---

### 2. Pasos de Instalación y Configuración del Entorno

#### Paso 1: Abrir la terminal en la raíz del proyecto

Abrir PowerShell o CMD (en Windows) o la terminal (en Linux/macOS) en la carpeta raíz del repositorio (`md-edu-analytics`).

#### Paso 2: Crear el entorno virtual aislado (`.venv`)

- **Windows (PowerShell / CMD):**
  ```powershell
  python -m venv .venv
  ```
- **Linux / macOS:**
  ```bash
  python3 -m venv .venv
  ```

#### Paso 3: Activar el entorno virtual

- **Windows (PowerShell):**
  ```powershell
  .venv\Scripts\Activate.ps1
  ```
  _(Si PowerShell bloquea la ejecución de scripts, ejecutar previamente: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`)_
- **Windows (CMD):**
  ```cmd
  .venv\Scripts\activate.bat
  ```
- **Linux / macOS:**
  ```bash
  source .venv/bin/activate
  ```

#### Paso 4: Instalar las dependencias del proyecto

Actualizar pip e instalar los paquetes fijados en `requirements.txt`:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

_(Opcional para reproducción estricta byte a byte: usar `requirements-lock.txt` con las 66 dependencias exactas: `python -m pip install -r requirements-lock.txt`)_

#### Paso 5: Comprobar la integridad de la instalación

Verificar que no existan conflictos de paquetes ejecutando:

```powershell
pip check
```

_(Debe responder: `No broken requirements found.`)_

#### Paso 6: Registrar el kernel para Jupyter y VS Code

Para que VS Code o Jupyter reconozcan el entorno con el nombre oficial del proyecto:

```powershell
python -m ipykernel install --user --name eduanalytics-py3106 --display-name "EduAnalytics (Python 3.10.6)"
```

---

## Cómo Ejecutar y Probar el Proyecto

### A. Para Ejecutar Notebooks (`.ipynb`)

1. Abrir VS Code o ejecutar `jupyter notebook`.
2. Abrir cualquier cuaderno del repositorio:
   - **Cuaderno Maestro de Referencia (CRISP-DM Fases 1 a 4):** [`docs/notebook_eduanalytics_md.ipynb`](docs/notebook_eduanalytics_md.ipynb).
   - **Entregables Autónomos (100% aislados):** En la carpeta [`ENTREGABLES/`](ENTREGABLES/):
     - [`edu_analitycs_arbol_d_cl.ipynb`](ENTREGABLES/edu_analitycs_arbol_d_cl.ipynb) (Árbol de Decisión CART).
     - [`edu_analitycs_Regresion_L.ipynb`](ENTREGABLES/edu_analitycs_Regresion_L.ipynb) (Regresión Logística Multinomial).
     - [`evaluacion1_grupal_proyecto_crisp_autonomo.ipynb`](ENTREGABLES/evaluacion1_grupal_proyecto_crisp_autonomo.ipynb) (CRISP-DM Fases 1 a 4).
   - **Flujo Modular de Wrangler:** En [`wrangler/`](wrangler/) (`01_entendimiento_negocio`, `02_comprension_datos_eda`, `03_preparacion_datos`, `04_MODELADO/`).
3. En la esquina superior derecha del notebook, seleccionar el kernel: **EduAnalytics (Python 3.10.6)** o el intérprete `.venv`.
4. Seleccionar **Restart Kernel and Run All** (Reiniciar y ejecutar todo).

### B. Para Ejecutar Scripts de Automatización y Modelado (`.py`)

Con el entorno virtual activado:

- **Auditoría general de Fases 1, 2 y 3:**
  ```powershell
  python tools/verificar_proyecto.py
  ```
- **Automatización del Modelado (Fase 4):**
  ```powershell
  python tools/ejecutar_modelado.py comparar
  python tools/verificar_modelado.py
  ```

---

## Documentación Complementaria

- [Cuaderno Maestro de Referencia (CRISP-DM Fases 1 a 4)](docs/notebook_eduanalytics_md.ipynb)
- [Diccionario de Variables y Datos](docs/DICCIONARIO_DATOS.md)
- [Verificación y Auditoría de Fases 1, 2 y 3](docs/VERIFICACION_FASES_1_2_3.md)
- [Manual de Modelado y Protocolo Experimental (Fase 4)](wrangler/04_MODELADO/README_FASE4.md)
