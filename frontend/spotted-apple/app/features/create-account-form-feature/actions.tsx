"use client";

import { CreateAccountState } from '@/app/features/create-account-form-feature/types'
import { CreateAccountFormSchema } from '@/app/features/create-account-form-feature/schemas'

function validateFields(formData: FormData) {
    return CreateAccountFormSchema.safeParse({
        email: formData.get('email'),
        firstName: formData.get('firstName'),
        lastName: formData.get('lastName'),
    })
}

export async function createAccount(prevState: CreateAccountState, formData: FormData,) {
    const validatedFields = validateFields(formData);
    if (!validatedFields.success) {
        const formErrors = validatedFields.error.flatten().fieldErrors;
        const enterValues: { [key: string]: string } = {};
        formData.forEach((value, key) => { enterValues[key] = value.toString(); });
        return {
            created: false,
            errors: formErrors,
            formData: enterValues};
    };

    const { firstName, lastName, email} = validatedFields.data;
    // Check if an account already exists
    const existingAccount = true;
    // // If not, collect and store email in browser, render a password creation template
    const cookieCreated = false;
    // return existingAccount;
    return {created: true} as CreateAccountState;

};