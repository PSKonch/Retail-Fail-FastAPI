from src.models.products import ProductModel
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import ProductDataMapper

class ProductRepository(BaseRepository):
    model = ProductModel
    mapper = ProductDataMapper

    