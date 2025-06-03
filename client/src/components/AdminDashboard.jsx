import { useState, useEffect } from "react";
import axios from "axios";
import "../App.css";

export default function AdminDashboard() {
  const [roles, setRoles] = useState([]);
  const [streets, setStreets] = useState([]);
  const [branches, setBranches] = useState([]);
  const [accountTypes, setAccountTypes] = useState([]);
  const [accountFromTypes, setAccountFromTypes] = useState([]);
  const [interestRates, setInterestRates] = useState([]);
  const [users, setUsers] = useState([]);
  const [operations, setOperations] = useState([]);
  const [message, setMessage] = useState("");

  const token = localStorage.getItem("access_token");

  const api = axios.create({
    baseURL: "http://localhost:8000",
    headers: { Authorization: `Bearer ${token}` },
  });

  useEffect(() => {
    async function fetchData() {
      try {
        const [
          rolesRes,
          streetsRes,
          branchesRes,
          accTypesRes,
          accFromTypesRes,
          interestRatesRes,
          usersRes,
          operationsRes,
        ] = await Promise.all([
          api.get("/roles"),
          api.get("/streets"),
          api.get("/branches"),
          api.get("/account_types"),
          api.get("/account_from_types"),
          api.get("/interest_rates"),
          api.get("/clients"),
          api.get("/operations/history"),
        ]);
        setRoles(rolesRes.data);
        setStreets(streetsRes.data);
        setBranches(branchesRes.data);
        setAccountTypes(accTypesRes.data);
        setAccountFromTypes(accFromTypesRes.data);
        setInterestRates(interestRatesRes.data);
        setUsers(usersRes.data);
        setOperations(operationsRes.data);
      } catch (error) {
        setMessage("Ошибка при загрузке данных: " + error.message);
      }
    }
    fetchData();
  }, []);

  async function createRole() {
    try {
      const roleName = prompt("Введите название роли:");
      if (!roleName) return;
      await api.post("/roles/", { роль: roleName });
      setMessage("Роль создана");
      const res = await api.get("/roles");
      setRoles(res.data);
    } catch (error) {
      setMessage(
        "Ошибка при создании роли: " +
          (error.response?.data?.detail || error.message)
      );
    }
  }

  async function createUser() {
    try {
      const email = prompt("Email:");
      const фамилия = prompt("Фамилия:");
      const имя = prompt("Имя:");
      const отчество = prompt("Отчество:");
      const пароль = prompt("Пароль:");
      const id_роли = parseInt(
        prompt(
          `Введите ID роли:\n${roles
            .map((r) => `${r.id_роли} — ${r.роль}`)
            .join("\n")}`
        ),
        10
      );

      if (!email || !фамилия || !имя || !пароль || isNaN(id_роли)) {
        setMessage("Неверные данные");
        return;
      }

      await api.post("/admin/create-user", {
        email,
        фамилия,
        имя,
        отчество,
        пароль,
        id_роли,
      });

      setMessage("Пользователь создан");

      const usersRes = await api.get("/clients");
      setUsers(usersRes.data);
    } catch (e) {
      setMessage("Ошибка: " + (e.response?.data?.detail || e.message));
    }
  }

  const handleBackup = async () => {
    try {
      const response = await api.post("/backup");
      if (response.data.status === "success") {
        setMessage("Бэкап успешно создан: " + response.data.path);
      } else {
        setMessage("Ошибка при создании бэкапа: " + response.data.message);
      }
    } catch (error) {
      setMessage(
        "Ошибка при создании бэкапа: " +
          (error.response?.data?.detail || error.message)
      );
    }
  };

  const handleInterestRateChange = async () => {
    try {
      const selectedId = parseInt(
        prompt(
          `Введите ID вида счёта:\n${accountFromTypes
            .map((v) => `${v.id_вида_счета} — ${v.название_вида_счета}`)
            .join("\n")}`
        ),
        10
      );
      if (isNaN(selectedId)) return;

      const rate = parseInt(prompt("Введите процентную ставку:"), 10);
      if (isNaN(rate)) return;

      const existing = interestRates.find(
        (r) => r.id_вида_счета === selectedId
      );

      if (existing) {
        await api.put(
          `/interest_rate/${existing.id_процентной_ставки}/update_at`
        );
        setMessage("Дата изменения обновлена");
      } else {
        await api.post("/interest_rate/", {
          процентная_ставка: rate,
          id_вида_счета: selectedId,
          дата_изменения: new Date().toISOString(),
        });
        setMessage("Процентная ставка добавлена");
      }

      const updatedRates = await api.get("/interest_rates");
      setInterestRates(updatedRates.data);
    } catch (e) {
      setMessage("Ошибка: " + (e.response?.data?.detail || e.message));
    }
  };

  return (
    <div className="admin-panel styled">
      <h2 className="section-title">Админская панель</h2>
      {message && <p className="message">{message}</p>}

      <div className="grid-container">
        {/* Все клиенты и счета */}
        <div className="card wide">
          <h3>Клиенты и счета</h3>
          <table className="client-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>ФИО</th>
                <th>Email</th>
                <th>Роль</th>
                <th>Счета</th>
              </tr>
            </thead>
            <tbody>
              {users.map((u) => (
                <tr key={u.id_клиента}>
                  <td>{u.id_клиента}</td>
                  <td>{`${u.фамилия} ${u.имя} ${u.отчество || ""}`}</td>
                  <td>{u.email}</td>
                  <td>{u.роль?.роль || "—"}</td>
                  <td>
                    <ul>
                      {u.счета.length > 0 ? (
                        u.счета.map((s) => (
                          <li key={s.id_счета}>
                            №{s.id_счета}, {s.баланс}₽,{" "}
                            {new Date(s.дата_открытия).toLocaleDateString()}
                          </li>
                        ))
                      ) : (
                        <li>Нет счетов</li>
                      )}
                    </ul>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Банковские операции */}
        <div className="card">
          <h3>Банковские операции</h3>
          <ul>
            {operations.map((op) => (
              <li key={op.id_банковской_операции}>
                Операция: {op.операция?.название_операции}, сумма: {op.сумма}₽,
                счёт #{op.id_счета}, дата:{" "}
                {new Date(op.дата_операции).toLocaleString()}
              </li>
            ))}
          </ul>
        </div>

        {/* Роли */}
        <div className="card">
          <h3>Роли</h3>
          <button className="action-button" onClick={createRole}>
            Создать роль
          </button>
          <ul>
            {roles.map((r) => (
              <li key={r.id_роли}>{r.роль}</li>
            ))}
          </ul>
        </div>

        {/* Пользователи */}
        <div className="card">
          <h3>Пользователи (админы/операторы)</h3>
          <button className="action-button" onClick={createUser}>
            Создать пользователя
          </button>
          <ul>
            {users
              .filter((u) => u.роль?.id_роли === 2 || u.роль?.id_роли === 3)
              .map((u) => (
                <li key={u.id_клиента}>
                  {u.email} — {u.имя} {u.фамилия} ({u.роль?.роль || "?"})
                </li>
              ))}
          </ul>
        </div>

        {/* Улицы */}
        <div className="card">
          <h3>Улицы</h3>
          <button
            className="action-button"
            onClick={async () => {
              const name = prompt("Введите название улицы:");
              if (!name) return;
              try {
                await api.post("/street/", { улица: name });
                setMessage("Улица создана");
                const res = await api.get("/streets");
                setStreets(res.data);
              } catch (e) {
                setMessage(
                  "Ошибка: " + (e.response?.data?.detail || e.message)
                );
              }
            }}
          >
            Создать улицу
          </button>
          <ul>
            {streets.map((s) => (
              <li key={s.id_улицы}>{s.название_улицы}</li>
            ))}
          </ul>
        </div>

        {/* Филиалы */}
        <div className="card">
          <h3>Филиалы</h3>
          <button
            className="action-button"
            onClick={async () => {
              const name = prompt("Введите название филиала:");
              if (!name) return;
              try {
                await api.post("/branch/", { филиал: name });
                setMessage("Филиал создан");
                const res = await api.get("/branches");
                setBranches(res.data);
              } catch (e) {
                setMessage(
                  "Ошибка: " + (e.response?.data?.detail || e.message)
                );
              }
            }}
          >
            Создать филиал
          </button>
          <ul>
            {branches.map((b) => {
              const street = streets.find(
                (s) => s.id_улицы === b.улица_филиала
              );
              return (
                <li key={b.id_филиала}>
                  {street ? street.название_улицы : `Улица #${b.улица_филиала}`}
                  , дом {b.дом_филиала}, корпус {b.корпус_филиала}
                </li>
              );
            })}
          </ul>
        </div>

        {/* Типы счетов */}
        <div className="card">
          <h3>Типы счетов</h3>
          <ul>
            {accountTypes.map((t) => (
              <li key={t.id_типа_счета}>{t.название_типа_счета}</li>
            ))}
          </ul>
        </div>

        {/* Виды счетов */}
        <div className="card">
          <h3>Виды счетов</h3>
          <ul>
            {accountFromTypes.map((kind) => {
              const accountType = accountTypes.find(
                (t) => t.id_типа_счета === kind.id_типа_счета
              );
              return (
                <li key={kind.id_вида_счета}>
                  {kind.название_вида_счета} (
                  {accountType?.название_типа_счета || "Неизвестный тип"})
                </li>
              );
            })}
          </ul>
        </div>

        {/* Процентные ставки */}
        <div className="card">
          <h3>Процентные ставки</h3>
          <button className="action-button" onClick={handleInterestRateChange}>
            Добавить / обновить процентную ставку
          </button>
          <ul>
            {interestRates.map((r) => {
              const accountFromType = accountFromTypes.find(
                (k) => k.id_вида_счета === r.id_вида_счета
              );
              return (
                <li key={r.id_процентной_ставки}>
                  {r.процентная_ставка} % (с{" "}
                  {new Date(r.дата_изменения).toLocaleDateString()}, вид счёта:{" "}
                  {accountFromType?.название_вида_счета || "неизвестно"})
                </li>
              );
            })}
          </ul>
        </div>

        {/* Бэкап БД */}
        <div className="card">
          <h3>Бэкап базы данных</h3>
          <button className="action-button" onClick={handleBackup}>
            Создать бэкап
          </button>
        </div>
      </div>
    </div>
  );
}
