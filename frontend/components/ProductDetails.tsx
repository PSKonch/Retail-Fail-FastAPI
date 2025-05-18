"use client";
import { useEffect, useState } from "react";
import api from "@/lib/api";
import { useAuthStore } from "@/store/auth";
import { useRouter } from "next/navigation";

type Product = {
  id: number;
  title: string;
  description?: string;
  quantity: number;
  price: number;
  slug: string;
};

export default function ProductDetails({ productId }: { productId: number }) {
  const [product, setProduct] = useState<Product | null>(null);
  const [loading, setLoading] = useState(true);
  const [quantity, setQuantity] = useState(1);
  const { token } = useAuthStore();
  const router = useRouter();

  useEffect(() => {
    api.get(`/categories/products`)
      .then(res => {
        const found = res.data.find((p: Product) => p.id === productId);
        setProduct(found);
      })
      .finally(() => setLoading(false));
  }, [productId]);

  const addToCart = async () => {
    if (!token) {
      router.push("/login");
      return;
    }
    await api.post(`/products?product_id=${productId}&quantity=${quantity}`);
    alert("Товар добавлен в корзину");
  };

  if (loading) return (
    <div style={{
      textAlign: "center",
      fontSize: "20px",
      color: "#3b82f6",
      margin: "40px 0"
    }}>Загрузка...</div>
  );
  if (!product) return (
    <div style={{
      textAlign: "center",
      color: "#888",
      fontSize: "1.12rem",
      margin: "40px 0"
    }}>Товар не найден</div>
  );

  return (
    <div style={{
      background: "#fff",
      borderRadius: 18,
      boxShadow: "0 2px 16px rgba(30,32,34,0.06)",
      border: "1px solid #e5e7eb",
      maxWidth: 440,
      margin: "40px auto",
      padding: "34px 22px",
      fontFamily: "'Segoe UI', Arial, sans-serif"
    }}>
      <h2 style={{
        fontSize: "2rem",
        fontWeight: 700,
        marginBottom: 14
      }}>{product.title}</h2>
      <div style={{
        fontSize: "1.09rem",
        color: "#374151",
        marginBottom: 12
      }}>{product.description}</div>
      <div style={{
        fontSize: "1rem",
        marginBottom: 9
      }}>В наличии: <b>{product.quantity}</b></div>
      <div style={{
        fontWeight: 700,
        fontSize: "1.21rem",
        marginBottom: 14
      }}>{product.price} ₽</div>
      <div>
        <input
          type="number"
          min={1}
          max={product.quantity}
          value={quantity}
          onChange={e => setQuantity(Number(e.target.value))}
          style={{
            border: "1px solid #d1d5db",
            borderRadius: 7,
            padding: "7px 13px",
            width: 80,
            marginRight: 16,
            fontSize: "1.07rem"
          }}
        />
        <button
          style={{
            padding: "9px 22px",
            borderRadius: 10,
            background: "#3b82f6",
            color: "#fff",
            fontWeight: 600,
            fontSize: "1.08rem",
            border: "none",
            cursor: "pointer"
          }}
          onClick={addToCart}
        >
          В корзину
        </button>
      </div>
    </div>
  );
}
