from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, ForeignKey

from src.db.postgres.database import Base

class ProductModel(Base):
    __tablename__ = 'product'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[str] = mapped_column(nullable=True)
    slug: Mapped[str]
    quantity: Mapped[int]
    price: Mapped[int]

    category_id: Mapped[int] = mapped_column(ForeignKey('category.id'))
    
    cart_items = relationship("CartModel", back_populates="product")