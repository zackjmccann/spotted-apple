"use client";

import { CreateAccountFormSchema } from '@/app/features/create-account-form-feature/schemas'
import {SignUpState} from '@/app/features/sign-up-feature/types'

function validateFields(formData: FormData) {
    return CreateAccountFormSchema.safeParse({
        email: formData.get('email'),
        firstName: formData.get('firstName'),
        lastName: formData.get('lastName'),
    })
}

export async function createAccount(prevState: SignUpState, formData: FormData,) {
    const validatedFields = validateFields(formData);
    const enterValues: { [key: string]: string } = {};
    formData.forEach((value, key) => { enterValues[key] = value.toString(); });

    if (!validatedFields.success) {
        const formErrors = validatedFields.error.flatten().fieldErrors;
        return {
            created: false,
            passwordSet: false,
            errors: formErrors,
            formData: enterValues};
    };

    return { created: true, passwordSet: false, formData: enterValues, } as SignUpState;
};