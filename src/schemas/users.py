from pydantic import BaseModel, EmailStr

class UserRequestAdd(BaseModel):
    first_name: str
    second_name: str
    email: EmailStr
    password: str   

class UserAdd(BaseModel):
    first_name: str
    second_name: str
    email: EmailStr
    hashed_password: str

class User(UserAdd):
    id: int
    is_active: bool

class UserLogin(BaseModel):
    email: EmailStr
    password: str