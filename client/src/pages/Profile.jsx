import { useEffect, useState, useRef } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import gsap from "gsap";

export default function Profile() {
  const navigate = useNavigate();
  const token = localStorage.getItem("access_token");
  const clientId = localStorage.getItem("client_id");

  const [clientData, setClientData] = useState(null);
  const [accounts, setAccounts] = useState([]);
  const [operationsByAccount, setOperationsByAccount] = useState({});
  const [loading, setLoading] = useState(true);
  const [filterDates, setFilterDates] = useState({ start: "", end: "" });

  const profileRef = useRef(null);
  const accountsRef = useRef(null);
  const operationsRef = useRef(null);

  const fetchClientData = async () => {
    setLoading(true);
    try {
      const clientResponse = await axios.get(
        `http://localhost:8000/clients/${clientId}`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      setClientData(clientResponse.data);

      const счета = clientResponse.data?.счета || [];
      setAccounts(счета);

      const operationsData = {};
      for (const acc of счета) {
        try {
          const response = await axios.get(
            `http://localhost:8000/operations/by-account/${acc.id_счета}`,
            {
              headers: {
                Authorization: `Bearer ${token}`,
              },
            }
          );
          operationsData[acc.id_счета] = response.data;
        } catch (err) {
          console.error(
            `Ошибка загрузки операций для счёта ${acc.id_счета}:`,
            err
          );
          operationsData[acc.id_счета] = [];
        }
      }
      setOperationsByAccount(operationsData);
    } catch (error) {
      console.error("Ошибка при получении данных клиента:", error);
      if (error.response?.status === 401 || error.response?.status === 403) {
        localStorage.clear();
        navigate("/login");
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (!token) {
      navigate("/login");
      return;
    }
    fetchClientData();
  }, [navigate, token, clientId]);

  useEffect(() => {
    if (!loading && clientData) {
      // Анимации GSAP после загрузки данных и рендера

      // Профиль: слева направо
      gsap.fromTo(
        profileRef.current,
        { opacity: 0, x: -50 },
        { opacity: 1, x: 0, duration: 1, ease: "power3.out" }
      );

      // Счета: справа налево с задержкой
      gsap.fromTo(
        accountsRef.current,
        { opacity: 0, x: 50 },
        { opacity: 1, x: 0, duration: 1, ease: "power3.out", delay: 0.3 }
      );

      // Операции: сверху вниз с задержкой
      gsap.fromTo(
        operationsRef.current,
        { opacity: 0, y: -30 },
        { opacity: 1, y: 0, duration: 1, ease: "power3.out", delay: 0.6 }
      );
    }
  }, [loading, clientData]);

  const handleCloseAccount = async (account) => {
    if (
      !window.confirm(
        `Вы уверены, что хотите закрыть счёт №${account.id_счета}?`
      )
    )
      return;

    try {
      await axios.delete(`http://localhost:8000/account/${account.id_счета}`, {
        params: { client_id: clientId },
        headers: { Authorization: `Bearer ${token}` },
      });
      alert("Счёт успешно закрыт");
      fetchClientData();
    } catch (error) {
      alert("Ошибка при закрытии счета");
      console.error(error);
    }
  };

  const fetchCardOperationsForPeriod = async (accountId) => {
    if (!dateRange.start || !dateRange.end) {
      alert("Укажите обе даты для фильтрации.");
      return;
    }

    try {
      const response = await axios.get(
        `http://localhost:8000/accounts/${accountId}/card-operations/`,
        {
          params: {
            start_date: dateRange.start,
            end_date: dateRange.end,
          },
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      setCardOperations((prev) => ({
        ...prev,
        [accountId]: response.data,
      }));
    } catch (error) {
      console.error(
        `Ошибка при загрузке операций по счёту ${accountId}`,
        error
      );
      alert("Не удалось загрузить операции.");
    }
  };

  if (loading) {
    return <div className="container">Загрузка данных...</div>;
  }

  if (!clientData) {
    return (
      <div className="container">Не удалось загрузить данные клиента.</div>
    );
  }

  return (
    <div style={{ padding: "2rem" }}>
      <div style={{ display: "flex", gap: "2rem", marginBottom: "2rem" }}>
        {/* Профиль */}
        <div className="card" style={{ flex: 1 }} ref={profileRef}>
          <h2 className="section-title">Профиль</h2>
          <p>
            <strong>ФИО:</strong> {clientData.фамилия} {clientData.имя}{" "}
            {clientData.отчество}
          </p>
          <p>
            <strong>Email:</strong> {clientData.email}
          </p>
          <p>
            <strong>Дата создания:</strong>{" "}
            {new Date(clientData.дата_создания).toLocaleString()}
          </p>
        </div>

        {/* Счета */}
        <div className="card" style={{ flex: 2 }} ref={accountsRef}>
          <h2 className="section-title">Ваши счета</h2>
          {accounts.length === 0 ? (
            <p>У вас пока нет счетов.</p>
          ) : (
            <table className="table-list">
              <thead>
                <tr>
                  <th>Номер счёта</th>
                  <th>Баланс</th>
                  <th>Тип счёта</th>
                  <th>Дата открытия</th>
                  <th>Действия</th>
                </tr>
              </thead>
              <tbody>
                {accounts.map((acc) => (
                  <tr key={acc.id_счета}>
                    <td>{acc.id_счета}</td>
                    <td>{acc.баланс}</td>
                    <td>{acc.вид?.название_вида_счета || "—"}</td>
                    <td>
                      {new Date(acc.дата_открытия).toLocaleDateString("ru-RU")}
                    </td>
                    <td>
                      <button
                        onClick={() => handleCloseAccount(acc)}
                        title="Закрыть счёт (баланс будет переведён на карту)"
                      >
                        Закрыть счёт
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
          <button
            onClick={() => navigate("/account-types")}
            style={{ marginTop: "1rem" }}
          >
            Открыть счёт
          </button>
        </div>
      </div>

      {/* Операции */}
      <div className="card" ref={operationsRef}>
        <h2 className="section-title">Банковские операции</h2>
        <div className="operation-filter">
          <label>
            От:
            <input
              type="date"
              value={filterDates.start}
              onChange={(e) =>
                setFilterDates((prev) => ({ ...prev, start: e.target.value }))
              }
            />
          </label>
          <label>
            До:
            <input
              type="date"
              value={filterDates.end}
              onChange={(e) =>
                setFilterDates((prev) => ({ ...prev, end: e.target.value }))
              }
            />
          </label>
          <button
            className="action-button"
            onClick={() => {
              if (!filterDates.start || !filterDates.end) {
                alert("Укажите обе даты.");
              }
            }}
          >
            Применить фильтр
          </button>
        </div>
        {accounts.length === 0 ? (
          <p>Нет данных по операциям — счета отсутствуют.</p>
        ) : (
          accounts.map((acc) => (
            <div key={acc.id_счета} style={{ marginBottom: "2rem" }}>
              <h3>Операции по счёту №{acc.id_счета}</h3>
              {(
                operationsByAccount[acc.id_счета]?.filter((op) => {
                  if (!filterDates.start || !filterDates.end) return true;
                  const date = new Date(op.дата_операции);
                  return (
                    date >= new Date(filterDates.start) &&
                    date <= new Date(filterDates.end)
                  );
                }) || []
              ).length > 0 ? (
                <table className="table-list">
                  <thead>
                    <tr>
                      <th>Счет</th>
                      <th>Дата</th>
                      <th>Тип</th>
                      <th>Сумма</th>
                    </tr>
                  </thead>
                  <tbody>
                    {operationsByAccount[acc.id_счета]
                      .filter((op) => {
                        if (!filterDates.start || !filterDates.end) return true;
                        const date = new Date(op.дата_операции);
                        return (
                          date >= new Date(filterDates.start) &&
                          date <= new Date(filterDates.end)
                        );
                      })
                      .map((op) => (
                        <tr key={op.id_операции}>
                          <td>{op.id_счета}</td>
                          <td>
                            {op.дата_операции
                              ? new Date(op.дата_операции).toLocaleString(
                                  "ru-RU"
                                )
                              : "—"}
                          </td>
                          <td>
                            {op.тип || op.операция?.название_операции || "—"}
                          </td>
                          <td>{op.сумма}</td>
                        </tr>
                      ))}
                  </tbody>
                </table>
              ) : (
                <p>Нет операций по этому счёту за выбранный период.</p>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
}
