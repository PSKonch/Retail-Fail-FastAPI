from typing import List
from fastapi import APIRouter
from sqlalchemy import select

from src.models.users import UserModel
from src.tasks.notifications import notify_user_about_orders_status
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

        # Отправка уведомлений на почту
        notify_user_about_orders_status.apply_async(args=[current_user_email, "pending", new_order.id])

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
    

@router.post("/order/{order_id}/to_user/{user_id}")
async def give_an_order_to_user(
    db: db_manager,
    employee_id: current_user_id,
    user_id: int,
    order_id: int
):
    """Эндпоинт сотрудника постамата, пользователь сообщает свой id (сменить на имя/почту)
    и номер заказа. После чего сотрудник вводит данные в запрос и меняет статус заказа
    """
    try:
        employee = await db.user.get_one_or_none(id=employee_id)
        if not employee or employee.role not in ["super_user", "supplier"]:
            return {"status": "error", "message": "Ошибка доступа"}
        
        user = await db.user.get_one_or_none(id=user_id)
        if not user:
            return {"status": "Пользователь не существует"}

        order = await db.order.get_one_or_none(user_id=user_id, id=order_id)
        if (not order) or (order.status != "arrived"):
            return {"status": "error", "message": "Заказ не найден или не поступил"}

        await db.order.update(
            filters={"user_id": user_id, "id": order_id},
            values={"status": "got"}
        )   
        await db.commit()
        
        notify_user_about_orders_status.apply_async(args=[user.email, "got", order.id])

        return {"status": "ok"}

    except Exception as e:
        await db.rollback()
        return {"status": "error", "message": str(e)}


@router.post("/orders/delivery")
async def delivery_an_order_to_post(
    db: db_manager,
    supplier_id: current_user_id,
    order_ids: List[int]
):
    try:
        supplier = await db.user.get_one_or_none(id=supplier_id)
        if not supplier or supplier.role not in ["super_user", "supplier"]:
            return {"status": "error", "message": "Ошибка доступа"}

        arrived_orders = []

        # Обновляем заказы, которые можно перевести в статус "arrived"
        for order_id in order_ids:
            order = await db.order.get_one_or_none(id=order_id)
            if not order:
                return {"status": "error", "message": f"Заказ {order_id} не найден"}

            await db.order.update(
                filters={"id": order_id},
                values={"status": "arrived"}
            )
            arrived_orders.append(order)

        await db.commit()

        # Отправляем уведомления пользователям о статусе заказов
        for order in arrived_orders:
            user = await db.user.get_one_or_none(id=order.user_id)
            if user:
                notify_user_about_orders_status.apply_async(args=[user.email, "arrived", order.id])

        return {"status": "ok"}

    except Exception as e:
        await db.rollback()
        return {"status": "error", "message": str(e)}