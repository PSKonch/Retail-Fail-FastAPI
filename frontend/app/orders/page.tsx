"use client";
import { useEffect, useState } from "react";
import api from "@/lib/api";
import { useAuthStore } from "@/store/auth";

type Order = {
  id: number;
  status: string;
  items: any[];
  total: number;
};

export default function OrdersPage() {
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  const { token } = useAuthStore();

  useEffect(() => {
    if (!token) return;
    api.get("/orders")
      .then(res => setOrders(res.data))
      .finally(() => setLoading(false));
  }, [token]);

  if (loading) return <div>Загрузка...</div>;

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Ваши заказы</h1>
      <ul>
        {orders.map(order => (
          <li key={order.id} className="mb-4 border rounded p-4">
            <div>Заказ #{order.id} — {order.status}</div>
            <div>Товаров: {order.items.length}</div>
            <div>Сумма: {order.total}</div>
            {/* Кнопка повторить заказ, отменить */}
          </li>
        ))}
      </ul>
    </div>
  );
}
