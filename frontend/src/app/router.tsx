import { Routes, Route, Outlet } from "react-router-dom";
import { LoginPage } from "@/pages/auth/LoginPage";
import { RegisterPage } from "@/pages/auth/RegisterPage";
import { DashboardHome } from "@/pages/dashboard/DashboardHome";
import ProtectedRoute from "@/components/ProtectedRoute";
import { MainLayout } from "@/app/layout";
import { TeamsPage } from "@/pages/teams";
import { TeamViewPage } from "@/pages/teams/TeamViewPage";
import { AcceptInvitePage } from "@/pages/teams/AcceptInvitePage";

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
        <Route
          path="/teams/:id"
          element={
            <ProtectedRoute>
              <TeamViewPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/accept-invite"
          element={
            <ProtectedRoute>
              <AcceptInvitePage />
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
