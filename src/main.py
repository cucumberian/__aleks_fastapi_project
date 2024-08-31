from routers.new_apart import new_aparts
from fastapi import FastAPI

app = FastAPI()

app.include_router(new_aparts)