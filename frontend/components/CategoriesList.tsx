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

  if (loading) return <div>Загрузка...</div>;

  return (
    <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
      {categories.map(cat => (
        <div key={cat.id} className="bg-white p-4 rounded-xl shadow hover:shadow-md">
          <div className="font-bold text-lg">{cat.title}</div>
          <div className="text-xs text-gray-500">{cat.slug}</div>
          <Link href={`/category/${cat.id}`} className="text-blue-600 text-sm mt-2 inline-block">Смотреть товары</Link>
        </div>
      ))}
    </div>
  );
}
