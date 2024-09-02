from fastapi import APIRouter, HTTPException, status, Cookie, Response
from models.user import SUserAuth
from auth.dao import UserDAO
from .auth import get_password_hash, verify_password, create_acces_token, authenticate_user

router = APIRouter(
    prefix='/auth',
    tags=["Auth % Users"]
)

@router.post('/register')
async def register_user(user_data: SUserAuth):
    existing_user = await UserDAO.find_one_or_none(email = user_data.email)
    if existing_user:
        raise HTTPException(status_code=403)
    hashed_password = get_password_hash(user_data.hashed_password)
    await UserDAO.create(email = user_data.email, hashed_password= hashed_password)

@router.post('/login')
async def register_user(response : Response , user_data: SUserAuth):
    existing_user = await authenticate_user(user_data.email, user_data.hashed_password)
    print(existing_user)
    if  not existing_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    access_token = create_acces_token({'sub' : existing_user.user_id})
    response.set_cookie("recommendation_tocken", access_token)
    return access_token

        
