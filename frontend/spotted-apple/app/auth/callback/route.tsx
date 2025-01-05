'use server'

import logger from '@/lib/logging'
import { NextRequest } from 'next/server'
import { getCookie } from '@/lib/cookies'
import redis from '@/lib/session/service'


export async function GET(request: NextRequest) {
    const searchParams = request.nextUrl.searchParams
    const authCode = searchParams.get('code')
    const authState = searchParams.get('state')


    // Retrieve session and state from Redis
    // const sessionId = request.cookies.get('sessionId')?.value;
    // if (!sessionId) { return new Response('Session ID missing', { status: 400 }); }
    // const sessionData = await redis.get(`session:${sessionId}`);
    // if (!sessionData) { return new Response('Session expired or invalid', { status: 400 }); }
    // const { state } = JSON.parse(sessionData);

    logger.debug(`code: ${authCode}`)
    logger.debug(`auth state: ${authState}`)
    // logger.debug(`stored state: ${state}`)

    const stateCookie = await getCookie('state')
    stateCookie ? logger.debug(`State cookie after auth callback: ${stateCookie}`) : null;

    let redirectUrl: string
   
    if (!authCode || !authState) {
        redirectUrl = '/test'
    } else if ('state' != 'state') {
    // } else if (state != expectedState) {
        logger.error('State returned from Auth Service does not match')
        redirectUrl = '/test'
    } else {
        redirectUrl = '/profile'
    }
    return Response.json({
        redirectUrl: redirectUrl,
        code: authCode,
        state: authState,
    })
}