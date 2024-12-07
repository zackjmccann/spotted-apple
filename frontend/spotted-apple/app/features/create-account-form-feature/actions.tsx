"use client";

import { CreateAccountFormSchema } from '@/app/features/create-account-form-feature/schemas'
import { SignUpState } from '@/app/features/sign-up-feature/types'

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

    // Check user email
    const email: string = enterValues.email

    // try {
    //     const response = await fetch(
    //         'http://localhost:3000/api/check-email',
    //     {
    //         method: 'POST',
    //         headers: { 'Content-Type': 'application/json' },
    //         body: JSON.stringify({ email }),
    //     });
  
    //     const data = await response.json();
  
    //     if (data.exists) {
    //       alert('Email already exists!');
    //       setEmailExists(true);
    //     } else {
    //       setEmailExists(false);
    //       setShowPasswordInput(true);
    //     }
    //   } catch (error) {
    //     console.error('Error:', error);
    //     alert('Something went wrong');
    //   }

    return { created: true, passwordSet: false, formData: enterValues, } as SignUpState;
};