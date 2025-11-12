from fastapi import FastAPI
from fastapi import APIRouter
from .api.main_router import mainRouter
from contextlib import asynccontextmanager
from app.models.usuario import Usuario
from fastapi.staticfiles import StaticFiles
from app.core.database import init_db
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from pathlib import Path


import uvicorn


print("rodando em http://localhost:8000")



@asynccontextmanager
async def lifespan(app: FastAPI):
  
    await init_db()
    print("aplicação rodando e conectada com o banco de dados")
    print("rodando em http://localhost:8000/api/v1/auth/login")
    print("rodando em http://localhost:8000/")


    yield 
    
   
    print("Aplicação encerrada, recursos liberados.")


app = FastAPI(
    title="spotify analytics",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[""
    "   http://localhost:5500",  
        "http://127.0.0.1:5500",
        "http://127.0.0.1:8000"],                     
    allow_credentials=True,
    allow_methods=["*"],                        
    allow_headers=["*"],                        
)

app.include_router(mainRouter)

app.mount(
    "/static", 
    StaticFiles(directory=Path("app/static")), 
    name="static"
)


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def serve_dashboard():
    """Serve o arquivo HTML principal quando o usuário acessa a raiz."""
    # Garanta que o caminho para o seu arquivo HTML esteja correto
    dashboard_path = Path("app/static/index.html")
    
    if not dashboard_path.is_file():
        return HTMLResponse("<h1>Erro 404: Arquivo dashboard.html não encontrado.</h1>")
        
    return FileResponse(dashboard_path)



if __name__ == "__main__":
    uvicorn.run("app.main:app", host="localhost", port=8000, reload=True)



