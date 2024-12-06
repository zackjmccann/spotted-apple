import { z } from 'zod';

export const CreateAccountFormSchema = z.object({
    firstName: z.string().min(1, { message: "Missing first name" }),
    lastName: z.string().min(1, {message: "Missing last name"}),
    email: z.string().email({ message: "Invalid email address" }),
  });

