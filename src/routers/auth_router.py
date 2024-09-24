from typing import Annotated
import datetime

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi import Depends
from fastapi import Body
from fastapi import status
from fastapi import Response

from fastapi import Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from fastapi.security import OAuth2PasswordBearer

from auth.auth import create_user_token
from auth.auth import authenticate_user
from auth.auth import get_current_user
from auth.auth import get_current_admin_user

from schema.user_schema import UserSchemaApiLogin
from schema.user_schema import UserSchemaApiResponse
from schema.user_schema import UserSchemaApiCreate
from schema.user_schema import UserSchemaApi

from service.user_service import UserService

from depends import get_user_service


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

router = APIRouter(prefix="/auth", tags=["Auth % Users"])

templates = Jinja2Templates(directory="./templates")


@router.post("/register")
async def register_user(
    user_data: UserSchemaApiCreate,
    user_service: UserService = Depends(get_user_service),
):
    created_user = await user_service.create(new_user=user_data)
    if created_user is None:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "User already registered"},
        )
    return RedirectResponse(url="/auth/login", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/login")
async def login_user(
    response: Response,
    user_data: UserSchemaApiLogin = Body(),
):
    try:
        existing_user = await authenticate_user(
            email=user_data.email,
            password=user_data.password,
        )
    except KeyError:
        return JSONResponse(
            status_code=404,
            content={"message": "User not found"},
        )
    except ValueError:
        return JSONResponse(
            status_code=401,
            content={"message": "Invalid password"},
        )

    access_token = create_user_token(user=existing_user)
    expire_time = datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=30)
    print(f"granted access_token: {access_token}")
    response.set_cookie(
        key="recommendation_token",
        value=access_token,
        httponly=True,
        expires=expire_time,
        path="/",
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/me")
@router.get("/me")
async def get_me(
    current_user: UserSchemaApi = Depends(get_current_user),
):
    return current_user


# куки можно удалять и через javascript на стороне клиента
# browser.cookies.remove({name: "recommendation_token", url: "/"})
@router.post("/logout")
@router.get("/logout")
async def logout_user(response: Response):
    response.delete_cookie(key="recommendation_token")
    return {"message": "Logout successful"}


@router.get("/admin/users", response_model=list[UserSchemaApiResponse])
async def get_all_users(
    current_admin_user: UserSchemaApi = Depends(get_current_admin_user),
    user_service: UserService = Depends(get_user_service),
):
    users = await user_service.get_all()
    return users


# Используйте GET для отображения страниц
@router.get("/login")  # Remove "auth/" if it's the root path
async def read_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/register")  # Remove "auth/" if it's the root path
async def read_register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})
