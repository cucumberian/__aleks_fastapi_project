from fastapi import APIRouter, FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi import Request
from fastapi.templating import Jinja2Templates
from routers.tabels_router import router as tabels_router
from routers.auth_router import router as auth_router
from fastapi import Depends
from auth.auth import get_current_user

index_router = APIRouter()

index_router.include_router(router=tabels_router)
index_router.include_router(router=auth_router)

templates = Jinja2Templates(directory="./templates")

@index_router.get("/health", tags=['health'])
async def healthcheck():
    return {"status": "ok"}

@index_router.get("/")
async def read_index(request: Request, user = Depends(get_current_user)):
    return templates.TemplateResponse("index.html", {"request": request})

