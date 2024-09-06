from fastapi import FastAPI, Request
from sqlalchemy import select
from models.new_apart import NewApart
from database import async_session_maker, schema
from sqlalchemy import text
from auth.router import router as auth_router
from routers.tabels import router as table_router
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Optional, List
from fastapi import Query

app = FastAPI()
# Подключаем статическую папку

templates = Jinja2Templates(directory="../templates")


app.include_router(auth_router)
app.include_router(table_router)

@app.get("/")
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})