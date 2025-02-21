from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime
import requests
import os
from dotenv import load_dotenv
from pydantic import BaseModel

# Cargar variables de entorno
load_dotenv()

# Crear una instancia de FastAPI
app = FastAPI()

# Crear una instancia de Jinja2Templates
plantillas = Jinja2Templates(directory="template")

# Obtener la API_KEY de OpenWeatherMap
OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")

# Definir el modelo de datos con Pydantic
class Clima(BaseModel):
    ciudad: str
    descripcion: str
    temperatura: float
    icono: str

# Función para obtener el clima actual
def obtener_clima(ciudad: str):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={OPENWEATHERMAP_API_KEY}&units=metric&lang=es"
    respuesta = requests.get(url)

    if respuesta.status_code == 200:
        datos = respuesta.json()
        descripcion_clima = datos["weather"][0]["description"].strip().lower()

        # Mapeo de íconos de OpenWeatherMap a FontAwesome
        iconos_clima = {
            "cielo despejado": "fas fa-sun",
            "algo de nubes": "fas fa-cloud-sun",
            "muy nuboso": "fas fa-cloud",
            "cielo claro": "fas fa-sun",
            "nubes rotas": "fas fa-cloud-meatball",
            "lluvia de ligera intensidad": "fas fa-cloud-showers-heavy",
            "lluvia": "fas fa-cloud-rain",
            "lluvia ligera": "fas fa-cloud-rain",
            "lluvia moderada": "fas fa-cloud-rain",
            "tormenta": "fas fa-bolt",
            "nieve": "fas fa-snowflake",
            "niebla": "fas fa-smog",
            "nubes": "fas fa-cloud",
        }

        icono = iconos_clima.get(descripcion_clima, "fas fa-question")

        clima = Clima(
            ciudad=datos["name"],
            descripcion=descripcion_clima.capitalize(),
            temperatura=round(datos["main"]["temp"], 1),
            icono=icono
        )

        return clima
    else:
        return None

# Endpoint para servir la página principal
@app.get("/", response_model=Clima, response_class=HTMLResponse)
async def leer_inicio(request: Request, ciudad: str = Query(default="Cosamaloapan", min_length=2, description="Nombre de la ciudad")):
    hora_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Obtener el clima de la ciudad
    clima = obtener_clima(ciudad)

    # Renderizar con mensaje si no hay datos disponibles
    return plantillas.TemplateResponse("index.html", {
        "request": request,
        "hora_actual": hora_actual,
        "clima": clima,
        "error": "No se pudo obtener el clima. Intenta más tarde." if not clima else None
    })
