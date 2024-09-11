from fastapi import FastAPI
from routers.index_router import index_router

app = FastAPI()

app.include_router(router=index_router)