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

  if (loading) return <div>Загрузка...</div>;

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Корзина</h1>
      {items.length === 0 ? (
        <div>Корзина пуста</div>
      ) : (
        <div>
          <ul>
            {items.map(item => (
              <li key={item.product_id} className="flex justify-between items-center py-2">
                <div>
                  {item.title} x {item.quantity}
                </div>
                <button className="btn btn-error" onClick={() => handleRemove(item.product_id)}>
                  Удалить
                </button>
              </li>
            ))}
          </ul>
          <button className="btn btn-warning mt-4 mr-2" onClick={handleClear}>
            Очистить корзину
          </button>
          <button className="btn btn-primary mt-4" onClick={handleOrder}>
            Оформить заказ
          </button>
        </div>
      )}
    </div>
  );
}
