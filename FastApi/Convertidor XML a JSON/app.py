from fastapi import FastAPI
import requests
import xmltodict
from fastapi.responses import JSONResponse

# Creamos la instancia de FastAPI
app = FastAPI()

# Función para obtener el XML de una URL y convertirlo a JSON
def get_xml_data(url: str) -> dict:
    """ Obtener el XML de una URL y convertirlo a JSON. """
    try:
        response = requests.get(url)
        response.raise_for_status()
        xml_data = response.content
        return xmltodict.parse(xml_data)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

# Endpoint para obtener el XML de una URL
@app.get("/get-xml", response_class=JSONResponse)
async def get_xml(url: str):
    """Endpoint that receives a URL and returns the XML content."""
    xml_data = get_xml_data(url)
    return xml_data
