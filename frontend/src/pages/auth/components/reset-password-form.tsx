import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useState } from "react";
import { Eye, EyeClosed, Loader2 } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  resetPasswordSchema,
  type ResetPasswordData,
} from "@/schemas/authentication";

interface ResetPasswordFormProps {
  onSubmit: (data: ResetPasswordData) => void;
}

export function ResetPasswordForm({ onSubmit }: ResetPasswordFormProps) {
  const [arePasswordsVisible, setArePasswordsVisible] = useState({
    password: false,
    confirmPassword: false,
  });

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<ResetPasswordData>({
    resolver: zodResolver(resetPasswordSchema),
  });

  return (
    <Card className="w-full max-w-md">
      <CardHeader>
        <CardTitle className="text-xl font-bold">Reset Your Password</CardTitle>
        <CardDescription>Enter a new password to use for authentication</CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          {/* New Password */}
          <div className="space-y-2 relative">
            <Label htmlFor="password">New Password</Label>
            <Input
              id="password"
              type={arePasswordsVisible.password ? "text" : "password"}
              {...register("password")}
            />
            <div
              onClick={() =>
                setArePasswordsVisible((prev) => ({
                  ...prev,
                  password: !prev.password,
                }))
              }
              className="absolute top-7 text-slate-600 right-2 cursor-pointer"
            >
              {arePasswordsVisible.password ? <EyeClosed /> : <Eye />}
            </div>
            {errors.password && (
              <p className="text-sm text-red-600">{errors.password.message}</p>
            )}
          </div>

          {/* Confirm Password */}
          <div className="space-y-2 relative">
            <Label htmlFor="confirmPassword">Confirm New Password</Label>
            <Input
              id="confirmPassword"
              type={arePasswordsVisible.confirmPassword ? "text" : "password"}
              {...register("confirmPassword")}
            />
            <div
              onClick={() =>
                setArePasswordsVisible((prev) => ({
                  ...prev,
                  confirmPassword: !prev.confirmPassword,
                }))
              }
              className="absolute top-7 text-slate-600 right-2 cursor-pointer"
            >
              {arePasswordsVisible.confirmPassword ? <EyeClosed /> : <Eye />}
            </div>
            {errors.confirmPassword && (
              <p className="text-sm text-red-600">
                {errors.confirmPassword.message}
              </p>
            )}
          </div>

          <Button type="submit" className="w-full" disabled={isSubmitting}>
            {isSubmitting && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
            Reset Password
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}
