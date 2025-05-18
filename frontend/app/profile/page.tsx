"use client";
import { useEffect, useState } from "react";
import api from "@/lib/api";
import { useAuthStore } from "@/store/auth";
import { useRouter } from "next/navigation";

export default function ProfilePage() {
  const [user, setUser] = useState<any>(null);
  const { token, setToken } = useAuthStore();
  const router = useRouter();

  useEffect(() => {
    if (!token) {
      router.push("/login");
      return;
    }
    api.get("/auth/me").then(res => setUser(res.data));
  }, [token, router]);

  const handleLogout = () => {
    setToken(null);
    localStorage.removeItem("token");
    router.push("/login");
  };

  if (!user) return (
    <div style={{
      textAlign: "center",
      fontSize: "20px",
      color: "#3b82f6",
      margin: "40px 0"
    }}>Загрузка...</div>
  );

  return (
    <div
      style={{
        maxWidth: 440,
        margin: "50px auto",
        background: "#fff",
        borderRadius: 18,
        padding: "38px 28px",
        boxShadow: "0 2px 16px rgba(30,32,34,0.10)",
        fontFamily: "'Segoe UI', Arial, sans-serif"
      }}
    >
      <h1 style={{ fontSize: "2rem", fontWeight: 700, marginBottom: 18 }}>Профиль</h1>
      <div style={{ marginBottom: 8 }}>Логин: <b>{user.username}</b></div>
      <div style={{ marginBottom: 8 }}>Имя: <b>{user.first_name}</b></div>
      <div style={{ marginBottom: 8 }}>Фамилия: <b>{user.second_name}</b></div>
      <div style={{ marginBottom: 20 }}>Email: <b>{user.email}</b></div>
      <button
        onClick={handleLogout}
        style={{
          width: "100%",
          padding: "12px",
          background: "#ef4444",
          color: "#fff",
          fontWeight: 600,
          border: "none",
          borderRadius: 10,
          fontSize: "1.08rem",
          cursor: "pointer"
        }}
      >
        Выйти
      </button>
    </div>
  );
}
