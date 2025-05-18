"use client";
import ProductDetails from "@/components/ProductDetails";
import { useParams } from "next/navigation";

export default function ProductPage() {
  const params = useParams();
  const productId = Number(params.id);

  return (
    <div>
      <ProductDetails productId={productId} />
    </div>
  );
}
