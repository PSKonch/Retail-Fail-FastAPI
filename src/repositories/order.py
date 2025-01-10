from sqlalchemy import select, update
from sqlalchemy.orm import selectinload, joinedload
from src.models.cart import CartModel
from src.models.order_items import OrderItemModel
from src.models.orders import OrderModel
from src.repositories.base import BaseRepository
from src.repositories.cart import CartRepository
from src.repositories.mappers.mappers import OrderDataMapper

class OrderRepository(BaseRepository):
    model = OrderModel
    mapper = OrderDataMapper

    async def create_order_with_cart(self, user_id: int):
        new_order = self.model(user_id=user_id, total_price=0, status='pending')
        self.session.add(new_order)
        await self.session.flush()

        query = (
            select(CartModel)
            .options(selectinload(CartModel.product)) 
            .where(CartModel.user_id == user_id)
        )
        result = await self.session.execute(query)
        cart_items = result.scalars().all()

        if not cart_items:
            raise ValueError("Корзина пользователя пуста")

        total_price = 0
        for cart_item in cart_items:
            item_price = cart_item.quantity * cart_item.product.price  
            total_price += item_price

            cart_item_data = {
                'product_id': cart_item.product_id,
                'quantity': cart_item.quantity,
                'price': cart_item.product.price,
                'order_id': new_order.id,
            }
            order_item = OrderItemModel(**cart_item_data)
            self.session.add(order_item)
            
        new_order.total_price = total_price
        await CartRepository(self.session).clear_cart(user_id=user_id)
        return new_order
    
    async def get_filtered(self, user_id: int | None = None, order_id: int | None = None):
        result = await self.session.execute(
            select(OrderModel)
            .options(selectinload(OrderModel.items).selectinload(OrderItemModel.product))  # Загружаем связанные данные
            .where(OrderModel.user_id == user_id, OrderModel.id == order_id)
        )
        return result.scalars().all()
    
    async def get_one_or_none(self, *filters, **filter_by):
        query = (select(self.model)
            .options(selectinload(self.model.items).selectinload(OrderItemModel.product))
            .filter(*filters).filter_by(**filter_by))
        result = await self.session.execute(query)
        return result.scalars().first() if result else None # Возвращает первый объект или None
    
    async def update(self, filters: dict, values: dict):
        query = update(self.model).where(*[getattr(self.model, key) == value for key, value in filters.items()]).values(**values)
        await self.session.execute(query)
    
    async def update_order_status(self, user_id: int, order_id: int, new_status: str):
        existing_order = await self.get_filtered(
            OrderModel.id == order_id,
            OrderModel.user_id == user_id
        )

        if existing_order:
            await self.update(
                OrderModel.id == order_id,
                OrderModel.user_id == user_id,
                values={"status": new_status}
            )
            return {"status": new_status}
        
        return {"error": "Order not found"}