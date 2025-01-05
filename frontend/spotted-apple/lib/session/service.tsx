import logger from '@/lib/logging'
import { Session } from '@/lib/session/types'

const opsServerHeaders = {
    'Content-Type': 'application/json',
    'Origin': process.env.ORIGIN, 
    'Access-Control-Request-Method': 'OPTIONS',
    'Access-Control-Request-Headers': 'Content-Type, Authorization',
}

export async function getSession(): Promise<Session | undefined> {
    const method = 'POST'
    const endpoint = '/auth/session/create'
    const url = `${process.env.OPS_SERVER}${endpoint}`
    const options: RequestInit = {
        method,
        headers: opsServerHeaders,
        credentials: 'include'
    }

    options.body = JSON.stringify({
        client_id: process.env.CLIENT_ID,
        username: process.env.CLIENT_USERNAME,
        secret: process.env.CLIENT_SECRET,
        grant_type: 'client_credentials'
    });
    
    let session: Session | undefined
    
    try {
        const response = await fetch(url, options)
        
        if (!response.ok) {
            throw new Error(`Failed to create session`)
        } else {
            const data = await response.json()
            session = {
                token: data['session'],
                expires: new Date(data['expires'])
            }
        }
    } catch (error) {
        const err = error instanceof Error ? error.message : String(error)
        logger.error(`Failed to create session: ${err}`);
    }

    return session
};

export async function validateSession(session: string | undefined): Promise<boolean | undefined> { 
    const method = 'POST'
    const endpoint = '/auth/session/introspect'
    const url = `${process.env.OPS_SERVER}${endpoint}`
    const options: RequestInit = {
        method,
        headers: opsServerHeaders,
        credentials: 'include'
    }

    options.body = JSON.stringify({ session: session, client_id: process.env.CLIENT_ID });

    let sessionIsValid: boolean

    try {
        const response = await fetch(url, options)
        
        if (!response.ok) {
            sessionIsValid = false
        } else {
            sessionIsValid = true
        }
    } catch (error) {
        const err = error instanceof Error ? error.message : String(error)
        logger.error(`Failed to validate session: ${err}`);
        sessionIsValid = false
    }
    return sessionIsValid
}
