"use server";

import { LoginFormSchema } from '@/features/login/schemas'
import { LoginState } from '@/features/login/types'
import { authFetch, RequestParameters } from "@/data-access/auth";


function validateFields(formData: FormData) {
    return LoginFormSchema.safeParse({
        email: formData.get('email'),
        password: formData.get('password'),
    })
}

export async function login(prevState: LoginState, formData: FormData,) {
    const validatedFields = validateFields(formData);
    const enteredValues: { [key: string]: string } = {};
    formData.forEach((value, key) => { enteredValues[key] = value.toString(); });

    if (!validatedFields.success) {
        const formErrors = validatedFields.error.flatten().fieldErrors;
        return { errors: formErrors, formData: enteredValues};
    };
    
    // Login logic
    const { email, password } = enteredValues;
    const authRequest: RequestParameters = {
        method: 'GET',
        endpoint: '/auth/authorize',
        queryParameters: {
            email: email,
            password: password,
            grant_type: 'authorization',
        },
    }

    try {
        const response = await authFetch(authRequest);    
        const data = await response.json()
        
        if (!response.ok) {
            throw new Error(`${data.message}`)
        } else {
            console.log('Authentication request successful.')
            // return data
            console.log(`data: ${JSON.stringify(data)}`)
        }
    } catch (error) {
        const err = error instanceof Error ? error.message : String(error)
        console.log(`Authentication Request Failed: ${err}`);
    }
    return prevState;
};