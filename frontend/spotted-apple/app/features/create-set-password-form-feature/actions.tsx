"use client";

import { SetPasswordState } from '@/app/features/create-set-password-form-feature/types'
import { SetPasswordFormSchema } from '@/app/features/create-set-password-form-feature/schemas'

function validateFields(formData: FormData) {
    return SetPasswordFormSchema.safeParse({
        email: formData.get('email'),
        password: formData.get('password'),
        confirmPassword: formData.get('confirmPassword'),
    })
}

export async function setPassword(prevState: SetPasswordState, formData: FormData,) {
    const validatedFields = validateFields(formData);
    if (!validatedFields.success) {
        const formErrors = validatedFields.error.flatten().fieldErrors;
        const enterValues: { [key: string]: string | File } = {};
        formData.forEach((value, key) => { enterValues[key] = value; });
        return {
            passwordSet: false,
            errors: formErrors,
            formData: enterValues};
    };


    return {passwordSet: true} as SetPasswordState;

};