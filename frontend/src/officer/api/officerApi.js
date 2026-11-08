import axios from "axios";

const TOKEN_KEY = "officer_token";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

// Attach the token to every request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem(TOKEN_KEY);
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// If the token is invalid or expired, go back to the login page
api.interceptors.response.use(
  (response) => response,
  (error) => {
    const isLoginCall = error.config && error.config.url === "/officer/login";
    if (error.response && error.response.status === 401 && !isLoginCall) {
      localStorage.removeItem(TOKEN_KEY);
      localStorage.removeItem("officer_name");
      window.location.href = "/officer/login";
    }
    return Promise.reject(error);
  }
);

export const saveSession = (data) => {
  localStorage.setItem(TOKEN_KEY, data.access_token);
  localStorage.setItem("officer_name", data.name);
};

export const clearSession = () => {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem("officer_name");
};

export const isLoggedIn = () => !!localStorage.getItem(TOKEN_KEY);

export const getOfficerName = () => localStorage.getItem("officer_name") || "";

export const loginOfficer = (username, password) =>
  api.post("/officer/login", { username, password });

export const getMyComplaints = (status) =>
  api.get("/officer/complaints", { params: status ? { status } : {} });

export const getComplaintDetails = (id) =>
  api.get(`/officer/complaints/${id}`);

export const updateComplaintStatus = (id, new_status, remarks) =>
  api.put(`/officer/complaints/${id}/status`, { new_status, remarks });

export default api;
