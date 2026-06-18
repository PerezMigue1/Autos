# Prediccion de precio de autos

Aplicacion Flask para desplegar en Render un modelo de regresion entrenado con `processes2.csv`.

## Ejecutar localmente

```bash
pip install -r requirements.txt
python app.py
```

## Despliegue en Render

1. Sube este proyecto a GitHub.
2. Crea un nuevo servicio **Web Service** en Render.
3. Usa estos comandos:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
4. Publica el servicio.

La app entrena el modelo al iniciar, guarda el modelo entrenado en `model/modelo_autos.pkl`, muestra metricas de evaluacion, permite descargar resultados y predice el precio de venta con los datos del formulario.
