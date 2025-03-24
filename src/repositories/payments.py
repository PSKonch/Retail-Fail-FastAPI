from sqlalchemy import insert, update

from src.models.payments import PaymentModel
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import PaymentDataMapper

class PaymentRepository(BaseRepository):
    model = PaymentModel
    mapper = PaymentDataMapper

    async def add(self, **values): # переопределенный классический метод add
        try:
            query = insert(self.model).values(**values)
            await self.session.execute(query)
        except Exception as e:
            raise ValueError(f"Failed to add entry to {self.model.__name__}: {e}")
        
    async def update(self, filters: dict, values: dict):
        query = update(self.model).where(*[getattr(self.model, key) == value for key, value in filters.items()]).values(**values)
        await self.session.execute(query)