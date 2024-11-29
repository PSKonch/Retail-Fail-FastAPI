from typing import Annotated

from fastapi import Depends, HTTPException, status
from jose import JWTError

from src.api.endpoints.auth import decode_token, oauth2_scheme
from src.db.postgres.manager import DBManager
from src.db.postgres.database import async_session_maker

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
    
async def get_db():
    async with DBManager(session_factory=async_session_maker) as db:
        yield db

db_manager = Annotated[DBManager, Depends(get_db)]