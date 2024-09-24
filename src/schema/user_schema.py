from pydantic import BaseModel
from pydantic import EmailStr


class UserSchemaDbCreate(BaseModel):
    email: EmailStr
    hashed_password: str
    role_id: int | None = None
    name: str | None = None
    surname: str | None = None
    last_name: str | None = None


class UserSchemaDb(UserSchemaDbCreate):
    user_id: int


class UserSchemaApiCreate(BaseModel):
    email: EmailStr
    password: str


class UserSchemaApi(UserSchemaDb):
    pass


class UserSchemaApiLogin(BaseModel):
    email: EmailStr
    password: str


class UserSchemaApiResponse(BaseModel):
    user_id: int
    role_id: int | None
    surname: str | None
    name: str | None
    email: str
    last_name: str | None
