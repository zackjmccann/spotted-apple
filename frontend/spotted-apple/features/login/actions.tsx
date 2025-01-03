'use server'

import logger from '@/lib/logging'
import { LoginFormSchema } from '@/features/login/schemas'
import { LoginState } from '@/features/login/types'
import { authFetch, RequestParameters } from '@/data-access/auth'
import { getCookie, setCookie, Cookie } from '@/lib/cookies'
import { randomBytes } from 'crypto'
import { redirect } from 'next/navigation'


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
    let redirectUrl: string
    
    // State and code challenges are required for identity authentication requests
    // and must be presevered for subsequent requests. For login authentication
    // requests, 'state' and 'code_challenge' cookies are set.
    // const state = randomBytes(64).toString('hex')
    // const codeChallenge = randomBytes(64).toString('hex')
    // await setCookie({name: 'state', value: state, maxAge: 60} as Cookie)
    // await setCookie({name: 'code_challenge', value: codeChallenge, maxAge: 60} as Cookie)
    
    const { email, password } = enteredValues;
    const authRequest: RequestParameters = {
        method: 'POST',
        endpoint: '/auth/login',
        body: {
            email: email,
            password: password,
            grant_type: 'authorization',
        },
    }

    try {
        const response = await authFetch(authRequest);    

        if (!response.ok) {
            const data = await response.json()
            throw new Error(`${data.message}`)
        } else {
            logger.debug('Authentication request successful.')
            const data = await response.json()
            const code = data['code']
            
            logger.info(`Auth Code: ${code}`)
            redirectUrl = 'http://localhost:3000/profile'
        }
    } catch (error) {
        const err = error instanceof Error ? error.message : String(error)
        logger.error(`Authentication Request Failed: ${err}`);
        redirectUrl = 'http://localhost:3000/test'
    }

    redirect(redirectUrl);
};
