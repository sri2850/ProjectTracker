from pydantic import BaseModel, EmailStr


class User(BaseModel):
    username: str
    email: str | None = None
    disabled: bool | None = None


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True
