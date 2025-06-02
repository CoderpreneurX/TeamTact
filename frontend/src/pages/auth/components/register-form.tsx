import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Link } from "react-router-dom";
import { useForm } from "react-hook-form"; // Import useForm
import { zodResolver } from "@hookform/resolvers/zod"; // Import zodResolver
import type { AuthCredentials } from "@/types/authentication";
import {
  registerFormSchema,
  type RegisterFormValues,
} from "@/schemas/authentication";
import { useState } from "react";
import LogoColoredBackground from "@/assets/ProjectLogo/png/TeamTact Logo - Colored Background.png";
import { Eye, EyeClosed } from "lucide-react";

interface RegisterFormProps {
  className?: string;
  onSubmit: (formData: AuthCredentials) => void;
}

export function RegisterForm({ className, onSubmit }: RegisterFormProps) {
  const [isPasswordVisible, setIsPasswordVisible] = useState<boolean>(false);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  // Initialize react-hook-form with zodResolver
  const {
    register, // Function to register inputs
    handleSubmit, // Function to handle form submission
    formState: { errors }, // Object containing form errors
  } = useForm<RegisterFormValues>({
    resolver: zodResolver(registerFormSchema), // Apply Zod schema for validation
    defaultValues: {
      // Set default values for the form fields
      fullname: "",
      username: "",
      email: "",
      password: "",
    },
  });

  // Function to handle form submission when validation passes
  const handleFormSubmit = async (data: RegisterFormValues) => {
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
          {/* Attach handleSubmit to the form's onSubmit event */}
          <form
            onSubmit={handleSubmit(handleFormSubmit)}
            className="p-6 md:p-8"
          >
            <div className="flex flex-col gap-6">
              <div className="flex flex-col items-center text-center">
                <h1 className="text-2xl font-bold">Getting Started</h1>
                <p className="text-muted-foreground text-balance">
                  Register your TeamTact account
                </p>
              </div>
              <div className="grid gap-3">
                <Label htmlFor="fullname">Full Name</Label>
                <Input
                  id="fullname"
                  type="text"
                  placeholder="M Smith"
                  // Register the input with react-hook-form
                  {...register("fullname")}
                />
                {/* Display validation error message for fullname */}
                {errors.fullname && (
                  <p className="text-xs text-red-500">
                    {errors.fullname.message}
                  </p>
                )}
              </div>
              <div className="grid gap-3">
                <Label htmlFor="username">Username</Label>
                <Input
                  id="username"
                  type="text"
                  placeholder="itz_m_smith"
                  {...register("username")}
                />
                {/* Display validation error message for username */}
                {errors.username && (
                  <p className="text-xs text-red-500">
                    {errors.username.message}
                  </p>
                )}
              </div>
              <div className="grid gap-3">
                <Label htmlFor="email">Email</Label>
                <Input
                  id="email"
                  type="email"
                  placeholder="m@example.com"
                  {...register("email")}
                />
                {/* Display validation error message for email */}
                {errors.email && (
                  <p className="text-xs text-red-500">{errors.email.message}</p>
                )}
              </div>
              <div className="grid gap-3 relative">
                <div className="flex items-center">
                  <Label htmlFor="password">Password</Label>
                </div>
                <Input
                  id="password"
                  placeholder="••••••••••••"
                  type={isPasswordVisible ? "text" : "password"}
                  {...register("password")}
                />
                <div className="absolute top-8 right-2 text-slate-500" onClick={() => setIsPasswordVisible(!isPasswordVisible)}>{isPasswordVisible ? <EyeClosed /> : <Eye />}</div>
                {/* Display validation error message for password */}
                {errors.password && (
                  <p className="text-xs text-red-500">
                    {errors.password.message}
                  </p>
                )}
              </div>
              <Button type="submit" disabled={isLoading} className="w-full">
                {isLoading && (
                  <div className="border-2 border-white border-r-transparent animate-spin h-4 w-4 mr-2 rounded-full" />
                )}
                {isLoading ? "Registering..." : "Register"}
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
                    className="mr-2 h-4 w-4"
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
                Already have an account?{" "}
                <Link to="/login" className="underline underline-offset-4">
                  Login
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
