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
    // logger.debug(`Set Cookie: ${name}`)
};

/**
 * Check if a cookie exists
 * 
 * Simply wrapper for Next cookies module, but exists to consolidate
 * all cookie interactions through this module (no need to interact with
 * next/headers and initialize cookieManager).
 * @param {string} name - Name of cookie to check for
 * @returns {Promise<Boolean>}
 */
export async function checkForCookie(name: string): Promise<Boolean> {
    const cookieManager = await cookies();
    return cookieManager.has(name)
};

/**
 * Check if a cookie exists
 * 
 * Simply wrapper for Next cookies module, but exists to consolidate
 * all cookie interactions through this module (no need to interact with
 * next/headers and initialize cookieManager).
 * @param {string} name - Name of cookie to retrieve
 * @returns {Promise<string>}
*/
export async function getCookie(name: string): Promise<string> {
    const cookieManager = await cookies();
    return cookieManager.get(name)!.value
}