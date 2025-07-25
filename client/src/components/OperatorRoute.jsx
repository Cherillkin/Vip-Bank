import { Navigate } from "react-router-dom";

export default function OperatorRoute({ children }) {
  const token = localStorage.getItem("access_token");
  const role = localStorage.getItem("role_id");

  if (!token || role !== "3") {
    return <Navigate to="/login" />;
  }

  return children;
}
