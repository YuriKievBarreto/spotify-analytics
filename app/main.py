from fastapi import FastAPI
from models.usuario import Usuario
from core.database import init_db


app = FastAPI(
    title="spotify analytics"
)

print("rodando em http://localhost:8000")




@app.get("/")
async def root():
    return {"message": "ola mundo, api rodando"}



