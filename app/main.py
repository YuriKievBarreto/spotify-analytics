from fastapi import FastAPI
from contextlib import asynccontextmanager
from models.usuario import Usuario
from core.database import init_db




print("rodando em http://localhost:8000")

@asynccontextmanager
async def lifespan(app: FastAPI):
  
    await init_db()
    print("aplicação rodando e conectada com o banco de dados")
    print("rodando em http://localhost:8000")


    yield 
    
   
    print("Aplicação encerrada, recursos liberados.")


app = FastAPI(
    title="spotify analytics",
    lifespan=lifespan
)

@app.get("/")
async def root():
    return {"message": "ola mundo, api rodando"}



