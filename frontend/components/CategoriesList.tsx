"use client";
import { useEffect, useState } from "react";
import api from "@/lib/api";
import Link from "next/link";

type Category = {
  id: number;
  title: string;
  slug: string;
};

export default function CategoriesList() {
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get("/categories/")
      .then(res => setCategories(res.data))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  if (loading) return (
    <div style={{
      textAlign: "center",
      fontSize: "20px",
      color: "#3b82f6",
      margin: "40px 0"
    }}>Загрузка...</div>
  );

  return (
    <div style={{
      display: "grid",
      gridTemplateColumns: "1fr",
      gap: 22,
      maxWidth: 950,
      margin: "0 auto",
      marginTop: 30,
      marginBottom: 30
    }}>
      {/* Адаптивность: 4 колонки на больших экранах */}
      <style>{`
        @media (min-width: 900px) {
          .categories-grid {
            grid-template-columns: repeat(4, 1fr);
          }
        }
      `}</style>
      <div className="categories-grid" style={{
        display: "grid",
        gridTemplateColumns: "1fr",
        gap: 22
      }}>
        {categories.map(cat => (
          <div key={cat.id} style={{
            background: "#fff",
            padding: "28px 20px",
            borderRadius: 18,
            boxShadow: "0 2px 16px rgba(30,32,34,0.06)",
            border: "1px solid #e5e7eb",
            display: "flex",
            flexDirection: "column",
            alignItems: "flex-start",
            transition: "box-shadow .2s",
          }}>
            <div style={{
              fontWeight: 700,
              fontSize: "1.18rem",
              marginBottom: 4
            }}>{cat.title}</div>
            <div style={{
              fontSize: "0.91rem",
              color: "#64748b",
              marginBottom: 8
            }}>{cat.slug}</div>
            <Link href={`/categories/${cat.id}`} style={{
              color: "#2563eb",
              fontSize: "0.99rem",
              marginTop: 8,
              textDecoration: "none",
              fontWeight: 500
            }}>
              Смотреть товары →
            </Link>
          </div>
        ))}
      </div>
    </div>
  );
}
