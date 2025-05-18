"use client";
import ProductsList from "@/components/ProductsList";
import { useParams } from "next/navigation";

export default function CategoryPage() {
  const params = useParams();
  const categoryId = Number(params.id);

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Товары категории</h1>
      <ProductsList categoryId={categoryId} />
    </div>
  );
}
