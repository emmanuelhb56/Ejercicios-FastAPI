from fastapi import FastAPI
# Create a FastAPI instance
app = FastAPI()
# Endpoint de bienvenida
@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de la práctica"}

# Endpoint de saludo
@app.get("/users/{user_id}")
def read_user(user_id: int, q: str = None):
    return 
    {
        "user_id": user_id,
        "q": q,
        "name": "John Doe",
        "age": 25,
        "email": "oKu8o@example.com",
        "is_active": True,
        "is_admin": False
    }
# Endpoint de items
@app.get("/sumar")
def sumar(num1: int, num2: int):
    return {"resultado": num1 + num2}
