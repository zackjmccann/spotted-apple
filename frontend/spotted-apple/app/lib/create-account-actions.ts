'use server';

import { z } from 'zod';
import { redirect } from 'next/navigation';
import { Aloe } from '@/db/aloe';

const CreateAccountFormSchema = z.object({
    firstName: z.string(),
    lastName: z.string(),
    email: z.string().email({ message: "Invalid email address" }),
    password: z.string(),
    passwordConfirmation: z.string(),
})
.refine((data) => data.password === data.passwordConfirmation, {
  message: "The entered passwords do not match.",
  path: ["confirmPassword"], // path of error
});

export type CreateAccountState = {
    errors?: {
        firstName?: string[];
        lastName?: string[];
        email?: string[];
        password?: string[];
        passwordConfirmation?: string[];
    };
    message?: string | null;
};

export async function createAccount(prevState: CreateAccountState, formData: FormData) {
    // Validate form fields
    const validatedFields = CreateAccountFormSchema.safeParse({
        firstName: formData.get('firstName'),
        lastName: formData.get('lastName'),
        email: formData.get('email'),
        password: formData.get('password'),
        passwordConfirmation: formData.get('passwordConfirmation')
    });

    if(!validatedFields.success) {
        return {
            errors: validatedFields.error.flatten().fieldErrors,
            message: 'Failed to create new account.',
        };
    };

    // Clean fields
    const { firstName, lastName, email, password } = validatedFields.data;

    // Create Account
    try {
        console.log(`firstName: ${firstName}`)
        console.log(`lastName: ${lastName}`)
        console.log(`email: ${email}`)
        console.log(`password: ${password}`)

    } catch (error) {
        // If a database error occurs, return a more specific error.
        return {
            message: 'Database Error: Failed to create account.',
        };
    };

    // Redirect the user.
    redirect('/login'); // TODO: Decide on a relative landing page

};