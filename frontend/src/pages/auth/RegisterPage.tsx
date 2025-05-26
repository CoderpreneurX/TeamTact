import type { AuthCredentials } from "@/types/authentication";
import { RegisterForm } from "./components/register-form";
import api from "@/utils/api";
import { API_ROUTES } from "@/utils/constants";
import { toast } from "sonner";
import { useNavigate } from "react-router-dom";

export const RegisterPage: React.FC = () => {
  const navigate = useNavigate()
  const handleSubmit = async (formData: AuthCredentials) => {
    try {
      const response = await api.post(API_ROUTES.AUTH.REGISTER, formData)

      if (response.data?.success) {
        toast.success(response.data?.message)
        navigate("/login")
      } else {
        toast.error(response.data?.message)
      }
    } catch {
      toast.error("Some Internal Server Error occured, Please try later!")
    }
  }

  return (
    <div className="flex justify-center items-center">
      <RegisterForm onSubmit={handleSubmit} />
    </div>
  );
};
