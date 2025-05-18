"use client";
import { useState } from "react";
import api from "@/lib/api";
import { useRouter } from "next/navigation";

export default function RegisterPage() {
  const [form, setForm] = useState({
    username: "",
    first_name: "",
    second_name: "",
    email: "",
    password: "",
  });
  const router = useRouter();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await api.post("/auth/", form);
      alert("Регистрация успешна, войдите!");
      router.push("/login");
    } catch (err) {
      alert("Ошибка регистрации!");
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      style={{
        maxWidth: 420,
        margin: "50px auto",
        padding: "32px 22px",
        background: "#fff",
        boxShadow: "0 2px 16px rgba(30,32,34,0.10)",
        borderRadius: 18,
        display: "flex",
        flexDirection: "column",
        gap: 16,
      }}
    >
      <h1 style={{ fontSize: "1.5rem", fontWeight: 700, marginBottom: 12, textAlign: "center" }}>
        Регистрация
      </h1>
      <input name="username" value={form.username} onChange={handleChange} placeholder="Логин" required style={inputStyle} />
      <input name="first_name" value={form.first_name} onChange={handleChange} placeholder="Имя" required style={inputStyle} />
      <input name="second_name" value={form.second_name} onChange={handleChange} placeholder="Фамилия" required style={inputStyle} />
      <input name="email" value={form.email} onChange={handleChange} placeholder="E-mail" required type="email" style={inputStyle} />
      <input type="password" name="password" value={form.password} onChange={handleChange} placeholder="Пароль" required style={inputStyle} />
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
        Зарегистрироваться
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
