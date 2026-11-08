import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { loginOfficer, saveSession } from "../api/officerApi";
import "../officer.css";

export default function OfficerLogin() {
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const res = await loginOfficer(username, password);
      saveSession(res.data);
      navigate("/officer/dashboard");
    } catch (err) {
      const msg = err.response?.data?.detail;
      setError(typeof msg === "string" ? msg : "Unable to log in. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="officer-login-page">
      <form className="officer-login-card" onSubmit={handleSubmit}>
        <h2>Officer Login</h2>
        <p className="officer-subtitle">University Complaint Management System</p>

        {error && <div className="officer-error">{error}</div>}

        <label htmlFor="username">Username</label>
        <input
          id="username"
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
          autoFocus
        />

        <label htmlFor="password">Password</label>
        <input
          id="password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        <button type="submit" disabled={loading}>
          {loading ? "Logging in..." : "Login"}
        </button>
      </form>
    </div>
  );
}
