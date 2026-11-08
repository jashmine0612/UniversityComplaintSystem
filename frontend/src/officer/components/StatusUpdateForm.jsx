import { useState } from "react";
import { updateComplaintStatus } from "../api/officerApi";

export default function StatusUpdateForm({ complaint, onUpdated }) {
  const [remarks, setRemarks] = useState("");
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const send = async (newStatus, remarksText) => {
    setError("");
    setSuccess("");
    setSaving(true);
    try {
      await updateComplaintStatus(complaint.id, newStatus, remarksText);
      setRemarks("");
      setSuccess("Status updated successfully.");
      await onUpdated();
    } catch (err) {
      const msg = err.response?.data?.detail;
      setError(typeof msg === "string" ? msg : "Could not update the status. Please try again.");
    } finally {
      setSaving(false);
    }
  };

  const handleSubmitResolution = (e) => {
    e.preventDefault();
    if (!remarks.trim()) {
      setError("Please enter resolution remarks before submitting.");
      return;
    }
    send("AWAITING_VERIFICATION", remarks.trim());
  };

  return (
    <div className="officer-card">
      <h3>Update status</h3>

      {error && <div className="officer-error">{error}</div>}
      {success && <div className="officer-success">{success}</div>}

      {complaint.status === "PENDING" && (
        <div>
          <p>This complaint has not been started yet.</p>
          <button
            className="officer-btn-primary"
            disabled={saving}
            onClick={() => send("IN_PROGRESS", null)}
          >
            {saving ? "Saving..." : "Start work"}
          </button>
        </div>
      )}

      {complaint.status === "IN_PROGRESS" && (
        <form onSubmit={handleSubmitResolution}>
          <label htmlFor="remarks"><strong>Resolution remarks (required)</strong></label>
          <textarea
            id="remarks"
            rows={4}
            value={remarks}
            onChange={(e) => setRemarks(e.target.value)}
            placeholder="Describe what was done to resolve this complaint"
          />
          <button className="officer-btn-primary" type="submit" disabled={saving}>
            {saving ? "Submitting..." : "Submit resolution"}
          </button>
        </form>
      )}

      {complaint.status === "AWAITING_VERIFICATION" && (
        <p>
          Resolution submitted. This complaint is waiting for student verification,
          so no further action is needed from you.
        </p>
      )}
    </div>
  );
}
