from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

# Configurar CORS para permitir acceso desde cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Clave de la API de Football Data
API_KEY = "9d00f3f179a24d6d978832791978026d"
BASE_URL = "https://api.football-data.org/v4"

# Header para autenticación en la API
headers = {"X-Auth-Token": API_KEY}

# Buscar equipos por nombre de la liga Premier League
@app.get("/buscar_equipo/{nombre}")
def buscar_equipo(nombre: str):
    url = f"{BASE_URL}/competitions/PL/teams"  # Se consulta la liga Premier League
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        equipos = response.json().get("teams", [])
        resultados = [
            {
                "id": equipo["id"],
                "nombre": equipo["name"],
                "shortName": equipo["shortName"],
                "tla": equipo["tla"],
                "escudo": equipo["crest"],
                "pais": equipo["area"]["name"],
                "bandera": equipo["area"]["flag"],
                "colores": equipo["clubColors"],
                "estadio": equipo["venue"],
                "fundacion": equipo["founded"],
                "sitio_web": equipo["website"]
            }
            for equipo in equipos if nombre.lower() in equipo["name"].lower()
        ]
        
        if not resultados:
            raise HTTPException(status_code=404, detail="No se encontraron equipos con ese nombre")
        
        return resultados
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)

# Obtener información de un equipo por ID
@app.get("/equipo/{equipo_id}")
def obtener_equipo(equipo_id: str):
    url = f"{BASE_URL}/teams/{equipo_id}"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        jugadores = data.get("squad", [])  # Manejo seguro de jugadores
        
        return {
            "id": data["id"],
            "nombre": data["name"],
            "shortName": data["shortName"],
            "tla": data["tla"],
            "escudo": data["crest"],
            "pais": data["area"]["name"],
            "bandera": data["area"]["flag"],
            "colores": data["clubColors"],
            "estadio": data["venue"],
            "fundacion": data["founded"],
            "sitio_web": data["website"],
            "jugadores": [
                {
                    "nombre": jugador.get("name", "Desconocido"),
                    "posicion": jugador.get("position", "No especificado"),
                    "nacionalidad": jugador.get("nationality", "No disponible")
                }
                for jugador in jugadores
            ]
        }
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)

