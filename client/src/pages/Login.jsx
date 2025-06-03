import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { loginClient } from "../api/auth";

export default function Login({ setAuth }) {
  const [credentials, setCredentials] = useState({ email: "", пароль: "" });
  const [message, setMessage] = useState("");
  const navigate = useNavigate();

  const handleChange = (e) => {
    setCredentials({ ...credentials, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await loginClient(credentials);
      localStorage.setItem("access_token", res.data.access_token);
      localStorage.setItem("client_id", res.data.client_id);
      localStorage.setItem("role_id", res.data.role_id);
      setMessage("");
      setAuth(true);
      navigate("/profile");
    } catch (err) {
      setMessage(err.response?.data?.detail || "Ошибка входа");
    }
  };

  return (
    <div className="container">
      <h2>Вход</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="email"
          name="email"
          placeholder="Email"
          onChange={handleChange}
          required
        />
        <input
          type="password"
          name="пароль"
          placeholder="Пароль"
          onChange={handleChange}
          required
        />
        <button type="submit">Войти</button>
      </form>
      {message && <p className="error">{message}</p>}
    </div>
  );
}
