import { Routes, Route, Navigate } from "react-router-dom";
import OfficerLogin from "./pages/OfficerLogin";
import OfficerDashboard from "./pages/OfficerDashboard";
import ComplaintDetails from "./pages/ComplaintDetails";

export default function OfficerRoutes() {
  return (
    <Routes>
      <Route path="login" element={<OfficerLogin />} />
      <Route path="dashboard" element={<OfficerDashboard />} />
      <Route path="complaints/:id" element={<ComplaintDetails />} />
      <Route path="*" element={<Navigate to="/officer/login" replace />} />
    </Routes>
  );
}
