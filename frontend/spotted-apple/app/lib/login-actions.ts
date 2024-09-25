'use server';

import { z } from 'zod';
import { redirect } from 'next/navigation';
import { Aloe } from '@/app/api/db/aloe';
import User from '@/app/api/db/interfaces/user';
import UserAuthentication from '@/app/api/db/interfaces/user-authentication';
import { validPasswordEntry } from '@/app/api/db/authentication';

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

    const { email, password } = validatedFields.data; // TODO: Change to "entered password"
    const db = new Aloe();

    try {
        db.connect();
        const user = await db.getUser('email', email)
        const userAuthentication = await db.getUserAuthentication(user.userId)
        const validPassword = await validPasswordEntry(password, userAuthentication.password)
        
        if(validPassword) {
            console.log('Login successful')
        } else {
            throw new Error('Authentication failed')
        }
        
    } catch (error: any) {
        console.log(`Error: ${error.name}: ${error.message}`)
        return {
            message: 'Database Error: Failed to log in.',
        };
    } finally {
        db.close();
    }
    redirect('/profile'); // TODO: Decide on a relative landing page
};
