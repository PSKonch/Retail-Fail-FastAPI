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

  if (!user) return <div>Загрузка...</div>;

  return (
    <div className="max-w-lg mx-auto bg-white rounded-xl p-8 shadow">
      <h1 className="text-2xl font-bold mb-4">Профиль</h1>
      <div>Логин: {user.username}</div>
      <div>Имя: {user.first_name}</div>
      <div>Фамилия: {user.second_name}</div>
      <div>Email: {user.email}</div>
      <button className="btn btn-error mt-4" onClick={handleLogout}>Выйти</button>
    </div>
  );
}
