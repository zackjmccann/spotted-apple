'use server';

import { z } from 'zod';
import { redirect } from 'next/navigation';
import { create } from 'domain';

const CreateAccountFormSchema = z.object({
    firstName: z.string().min(1, { message: "Missing first name" }),
    lastName: z.string().min(1, {message: "Missing last name"}),
    email: z.string().email({ message: "Invalid email address" }),
  });

export type CreateAccountState = {
        message: string;
        errors: { [key: string]: string[] };
        created: boolean;
      } | { created: boolean; message?: undefined; errors?: undefined; }
//     message?: string | null;
//     errors: { [key: string]: string[] };
//     // errors?: {
//     //     firstName?: string[],
//     //     lastName?: string[],
//     //     email?: string[],
//     // };
//     created?: boolean | undefined;
// };

export async function createAccount(prevState: CreateAccountState, formData: FormData,) {
    const validatedFields = CreateAccountFormSchema.safeParse({
        email: formData.get('email'),
        firstName: formData.get('firstName'),
        lastName: formData.get('lastName'),
    });
    
    if (!validatedFields.success) {
        const errors: { [key: string]: string[] } = validatedFields.error.flatten().fieldErrors;
        return {
            message: 'Invalid form entires',
            errors: errors,
            created: false,
        };
    };

    const { firstName, lastName, email} = validatedFields.data;
    // Check if an account already exists
    const existingAccount = true;
    // // If not, collect and store email in browser, render a password creation template
    const cookieCreated = false;
    // return existingAccount;
    return {created: true}

};
