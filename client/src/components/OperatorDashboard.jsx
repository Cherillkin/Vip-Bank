import { useEffect, useState } from "react";
import axios from "axios";
import "../App.css";

const OperatorDashboard = ({ user }) => {
  const [clients, setClients] = useState([]);
  const [loading, setLoading] = useState(true);
  const [accessDenied, setAccessDenied] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("access_token");

    const now = new Date();
    const hour = now.getHours();

    if (user?.role === 3 && (hour < 9 || hour >= 18)) {
      setAccessDenied(true);
      setLoading(false);
      return;
    }

    const fetchClients = async () => {
      try {
        const response = await axios.get(`http://localhost:8000/clients`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        setClients(response.data);
      } catch (error) {
        console.error("Ошибка при получении клиентов:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchClients();
  }, [user]);

  if (loading) return <div className="admin-panel">Загрузка...</div>;

  if (accessDenied) {
    return (
      <div className="admin-panel">
        <p className="message">
          Доступ к панели оператора разрешён только с 09:00 до 18:00.
        </p>
      </div>
    );
  }

  return (
    <div className="admin-panel styled">
      <h1 className="section-title">Панель оператора</h1>
      {clients.map((client) => (
        <div key={client.id_клиента} className="card">
          <h3>
            {client.фамилия} {client.имя} {client.отчество}
          </h3>
          <p>
            <strong>Email:</strong> {client.email}
          </p>
          <p>
            <strong>Роль:</strong> {client.роль?.роль}
          </p>

          <h4 style={{ marginTop: "1rem", marginBottom: "0.5rem" }}>Счета:</h4>
          {client.счета.length === 0 ? (
            <p className="message">Нет счетов</p>
          ) : (
            client.счета.map((счет) => (
              <div
                key={счет.id_счета}
                className="card"
                style={{ backgroundColor: "#f8f8f8" }}
              >
                <p>
                  <strong>ID счёта:</strong> {счет.id_счета}
                </p>
                <p>
                  <strong>Баланс:</strong> {счет.баланс}₽
                </p>
                <p>
                  <strong>Дата открытия:</strong>{" "}
                  {new Date(счет.дата_открытия).toLocaleDateString()}
                </p>

                <h5 style={{ marginTop: "0.5rem" }}>Операции:</h5>
                {счет.операции?.length === 0 ? (
                  <p style={{ fontSize: "0.9rem", color: "#777" }}>
                    Нет операций
                  </p>
                ) : (
                  <ul>
                    {счет.операции.map((оп) => (
                      <li key={оп.id_банковской_операции}>
                        <strong>{оп.операция.название_операции}</strong>:{" "}
                        {оп.сумма}₽ —{" "}
                        {new Date(оп.дата_операции).toLocaleString()}
                      </li>
                    ))}
                  </ul>
                )}
              </div>
            ))
          )}
        </div>
      ))}
    </div>
  );
};

export default OperatorDashboard;
