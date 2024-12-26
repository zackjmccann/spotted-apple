export type RequestParameters = {
    method: 'GET' | 'POST' | 'PUT' | 'DELETE';
    endpoint: string;
    queryParameters?: Record<string, string>;
    body?: Record<string, string>;
    headers?: Record<string, string>;
}


export type AuthCredentials = {
    origin: string;
    authServer: string;
    username: string;
    password: string;
    appId: number;
}