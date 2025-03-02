from typing import List, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from src.db.postgres.database import Base

# статусы указаны в src.utils.constants

class OrderModel(Base):
    __tablename__ = 'order'

    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[str]
    total_price: Mapped[int]

    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))

    items: Mapped[List['OrderItemModel']] = relationship('OrderItemModel', back_populates='order') # type: ignore
    payment: Mapped[Optional["PaymentModel"]] = relationship("PaymentModel", back_populates="order") # type: ignore