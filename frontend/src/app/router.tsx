import { Routes, Route, Outlet } from "react-router-dom";
import { LoginPage } from "@/pages/auth/LoginPage";
import { RegisterPage } from "@/pages/auth/RegisterPage";
import { DashboardHome } from "@/pages/dashboard/DashboardHome";
import ProtectedRoute from "@/components/ProtectedRoute";
import { MainLayout } from "@/app/layout";
import { TeamsPage } from "@/pages/teams";

const SidebarLayout = () => (
  <MainLayout>
    <Outlet />
  </MainLayout>
);

export const AppRouter = () => {
  return (
    <Routes>
      {/* No sidebar routes */}
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />

      {/* Sidebar layout routes */}
      <Route element={<SidebarLayout />}>
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <DashboardHome />
            </ProtectedRoute>
          }
        />
        <Route
          path="/teams"
          element={
            <ProtectedRoute>
              <TeamsPage />
            </ProtectedRoute>
          }
        />
        {/* Add more routes here that should have the sidebar */}
      </Route>

      {/* Optional: add 404 route here */}
      {/* <Route path="*" element={<NotFoundPage />} /> */}
    </Routes>
  );
};
