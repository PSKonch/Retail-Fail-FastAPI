from sqlalchemy import delete, select

from src.core.celery_app import celery_app
from src.db.postgres.database import SessionLocal
from src.db.mongodb.manager import mongodb_manager
from src.models.order_items import OrderItemModel
from src.models.orders import OrderModel

@celery_app.task
def migrate_old_orders():
    """Перенос заказов со статусами 'got' и 'canceled' в MongoDB"""
    
    with SessionLocal() as session:
        # Ищем заказы в PostgreSQL
        query = select(OrderModel).where(OrderModel.status.in_(["got", "canceled"]))
        result = session.execute(query)
        orders = result.scalars().all()

        if not orders:
            print("Нет заказов для переноса.")
            return

        # Подключаем MongoDB (синхронный режим)
        mongodb_manager.connect_sync()

        # Переносим заказы
        orders_to_mongo = [
            {
                "order_id": order.id,
                "user_id": order.user_id,
                "items": [
                    {
                        "product_id": item.product_id,
                        "quantity": item.quantity,
                        "price": item.price
                    } for item in order.items
                ],
                "total_price": order.total_price,
                "status": order.status,
            }
            for order in orders
        ]

        # Сохраняем в MongoDB (синхронный insert)
        mongodb_manager.sync_db["order_history"].insert_many(orders_to_mongo)
        print(f"Перенесено {len(orders_to_mongo)} заказов в MongoDB")

        session.execute(
            delete(OrderItemModel).where(OrderItemModel.order_id.in_(
                session.query(OrderModel.id).filter(OrderModel.status.in_(["got", "canceled"]))
            ))
        )

        # Удаляем заказы из PostgreSQL
        session.execute(
            delete(OrderModel).where(OrderModel.status.in_(["got", "canceled"]))
        )
        session.commit()
        print("Удалены заказы из PostgreSQL")

        # Закрываем соединение с MongoDB
        mongodb_manager.close_sync()


@celery_app.task
def update_order_status(order_id: int, order_status: str):
    """Обновляет статус заказа в БД"""
    with SessionLocal() as session:
        order = session.query(OrderModel).filter_by(id=order_id).first()
        if order and order.status not in ["canceled", "got"]:
            session.query(OrderModel).filter_by(id=order_id).update({"status": order_status})
            session.commit()