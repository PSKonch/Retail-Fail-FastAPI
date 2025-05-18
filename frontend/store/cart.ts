import { create } from "zustand";

type CartItem = {
  product_id: number;
  title: string;
  quantity: number;
  price: number;
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
