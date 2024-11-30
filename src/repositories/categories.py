from src.models.categories import CategoryModel
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import CategoryDataMapper

class CategoryRepository(BaseRepository):
    model = CategoryModel
    mapper = CategoryDataMapper