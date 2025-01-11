from pydantic import BaseModel, EmailStr

class UserRequestAdd(BaseModel):
    username: str
    first_name: str
    second_name: str
    email: EmailStr
    password: str   

class UserAdd(BaseModel):
    username: str
    first_name: str
    second_name: str
    email: EmailStr
    hashed_password: str

class User(UserAdd):
    id: int
    is_active: bool
    role: str | None = None
 
class UserLogin(BaseModel):
    username: str
    password: str