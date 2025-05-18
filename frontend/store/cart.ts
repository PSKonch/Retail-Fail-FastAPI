import { create } from "zustand";

type Product = {
  id: number;
  title: string;
  price: number;
  description?: string;
  quantity: number;
  slug: string;
};

type CartItem = {
  product_id: number;
  quantity: number;
  id: number;
  user_id: number;
  product: Product;
};

type CartState = {
  items: CartItem[];
  setCart: (items: CartItem[]) => void;
  clearCart: () => void;
};

export const useCartStore = create<CartState>((set) => ({
  items: [],
  setCart: (items) => set({ items }),
  clearCart: () => set({ items: [] }),
}));
