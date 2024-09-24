from typing import Any
from datetime import datetime, timedelta, timezone

from passlib.context import CryptContext
from jose import jwt
from jose import JWTError
from pydantic import EmailStr

from fastapi import status, Request, Depends
from fastapi import HTTPException

from schema.user_schema import UserSchemaDb
from schema.user_schema import UserSchemaApi
import depends
from config import Settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """
    Возвращает хэш от строки
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return pwd_context.verify(secret=plain_password, hash=hashed_password)
    except Exception:
        return False


def create_access_token(data: dict[str, Any]) -> str:
    """Возвращает JWT токен с data и сроком действия exp"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(
        claims=to_encode,
        key=Settings.HASH_TOKEN,
        algorithm=Settings.ALGORITHM,
    )
    return encode_jwt


def create_user_token(user: UserSchemaDb):
    """Создание JWT токена для пользователя"""
    user_data = {"sub": f"{user.user_id}"}
    token = create_access_token(data=user_data)
    return token


async def authenticate_user(email: EmailStr, password: str):
    user_db = await depends.user_dao.find_one(email=email)
    if user_db is None:
        raise KeyError("User not found")
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    is_correct_password = verify_password(
        plain_password=password,
        hashed_password=user_db.hashed_password,
    )
    if not is_correct_password:
        raise ValueError("Incorrect password")
        # raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return user_db


def get_token(request: Request):
    token = request.cookies.get("recommendation_token")
    if not token:
        raise HTTPException(status_code=401, detail="Token not provided")
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token=token,
            key=Settings.HASH_TOKEN,
            algorithms=Settings.ALGORITHM,  # или ALGORITHM, если так указано в Settings
        )
    except JWTError:
        # return RedirectResponse(url="/auth/login")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
    # вроде декодирование истекшего токена приводит к JWTError
    # так что на время можно и не проверять
    expire: int | None = payload.get("exp")
    if not expire or expire < int(datetime.now(timezone.utc).timestamp()):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired"
        )

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user ID"
        )

    try:
        # Преобразуем user_id в int перед запросом
        user_id = int(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user ID format"
        )

    user = await depends.user_service.find_by_id(user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    return user


async def get_current_admin_user(
    current_user: UserSchemaApi = Depends(get_current_user)
):
    if current_user.role_id == 1:
        return current_user
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
