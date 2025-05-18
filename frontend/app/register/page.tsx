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
    <form onSubmit={handleSubmit} className="max-w-md mx-auto mt-10 p-6 bg-white shadow-xl rounded-2xl">
      <h1 className="text-xl font-bold mb-6">Регистрация</h1>
      <input name="username" value={form.username} onChange={handleChange} placeholder="Логин" className="mb-4 input input-bordered w-full" />
      <input name="first_name" value={form.first_name} onChange={handleChange} placeholder="Имя" className="mb-4 input input-bordered w-full" />
      <input name="second_name" value={form.second_name} onChange={handleChange} placeholder="Фамилия" className="mb-4 input input-bordered w-full" />
      <input name="email" value={form.email} onChange={handleChange} placeholder="E-mail" className="mb-4 input input-bordered w-full" />
      <input type="password" name="password" value={form.password} onChange={handleChange} placeholder="Пароль" className="mb-4 input input-bordered w-full" />
      <button type="submit" className="btn btn-primary w-full">Зарегистрироваться</button>
    </form>
  );
}
