from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import jwt, JWTError
from fastapi import HTTPException, status
from src.db.postgres.manager import DBManager  
from src.schemas.users import UserLogin, User

SECRET_KEY = '8c367ae6527dbdb0f398d7670d9516d46e44b1bd8dd232912488ba7762d0df94'
ALGORITHM = 'HS256'
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

class AuthService:
    def __init__(self, db_manager: DBManager):
        self.db_manager = db_manager
        self.user_repo = db_manager.user  

    async def create_access_token(self, user: User, expire_delta: timedelta) -> str:
        encode = {
            "sub": user.username,
            "id": user.id,
            "email": user.email
        }
        expires = datetime.now(timezone.utc) + expire_delta
        encode.update({"exp": expires})
        return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    async def decode_token(self, token: str) -> dict:
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    async def authenticate_user(self, data: UserLogin):
        user = await self.user_repo.get_by_username(data.username)
        if not user or not bcrypt_context.verify(data.password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        return user
    
async def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")