import { RequestParameters } from "@/data-access/types";
// import { parse } from 'cookie';

export class Aloe {
    origin: string;
    backendServer: string;
    authEndpoint: string;
    username: string;
    password: string;
    appId: number;
    token:  string | null = null;

    constructor() {
        this.origin = process.env.NEXT_PUBLIC_ORIGIN!
        this.backendServer = process.env.NEXT_PUBLIC_BACKEND_SERVER!
        this.authEndpoint = process.env.NEXT_PUBLIC_BACKEND_AUTH_ENDPOINT!
        this.username = process.env.NEXT_PUBLIC_BACKEND_USERNAME!
        this.password = process.env.NEXT_PUBLIC_BACKEND_PASSWORD!
        this.appId = parseInt(process.env.NEXT_PUBLIC_APP_ID!)        
    };

    async sendRequest(params: RequestParameters): Promise<Response> {
        const query = new URLSearchParams(params.queryParameters).toString();
        const url = `${this.backendServer}${params.endpoint}${query ? `?${query}` : ''}`
        const method = params.method
        const options: RequestInit = {
            method,
            headers: {
                'Content-Type': 'application/json',
                'Origin': this.origin, 
                'Access-Control-Request-Method': 'OPTIONS',
                'Access-Control-Request-Headers': 'Content-Type, Authorization',
                ...await this.getClient(),
                ...params.headers
            }
        };

        if (params.body && ['POST', 'PUT'].includes(method)) {
            options.body = JSON.stringify(params.body);
        };
        const response = await fetch(url, options);
        return await response;        
    };

    async getClient() {
        // 1. Check cookies for access_token
        //  a. If no access_token, check for refresh_token
        //  b. If no access or refresh tokens, request one from the Auth Server
        // 2. From access_token in cookie, construct the client
        if(!this.token) {
            console.log(`HERE`)
            this.authenticate()
        }
        console.log(`TOKEN: ${this.token}`)
        return {'Authorization': `Bearer ${this.token}`};
    }

    async authenticate() {
        console.log('authenticating...')
        const requestParams: RequestParameters = {
            method: 'POST',
            endpoint: '/auth/token',
            body: {
                username: this.username,
                password: this.password,
                id: this.appId.toString(),
                grant_type: 'client_credentials',
            },
        }

        let token: string | null = null

        try {
            const response = await this.sendRequest(requestParams);    
            if (!response.ok) {
                const data = await response.json()
                throw new Error(`${data.message}`)
            } else {
                console.log(`response: ${response}`)
                const data = await response.json()
                console.log(`data: ${data}`)
                token = data.token
            }
        } catch (error) {
            const err = error instanceof Error ? error.message : String(error)
            console.log(`Request Failed: ${err}`);
        }

        this.token = token
    }
};