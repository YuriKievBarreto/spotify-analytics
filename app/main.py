from fastapi import FastAPI

app = FastAPI(
    title="spotify analytics"
)

@app.get("/")
async def root():
    return {"message": "ola mundo, api rodando"}
