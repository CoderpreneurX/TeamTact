import { Routes, Route } from 'react-router-dom';
import { LoginPage } from '@/pages/auth/LoginPage';
import { DashboardHome } from '@/pages/dashboard/DashboardHome';

export const AppRouter = () => {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/dashboard" element={<DashboardHome />} />
      {/* We'll add 404 route or layout wrappers later */}
    </Routes>
  );
};
