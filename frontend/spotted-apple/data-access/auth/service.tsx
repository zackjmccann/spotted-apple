"use server";

import { RequestParameters, AuthCredentials } from "@/data-access/types";
import { cookies } from 'next/headers';


const credentials: AuthCredentials = {
    origin: process.env.NEXT_PUBLIC_ORIGIN!,
    authServer: process.env.NEXT_PUBLIC_AUTH_SERVER!,
    username: process.env.NEXT_PUBLIC_CLIENT_USERNAME!,
    password: process.env.NEXT_PUBLIC_CLIENT_PASSWORD!,
    appId: parseInt(process.env.NEXT_PUBLIC_APP_ID!),
}


async function authenticateWithBackend() {
    const {origin, authServer, username, password, appId} = credentials
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
            'Origin': origin, 
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
            return data['access_token']
        }
    } catch (error) {
        const err = error instanceof Error ? error.message : String(error)
        console.log(`Authentication Request Failed: ${err}`);
    }
}

async function refreshTokens(refreshToken: string) {
    const {origin, authServer} = credentials
    const method: string =  'POST'
    const endpoint: string = '/auth/token'
    const url = `${authServer}${endpoint}`
    const body: object = { refresh_token: refreshToken }
    const options: RequestInit = {
        method,
        headers: {
            'Content-Type': 'application/json',
            'Origin': origin, 
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
            console.log('Token Refresh request successful.')
            return data['access_token']
        }
    } catch (error) {
        const err = error instanceof Error ? error.message : String(error)
        console.log(`Token Refresh Request Failed: ${err}`);
    }
};


async function getAccessToken() {
    const cookieManager = await cookies()
    const hasAccessToken = cookieManager.has('access_token')
    const hasRefreshToken = cookieManager.has('refresh_token')
    
    if (!hasAccessToken && !hasRefreshToken) {
        console.log('no tokens found...')
        return await authenticateWithBackend()
    }
    
    if (!hasAccessToken) {
        console.log('refreshing tokens...')
        return await refreshTokens(cookieManager.get('refresh_token')!.value)
    }
    
    const token = cookieManager.get('access_token')
    return token!.value
}

export async function authService({method, endpoint, queryParameters, body, headers}: RequestParameters) {
    const token = await getAccessToken()
    const {origin, authServer} = credentials
    const query = new URLSearchParams(queryParameters).toString();
    const url = `${authServer}${endpoint}${query ? `?${query}` : ''}`
    const options: RequestInit = {
        method,
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
            'Origin': origin, 
            'Access-Control-Request-Method': 'OPTIONS',
            'Access-Control-Request-Headers': 'Content-Type, Authorization',
            ...headers
        },
        credentials: 'include'
        };

        if (body && ['POST', 'PUT'].includes(method)) {
            options.body = JSON.stringify(body);
        };

        const response = await fetch(url, options);

        if (!response.ok){
            console.log('AuthService request failed')
            return {}
        }
        const data = await response.json()
        return data
};
