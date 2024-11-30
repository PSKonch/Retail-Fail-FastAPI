from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.postgres.database import Base

class OrderItemModel(Base):
    __tablename__ = 'order_item'

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey('order.id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'))
    quantity: Mapped[int]
    price: Mapped[int]

    order: Mapped['OrderModel'] = relationship('OrderModel', back_populates='items') # type: ignore
    product: Mapped['ProductModel'] = relationship('ProductModel') # type: ignore