from fastapi import APIRouter

from src.tasks.notifications import notify_user_about_orders_status
from src.tasks.orders import update_order_status
from src.utils.dependencies import db_manager, current_user_id, current_user_email

router = APIRouter(prefix='', tags=['Заказ'])

@router.get("/orders")
async def get_all_orders(
    db: db_manager,
    user_id: current_user_id,   
):
    return await db.order.get_filtered(user_id=user_id)

@router.get('/order/{order_id}')
async def get_order_by_order_id(
    db: db_manager,
    user_id: current_user_id,
    order_id: int
):
    return await db.order.get_filtered(user_id=user_id, order_id=order_id)

@router.post("/cart/order")
async def create_order(
    db: db_manager,
    current_user: current_user_id,
    current_user_email: current_user_email
):
    try:
        new_order = await db.order.create_order_with_cart(user_id=current_user)
        await db.commit()

        # Обновление статуса в БД + отправка уведомлений
        update_order_status.apply_async(args=[new_order.id, "pending"])
        notify_user_about_orders_status.apply_async(args=[current_user_email, "pending", new_order.id])

        # Todo: Создать эндпоинт для перевозчика, который принимает массив из заказов и меняет их статус на arrived
        # Имитация доставки заказа в пункт выдачи за 15 минут
        update_order_status.apply_async(args=[new_order.id, "arrived"], countdown=15)
        notify_user_about_orders_status.apply_async(args=[current_user_email, "arrived", new_order.id], countdown=15)

        return {"status": "ok", "order_id": new_order.id, "total_price": new_order.total_price}
    
    except ValueError as e:
        await db.rollback()
        return {"status": "error", "message": str(e)}
    
@router.delete("/order/{order_id}/cancel")
async def cancel_order(
    db: db_manager, 
    current_user_id: current_user_id,
    current_user_email: current_user_email,
    order_id: int
):
    try: 
        order = await db.order.get_one_or_none(user_id=current_user_id, id=order_id)

        if not order:
            return {"status": "error", "message": "Заказ не найден."}
        
        if order.status == "got":
            return {"status": "error", "message": "Этот заказ уже получен и не может быть отменен."}

        await db.order.update(
            filters={"id": order_id, "user_id": current_user_id},
            values={"status": "canceled"}
        )
        await db.commit()      

        notify_user_about_orders_status.apply_async(args=[current_user_email, "canceled", order.id])

        return {"status": "ok"}

    except ValueError as e:
        await db.rollback()
        return {"status": "error", "message": str(e)}
