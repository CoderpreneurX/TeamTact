import { useEffect, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import api from "@/utils/api";
import { API_ROUTES, APP_ROUTES } from "@/utils/constants";
import { AlertCircleIcon, CircleCheckIcon, Loader2 } from "lucide-react";
import { Header } from "@/components/Header";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

type Status = "loading" | "valid" | "invalid";

export function VerifyEmailPage() {
  const [URLSearchParams] = useSearchParams();
  const token = URLSearchParams.get("token");
  const [status, setStatus] = useState<Status>("loading");

  useEffect(() => {
    const verifyEmail = async () => {
      try {
        const response = await api.post(
          API_ROUTES.AUTH.VERIFY_EMAIL,
          { token: token }
        );

        setStatus(response.data.success ? "valid" : "invalid");
      } catch {
        setStatus("invalid");
      }
    };

    if (token) {
      verifyEmail();
    } else {
      setStatus("invalid")
    }

  }, [token]);

  let content;

  if (status === "loading") {
    content = (
      <div className="flex items-center gap-x-2 justify-center ">
        <Loader2 className="size-6 animate-spin" />
        Verifying your email...
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
              This email verification link is no longer valid. Please re-check the link or request a new
              one.
            </AlertDescription>
          </Alert>
          <Link to={APP_ROUTES.REQUEST_EMAIL_VERIFICATION}>
            <Button className="w-full">Request Email Verification</Button>
          </Link>
        </CardContent>
      </Card>
    );
  } else {
    content = (
      <Card className="w-full max-w-md">
        <CardContent className="space-y-4">
          <Alert variant="default">
            <CircleCheckIcon />
            <AlertTitle>Email Verification Successful</AlertTitle>
            <AlertDescription>
              You can now log in to you account.
            </AlertDescription>
          </Alert>
          <Link to={APP_ROUTES.LOGIN}>
            <Button className="w-full">Login to your account</Button>
          </Link>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="space-y-2 flex flex-col h-screen">
      <Header />
      <div className="flex-1 flex justify-center items-center">{content}</div>
    </div>
  );
}
