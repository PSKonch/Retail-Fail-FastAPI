from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import select, insert
from typing import Annotated
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

from src.models.users import UserModel
from src.schemas.users import User, UserRequestAdd, UserLogin
from src.db.postgres.database import database as db

router = APIRouter(prefix='/auth', tags=['Авторизация'])

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

SECRET_KEY = '8c367ae6527dbdb0f398d7670d9516d46e44b1bd8dd232912488ba7762d0df94'
ALGORITHM = 'HS256'

async def create_access_token(data: User, expire_delta: timedelta):
    encode = {
        'sub': data.username, 
        'id': data.id, 
        'email': data.email
    }
    expires = datetime.now(timezone.utc) + expire_delta
    encode.update({'exp': expires})

    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def auth_user(db: db, data: UserLogin):

    user = await db.scalar(select(UserModel).where(UserModel.username == data.username))
    
    if (not user) or (not bcrypt_context.verify(data.password, user.hashed_password)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    return user


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
    }


@router.post('/token', response_model=dict)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: db,  # Ваша зависимость для базы данных
):
    user_login = UserLogin(username=form_data.username, password=form_data.password)
    user = await auth_user(db, user_login)

    token = await create_access_token(user, expire_delta=timedelta(minutes=30))

    return {
        'access_token': token,
        'token_type': 'bearer'
    }


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(
    create_user: UserRequestAdd,
    db: db
):
    query = insert(UserModel).values(
        first_name=create_user.first_name,
        second_name=create_user.second_name,
        username=create_user.username,
        email=create_user.email,
        hashed_password=bcrypt_context.hash(create_user.password),
    )
    await db.execute(query)
    await db.commit()

    return {
        'status': 'success',
        'transaction': 'User created successfully',
    }