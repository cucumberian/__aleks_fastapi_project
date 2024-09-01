from fastapi import APIRouter, HTTPException
from models.user import SUserRegister
from auth.dao import UserDAO
from .auth import get_password_hash


router = APIRouter(
    prefix='/auth',
    tags=["Auth % Users"]
)

@router.post('/register')
async def register_user(user_data: SUserRegister):
    existing_user = await UserDAO.find_one_or_none(email = user_data.email)
    if existing_user:
        raise HTTPException(status_code=401)
    hashed_password = get_password_hash(user_data.hashed_password)
    await UserDAO.create_user(email = user_data.email, hashed_password= user_data.hashed_password)
    
    