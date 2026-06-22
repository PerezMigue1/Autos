# Prediccion de precio de autos

Aplicacion web creada con Flask para desplegar en Render un modelo de regresion que predice el precio de venta (`selling_price`) de autos usando el dataset `processes2.csv`.

El proyecto entrena el modelo al iniciar, calcula metricas, genera graficas, guarda el modelo entrenado con `joblib` y permite hacer predicciones desde un formulario web.

## Requisitos

- Python 3.11 recomendado para Render.
- Python 3.14 tambien funciona localmente con las versiones compatibles del `requirements.txt`.
- Git instalado.
- Cuenta de GitHub.
- Cuenta de Render.

## Estructura del proyecto

```text
app.py
processes2.csv
requirements.txt
Procfile
runtime.txt
.python-version
.gitignore
README.md
Regresion_Processes2.ipynb
templates/
  index.html
static/
  styles.css
  charts/
model/
  modelo_autos.pkl
myenv/
```

## Crear entorno virtual

Desde la carpeta del proyecto:

```bash
python -m venv myenv
```

Activar el entorno virtual en Windows:

```bash
myenv\Scripts\activate
```

Cuando este activo, la terminal mostrara algo parecido a:

```text
(myenv)
```

## Instalar dependencias

Con el entorno virtual activo:

```bash
pip install -r requirements.txt
```

Dependencias principales:

```text
Flask
gunicorn
joblib
pandas
numpy
scikit-learn
matplotlib
seaborn
openpyxl
```

## Ejecutar localmente

Con el entorno virtual activo:

```bash
python app.py
```

Abrir en el navegador:

```text
http://127.0.0.1:5055/
```

## Que hace la aplicacion

- Carga el dataset `processes2.csv`.
- Entrena un modelo `RandomForestRegressor`.
- Predice la variable `selling_price`.
- Usa variables como marca, ano, kilometraje, potencia, rendimiento y motor.
- Calcula metricas `R2` y `MAE`.
- Genera graficas de valores reales vs predicciones y distribucion de residuos.
- Guarda el modelo entrenado en:

```text
model/modelo_autos.pkl
```

- Permite descargar resultados en CSV y Excel.

## Archivos importantes

`app.py`: contiene la aplicacion Flask, el entrenamiento del modelo, las rutas web y la exportacion del modelo con `joblib`.

`templates/index.html`: contiene la interfaz web.

`static/styles.css`: contiene los estilos visuales del sitio.

`requirements.txt`: contiene las dependencias necesarias.

`Procfile`: indica a Render como iniciar la aplicacion.

`.python-version`: fija Python 3.11.9 para Render.

`.gitignore`: evita subir carpetas y archivos innecesarios como `myenv/`, `__pycache__/` y `.env`.

## Procfile

El archivo `Procfile` debe estar en la raiz del proyecto y contiene:

```text
web: gunicorn app:app
```

## Git y GitHub

Inicializar repositorio, si todavia no existe:

```bash
git init
```

Agregar archivos:

```bash
git add .
```

Crear commit:

```bash
git commit -m "Initial commit"
```

Conectar con GitHub:

```bash
git remote add origin https://github.com/USUARIO/REPOSITORIO.git
```

Subir cambios:

```bash
git push -u origin main
```

Si el repositorio ya existe, despues de hacer cambios:

```bash
git add .
git commit -m "Actualizar proyecto"
git push
```

## Despliegue en Render

1. Subir el proyecto a GitHub.
2. Entrar a Render.
3. Crear un nuevo **Web Service**.
4. Seleccionar el repositorio de GitHub.
5. Configurar:

```text
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app
```

6. Verificar que Render use Python 3.11.9.

El proyecto incluye `.python-version` con:

```text
3.11.9
```

Si Render usa otra version de Python, agregar una variable de entorno:

```text
PYTHON_VERSION=3.11.9
```

7. Presionar **Deploy Web Service**.

Al terminar, Render mostrara una URL parecida a:

```text
https://nombre-del-servicio.onrender.com
```

## Comandos utiles

Activar entorno virtual:

```bash
myenv\Scripts\activate
```

Desactivar entorno virtual:

```bash
deactivate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Ejecutar aplicacion:

```bash
python app.py
```

Guardar dependencias instaladas:

```bash
pip freeze > requirements.txt
```

Ver estado de Git:

```bash
git status
```

Subir cambios:

```bash
git add .
git commit -m "Mensaje del cambio"
git push
```
