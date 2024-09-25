'use server';

import { z } from 'zod';
import { redirect } from 'next/navigation';
import { Aloe } from '@/app/api/db/aloe';
import User from '@/app/api/db/interfaces/user';
import UserAuthentication from '@/app/api/db/interfaces/user-authentication';
import { hashPassword } from '@/app/api/db/authentication';

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

    const { firstName, lastName, email, password } = validatedFields.data;
    const newUser = <User> {
        email: email,
        firstName: firstName,
        lastName: lastName,
    };
    
    const db = new Aloe();

    try {
        db.connect();
        const newUserId = await db.insertUser(newUser)
        console.log(`NewUserID: ${newUserId}`)
        
        // Create user_authentication record
        const [hash, salt] = await hashPassword(password)
        const newUserAuthId = await db.insertUserAuthentication(
            <UserAuthentication> {
                userId: newUserId,
                password: hash,
                salt: salt
            }
        )
        console.log(`NewUserAuthenticationID: ${newUserAuthId}`)

    } catch (error: any) {
        if(error.name === 'AloeExistingUserError' ) {
            return { message: 'An account with that email already exists.' }
        } else {
            return { message: 'Internal error occurred. Please try again.'}
        }
    } finally {
        db.close();
    }

    redirect('/login');

};