import LogoTransparent from "@/assets/ProjectLogo/png/TeamTact Logo - Transparent Background.png"
import { RequestPasswordResetForm } from "./components/request-password-reset-form";
import api from "@/utils/api";
import { API_ROUTES } from "@/utils/constants";
import { toast } from "sonner";
import type { PasswordResetFormData } from "@/schemas/authentication";

export function RequestResetPasswordPage() {
  const handleSubmit = async (email: PasswordResetFormData) => {
    try {
      const response = await api.post(API_ROUTES.AUTH.REQUEST_RESET_PASSWORD, email)

      if (response.data?.success === true) {
        toast.success(response.data?.message)
      } else {
        toast.error(response.data?.message)
      }
    } catch {
      toast.error("Some Internal Error occured, please try later!")
    }
  }
  return (
    <div className="space-y-2 flex flex-col h-screen">
      <header className="h-15 p-1.5 sticky top-0 bg-white z-10 border-b">
        <img
          src={LogoTransparent}
          alt="TeamTact Logo"
          className="h-12 w-auto"
        />
      </header>
      <div className="grid flex-1 place-items-center p-4">
        <RequestPasswordResetForm onSubmit={handleSubmit} />
      </div>
    </div>
  );
}
