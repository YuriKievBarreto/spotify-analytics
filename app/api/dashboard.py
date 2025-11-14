from fastapi import APIRouter, Request
dashboard_router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

@dashboard_router.get("/?user_id")
async def dashboard(request: Request):
    user_id = request.query_params.get("user_id")
    return {"id do usuario: ", }