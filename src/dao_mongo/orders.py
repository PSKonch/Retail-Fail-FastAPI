from bson.objectid import ObjectId
from pymongo import DESCENDING

from src.db.mongodb.manager import mongodb_manager
from src.db.postgres.database import async_session_maker
from src.models.order_items import OrderItemModel
from src.models.orders import OrderModel

async def get_last_order_mongo(
        user_id: int,
):
    result = await mongodb_manager.db["order_history"].find_one(
        {"user_id": user_id},
        sort=[("order_id", DESCENDING)]
    )
    if result:
        result["_id"] = str(result["_id"])
    return result

async def reorder_last_order_mongo(
        user_id: int
):
    last_order = await get_last_order_mongo(user_id)
    async with async_session_maker() as session:
        order_to_reorder = OrderModel(
            user_id=user_id,
            total_price=last_order["total_price"],
            status="pending"
        )
        session.add(order_to_reorder)
        await session.flush()

        reorder_order_items = [
            OrderItemModel(
                order_id=order_to_reorder.id,
                quantity=item["quantity"],
                price=item["price"],
                product_id=item["product_id"]
            )
            for item in last_order["items"]
        ]
        session.add_all(reorder_order_items)
        await session.commit()
        return order_to_reorder