import { z } from 'zod';

export const SetPasswordFormSchema = z.object({
    email: z.string().email({ message: "Invalid email address" }),
    password: z.string(),
    confirmPassword: z.string()
  })
  .refine((data) => data.password === data.confirmPassword, {
    message: "The entered passwords do not match.",
    path: ["confirmPassword"], // path of error
  });