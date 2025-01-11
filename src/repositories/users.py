from src.models.users import UserModel
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import UserDataMapper


class UserRepository(BaseRepository):
    model = UserModel
    mapper = UserDataMapper