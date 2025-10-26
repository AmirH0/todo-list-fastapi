from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TodoBase(BaseModel):
    title: str
    description: str | None = None

class TodoCreate(TodoBase):
    pass

class TodoRead(TodoBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True