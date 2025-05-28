import { Routes, Route } from 'react-router-dom';
import { LoginPage } from '@/pages/auth/LoginPage';
import { RegisterPage } from '@/pages/auth/RegisterPage';
import { DashboardHome } from '@/pages/dashboard/DashboardHome';
import ProtectedRoute from '@/components/ProtectedRoute';

export const AppRouter = () => {
  return (
    <Routes>
      <Route path="/register" element={<RegisterPage />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/dashboard" element={
        <ProtectedRoute>
          <DashboardHome />
        </ProtectedRoute>
      } />
      {/* We'll add 404 route or layout wrappers later */}
    </Routes>
  );
};
