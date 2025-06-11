import { z } from "zod";

export const loginSchema = z.object({
  email: z.string().email("Enter a valid email"),
  password: z.string().min(6, "Password must be at least 6 characters"),
});

export const registerFormSchema = z.object({
  fullname: z.string().min(1, { message: "Full Name is required." }),
  username: z.string().min(1, { message: "Username is required." }),
  email: z
    .string()
    .email({ message: "Invalid email address." })
    .min(1, { message: "Email is required." }),
  password: z
    .string()
    .min(8, { message: "Password must be at least 8 characters." }),
});

export const resetPasswordFormSchema = z.object({
  email: z.string().email("Enter a valid email"),
});

export const requestEmailVerificationSchema = z.object({
  email: z.string().email("Enter a valid email"),
});

export const resetPasswordSchema = z
  .object({
    password: z.string().min(8, "Password must be at least 8 characters long"),
    confirmPassword: z.string(),
  })
  .refine((data) => data.password === data.confirmPassword, {
    message: "Passwords do not match",
    path: ["confirmPassword"],
  });

export type LoginFormSchema = z.infer<typeof loginSchema>;
export type RegisterFormValues = z.infer<typeof registerFormSchema>;
export type PasswordResetFormData = z.infer<typeof resetPasswordFormSchema>;
export type ResetPasswordData = z.infer<typeof resetPasswordSchema>;
export type RequestEmailVerificationFormData = z.infer<typeof requestEmailVerificationSchema>;
