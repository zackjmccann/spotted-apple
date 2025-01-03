'use server'

import logger from '@/lib/logging'
import { LoginFormSchema } from '@/features/login/schemas'
import { LoginState, AccessTokens } from '@/features/login/types'
import { opsFetch, RequestParameters } from '@/data-access/auth'
import { getCookie, setCookie, Cookie } from '@/lib/cookies'
// import { randomBytes } from 'crypto'
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
    
    let redirectUrl: string = process.env.ORIGIN

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
    
    const authCode = await getAuthorizationCode(authRequest); 
    
    if (authCode) {
        const tokenRequest: RequestParameters = {
            method: 'POST',
            endpoint: '/auth/token/exchange',
            body: { code: authCode, grant_type: 'authentication_code' },
        }
        
        const tokens = await getAccessTokens(tokenRequest); 
        
        if (tokens) {
            setCookie({name: 'idToken', value: tokens.idToken} as Cookie)
            setCookie({name: 'acccessToken', value: tokens.accessToken} as Cookie)
            setCookie({name: 'refreshToken', value: tokens.refreshToken} as Cookie)
            redirectUrl = `${redirectUrl}/profile`

        } else {
            logger.error(`Authentication Request Failed: No tokens received.`);
            redirectUrl = redirectUrl = `${redirectUrl}/test`
        }

    } else {
        logger.error(`Authentication Request Failed: No auth code received.`);
        redirectUrl = redirectUrl = `${redirectUrl}/test`
    }

    redirect(redirectUrl);
};


async function getAuthorizationCode(authRequest: RequestParameters): Promise<string | undefined> {
    try {
        const response = await opsFetch(authRequest);    
        if (!response.ok) {
            const data = await response.json()
            throw new Error(`${data.message}`)

        } else {
            const data = await response.json()            
            return data['code']
        }
    } catch (error) {
        const err = error instanceof Error ? error.message : String(error)
        logger.error(`Authentication Request Failed: ${err}`);
        return undefined
    }
}

async function getAccessTokens(tokenRequest: RequestParameters): Promise<AccessTokens | undefined> {
    try {
        const response = await opsFetch(tokenRequest);    
        if (!response.ok) {
            const data = await response.json()
            throw new Error(`${data.message}`)
    
        } else {
            const data = await response.json()
            return {
                idToken: data.id_token,
                accessToken: data.access_token,
                refreshToken: data.refresh_token,
            } as AccessTokens
        }

    } catch (error) {
        const err = error instanceof Error ? error.message : String(error)
        logger.error(`Authentication Request Failed: ${err}`);
        return undefined
    }
}
