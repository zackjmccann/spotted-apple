'use server';

import { z } from 'zod';
import { redirect } from 'next/navigation';

const LoginFormSchema = z.object({
    email: z.string().email({ message: "Invalid email address" }),
    password: z.string()
  });

export type LoginState = {
    errors?: {
        email?: string[];
        password?: string[];
    };
    message?: string | null;
};


export async function loginUser(prevState: LoginState, formData: FormData) {
    // Validate form fields using Zod
    const validatedFields = LoginFormSchema.safeParse({
        email: formData.get('email'),
        password: formData.get('password'),
    });

    // If form validation fails, return errors early. Otherwise, continue.
    if (!validatedFields.success) {
        return {
            errors: validatedFields.error.flatten().fieldErrors,
            message: 'Log in failed.',
        };
    };

    // Prepare data for validation against database
    const { email, password } = validatedFields.data;

    // Login/Authentication logic 
    try {
        const login = false;

    } catch (error) {
        // If a database error occurs, return a more specific error.
        return {
        message: 'Database Error: Failed to log in.',
        };

    };

    // Redirect the user.
    redirect('/profile'); // TODO: Decide on a relative landing page

};
