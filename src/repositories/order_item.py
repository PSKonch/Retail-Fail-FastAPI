from src.models.order_items import OrderItemModel
from src.repositories.base import BaseRepository
from src.repositories.cart import CartRepository
from src.repositories.mappers.mappers import OrderItemDataMapper
from src.schemas.order_items import OrderItem

class OrderItemRepository(BaseRepository):
    model = OrderItemModel
    mapper = OrderItemDataMapper

    async def set_to_order_from_cart(self, user_id: int, order_id: int):
        cart_items = await CartRepository(self.session).get_filtered(user_id=user_id)

        for cart_item in cart_items:
            cart_item_data = {
                'product_id': cart_item.product_id,
                'quantity': cart_item.quantity,
                'price': cart_item.product.price,
                'order_id': order_id
            }
            order_item = self.mapper.map_to_persistence_entity(OrderItem(**cart_item_data))
            self.session.add(order_item)
        
        await CartRepository(self.session).clear_cart(user_id=user_id)
        