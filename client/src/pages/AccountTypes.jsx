import { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

export default function AccountTypes() {
  const [accountTypes, setAccountTypes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedTypeId, setSelectedTypeId] = useState(null);
  const [amount, setAmount] = useState("");
  const [showForm, setShowForm] = useState(false);
  const [selectedBranchId] = useState(1);
  const [clientAccounts, setClientAccounts] = useState([]);
  const [sourceAccountId, setSourceAccountId] = useState(null);

  const token = localStorage.getItem("access_token");
  const currentClientId = Number(localStorage.getItem("client_id"));
  const navigate = useNavigate();

  useEffect(() => {
    const fetchAccountTypes = async () => {
      try {
        const response = await axios.get(
          "http://localhost:8000/account_from_types",
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );
        setAccountTypes(response.data);
      } catch (error) {
        console.error("Ошибка при загрузке видов счетов:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchAccountTypes();
  }, [token]);

  useEffect(() => {
    const fetchClientAccounts = async () => {
      try {
        const response = await axios.get(
          `http://localhost:8000/accounts/client/${currentClientId}`,
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );
        setClientAccounts(response.data);
      } catch (error) {
        console.error("Ошибка при загрузке счетов клиента:", error);
      }
    };
    fetchClientAccounts();
  }, [currentClientId, token]);

  const getAccountTypeIdById = (typeId) => {
    const found = accountTypes.find((type) => type.id_вида_счета === typeId);
    return found?.тип?.id_типа_счета;
  };

  const handleOpenAccount = (typeId) => {
    setSelectedTypeId(typeId);
    setAmount("");
    setSourceAccountId(null);
    setShowForm(true);
  };

  const handleCreateAccount = async () => {
    if (!amount || isNaN(amount)) {
      alert("Введите корректную сумму");
      return;
    }

    const accountTypeId = getAccountTypeIdById(selectedTypeId);

    if ([2, 3, 4].includes(accountTypeId) && !sourceAccountId) {
      alert("Для данного типа счёта необходимо выбрать счёт-источник");
      return;
    }

    const accountData = {
      баланс: parseInt(amount, 10),
      id_клиента: currentClientId,
      id_филиала: selectedBranchId,
      id_вида_счета: selectedTypeId,
      дата_открытия: new Date().toISOString(),
      ...(sourceAccountId && { id_счета_источника: sourceAccountId }),
    };

    try {
      await axios.post("http://localhost:8000/account", accountData, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      alert("Счёт успешно открыт");
      setShowForm(false);
      navigate("/profile");
    } catch (error) {
      console.error("Ошибка при создании счёта:", error);
      alert(
        "Не удалось открыть счёт: " + error.response?.data?.detail ||
          "Неизвестная ошибка"
      );
    }
  };

  if (loading) return <div className="container">Загрузка...</div>;

  return (
    <div className="admin-panel">
      <h2 className="section-title">Доступные виды счетов</h2>
      <div className="account-types-list">
        {accountTypes.map((type) => (
          <div key={type.id_вида_счета} className="card">
            <h3>{type.название_вида_счета}</h3>
            <p>
              <strong>Тип счёта:</strong> {type.тип?.название_типа_счета}
            </p>
            {type.процентные_ставки?.length > 0 ? (
              <p>
                <strong>Процентная ставка:</strong>{" "}
                {type.процентные_ставки.at(-1).процентная_ставка}%
              </p>
            ) : (
              <p className="error">Процентная ставка не указана</p>
            )}
            <button onClick={() => handleOpenAccount(type.id_вида_счета)}>
              Открыть счёт
            </button>
          </div>
        ))}
      </div>

      {showForm && (
        <div className="modal-overlay" onClick={() => setShowForm(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <h3>Введите сумму для открытия счёта</h3>
            <input
              type="number"
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
              placeholder="Сумма"
            />

            {[2, 3, 4].includes(getAccountTypeIdById(selectedTypeId)) && (
              <div>
                <label>Выберите счёт-источник</label>
                <select
                  value={sourceAccountId || ""}
                  onChange={(e) => setSourceAccountId(Number(e.target.value))}
                >
                  <option value="">-- выберите счёт --</option>
                  {clientAccounts.map((acc) => (
                    <option key={acc.id_} value={acc.id_счета}>
                      №{acc.id_счета} — баланс: {acc.баланс}
                    </option>
                  ))}
                </select>
              </div>
            )}

            <div style={{ marginTop: "1rem" }}>
              <button onClick={handleCreateAccount}>Подтвердить</button>
              <button onClick={() => setShowForm(false)}>Отмена</button>
            </div>
          </div>
        </div>
      )}

      <div style={{ textAlign: "center", marginTop: "2rem" }}>
        <button
          onClick={() => navigate("/profile")}
          style={{
            backgroundColor: "#e0e0e0",
            color: "#333",
            border: "none",
            padding: "0.5rem 1rem",
            borderRadius: "6px",
            cursor: "pointer",
          }}
        >
          ← Вернуться в профиль
        </button>
      </div>
    </div>
  );
}
