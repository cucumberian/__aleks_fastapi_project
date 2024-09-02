from fastapi import FastAPI
from sqlalchemy import select
from models.new_apart import NewApart
from database import async_session_maker, schema
from sqlalchemy import text
from auth.router import router as auth_router

app = FastAPI()

app.include_router(auth_router)
