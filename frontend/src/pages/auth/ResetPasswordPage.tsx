import { useEffect, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import api from "@/utils/api";
import { API_ROUTES, APP_ROUTES } from "@/utils/constants";
import { ResetPasswordForm } from "./components/reset-password-form";
import { AlertCircleIcon, CircleCheckIcon, Loader2 } from "lucide-react";
import type { ResetPasswordData } from "@/schemas/authentication";
import { Header } from "@/components/Header";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

type Status = "loading" | "valid" | "invalid" | "submitting" | "success";

export function ResetPasswordPage() {
  const [URLSearchParams, setURLSearchParams] = useSearchParams();
  const token = URLSearchParams.get("token");
  const [status, setStatus] = useState<Status>("loading");

  useEffect(() => {
    const verifyToken = async () => {
      try {
        const response = await api.post(
          API_ROUTES.AUTH.VALIDATE_RESET_PASSWORD_TOKEN,
          { code: token }
        );

        setStatus(response.data.success ? "valid" : "invalid");
        setURLSearchParams({});
      } catch {
        setStatus("invalid");
      }
    };

    verifyToken();
  }, []);

  const onSubmit = async (data: ResetPasswordData) => {
    try {
      setStatus("submitting");
      await api.post(API_ROUTES.AUTH.CONFIRM_RESET_PASSWORD, {
        token,
        new_password: data.password,
      });
      setStatus("success");
    } catch {
      setStatus("valid");
    }
  };

  let content;

  if (status === "loading") {
    content = (
      <div className="flex items-center gap-x-2 justify-center ">
        <Loader2 className="size-6 animate-spin" />
        Verifying reset link...
      </div>
    );
  } else if (status === "invalid") {
    content = (
      <Card className="">
        <CardContent className="space-y-4">
          <Alert variant="destructive">
            <AlertCircleIcon />
            <AlertTitle>Invalid or Expired Link</AlertTitle>
            <AlertDescription>
              This password reset link is no longer valid. Please request a new
              one.
            </AlertDescription>
          </Alert>
          <Link to={APP_ROUTES.REQUEST_RESET_PASSWORD}>
            <Button className="w-full">Request Reset Password</Button>
          </Link>
        </CardContent>
      </Card>
    );
  } else if (status === "success") {
    content = (
      <Card className="w-full max-w-md">
        <CardContent className="space-y-4">
          <Alert variant="default">
            <CircleCheckIcon />
            <AlertTitle>Password Reset Successful</AlertTitle>
            <AlertDescription>
              You can now log in with your new password.
            </AlertDescription>
          </Alert>
          <Link to={APP_ROUTES.LOGIN}>
            <Button className="w-full">Login to your account</Button>
          </Link>
        </CardContent>
      </Card>
    );
  } else {
    // For "valid" and "submitting"
    content = <ResetPasswordForm onSubmit={onSubmit} />;
  }

  return (
    <div className="space-y-2 flex flex-col h-screen">
      <Header />
      <div className="flex-1 flex justify-center items-center">{content}</div>
    </div>
  );
}
