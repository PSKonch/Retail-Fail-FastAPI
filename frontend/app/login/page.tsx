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
    <form onSubmit={handleSubmit} className="max-w-md mx-auto mt-10 p-6 bg-white shadow-xl rounded-2xl">
      <h1 className="text-xl font-bold mb-6">Вход</h1>
      <input type="text" value={username} onChange={e=>setUsername(e.target.value)} placeholder="Логин" className="mb-4 input input-bordered w-full" />
      <input type="password" value={password} onChange={e=>setPassword(e.target.value)} placeholder="Пароль" className="mb-4 input input-bordered w-full" />
      <button type="submit" className="btn btn-primary w-full">Войти</button>
    </form>
  );
}
