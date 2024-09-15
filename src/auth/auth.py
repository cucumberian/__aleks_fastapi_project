from typing import Any
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt
from pydantic import EmailStr
from auth.dao import UserDAO
from config import Settings
from fastapi import HTTPException, status, Request, Depends
from jose import JWTError, jwt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict[str, Any]) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(
        to_encode,
        Settings.HASH_TOKEN,
        algorithm=Settings.ALGORITHM,
    )
    return encode_jwt

async def authenticate_user(email: EmailStr, password: str):
    user = await UserDAO.find_one_or_none(email=email)
    if not user:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if not verify_password(password, user.hashed_password):
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return user

def get_token(request: Request):
    token = request.cookies.get('recommendation_token')
    if not token:
        raise HTTPException(status_code=401)
    return token

async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token,
            Settings.HASH_TOKEN,
            Settings.ALGORITHM,  # или ALGORITHM, если так указано в Settings
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

    expire: int = payload.get("exp")
    if not expire or expire < int(datetime.now(timezone.utc).timestamp()):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")

    user_id: str = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user ID")
    
    try:
        # Преобразуем user_id в int перед запросом
        user_id = int(user_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user ID format")

    user = await UserDAO.find_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    
    return user

async def get_current_admin_user(current_user: UserDAO = Depends(get_current_user)):
    if current_user.role_id == 1:
        return current_user
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    
    
