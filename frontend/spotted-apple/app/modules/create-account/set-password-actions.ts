'use server';

import { z } from 'zod';
import { redirect } from 'next/navigation';

const SetPasswordFormSchema = z.object({
    email: z.string().email({ message: "Invalid email address" }),
    password: z.string(),
    confirmPassword: z.string()
  })
  .refine((data) => data.password === data.confirmPassword, {
    message: "The entered passwords do not match.",
    path: ["confirmPassword"], // path of error
  });

export type SetPasswordState = {
    errors?: {
        email?: string[];
        password?: string[];
        confirmPassword?: string[];
    };
    message?: string | null;
};


export async function setPassword(prevState: SetPasswordState, formData: FormData) {
    const validatedFields = SetPasswordFormSchema.safeParse({
        email: formData.get('email'),
        password: formData.get('password'),
        confirmPassword: formData.get('confirmPassword'),
    });
    
    if (!validatedFields.success) {
        console.log(validatedFields.error.flatten().fieldErrors)
        return {
            errors: validatedFields.error.flatten().fieldErrors,
            message: 'Set password failed.',
        };
    };
    
    const { email, password} = validatedFields.data;

    // Check if an account already exists
    const passwordSet = true;

    if(passwordSet) {
        redirect('/login');
    } else {
        // Rended new component
        redirect('/');
    }

};
