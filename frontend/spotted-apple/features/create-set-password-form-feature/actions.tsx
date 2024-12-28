"use server";

import { SetPasswordFormSchema } from '@/features/create-set-password-form-feature/schemas'
import { SignUpState } from '@/features/sign-up-feature/types'
import { createAccount } from '@/data-access/auth/auth'
import { AccountCreationData } from '@/data-access/auth/types'
import { cookies } from 'next/headers';


function validateFields(formData: FormData) {
    return SetPasswordFormSchema.safeParse({
        email: formData.get('email'),
        password: formData.get('password'),
        confirmPassword: formData.get('confirmPassword'),
    })
}

export async function setPassword(prevState: SignUpState, formData: FormData) {
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

    const enteredAccountData: AccountCreationData = {
        email: enterValues.email,
        password: enterValues.password,
        firstName: prevState.accountData!['firstName'],
        lastName: prevState.accountData!['lastName'],
    }

    await createAccount(enteredAccountData)

    const cookieManager = await cookies()
    const hasUserAccessToken = cookieManager.has('user_access_token')

    if (!hasUserAccessToken) {
        return {
            created: prevState.created,
            passwordSet: false,
            formData: enterValues
        } as SignUpState;
        
    }
    return { created: prevState.created, passwordSet: true, } as SignUpState;
    ;
};