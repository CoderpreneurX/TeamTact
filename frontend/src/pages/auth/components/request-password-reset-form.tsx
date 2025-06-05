import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  resetPasswordFormSchema,
  type PasswordResetFormData,
} from "@/schemas/authentication";

interface PasswordResetFormProps {
  onSubmit: (data: PasswordResetFormData) => Promise<void>;
}

export function RequestPasswordResetForm({ onSubmit }: PasswordResetFormProps) {
  const [isLoading, setIsLoading] = useState(false);

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<PasswordResetFormData>({
    resolver: zodResolver(resetPasswordFormSchema),
  });

  const handleFormSubmit = async (data: PasswordResetFormData) => {
    try {
      setIsLoading(true);
      await onSubmit(data);
      reset();
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Card className="m-4 p-4 w-full max-w-lg gap-2">
      <CardTitle className="text-xl font-bold">Reset your password</CardTitle>
      <CardDescription>
        Enter your email to receive a link to reset your password.
      </CardDescription>

      <CardContent className="px-0">
        <form
          onSubmit={handleSubmit(handleFormSubmit)}
          className="space-y-4 mt-4"
        >
          <div className="space-y-2">
            <Label htmlFor="email">Email</Label>
            <Input
              type="email"
              id="email"
              placeholder="user@example.com"
              {...register("email")}
              disabled={isLoading}
            />
            {errors.email && (
              <p className="text-sm text-red-500">{errors.email.message}</p>
            )}
          </div>

          <Button className="w-full" type="submit" disabled={isLoading}>
            {isLoading ? "Verifying..." : "Verify"}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}
