import { useEffect, useState } from "react";
import axios from "axios";

export default function AccountsList({ clientId, token }) {
  const [accounts, setAccounts] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchAccounts = async () => {
    try {
      const response = await axios.get(
        `http://localhost:8000/accounts?client_id=${clientId}`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      setAccounts(response.data);
    } catch (error) {
      console.error("Ошибка при загрузке счетов:", error);
      alert("Не удалось загрузить счета");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAccounts();
  }, []);

  const handleCloseAccount = async (accountId) => {
    if (!window.confirm("Вы уверены, что хотите закрыть счет?")) return;

    try {
      await axios.delete(`http://localhost:8000/account/${accountId}`, {
        params: { client_id: clientId },
        headers: { Authorization: `Bearer ${token}` },
      });
      alert("Счет успешно закрыт");
      fetchAccounts();
    } catch (error) {
      console.error("Ошибка при закрытии счета:", error);
      alert("Не удалось закрыть счет");
    }
  };

  if (loading) return <div className="container">Загрузка счетов...</div>;

  if (accounts.length === 0)
    return <div className="container">У вас нет счетов</div>;

  return (
    <div className="accounts-list">
      <h2>Ваши счета</h2>
      {accounts.map((account) => (
        <div key={account.id_счета} className="account-card">
          <p>Тип: {account.вид.название_вида_счета}</p>
          <p>Баланс: {account.баланс}</p>
          <button
            onClick={() => handleCloseAccount(account.id_счета, account.баланс)}
          >
            Закрыть счет
          </button>
        </div>
      ))}
    </div>
  );
}
