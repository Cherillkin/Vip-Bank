import { useState } from "react";
import { registerClient } from "../api/auth";

export default function Register() {
  const [formData, setFormData] = useState({
    фамилия: "",
    имя: "",
    отчество: "",
    email: "",
    пароль: "",
  });
  const [message, setMessage] = useState("");

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await registerClient(formData);
      setMessage("Регистрация прошла успешно!");
    } catch (err) {
      setMessage(err.response?.data?.detail || "Ошибка регистрации");
    }
  };

  return (
    <div className="container">
      <h2>Регистрация</h2>
      <form onSubmit={handleSubmit}>
        {["фамилия", "имя", "отчество", "email", "пароль"].map((field) => (
          <input
            key={field}
            type={field === "пароль" ? "password" : "text"}
            name={field}
            placeholder={field}
            onChange={handleChange}
            required={field !== "отчество"}
          />
        ))}
        <button type="submit">Зарегистрироваться</button>
      </form>
      <p>{message}</p>
    </div>
  );
}
