import User from "./schemas/user" // TODO: Target this import statement: import { User } from "@/app/lib/definitions"

export class Aloe {
    private backendServer: string;
    private authEndpoint: string;
    private username: string;
    private password: string;
    private appId: number;
    private token:  string | null = null;
    private client: any;

    constructor() {
        this.backendServer = process.env.BACKEND_SERVER!
        this.authEndpoint = process.env.BACKEND_AUTH_ENDPOINT!
        this.username = process.env.BACKEND_USERNAME!
        this.password = process.env.BACKEND_PASSWORD!
        this.appId = parseInt(process.env.APP_ID!)
        this.client = this._getClient()
    };

    private async _getClient() {
        if (!this.token) {
            await this._authenticate()
        } else {
            let valid_token = await this._validateToken()
            if (!valid_token) {
                await this._authenticate()
            }
        }
        return {'Authorization': `Bearer ${this.token}`};
    };

    private async _authenticate() {
        const authUrl = `${this.backendServer}/${this.authEndpoint}/token`

        try {
            const response = await fetch(authUrl , {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    username: this.username,
                    password: this.password,
                    id: this.appId,
                    grant_type: 'client_credentials',
                }),
            });

            if (!response.ok) {
                throw new Error(`Backend Authentication Failed: ${response.status}`)
            }
            
            const data = await response.json();

            if (!data.token) {
                throw new Error(`No token found.`)
            }

            this.token = data.token;

        } catch (error: unknown) {
            if (error instanceof Error) {
                throw error;
            } else {
              console.error('Request Failed, An unknown error occurred: ', error);
            };
        };
    };

    private async _validateToken() {
        const authUrl = `${this.backendServer}/${this.authEndpoint}/introspect`

        try {
            const response = await fetch(authUrl , {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ token: this.token, }),
            });

            if (!response.ok) {
                throw new Error(`Backend Authentication Failed: ${response.status}`)
            }
            
            const data = await response.json();
            return data.valid

        } catch (error) {
            const err = error instanceof Error ? error.message : String(error)
            throw new Error(`Request Failed, An unknown error occurred: ${err}`);
        };   
    }

    async sendRequest(
        method: 'GET' | 'POST' | 'PUT' | 'DELETE' = 'GET',
        endpoint: string,
        queryParameters: Record<string, string> = {},
        headers?: Record<string, string>,
        body?: any,
    ): Promise<any> {
        const query = new URLSearchParams(queryParameters).toString();
        const url = query ? `${this.backendServer}${endpoint}?${query}` : `${this.backendServer}${endpoint}`;
        const options: RequestInit = {
            method,
            headers: {
                'Content-Type': 'application/json',
                ...await this.client,
                ...headers,
            },
        };

        try {
            if (body && ['POST', 'PUT'].includes(method)) {
                options.body = JSON.stringify(body);
            };
            
            const response = await fetch(url, options);
            return await response;

        } catch (error) {
            const err = error instanceof Error ? error.message : String(error)
            throw new Error(`Request Failed: ${err}`);
        };
        
    };

    async getUser(id: number): Promise<User> {
        let response = await this.sendRequest(
            'GET',
            '/users/get',
            {'id': id.toString()}
        );

        if (!response.ok) {
            let data = await response.json()
            throw new Error(`${data.message}`)
        } else {
            const data = await response.json()
            return data.user as User
        }
    };
};