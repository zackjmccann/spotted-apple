"use server";

import logger from '@/lib/logging'
import { getSession, Session } from '@/lib/session'


export async function testAction(formData: FormData,) {
    const enteredValues: { [key: string]: string } = {}
    formData.forEach((value, key) => { enteredValues[key] = value.toString(); })
    
    // Test logic
    const { testField } = enteredValues
    logger.debug(`Input: ${testField}`)
    
    const session: Session = await getSession()
    logger.debug(`session: ${JSON.stringify(session)}`)

    const expires_at = session['expires']
    // TODO: logic will need to be added to consider a session wasn't created
    logger.debug(`Expires At: ${expires_at}`)
    const extendedExpires = expires_at!.setMinutes(expires_at!.getMinutes() + 5)
    logger.debug(`Expires At Math: ${new Date(extendedExpires)}`)

};
