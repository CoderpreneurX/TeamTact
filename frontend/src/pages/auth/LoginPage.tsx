import api from "@/utils/api";
import { LoginForm } from "./components/login-form";
import type { AuthCredentials } from "@/types/authentication";
import { API_ROUTES } from "@/utils/constants";
import { toast } from "sonner";
import { useNavigate } from "react-router-dom";
import useUserStore from "@/store/UserStore";
import { Header } from "@/components/Header";

export const LoginPage: React.FC = () => {
  const navigate = useNavigate();

  const handleSubmit = async (formData: AuthCredentials) => {
    try {
      const response = await api.post(API_ROUTES.AUTH.LOGIN, formData);

      if (response.data?.success === true) {
        toast.success(response.data?.message);
        useUserStore.getState().setUser(response.data?.data);
        navigate("/dashboard");
      } else {
        toast.error(response.data?.message);
      }
    } catch {
      toast.error("Some Internal Server Error occured, Please try later!");
    }
  };

  return (
    <div className="space-y-2 flex flex-col h-screen">
      <Header />
      <div className="grid flex-1 place-items-center p-4">
        <LoginForm onSubmit={handleSubmit} />
      </div>
    </div>
  );
};
