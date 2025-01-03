import logger from '@/lib/logging'
import { getSession, validateSession } from '@/lib/session'
import { NextResponse } from 'next/server'
import { checkForCookie, getCookie } from '@/lib/cookies'

export async function middleware() {
    let validSession: boolean;
    
    const hasSessionId = await checkForCookie('sessionId')
    
    if (!hasSessionId) {
        validSession = false
    } else {
        const sessionId = await getCookie('sessionId')
        validSession = await validateSession(sessionId) ?? false
    }
    
    if (validSession) {
        return NextResponse.next()

    } else {
        try {
            const session = await getSession()
            const response = NextResponse.next()

            if (session) {
                response.cookies.set({ name: 'sessionId', value: session.id, expires: session.expires})
                return response

            } else {
                throw Error(`Session creation failed`)

            }

        } catch (error) {
            const err = error instanceof Error ? error.message : String(error)
            logger.error(`Client Error: ${err}`);

        }
     }
}

export const config = {
    matcher: ["/((?!api|_next/static|_next/image|favicon.ico|global-error).*)"],
};
