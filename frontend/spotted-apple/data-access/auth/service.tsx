import logger from '@/lib/logging'
import { RequestParameters } from "@/data-access/auth/types";
import { setCookie, Cookie } from '@/lib/cookies'
import { randomBytes } from 'crypto';

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
function getAuthenticationQueryParameters(): Record<string, string> {
    const state = randomBytes(64).toString('hex');
    const codeChallenge = randomBytes(64).toString('hex');
    return {
        client_id: process.env.AUTH_CLIENT_ID,
        redirect_uri: `${process.env.OPS_SERVER}/auth/callback`,
        state: state,
        response_type: 'code',
        scope: 'profile offline_access openid',
        code_challenge: codeChallenge,
        code_challenge_method: 'S256',
    }
}

/**
 * Fetch Wrapper class specifically for interacting with the Authentication Service
 * @param requestParameters 
 */
export async function authFetch({
    method,
    endpoint,
    queryParameters,
    body,
    headers,
}: RequestParameters): Promise<Response> {
    const authQueryParameters = getAuthenticationQueryParameters()
    const query = {...authQueryParameters, ...queryParameters}
    const url = `${process.env.AUTH_SERVER}${endpoint}?${getUrlParams(query)}`
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
    options.body = JSON.stringify(body);

    // State and code challenges are required for all authentication requests
    // and must be presevered for subsequent request. Therefore, anytime an authentication
    // request is initiated, 'state' and 'code_challenge' cookies are set.
    await setCookie({name: 'state', value: authQueryParameters.state, maxAge: 60} as Cookie);
    await setCookie({name: 'code_challenge', value: authQueryParameters.codeChallenge, maxAge: 60} as Cookie);
    logger.debug(`Initiating ${method} to ${process.env.AUTH_SERVER}${endpoint}`)
    return await fetch(url, options);
};
