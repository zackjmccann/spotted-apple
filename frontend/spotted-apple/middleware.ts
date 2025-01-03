import logger from '@/lib/logging'
import { getSession, validateSession } from '@/lib/session'
import { NextResponse } from 'next/server'
import { checkForCookie, getCookie } from '@/lib/cookies'

export async function middleware() {
    let validSession: boolean;
    
    const hasSession = await checkForCookie('session')
    
    if (!hasSession) {
        validSession = false
    } else {
        const session = await getCookie('session')
        validSession = await validateSession(session) ?? false
    }
    
    if (validSession) {
        return NextResponse.next()

    } else {
        try {
            const session = await getSession()
            const response = NextResponse.next()

            if (session) {
                response.cookies.set({ name: 'session', value: session.token, expires: session.expires})
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
