from src.models.cart import CartModel
from src.models.order_items import OrderItemModel
from src.models.orders import OrderModel
from src.models.payments import PaymentModel
from src.models.products import ProductModel
from src.models.categories import CategoryModel
from src.models.users import UserModel
from src.repositories.mappers.base import DataMapper
from src.schemas.cart import Cart
from src.schemas.order import Order
from src.schemas.order_items import OrderItem
from src.schemas.payment import Payment
from src.schemas.products import Product
from src.schemas.categories import Category
from src.schemas.users import User


class ProductDataMapper(DataMapper):
    db_model = ProductModel
    schema = Product

class CartDataMapper(DataMapper):
    db_model = CartModel
    schema = Cart

class CategoryDataMapper(DataMapper):
    db_model = CategoryModel
    schema = Category

class OrderDataMapper(DataMapper):
    db_model = OrderModel
    schema = Order

class OrderItemDataMapper(DataMapper):
    db_model = OrderItemModel
    schema = OrderItem

class UserDataMapper(DataMapper):
    db_model = UserModel
    schema = User


class PaymentDataMapper(DataMapper):
    db_model = PaymentModel
    schema = Payment