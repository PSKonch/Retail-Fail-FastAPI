from typing import Annotated

from fastapi import Depends, HTTPException, status
from jose import JWTError

from src.api.endpoints.auth import oauth2_scheme
from src.db.postgres.manager import DBManager
from src.db.postgres.database import async_session_maker
from src.services.auth_service import decode_token

async def user_id_dependency(token: Annotated[str, Depends(oauth2_scheme)]) -> int:
    try:
        payload = await decode_token(token)
        user_id = payload.get("id")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )
        return user_id
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    
current_user_id = Annotated[int, Depends(user_id_dependency)]

async def user_email_dependency(token: Annotated[str, Depends(oauth2_scheme)]) -> int:
    try:
        payload = await decode_token(token)
        user_email = payload.get("email")
        if not user_email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )
        return user_email
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    
current_user_email = Annotated[str, Depends(user_email_dependency)]
    
async def get_db():
    async with DBManager(session_factory=async_session_maker) as db:
        yield db

db_manager = Annotated[DBManager, Depends(get_db)]