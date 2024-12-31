"use server";

import logger from '@/lib/logging'
import { ClientCredentials, RequestParameters, AccountCreationData } from '@/data-access/auth/types'
import { setCookie, getCookie, checkForCookie, Cookie } from '@/lib/cookies'
import { authFetch } from '@/data-access/auth'


const clientCredentials: ClientCredentials = {
    username: process.env.CLIENT_USERNAME,
    password: process.env.CLIENT_PASSWORD,
    appId: parseInt(process.env.APP_ID),
}

async function authenticateWithBackend() {
    const {username, password, appId} = clientCredentials
    const authRequest: RequestParameters = {
        method: 'POST',
        endpoint: '/auth/token',
        body: {
            username: username!,
            password: password!,
            id: appId!,
            grant_type: 'client_credentials',
        } 
    }

    try {
        const response = await authFetch(authRequest);    
        const data = await response.json()
        
        if (!response.ok) {
            throw new Error(`${data.message}`)
        } else {
            logger.debug('Authentication request successful.')
            return data
        }
    } catch (error) {
        const err = error instanceof Error ? error.message : String(error)
        logger.error(`Authentication Request Failed: ${err}`);
    }
}

async function refreshTokens(refreshToken: string) {
    const authRequest: RequestParameters = {
        method: 'POST',
        endpoint: '/auth/refresh',
        body: { refresh_token: refreshToken } 
    }

    try {
        const response = await authFetch(authRequest);      
        const data = await response.json()
        
        if (!response.ok) {
            throw new Error(`${data.message}`)
        } else {
            logger.debug('Token refresh request successful.')
            return data
        }
    } catch (error) {
        const err = error instanceof Error ? error.message : String(error)
        logger.debug(`Token refresh request failed: ${err}`);
    }
}

async function setAuthenticationCookies(authData: Record<string, string>) {
    const cookie_configs: Record<string, number> = {
        'access_token': 10, // 10 seconds
        'refresh_token': 7 * 24 * 60 * 60, // 7 days
        'user_access_token': 10,
        'user_refresh_token': 7 * 24 * 60 * 60,
    }
    
    for (const [key, value] of Object.entries(authData)) {
        if (key != 'status') {
            await setCookie({
                name: key,
                value: value,
                httpOnly: true,
                secure: true,
                sameSite: 'lax',
                maxAge: cookie_configs[key],
            } as Cookie);
        }
    }
}

export async function getAccessToken() {
    const hasAccessToken = await checkForCookie('access_token')
    const hasRefreshToken = await checkForCookie('refresh_token')

    if (!hasAccessToken && hasRefreshToken) {
        const refreshTokenValue = await getCookie('refresh_token')
        const tokenRefreshResponseData = await refreshTokens(refreshTokenValue)
        await setAuthenticationCookies(tokenRefreshResponseData)
    } else if (!hasAccessToken) {
        const authResponseData = await authenticateWithBackend()
        await setAuthenticationCookies(authResponseData)
    }
    return await getCookie('access_token')
}

export async function checkIfEmailExists(email: string): Promise<boolean | null> {
    let emailExists = null
    const token = await getAccessToken()
    const requestdata: RequestParameters = {
        method: 'POST',
        endpoint: '/register/introspect',
        body: {'email': email},
        headers: {Authorization: `Bearer ${token}`},
    }
    
    try {
        const response = await authFetch(requestdata)
        try {
            const data = await response!.json()
            emailExists = data['registered']
        } catch (error) {
            logger.error('Failed to process response:', error)
        }
    } catch (error) {
        logger.error('Failed to check email register:', error)
    }
    return emailExists
}

export async function createAccount({email, password, firstName, lastName}: AccountCreationData) {
    const token = await getAccessToken()
    
    const requestdata: RequestParameters = {
        method: 'POST',
        endpoint: '/register/account',
        body: {
            email: email,
            password: password,
            firstName: firstName,
            lastName: lastName
        },
        headers: {Authorization: `Bearer ${token}`},
    }

    try {
        const response = await authFetch(requestdata)
        try {
            const userData = await response!.json()
            await setAuthenticationCookies(userData)
        } catch (error) {
            logger.error('Failed to process response:', error)
        }
    } catch (error) {
        logger.error('Failed to register account:', error)
    }
}