import { RequestParameters } from "@/app/data-access/types";

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

    async getClient(){
        this.token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzcG90dGVkLWFwcGxlLWJhY2tlbmQiLCJhdWQiOlsiMSJdLCJpYXQiOjE3MzM3MjA2MDAsImV4cCI6MTczMzcyMDkwMCwianRpIjoiYmFja2VuZF9zZXJ2aWNlc18yMDI0MTIwOV8wMDAzIiwiY29udGV4dCI6eyJ1c2VybmFtZSI6ImZyb250ZW5kIiwicm9sZXMiOlsiY2xpZW50Il19fQ.kVIGpJri7vHHDYRacZcWRYLnscxbP8eo0smt8Co5zms"
        return {'Authorization': `Bearer ${this.token}`};
    }
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
};