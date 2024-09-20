'use server';

import { z } from 'zod';
import { redirect } from 'next/navigation';
import { Aloe } from '@/db/aloe';

const LoginFormSchema = z.object({
    email: z.string().email({ message: "Invalid email address or password." }),
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
    const validatedFields = LoginFormSchema.safeParse({
        email: formData.get('email'),
        password: formData.get('password'),
    });

    if (!validatedFields.success) {
        return {
            errors: validatedFields.error.flatten().fieldErrors,
            message: 'Log in failed.',
        };
    };

    const { email, password } = validatedFields.data;

    try {
        console.log(`email: ${email}`)
        console.log(`password: ${password}`)

    } catch (error) {
        // If a database error occurs, return a more specific error.
        return {
            message: 'Database Error: Failed to log in.',
        };
    };

    // Redirect the user.
    redirect('/profile'); // TODO: Decide on a relative landing page

};
