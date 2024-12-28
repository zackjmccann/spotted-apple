import { z } from 'zod';

export const SetPasswordFormSchema = z.object({
    email: z.string().email({ message: "Invalid email address" }),
    password: z
      .string()
      .min(8, "Password must be at least 8 characters long")
      .regex(/[a-z]/, "Password must include at least one lowercase letter")
      .regex(/[A-Z]/, "Password must include at least one uppercase letter")
      .regex(/\d/, "Password must include at least one number")
      .regex(/[!@~#$%^&*(),.?":{}|<>]/, "Password must include at least one special character")
      .regex(/^\S*$/, "Password must not contain spaces"),
    confirmPassword: z.string()
  })
  .refine((data) => data.password === data.confirmPassword, {
    message: "The entered passwords do not match.",
    path: ["confirmPassword"], // path of error
  });