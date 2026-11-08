import { useEffect, useState } from "react";
import { Link, Navigate, useParams } from "react-router-dom";
import { getComplaintDetails, isLoggedIn } from "../api/officerApi";
import StatusUpdateForm from "../components/StatusUpdateForm";
import "../officer.css";

const formatDate = (d) => (d ? new Date(d).toLocaleString() : "-");

export default function ComplaintDetails() {
  const { id } = useParams();
  const [complaint, setComplaint] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const loadComplaint = () =>
    getComplaintDetails(id)
      .then((res) => setComplaint(res.data))
      .catch((err) => {
        const code = err.response?.status;
        if (code === 403) setError("You are not allowed to view this complaint.");
        else if (code === 404) setError("Complaint not found.");
        else setError("Could not load the complaint. Is the backend running?");
      });

  useEffect(() => {
    if (!isLoggedIn()) return;
    setLoading(true);
    setError("");
    loadComplaint().finally(() => setLoading(false));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id]);

  if (!isLoggedIn()) {
    return <Navigate to="/officer/login" replace />;
  }

  return (
    <div className="officer-page">
      <header className="officer-header">
        <h2>Complaint Details</h2>
        <Link className="officer-back-link" to="/officer/dashboard">
          &larr; Back to dashboard
        </Link>
      </header>

      {loading && <p>Loading...</p>}
      {error && <div className="officer-error">{error}</div>}

      {complaint && (
        <>
          <div className="officer-card">
            <h3>
              {complaint.complaint_code}{" "}
              <span className={"badge status-" + complaint.status}>
                {complaint.status.replace(/_/g, " ")}
              </span>
            </h3>

            <div className="officer-detail-grid">
              <div><strong>Category:</strong> {complaint.category || "-"}</div>
              <div>
                <strong>Priority:</strong>{" "}
                <span className={"badge priority-" + complaint.priority}>
                  {complaint.priority}
                </span>
              </div>
              <div><strong>Location:</strong> {complaint.location}</div>
              <div><strong>Roll number:</strong> {complaint.roll_number}</div>
              <div><strong>Submitted:</strong> {formatDate(complaint.created_at)}</div>
              <div><strong>Deadline:</strong> {formatDate(complaint.deadline)}</div>
            </div>

            <h4>Description</h4>
            <p className="officer-text-block">{complaint.description}</p>

            <h4>Resolution remarks</h4>
            <p className="officer-text-block">
              {complaint.resolution_remarks || "No remarks yet."}
            </p>
          </div>

          <StatusUpdateForm complaint={complaint} onUpdated={loadComplaint} />

          <div className="officer-card">
            <h3>Status history</h3>
            {complaint.history.length === 0 ? (
              <p>No status changes yet.</p>
            ) : (
              <table className="officer-table">
                <thead>
                  <tr>
                    <th>When</th>
                    <th>From</th>
                    <th>To</th>
                    <th>Remarks</th>
                  </tr>
                </thead>
                <tbody>
                  {complaint.history.map((h) => (
                    <tr key={h.id}>
                      <td>{formatDate(h.changed_at)}</td>
                      <td>{h.old_status ? h.old_status.replace(/_/g, " ") : "-"}</td>
                      <td>{h.new_status.replace(/_/g, " ")}</td>
                      <td>{h.remarks || "-"}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        </>
      )}
    </div>
  );
}

