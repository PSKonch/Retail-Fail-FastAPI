from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from src.db.postgres.database import Base

class PaymentModel(Base):
    __tablename__ = "payment"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("order.id"), unique=True)
    payment_intent_id: Mapped[str] = mapped_column(unique=True) 
    status: Mapped[str] = mapped_column(default="created") 
    
    order: Mapped["OrderModel"] = relationship("OrderModel", back_populates="payment") # type: ignore