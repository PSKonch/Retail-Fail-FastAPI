from src.models.cart import CartModel
from src.models.products import ProductModel
from src.repositories.mappers.base import DataMapper
from src.schemas.cart import Cart
from src.schemas.products import Product

class ProductDataMapper(DataMapper):
    db_model = ProductModel
    schema = Product

class CartDataMapper(DataMapper):
    db_model = CartModel
    schema = Cart