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

const STATUS_LABELS: Record<string, string> = {
  processing: "В обработке",
  arrived: "Доставлен",
  canceled: "Отменен",
  got: "Получен",
  pending: "В ожидании",
};

const STATUS_STYLES: Record<string, React.CSSProperties> = {
  arrived: {
    color: "#059669",
    background: "#d1fae5",
  },
  canceled: {
    color: "#be123c",
    background: "#fee2e2",
  },
  processing: {
    color: "#f59e42",
    background: "#fef3c7",
  },
  got: {
    color: "#2563eb",
    background: "#dbeafe",
  },
  pending: {
    color: "#78716c",
    background: "#f5f5f4",
  },
};

export default function OrdersPage() {
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  const { token } = useAuthStore();

  useEffect(() => {
    if (!token) return;
    api.get("/orders")
      .then(res => {
        console.log("orders from API:", res.data);
        setOrders(res.data[0]); // если массив массивов — как у тебя
      })
      .finally(() => setLoading(false));
  }, [token]);

  if (loading) {
    return (
      <div style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        height: "200px"
      }}>
        <span style={{
          fontSize: "20px",
          color: "#3b82f6"
        }}>Загрузка...</span>
      </div>
    );
  }

  return (
    <div style={{
      maxWidth: 700,
      margin: "40px auto",
      padding: "0 12px",
      fontFamily: "'Segoe UI', Arial, sans-serif",
    }}>
      <div style={{
        display: "flex",
        alignItems: "center",
        gap: 12,
        fontSize: "2.2rem",
        fontWeight: "bold",
        marginBottom: 32
      }}>
        <span style={{fontSize: "2rem"}}>🛒</span>
        Ваши заказы
      </div>
      {orders.length === 0 ? (
        <div style={{
          textAlign: "center",
          color: "#888",
          fontSize: "1.18rem",
          padding: "60px 0"
        }}>
          У вас нет заказов.
        </div>
      ) : (
        <div style={{
          display: "grid",
          gridTemplateColumns: "1fr",
          gap: 22,
        }}>
          {orders.map(order => (
            <div key={order.id} style={{
              background: "#fff",
              borderRadius: 20,
              boxShadow: "0 2px 16px rgba(30,32,34,0.06), 0 1.5px 4px #dbeafe",
              border: "1px solid #e5e7eb",
              padding: "28px 22px",
              display: "flex",
              flexDirection: "column",
              gap: 12,
              transition: "box-shadow .2s",
            }}>
              <div style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                fontSize: "1.13rem",
                fontWeight: 600
              }}>
                <span>Заказ #{order.id}</span>
                <span style={{
                  padding: "4px 16px",
                  borderRadius: 18,
                  fontSize: "0.98rem",
                  fontWeight: 500,
                  letterSpacing: "0.5px",
                  ...STATUS_STYLES[order.status] || { color: "#2563eb", background: "#dbeafe" }
                }}>
                  {STATUS_LABELS[order.status] || order.status}
                </span>
              </div>
              <div style={{
                color: "#374151",
                marginTop: 3,
                fontSize: "1rem"
              }}>
                Товаров: <span style={{fontWeight: "bold"}}>{order.items.length}</span><br />
                Сумма: <span style={{fontWeight: "bold"}}>{order.total} ₽</span>
              </div>
              <div style={{
                display: "flex",
                gap: 10,
                marginTop: 6
              }}>
                <button style={{
                  display: "inline-flex",
                  alignItems: "center",
                  gap: 7,
                  border: "none",
                  borderRadius: 13,
                  padding: "7px 17px",
                  fontSize: "1rem",
                  fontWeight: 500,
                  background: "#3b82f6",
                  color: "white",
                  cursor: "pointer",
                  transition: "background .18s"
                }}>
                  🔁 <span style={{marginLeft: 4}}>Повторить</span>
                </button>
                {(order.status === "processing" || order.status === "arrived") && (
                  <button style={{
                    display: "inline-flex",
                    alignItems: "center",
                    gap: 7,
                    border: "none",
                    borderRadius: 13,
                    padding: "7px 17px",
                    fontSize: "1rem",
                    fontWeight: 500,
                    background: "#fee2e2",
                    color: "#be123c",
                    cursor: "pointer",
                    transition: "background .18s"
                  }}>
                    ✖️ <span style={{marginLeft: 4}}>Отменить</span>
                  </button>
                )}
                {order.status === "got" && (
                  <span style={{
                    display: "inline-flex",
                    alignItems: "center",
                    gap: 7,
                    borderRadius: 13,
                    padding: "7px 17px",
                    fontSize: "1rem",
                    fontWeight: 500,
                    background: "#dbeafe",
                    color: "#2563eb",
                  }}>
                    ✔️ <span style={{marginLeft: 4}}>Получен</span>
                  </span>
                )}
                {order.status === "canceled" && (
                  <span style={{
                    display: "inline-flex",
                    alignItems: "center",
                    gap: 7,
                    borderRadius: 13,
                    padding: "7px 17px",
                    fontSize: "1rem",
                    fontWeight: 500,
                    background: "#f3f4f6",
                    color: "#888",
                  }}>
                    ✖️ <span style={{marginLeft: 4}}>Отменен</span>
                  </span>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
