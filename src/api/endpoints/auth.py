from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, OAuth2PasswordRequestFormStrict
from datetime import timedelta
from src.schemas.users import UserAdd, UserRequestAdd, UserLogin
from src.db.postgres.manager import DBManager
from src.services.auth_service import AuthService, bcrypt_context
from src.db.postgres.database import async_session_maker 

router = APIRouter(prefix="/auth", tags=["Авторизация"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

async def get_auth_service():
    async with DBManager(async_session_maker) as db:
        yield AuthService(db)

@router.get("/me")
async def read_current_user(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(get_auth_service),
):
    payload = await auth_service.decode_token(token)
    return {
        "username": payload.get("sub"),
        "user_id": payload.get("id"),
    }

@router.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service),
):
    user_login = UserLogin(username=form_data.username, password=form_data.password)
    user = await auth_service.authenticate_user(user_login)
    token = await auth_service.create_access_token(user, expire_delta=timedelta(minutes=30))

    return {
        "access_token": token,
        "token_type": "bearer",
    }

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(
    create_user: UserRequestAdd,
    auth_service: AuthService = Depends(get_auth_service),
):
    hashed_password = bcrypt_context.hash(create_user.password)
    user_data = UserAdd(
        username=create_user.username,
        first_name=create_user.first_name,
        second_name=create_user.second_name,
        email=create_user.email,
        hashed_password=hashed_password
    )
    
    await auth_service.user_repo.add(user_data)

    return {
        "status": "success",
        "transaction": "User created successfully",
    }