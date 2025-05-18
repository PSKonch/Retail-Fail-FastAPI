"use client";
import { useEffect, useState } from "react";
import api from "@/lib/api";
import { useCartStore } from "@/store/cart";
import { useAuthStore } from "@/store/auth";
import { useRouter } from "next/navigation";

export default function CartPage() {
  const [loading, setLoading] = useState(true);
  const { items, setCart, clearCart } = useCartStore();
  const { token } = useAuthStore();
  const router = useRouter();

  useEffect(() => {
    if (!token) {
      router.push("/login");
      return;
    }
    api.get("/cart")
      .then(res => setCart(res.data))
      .finally(() => setLoading(false));
  }, [token, setCart, router]);

  const handleRemove = (product_id: number) => {
    api.delete("/cart", { params: { product_id } })
      .then(() => setCart(items.filter(item => item.product_id !== product_id)));
  };

  const handleClear = () => {
    api.delete("/cart/clear").then(() => clearCart());
  };

  const handleOrder = () => {
    api.post("/cart/order").then(() => {
      clearCart();
      alert("Заказ оформлен!");
      router.push("/orders");
    });
  };

  if (loading) return (
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

  // Подсчет суммы корзины
  const total = items.reduce((sum, item) => sum + item.product.price * item.quantity, 0);

  return (
    <div style={{
      maxWidth: 500,
      margin: "40px auto",
      background: "#fff",
      borderRadius: 20,
      boxShadow: "0 2px 16px rgba(30,32,34,0.06), 0 1.5px 4px #dbeafe",
      border: "1px solid #e5e7eb",
      padding: "38px 30px 28px 30px",
      fontFamily: "'Segoe UI', Arial, sans-serif"
    }}>
      <h1 style={{
        fontSize: "2rem",
        fontWeight: "bold",
        marginBottom: 24,
        display: "flex",
        alignItems: "center",
        gap: 10,
      }}>
        🛒 Корзина
      </h1>
      {items.length === 0 ? (
        <div style={{
          color: "#888",
          textAlign: "center",
          fontSize: "1.18rem",
          padding: "45px 0"
        }}>
          Корзина пуста
        </div>
      ) : (
        <>
          <ul style={{
            listStyle: "none",
            margin: 0,
            padding: 0,
            borderTop: "1px solid #e5e7eb",
            borderBottom: "1px solid #e5e7eb",
          }}>
            {items.map(item => (
              <li key={item.product_id} style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                padding: "17px 0",
                borderBottom: "1px solid #f3f4f6",
              }}>
                <div>
                  <span style={{fontWeight: "600"}}>{item.product.title}</span>
                  <span style={{
                    color: "#888",
                    marginLeft: 7,
                    fontSize: "1rem"
                  }}>
                    × {item.quantity}
                  </span>
                  <span style={{
                    color: "#374151",
                    marginLeft: 14,
                    fontWeight: "500"
                  }}>
                    {item.product.price} ₽
                  </span>
                </div>
                <button
                  style={{
                    marginLeft: 14,
                    padding: "6px 18px",
                    borderRadius: 11,
                    background: "#fee2e2",
                    color: "#be123c",
                    border: "none",
                    fontWeight: 500,
                    fontSize: "1rem",
                    cursor: "pointer",
                    transition: "background .18s"
                  }}
                  onClick={() => handleRemove(item.product_id)}
                >
                  ✖️ Удалить
                </button>
              </li>
            ))}
          </ul>
          <div style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            marginTop: 18,
            fontSize: "1.15rem"
          }}>
            <span style={{fontWeight: 500}}>Итого:</span>
            <span style={{fontWeight: "bold", fontSize: "1.19rem"}}>{total} ₽</span>
          </div>
        </>
      )}
      {items.length > 0 && (
        <div style={{
          display: "flex",
          gap: 12,
          marginTop: 30
        }}>
          <button
            style={{
              flex: 1,
              padding: "10px 0",
              borderRadius: 13,
              background: "#fbbf24",
              color: "#fff",
              border: "none",
              fontWeight: 600,
              fontSize: "1.08rem",
              cursor: "pointer",
              transition: "background .18s"
            }}
            onClick={handleClear}
          >
            Очистить корзину
          </button>
          <button
            style={{
              flex: 1,
              padding: "10px 0",
              borderRadius: 13,
              background: "#3b82f6",
              color: "#fff",
              border: "none",
              fontWeight: 600,
              fontSize: "1.08rem",
              cursor: "pointer",
              transition: "background .18s"
            }}
            onClick={handleOrder}
          >
            Оформить заказ
          </button>
        </div>
      )}
    </div>
  );
}
