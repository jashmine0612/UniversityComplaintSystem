import { useEffect, useState } from "react";
import { Link, Navigate, useNavigate } from "react-router-dom";
import { getMyComplaints, isLoggedIn, clearSession, getOfficerName } from "../api/officerApi";
import "../officer.css";

const STATUSES = ["", "PENDING", "IN_PROGRESS", "AWAITING_VERIFICATION"];

export default function OfficerDashboard() {
  const navigate = useNavigate();
  const [complaints, setComplaints] = useState([]);
  const [statusFilter, setStatusFilter] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!isLoggedIn()) return;
    setLoading(true);
    setError("");
    getMyComplaints(statusFilter)
      .then((res) => setComplaints(res.data))
      .catch(() => setError("Could not load complaints. Is the backend running?"))
      .finally(() => setLoading(false));
  }, [statusFilter]);

  if (!isLoggedIn()) {
    return <Navigate to="/officer/login" replace />;
  }

  const handleLogout = () => {
    clearSession();
    navigate("/officer/login");
  };

  return (
    <div className="officer-page">
      <header className="officer-header">
        <h2>Officer Dashboard</h2>
        <div className="officer-header-right">
          <span>Welcome, {getOfficerName()}</span>
          <button className="officer-btn-light" onClick={handleLogout}>Logout</button>
        </div>
      </header>

      <div className="officer-toolbar">
        <label htmlFor="statusFilter">Filter by status: </label>
        <select
          id="statusFilter"
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
        >
          {STATUSES.map((s) => (
            <option key={s} value={s}>{s === "" ? "All" : s.replace("_", " ")}</option>
          ))}
        </select>
      </div>

      {error && <div className="officer-error">{error}</div>}
      {loading && <p>Loading...</p>}

      {!loading && !error && complaints.length === 0 && (
        <p>No complaints found.</p>
      )}

      {!loading && complaints.length > 0 && (
        <table className="officer-table">
          <thead>
            <tr>
              <th>Complaint ID</th>
              <th>Category</th>
              <th>Priority</th>
              <th>Location</th>
              <th>Submitted</th>
              <th>Status</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {complaints.map((c) => (
              <tr key={c.id}>
                <td>{c.complaint_code}</td>
                <td>{c.category || "-"}</td>
                <td><span className={"badge priority-" + c.priority}>{c.priority}</span></td>
                <td>{c.location}</td>
                <td>{c.created_at ? new Date(c.created_at).toLocaleDateString() : "-"}</td>
                <td><span className={"badge status-" + c.status}>{c.status.replace("_", " ")}</span></td>
                <td><Link to={"/officer/complaints/" + c.id}>View</Link></td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
