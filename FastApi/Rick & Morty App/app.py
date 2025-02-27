from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import requests

# Create an instance of FastAPI
app = FastAPI()

# Montaje de la carpeta static
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configurar Jinja2Templates para usar la carpeta templates
templates = Jinja2Templates(directory="templates")

# Función para obtener a los personajes de la API
def obtener_personajes():
    url = "https://rickandmortyapi.com/api/character"
    personajes = []
    
    while url:  # Mientras haya más páginas de personajes
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                personajes.extend(data["results"])  # Añadir los personajes a la lista
                url = data.get("info", {}).get("next")  # Obtener la URL de la siguiente página
            else:
                break  # Si algo sale mal, se sale del bucle
        
            return personajes
    
# Endpoint para servir la página principal
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    personajes = obtener_personajes()
    return templates.TemplateResponse("index.html", {"request": request, "personajes": personajes})
