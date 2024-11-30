from src.models.cart import CartModel
from src.models.products import ProductModel
from src.models.categories import CategoryModel
from src.repositories.mappers.base import DataMapper
from src.schemas.cart import Cart
from src.schemas.products import Product
from src.schemas.categories import Category


class ProductDataMapper(DataMapper):
    db_model = ProductModel
    schema = Product

class CartDataMapper(DataMapper):
    db_model = CartModel
    schema = Cart

class CategoryDataMapper(DataMapper):
    db_model = CategoryModel
    schema = Category