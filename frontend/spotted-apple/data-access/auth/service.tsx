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
async function getAuthenticationQueryParameters(): Promise<Record<string, string>> {
  const sessionId = await getCookie('sessionId')
    return {
        client_id: process.env.AUTH_CLIENT_ID,
        response_type: 'code',
        session_id: sessionId ?? '',
        scope: 'profile offline_access openid',
        // code_challenge_method: 'S256',
    }
}

/**
 * Fetch Wrapper class specifically for interacting with the Authentication Service
 * @param requestParameters 
 */
export async function authFetch({
    method,
    endpoint,
    // queryParameters,
    body,
    headers,
}: RequestParameters): Promise<Response> {
    const authQueryParameters = await getAuthenticationQueryParameters()
    // const query = {...authQueryParameters, ...queryParameters}
    // const url = `${process.env.AUTH_SERVER}${endpoint}?${getUrlParams(query)}`
    const payload = {...authQueryParameters, ...body}
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
