import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:8000",
  withCredentials: true,
});

export const registerClient = (data) => {
  return API.post("/clients/", {
    ...data,
    id_роли: 1,
  });
};

export const loginClient = (data) => {
  return API.post("/login/", data);
};
