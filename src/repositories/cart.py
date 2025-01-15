from sqlalchemy import delete, insert, select, update
from sqlalchemy.orm import selectinload, joinedload
from src.models.cart import CartModel
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import CartDataMapper

class CartRepository(BaseRepository):
    model = CartModel
    mapper = CartDataMapper

    async def get_filtered(self, *filters, **filter_by):
        query = (
            select(self.model)
            .where(*filters, *[getattr(self.model, key) == value for key, value in filter_by.items()])
            .options(joinedload(self.model.product))  # Проверяем подгрузку товара
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def add(self, **values): # переопределенный классический метод add
        try:
            query = insert(self.model).values(**values)
            await self.session.execute(query)
        except Exception as e:
            raise ValueError(f"Failed to add entry to {self.model.__name__}: {e}")

    async def add_or_update_cart(self, user_id: int, product_id: int, quantity: int):
        existing_item = await self.get_filtered(
            CartModel.product_id == product_id,
            CartModel.user_id == user_id
        )

        if existing_item:
            await self.update(
                CartModel.product_id == product_id,
                CartModel.user_id == user_id,
                quantity=CartModel.quantity + quantity
            )
        else:
            await self.add(
                product_id=product_id,
                user_id=user_id,
                quantity=quantity
            )

    async def remove_or_decrease_quantity(
        self, user_id: int, product_id: int, quantity: int
    ):
        try:
            existing_item = await self.get_one_or_none(
                CartModel.user_id == user_id,
                CartModel.product_id == product_id
            )

            # Если количество меньше или равно запрошенному, удаляем элемент
            if existing_item.quantity <= quantity:
                query = delete(self.model).where(
                    self.model.user_id == user_id,
                    self.model.product_id == product_id
                )
            else:
                # Иначе уменьшаем количество
                query = (
                    update(self.model)
                    .where(
                        self.model.user_id == user_id,
                        self.model.product_id == product_id
                    )
                    .values(quantity=self.model.quantity - quantity)
                )

            await self.session.execute(query)
        except Exception as e:
            raise ValueError(f"Failed to remove or decrease quantity for item {product_id} in cart: {e}")

    async def clear_cart(self, user_id: int):
        try:
            query = delete(self.model).where(self.model.user_id == user_id)
            await self.session.execute(query)
        except Exception as e:
            raise ValueError(f"Failed to clear cart for user {user_id}: {e}")
