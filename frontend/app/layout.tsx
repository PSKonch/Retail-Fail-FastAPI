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
      <body style={{ margin: 0, background: "#f3f4f6", minHeight: "100vh" }}>
        {/* --- Header --- */}
        <header style={{
          background: "#fff",
          boxShadow: "0 2px 8px rgba(30,32,34,0.06)",
          marginBottom: 0,
        }}>
          <nav style={{
            maxWidth: 1200,
            margin: "0 auto",
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            padding: "22px 18px",
            fontFamily: "'Segoe UI', Arial, sans-serif"
          }}>
            <Link href="/" style={{
              fontWeight: 700,
              fontSize: "1.27rem",
              letterSpacing: ".6px",
              color: "#2563eb",
              textDecoration: "none"
            }}>Retail Fail</Link>
            <div style={{
              display: "flex",
              gap: 20,
              fontSize: "1rem"
            }}>
              <Link href="/cart" style={navLinkStyle}>Корзина</Link>
              <Link href="/orders" style={navLinkStyle}>Заказы</Link>
              <Link href="/profile" style={navLinkStyle}>Профиль</Link>
              <Link href="/login" style={navLinkStyle}>Вход</Link>
              <Link href="/register" style={navLinkStyle}>Регистрация</Link>
            </div>
          </nav>
        </header>
        {/* --- Main --- */}
        <main style={{
          maxWidth: 1100,
          margin: "0 auto",
          padding: "36px 12px 48px 12px",
          minHeight: "calc(100vh - 80px)"
        }}>
          {children}
        </main>
      </body>
    </html>
  );
}

const navLinkStyle: React.CSSProperties = {
  color: "#1e293b",
  textDecoration: "none",
  fontWeight: 500,
  padding: "4px 0",
  borderBottom: "2px solid transparent",
  transition: "border 0.15s",
  cursor: "pointer"
};
