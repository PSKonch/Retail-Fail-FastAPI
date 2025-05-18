"use client";
import { useState } from "react";
import api, { setAuthToken } from "@/lib/api";
import { useRouter } from "next/navigation";
import { useAuthStore } from "@/store/auth";

export default function LoginPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const { setToken } = useAuthStore();
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const data = new URLSearchParams();
    data.append("username", username);
    data.append("password", password);

    try {
      const res = await api.post("/auth/token", data, {
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
      });
      setAuthToken(res.data.access_token);
      setToken(res.data.access_token);
      localStorage.setItem("token", res.data.access_token);
      router.push("/");
    } catch (err) {
      alert("Ошибка авторизации!");
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      style={{
        maxWidth: 380,
        margin: "50px auto",
        padding: "32px 22px",
        background: "#fff",
        boxShadow: "0 2px 16px rgba(30,32,34,0.10)",
        borderRadius: 18,
        display: "flex",
        flexDirection: "column",
        gap: 18,
      }}
    >
      <h1 style={{ fontSize: "1.5rem", fontWeight: 700, marginBottom: 12, textAlign: "center" }}>
        Вход
      </h1>
      <input
        type="text"
        value={username}
        onChange={e => setUsername(e.target.value)}
        placeholder="Логин"
        required
        style={inputStyle}
      />
      <input
        type="password"
        value={password}
        onChange={e => setPassword(e.target.value)}
        placeholder="Пароль"
        required
        style={inputStyle}
      />
      <button
        type="submit"
        style={{
          padding: "12px",
          background: "#2563eb",
          color: "#fff",
          fontWeight: 600,
          border: "none",
          borderRadius: 10,
          fontSize: "1.08rem",
          cursor: "pointer",
          marginTop: 10
        }}
      >
        Войти
      </button>
    </form>
  );
}

const inputStyle: React.CSSProperties = {
  padding: "11px 14px",
  fontSize: "1rem",
  border: "1px solid #d1d5db",
  borderRadius: 8,
  outline: "none",
  fontWeight: 500,
  marginBottom: 2
};
