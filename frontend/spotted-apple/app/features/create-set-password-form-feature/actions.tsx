"use client";

import { SetPasswordFormSchema } from '@/app/features/create-set-password-form-feature/schemas'
import { SignUpState } from '@/app/features/sign-up-feature/types'

function validateFields(formData: FormData) {
    return SetPasswordFormSchema.safeParse({
        email: formData.get('email'),
        password: formData.get('password'),
        confirmPassword: formData.get('confirmPassword'),
    })
}

export async function setPassword(prevState: SignUpState, formData: FormData,) {
    const validatedFields = validateFields(formData);
    const enterValues: { [key: string]: string } = {};
    formData.forEach((value, key) => { enterValues[key] = value.toString(); });

    if (!validatedFields.success) {
        const formErrors = validatedFields.error.flatten().fieldErrors;
        return {
            created: prevState.created,
            passwordSet: false,
            errors: formErrors,
            formData: enterValues};
    };

    return {created: prevState.created, passwordSet: true, formData: enterValues} as SignUpState;
    ;
};