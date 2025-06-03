import { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Register from "./pages/Register";
import Login from "./pages/Login";
import Profile from "./pages/Profile";
import AdminDashboard from "./components/AdminDashboard";
import AdminRoute from "./components/AdminRoute";
import OperatorRoute from "./components/OperatorRoute";
import AccountTypes from "./pages/AccountTypes";
import axios from "axios";
import "./App.css";
import OperatorDashboard from "./components/OperatorDashboard";

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [showTransferModal, setShowTransferModal] = useState(false);
  const [transferData, setTransferData] = useState({
    id_sender_account: "",
    id_recipient_account: "",
    amount: "",
  });
  const [transferMessage, setTransferMessage] = useState("");

  const roleId = localStorage.getItem("role_id");

  useEffect(() => {
    if (localStorage.getItem("access_token")) {
      setIsAuthenticated(true);
    }
  }, []);

  const handleLogout = () => {
    localStorage.clear();
    setIsAuthenticated(false);
  };

  const handleTransferSubmit = async (e) => {
    e.preventDefault();
    const token = localStorage.getItem("access_token");
    try {
      const res = await axios.post(
        "http://localhost:8000/translation",
        {},
        {
          params: {
            id_sender_account: transferData.id_sender_account,
            id_recipient_account: transferData.id_recipient_account,
            amount: transferData.amount,
          },
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      setTransferMessage(res.data.message);
      setTransferData({
        id_sender_account: "",
        id_recipient_account: "",
        amount: "",
      });
    } catch (err) {
      setTransferMessage(
        err.response?.data?.detail || "Ошибка при переводе средств"
      );
    }
  };

  return (
    <Router>
      <nav className="navbar">
        <div className="nav-links">
          {!isAuthenticated ? (
            <>
              <Link to="/register">Регистрация</Link>
              <span>|</span>
              <Link to="/login">Вход</Link>
            </>
          ) : (
            <>
              <Link to="/profile">Профиль</Link>
              {roleId === "2" && <Link to="/admin">Админка</Link>}
              {roleId === "3" && <Link to="/operator">Операторка</Link>}
              <button
                className="transfer-button"
                onClick={() => setShowTransferModal(true)}
              >
                Перевести деньги
              </button>
            </>
          )}
        </div>
        {isAuthenticated && (
          <button className="logout-button" onClick={handleLogout}>
            Выйти
          </button>
        )}
      </nav>

      {/* Модальное окно */}
      {showTransferModal && (
        <div className="modal-overlay">
          <div className="modal">
            <h3>Перевод средств</h3>
            <form onSubmit={handleTransferSubmit} className="transfer-form">
              <label>ID_счета отправителя</label>
              <input
                type="number"
                value={transferData.id_sender_account}
                onChange={(e) =>
                  setTransferData({
                    ...transferData,
                    id_sender_account: e.target.value,
                  })
                }
                required
              />
              <label>ID_счета получателя</label>
              <input
                type="number"
                value={transferData.id_recipient_account}
                onChange={(e) =>
                  setTransferData({
                    ...transferData,
                    id_recipient_account: e.target.value,
                  })
                }
                required
              />
              <label>Сумма</label>
              <input
                type="number"
                value={transferData.amount}
                onChange={(e) =>
                  setTransferData({ ...transferData, amount: e.target.value })
                }
                required
              />
              <button type="submit" className="action-button">
                Отправить
              </button>
              <button
                type="button"
                className="cancel-button"
                onClick={() => {
                  setShowTransferModal(false);
                  setTransferMessage("");
                }}
              >
                Отмена
              </button>
            </form>
            {transferMessage && <p className="message">{transferMessage}</p>}
          </div>
        </div>
      )}

      <Routes>
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login setAuth={setIsAuthenticated} />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/account-types" element={<AccountTypes />} />
        <Route
          path="/admin"
          element={
            <AdminRoute>
              <AdminDashboard />
            </AdminRoute>
          }
        />
        <Route
          path="/operator"
          element={
            <OperatorRoute>
              <OperatorDashboard />
            </OperatorRoute>
          }
        />
      </Routes>
    </Router>
  );
}

export default App;
