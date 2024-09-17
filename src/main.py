from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse
from routers.index_router import index_router

app = FastAPI()

app.include_router(router=index_router)

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 401:
        return RedirectResponse(url="/auth/login")
    return await request.app.exception_handler(request, exc)