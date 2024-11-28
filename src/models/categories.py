from sqlalchemy.orm import relationship, mapped_column, Mapped

from src.db.postgres.database import Base

class CategoryModel(Base):
    __tablename__ = 'category'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    slug: Mapped[str]