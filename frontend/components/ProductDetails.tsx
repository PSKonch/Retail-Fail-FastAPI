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

  if (loading) return <div>Загрузка...</div>;
  if (!product) return <div>Товар не найден</div>;

  return (
    <div className="bg-white p-6 rounded-xl shadow max-w-lg mx-auto">
      <h2 className="text-2xl font-bold mb-2">{product.title}</h2>
      <div className="mb-2">{product.description}</div>
      <div className="mb-2">В наличии: {product.quantity}</div>
      <div className="font-bold mb-4">{product.price} ₽</div>
      <input
        type="number"
        min={1}
        max={product.quantity}
        value={quantity}
        onChange={e => setQuantity(Number(e.target.value))}
        className="border p-2 rounded w-24 mb-4"
      />
      <button className="btn btn-primary ml-4" onClick={addToCart}>
        В корзину
      </button>
    </div>
  );
}
