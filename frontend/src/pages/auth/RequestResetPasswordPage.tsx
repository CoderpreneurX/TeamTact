import { RequestPasswordResetForm } from "./components/request-password-reset-form";
import api from "@/utils/api";
import { API_ROUTES, INTERNAL_SERVER_ERROR_MESSAGE } from "@/utils/constants";
import { toast } from "sonner";
import type { PasswordResetFormData } from "@/schemas/authentication";
import { Header } from "@/components/Header";

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
      toast.error(INTERNAL_SERVER_ERROR_MESSAGE)
    }
  }
  return (
    <div className="space-y-2 flex flex-col h-screen">
      <Header />
      <div className="grid flex-1 place-items-center p-4">
        <RequestPasswordResetForm onSubmit={handleSubmit} />
      </div>
    </div>
  );
}
