"use server";

import { ClientCredentials} from '@/features/auth/types'
import { cookies } from 'next/headers';

const clientCredentials: ClientCredentials = {
    origin: process.env.ORIGIN,
    authServer: process.env.AUTH_SERVER,
    username:process.env.CLIENT_USERNAME,
    password: process.env.CLIENT_PASSWORD,
    appId: parseInt(process.env.APP_ID!),
}

export async function authenticateWithBackend() {
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
            // return data['access_token']
            // await setAuthenticationCookies(data)
            return data
        }
    } catch (error) {
        const err = error instanceof Error ? error.message : String(error)
        console.log(`Authentication Request Failed: ${err}`);
    }
}

export async function setAuthenticationCookies(authData: Record<string, string>) {
    const cookie_configs: Record<string, number> = {
        'access_token': 60 * 15, // 15 minutes
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
                expires: cookie_configs[key],
            })
        }
    }
}

async function getAccessToken() {
    const cookieManager = await cookies()
    const hasAccessToken = cookieManager.has('access_token')
    const hasRefreshToken = cookieManager.has('refresh_token')
    
    if (!hasAccessToken && !hasRefreshToken) {
        console.log('no tokens found...')
        const authResponseData = await authenticateWithBackend()
        setAuthenticationCookies(authResponseData)
    }
    
    // if (!hasAccessToken) {
    //     console.log('refreshing tokens...')
    //     return await refreshTokens(cookieManager.get('refresh_token')!.value)
    // }

    const token = cookieManager.get('access_token')
    return token!.value
}