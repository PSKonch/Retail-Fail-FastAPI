from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from src.db.postgres.database import Base

class CartModel(Base):
    __tablename__ = 'cart'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'))
    quantity: Mapped[int]