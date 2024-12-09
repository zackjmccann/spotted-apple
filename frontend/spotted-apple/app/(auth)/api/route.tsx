import { Aloe } from '@/app/data-access/aloe'
import { RequestParameters } from "@/app/data-access/types";


export async function checkIfEmailExists(email: string): Promise<boolean | null> {
    let aloe = new Aloe()
    
    const requestParams: RequestParameters = {
        method: 'POST',
        endpoint: '/api/check-email',
        body: {email: email},
    }

    let registered: boolean | null = null

    try {
        const response = await aloe.sendRequest(requestParams);

        if (!response.ok) {
            const data = await response.json()
            throw new Error(`${data.message}`)
        } else {
            const data = await response.json()
            registered = data.registered
        }
    } catch (error) {
        const err = error instanceof Error ? error.message : String(error)
        console.log(`Request Failed: ${err}`);
        registered = false
    }

    return registered
};
