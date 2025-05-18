"use client";
import { useEffect, useState } from "react";
import api from "@/lib/api";
import { useRouter } from "next/navigation";

type Product = {
  id: number;
  title: string;
  description?: string;
  quantity: number;
  price: number;
  slug: string;
};

export default function ProductsList({ categoryId }: { categoryId: number }) {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    api.get(`/categories/${categoryId}/products`)
      .then(res => setProducts(res.data))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [categoryId]);

  if (loading) return (
    <div style={{
      textAlign: "center",
      fontSize: "20px",
      color: "#3b82f6",
      margin: "40px 0"
    }}>Загрузка...</div>
  );
  if (!products.length) return (
    <div style={{
      textAlign: "center",
      color: "#888",
      fontSize: "1.15rem",
      margin: "40px 0"
    }}>Нет товаров</div>
  );

  return (
    <div style={{
      display: "grid",
      gridTemplateColumns: "1fr",
      gap: 26,
      maxWidth: 1100,
      margin: "0 auto",
      marginTop: 25,
      marginBottom: 25
    }}>
      {/* Адаптивность: 3 колонки на больших экранах */}
      <style>{`
        @media (min-width: 900px) {
          .products-grid {
            grid-template-columns: repeat(3, 1fr);
          }
        }
      `}</style>
      <div className="products-grid" style={{
        display: "grid",
        gridTemplateColumns: "1fr",
        gap: 26
      }}>
        {products.map(product => (
          <div key={product.id} style={{
            background: "#fff",
            borderRadius: 16,
            padding: "26px 18px",
            boxShadow: "0 2px 16px rgba(30,32,34,0.06)",
            border: "1px solid #e5e7eb",
            display: "flex",
            flexDirection: "column",
            transition: "box-shadow .2s"
          }}>
            <div style={{
              fontWeight: 700,
              fontSize: "1.13rem",
              marginBottom: 5
            }}>{product.title}</div>
            <div style={{
              color: "#64748b",
              fontSize: "0.97rem",
              marginBottom: 8
            }}>{product.description}</div>
            <div style={{marginBottom: 4}}>В наличии: <b>{product.quantity}</b></div>
            <div style={{
              fontWeight: 600,
              fontSize: "1.11rem",
              marginBottom: 12
            }}>{product.price} ₽</div>
            <button
              style={{
                padding: "9px 0",
                borderRadius: 10,
                background: "#3b82f6",
                color: "#fff",
                fontWeight: 600,
                fontSize: "1rem",
                border: "none",
                cursor: "pointer",
                marginTop: "auto"
              }}
              onClick={() => router.push(`/product/${product.id}`)}
            >
              Подробнее
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
