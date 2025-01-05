import logger from '@/lib/logging'
import { RequestParameters } from '@/data-access/auth/types'
import { getCookie } from '@/lib/cookies'

/**
 * Transform an object into a URL query string
 * 
 * @param {object} urlParameterMappings - An object with key, value pairs representing query parameters
 * @returns {string}
 */
function getUrlParams(urlParameterMappings: Record<string, any>): string {
    const params = new URLSearchParams();
    for (const key in urlParameterMappings) {
      if (urlParameterMappings.hasOwnProperty(key)) {
        const value = urlParameterMappings[key];
        if (Array.isArray(value)) {
          value.forEach(item => params.append(key, item));
        } else {
          params.append(key, value);
        }
      }
    }
    return params.toString();
  }

/**
 * All authentication requests require client id, redirect uri, state
 * response type, scope, code challenge and method parameters. This function
 * compiles these common/standard parameters.
 * @returns {Record<string, string>}
 */
async function getAuthenticationParameters(): Promise<Record<string, string>> {
  const session = await getCookie('session')
    return {
        client_id: process.env.CLIENT_ID,
        client_secret: process.env.CLIENT_SECRET,
        session: session ?? '',
        scope: 'profile offline_access openid',
        // code_challenge_method: 'S256',
    }
}

/**
 * Fetch Wrapper class specifically for interacting with the Operations Service
 * @param requestParameters 
 */
export async function opsFetch({
    method,
    endpoint,
    // queryParameters,
    body,
    headers,
}: RequestParameters): Promise<Response> {
    const authParameters = await getAuthenticationParameters()
    const payload = {...authParameters, ...body}
    const url = `${process.env.OPS_SERVER}${endpoint}`
    const options: RequestInit = {
        method,
        headers: {
            'Content-Type': 'application/json',
            'Origin': process.env.ORIGIN, 
            'Access-Control-Request-Method': 'OPTIONS',
            'Access-Control-Request-Headers': 'Content-Type, Authorization',
            ...headers
        },
        credentials: 'include'
    };
    options.body = JSON.stringify(payload);
    return await fetch(url, options);
};
