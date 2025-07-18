import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Link } from "react-router-dom";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useState } from "react";
import { loginSchema } from "@/schemas/authentication";
import type { LoginFormSchema } from "@/schemas/authentication";
import { Eye, EyeClosed } from "lucide-react";
import LogoColoredBackground from "@/assets/ProjectLogo/png/TeamTact Logo - Colored Background.png"

interface LoginFormProps {
  className?: string;
  onSubmit: (formData: LoginFormSchema) => void;
}

export function LoginForm({ className, onSubmit }: LoginFormProps) {
  const [isLoading, setIsLoading] = useState(false);
  const [isPasswordVisible, setIsPasswordVisible] = useState<boolean>(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginFormSchema>({
    resolver: zodResolver(loginSchema),
  });

  const handleFormSubmit = async (data: LoginFormSchema) => {
    setIsLoading(true);
    try {
      await onSubmit(data);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={cn("flex flex-col gap-6", className)}>
      <Card className="overflow-hidden p-0">
        <CardContent className="grid p-0 md:grid-cols-2">
          <form
            className="p-6 md:p-8"
            onSubmit={handleSubmit(handleFormSubmit)}
          >
            <div className="flex flex-col gap-6">
              <div className="flex flex-col items-center text-center">
                <h1 className="text-2xl font-bold">Welcome back</h1>
                <p className="text-muted-foreground text-balance">
                  Login to your TeamTact account
                </p>
              </div>

              <div className="grid gap-3">
                <Label htmlFor="email">Email</Label>
                <Input
                  id="email"
                  type="email"
                  placeholder="m@example.com"
                  {...register("email")}
                />
                {errors.email && (
                  <p className="text-xs text-destructive">
                    {errors.email.message}
                  </p>
                )}
              </div>

              <div className="grid gap-3 relative">
                <div className="flex items-center">
                  <Label htmlFor="password">Password</Label>
                  <Link
                    to="/request-reset-password"
                    className="ml-auto text-sm underline-offset-2 hover:underline"
                  >
                    Forgot your password?
                  </Link>
                </div>
                <Input
                  id="password"
                  type={isPasswordVisible ? "text" : "password"}
                  placeholder="••••••••••••"
                  {...register("password")}
                />
                <div
                  onClick={() => setIsPasswordVisible(!isPasswordVisible)}
                  className="absolute top-9.5 right-2 text-slate-500"
                >
                  {isPasswordVisible ? <EyeClosed /> : <Eye />}
                </div>
                {errors.password && (
                  <p className="text-xs text-destructive">
                    {errors.password.message}
                  </p>
                )}
              </div>

              <Button type="submit" disabled={isLoading} className="w-full">
                {isLoading && (
                  <div className="border-2 border-white border-r-transparent animate-spin h-4 w-4 mr-2 rounded-full" />
                )}
                {isLoading ? "Logging in..." : "Login"}
              </Button>

              <div className="after:border-border relative text-center text-sm after:absolute after:inset-0 after:top-1/2 after:z-0 after:flex after:items-center after:border-t">
                <span className="bg-card text-muted-foreground relative z-10 px-2">
                  Or continue with
                </span>
              </div>

              <div className="grid gap-4">
                <Button variant="outline" type="button" className="w-full">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 24 24"
                    className="h-4 w-4 mr-2"
                  >
                    <path
                      d="M12.48 10.92v3.28h7.84c-.24 1.84-.853 3.187-1.787 4.133-1.147 1.147-2.933 2.4-6.053 2.4-4.827 0-8.6-3.893-8.6-8.72s3.773-8.72 8.6-8.72c2.6 0 4.507 1.027 5.907 2.347l2.307-2.307C18.747 1.44 16.133 0 12.48 0 5.867 0 .307 5.387.307 12s5.56 12 12.173 12c3.573 0 6.267-1.173 8.373-3.36 2.16-2.16 2.84-5.213 2.84-7.667 0-.76-.053-1.467-.173-2.053H12.48z"
                      fill="currentColor"
                    />
                  </svg>
                  <span className="sr-only">Login with Google</span>
                </Button>
              </div>

              <div className="text-center text-sm">
                Don&apos;t have an account?{" "}
                <Link to="/register" className="underline underline-offset-4">
                  Sign up
                </Link>
              </div>
            </div>
          </form>

          <div className="bg-logo-background relative hidden md:block">
            <img
              src={LogoColoredBackground}
              alt="TeamTact Logo"
              className="absolute top-[calc(50%-30px)] left-[calc(50%-115px)]"
              onError={(e) => {
                e.currentTarget.src =
                  "https://placehold.co/600x400/E5E7EB/1F2937?text=TeamTact";
              }}
            />
          </div>
        </CardContent>
      </Card>

      <div className="text-muted-foreground *:[a]:hover:text-primary text-center text-xs text-balance *:[a]:underline *:[a]:underline-offset-4">
        By clicking continue, you agree to our <a href="#">Terms of Service</a>{" "}
        and <a href="#">Privacy Policy</a>.
      </div>
    </div>
  );
}
