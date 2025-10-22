from fastapi import FastAPI
from fastapi import APIRouter
from .api.main_router import mainRouter
from contextlib import asynccontextmanager
from app.models.usuario import Usuario
from app.core.database import init_db
from fastapi.middleware.cors import CORSMiddleware


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

app.add_middleware(
    CORSMiddleware,
    allow_origins=[""
    "   http://localhost:5500",  # Se você usar localhost
        "http://127.0.0.1:5500",],                      # Permite requisições destas origens
    allow_credentials=True,                     # Permite cookies de autenticação
    allow_methods=["*"],                        # Permite todos os métodos (GET, POST, etc.)
    allow_headers=["*"],                        # Permite todos os cabeçalhos
)

app.include_router(mainRouter)

@app.get("/")
async def root():
    return {"message": "ola mundo, api rodando"}



