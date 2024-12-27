"use server";

import { ClientCredentials, RequestParameters } from '@/data-access/auth/types'
import { cookies } from 'next/headers';

const clientCredentials: ClientCredentials = {
    origin: process.env.ORIGIN,
    authServer: process.env.AUTH_SERVER,
    username:process.env.CLIENT_USERNAME,
    password: process.env.CLIENT_PASSWORD,
    appId: parseInt(process.env.APP_ID!),
}

async function authenticateWithBackend() {
    const {origin, authServer, username, password, appId} = clientCredentials
    const method: string =  'POST'
    const endpoint: string = '/auth/token'
    const url = `${authServer}${endpoint}`
    const body: object = {
        username: username,
        password: password,
        id: appId,
        grant_type: 'client_credentials',
    }    
    
    const options: RequestInit = {
        method,
        headers: {
            'Content-Type': 'application/json',
            'Origin': origin!, 
            'Access-Control-Request-Method': 'OPTIONS',
            'Access-Control-Request-Headers': 'Content-Type, Authorization',
        },
        credentials: 'include'
    };
    
    options.body = JSON.stringify(body);
    
    try {
        const response = await fetch(url, options);    
        const data = await response.json()
        
        if (!response.ok) {
            throw new Error(`${data.message}`)
        } else {
            console.log('Authentication request successful.')
            return data
        }
    } catch (error) {
        const err = error instanceof Error ? error.message : String(error)
        console.log(`Authentication Request Failed: ${err}`);
    }
}

async function refreshTokens(refreshToken: string) {
    const {origin, authServer} = clientCredentials
    const method: string =  'POST'
    const endpoint: string = '/auth/refresh'
    const url = `${authServer}${endpoint}`
    const body: object = { refresh_token: refreshToken }    
    const options: RequestInit = {
        method,
        headers: {
            'Content-Type': 'application/json',
            'Origin': origin!, 
            'Access-Control-Request-Method': 'OPTIONS',
            'Access-Control-Request-Headers': 'Content-Type, Authorization',
        },
        credentials: 'include'
    };
    
    options.body = JSON.stringify(body);
    
    try {
        const response = await fetch(url, options);    
        const data = await response.json()
        
        if (!response.ok) {
            throw new Error(`${data.message}`)
        } else {
            console.log('Token refresh request successful.')
            return data
        }
    } catch (error) {
        const err = error instanceof Error ? error.message : String(error)
        console.log(`Token refresh request failed: ${err}`);
    }
}

async function setAuthenticationCookies(authData: Record<string, string>) {
    const cookie_configs: Record<string, number> = {
        // 'access_token': 60 * 15, // 15 minutes
        'access_token': 10, // 10 seconds
        'refresh_token': 7 * 24 * 60 * 60, // 7 days
    }
    
    for (const [key, value] of Object.entries(authData)) {
        if (key != 'status') {
            (await cookies()).set({
                name: key,
                value: value,
                httpOnly: true,
                secure: true,
                sameSite: 'strict',
                maxAge: cookie_configs[key],
            })
        }
    }
}

export async function getAccessToken() {
    const cookieManager = await cookies()
    const hasAccessToken = cookieManager.has('access_token')
    const hasRefreshToken = cookieManager.has('refresh_token')
    
    if (!hasAccessToken && !hasRefreshToken) {
        console.log('no tokens found...')
        const authResponseData = await authenticateWithBackend()
        await setAuthenticationCookies(authResponseData)
    }
    
    if (!hasAccessToken) {
        console.log('refreshing tokens...')
        const tokenRefreshResponseData = await refreshTokens(cookieManager.get('refresh_token')!.value)
        await setAuthenticationCookies(tokenRefreshResponseData)
    }
    
    const token = cookieManager.get('access_token')
    return token!.value
}

async function authService(requestData: RequestParameters) {
    const {origin, authServer} = clientCredentials
    const method = requestData.method
    const url = `${authServer}${requestData.endpoint}` 
    const options: RequestInit = {
        method,
        headers: {
            'Content-Type': 'application/json',
            'Origin': origin!, 
            'Access-Control-Request-Method': 'OPTIONS',
            'Access-Control-Request-Headers': 'Content-Type, Authorization',
            'Authorization': `Bearer ${requestData.authToken}`,
            ...requestData.headers
        },
        credentials: 'include'
    };
    
    options.body = JSON.stringify(requestData.body);
    
    try {
        const response = await fetch(url, options);            
        if (!response.ok) {
            throw new Error(`${(await response.json()).message}`)
        } else {
            return response
        }
    } catch (error) {
        const err = error instanceof Error ? error.message : String(error)
        console.log(`Authentication Service Request Failed: ${err}`);
    }
}

export async function checkIfEmailExists(email: string): Promise<boolean | null> {
    let emailExists = null
    const token = await getAccessToken()
    const requestdata: RequestParameters = {
        method: 'POST',
        endpoint: '/register/introspect',
        body: {'email': email},
        authToken: token,
    }

    try {
        const response = await authService(requestdata)
        try {
            const data = await response!.json()
            emailExists = data['registered']
        } catch (error) {
            console.error('Failed to process response:', error)
        }
    } catch (error) {
        console.error('Failed to check email register:', error)
    }
    return emailExists
}