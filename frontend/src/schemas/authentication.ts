import { z } from "zod";

export const loginSchema = z.object({
  email: z.string().email("Enter a valid email"),
  password: z.string().min(6, "Password must be at least 6 characters"),
});

export type LoginFormSchema = z.infer<typeof loginSchema>;

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

export type RegisterFormValues = z.infer<typeof registerFormSchema>;

export const resetPasswordFormSchema = z.object({
  email: z.string().email("Enter a valid email"),
});

export type PasswordResetFormData = z.infer<typeof resetPasswordFormSchema>;
