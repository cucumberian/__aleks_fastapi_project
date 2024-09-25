from fastapi import APIRouter
from fastapi import Request
from fastapi import Depends
from fastapi.templating import Jinja2Templates

from routers.tables_router import router as tables_router
from routers.auth_router import router as auth_router

from auth.auth import get_current_user
from schema.user_schema import UserSchemaApi

index_router = APIRouter()

index_router.include_router(router=tables_router)
index_router.include_router(router=auth_router)

templates = Jinja2Templates(directory="./templates")


@index_router.get("/health", tags=["health"])
async def healthcheck():
    return {"status": "ok"}


@index_router.get("/")
async def read_index(
    request: Request,
    user: UserSchemaApi = Depends(get_current_user),
):
    return templates.TemplateResponse("index.html", {"request": request})
