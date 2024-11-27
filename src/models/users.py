from sqlalchemy import Boolean, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from src.db.postgres.database import Base

class UserModel(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str]
    second_name: Mapped[str]
    username: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)
