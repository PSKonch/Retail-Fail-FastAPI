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

  if (loading) return <div>Загрузка...</div>;
  if (!products.length) return <div>Нет товаров</div>;

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      {products.map(product => (
        <div key={product.id} className="bg-white rounded-xl p-6 shadow">
          <div className="font-bold text-lg">{product.title}</div>
          <div className="text-gray-500 text-sm mb-2">{product.description}</div>
          <div>В наличии: {product.quantity}</div>
          <div className="font-bold mb-2">{product.price} ₽</div>
          <button
            className="btn btn-primary"
            onClick={() => router.push(`/product/${product.id}`)}
          >
            Подробнее
          </button>
        </div>
      ))}
    </div>
  );
}
