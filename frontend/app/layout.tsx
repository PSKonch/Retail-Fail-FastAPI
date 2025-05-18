import './globals.css';
import type { Metadata } from 'next';
import { ReactNode } from 'react';
import Link from 'next/link';

export const metadata: Metadata = {
  title: 'Retail Fail',
  description: 'Интернет-магазин на FastAPI'
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="ru">
      <body>
        <header className="bg-white shadow">
          <nav className="container mx-auto flex justify-between items-center py-4">
            <Link href="/" className="font-bold text-lg">Retail Fail</Link>
            <div className="flex gap-4">
              <Link href="/cart">Корзина</Link>
              <Link href="/orders">Заказы</Link>
              <Link href="/profile">Профиль</Link>
              <Link href="/login">Вход</Link>
              <Link href="/register">Регистрация</Link>
            </div>
          </nav>
        </header>
        <main className="container mx-auto py-8">{children}</main>
      </body>
    </html>
  );
}
