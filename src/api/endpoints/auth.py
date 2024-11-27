from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert
from typing import Annotated
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

from src.models.users import UserModel
from src.schemas.users import User, UserAdd, UserRequestAdd, UserLogin
from src.db.postgres.database import database as db

router = APIRouter(prefix='/auth', tags=['auth'])


bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

SECRET_KEY = '8c367ae6527dbdb0f398d7670d9516d46e44b1bd8dd232912488ba7762d0df94'
ALGORITHM = 'HS256'


async def create_access_token(username: str, user_id: int, 
                              is_supplier: bool, is_customer: bool, is_admin: bool, 
                              expire_delta: timedelta):

    encode = {
        'sub': username, 
        'id': user_id, 
        'is_admin': is_admin, 
        'is_supplier': is_supplier, 
        'is_customer': is_customer
    }
    expires = datetime.now(timezone.utc) + expire_delta
    encode.update({'exp': expires})

    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def auth_user(db: db, data: UserLogin):

    user = await db.scalar(select(User).where(User.email == data.email))
    
    if (not user) or (not user.is_active) or (not bcrypt_context.verify(data.password, user.hashed_password)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    return user


@router.post('/token')
async def login(db: db, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):

    user = await auth_user(db, form_data.username, form_data.password)

    if not user or user.is_active == False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='User not found or inactive'
        )
    
    token = await create_access_token(user.username, user.id, 
                                      user.is_supplier, user.is_customer, user.is_admin, 
                                      expire_delta=timedelta(minutes=30))
    
    return {
        'access_token': token,
        'token_type': 'bearer'
    }


async def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )


@router.get('/me')
async def read_current_user(token: Annotated[str, Depends(oauth2_scheme)]):

    payload = await decode_token(token)
    return {
        "username": payload.get("sub"),
        "user_id": payload.get("id"),
        "is_admin": payload.get("is_admin"),
        "is_supplier": payload.get("is_supplier"),
        "is_customer": payload.get("is_customer")
    }


@router.post('/')
async def create_user(db: db, create_user: UserRequestAdd):

    await db.execute(insert(User).values(first_name=create_user.first_name, 
                                         last_name=create_user.second_name, 
                                         username=create_user.username, 
                                         email=create_user.email, 
                                         hashed_password=bcrypt_context.hash(create_user.password)))
    await db.commit()

    return {
        'status': status.HTTP_201_CREATED,
        'transaction': 'success'
    }