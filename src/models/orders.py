from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

from src.db.postgres.database import Base

class OrderModel(Base):
    __tablename__ = 'order'

    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[str]
    total_price: Mapped[int]

    user_id: Mapped[int] = mapped_column(ForeignKey ('user.id'))