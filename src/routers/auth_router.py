from fastapi import APIRouter, HTTPException, status, Cookie, Response, Depends
from models.user import SUserAuth, UserResponse
from auth.dao import UserDAO
from auth.auth import get_password_hash, verify_password, create_access_token, authenticate_user, get_current_user, get_current_admin_user
from datetime import datetime, timedelta, timezone
from fastapi import Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix='/auth',
    tags=["Auth % Users"]
)

templates = Jinja2Templates(directory="./templates")

@router.post('/register')
async def register_user(user_data: SUserAuth):
    existing_user = await UserDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise HTTPException(status_code=403)
    hashed_password = get_password_hash(user_data.hashed_password)
    await UserDAO.create(email=user_data.email, hashed_password=hashed_password)
    return RedirectResponse(url="/auth/login", status_code=status.HTTP_303_SEE_OTHER)

@router.post('/login')
async def login_user(response: Response, user_data: SUserAuth):
    existing_user = await authenticate_user(user_data.email, user_data.hashed_password)
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    access_token = create_access_token({'sub': str(existing_user.user_id)})
    expire_time = datetime.now(timezone.utc) + timedelta(minutes=30)
    response.set_cookie("recommendation_token", access_token, httponly=True, expires=expire_time, path="/")

@router.post('/me')
async def get_me(current_user: int = Depends(get_current_user)):
    return current_user

@router.post('/logout')
async def logout_user(response: Response):
    response.delete_cookie("recommendation_token")

@router.get('/admin/users', response_model=UserResponse)
async def get_all_users(current_user: int = Depends(get_current_admin_user)):
    result = await UserDAO.get_info()
    return result

# Используйте GET для отображения страниц
@router.get("/login")  # Remove "auth/" if it's the root path
async def read_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/register") # Remove "auth/" if it's the root path
async def read_register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})
