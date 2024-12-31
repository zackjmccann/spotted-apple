"use server";

import logger from '@/lib/logging'
import { Cookie } from '@/lib/cookies/types'
import { cookies } from 'next/headers';

/**
 * setCookie is a server actions for setting cookies on the browser.
 * The function does not contain a return value, instead simply setting
 * the cookie provided.
 * 
 * By default, all cookies are httpOnly, secure, and contain
 *  a "lax" sameSite configuration.
 * 
 * @param {string} name - Name of the cookie 
 * @param {string} value - Value of the cookie
 * @param {number} maxAge - MaxAge of the cookie
 */
export async function setCookie({name, value, maxAge}: Cookie) {
    (await cookies()).set({
        name: name,
        value: value,
        httpOnly: true,
        secure: true,
        sameSite: 'lax',
        maxAge: maxAge,
    });
    logger.debug(`Set Cookie: ${name}`)
};
