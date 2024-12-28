export type ClientCredentials = {
    origin?: string
    authServer?: string;
    username?: string;
    password?: string;
    appId?: number;
}

export type RequestParameters = {
    method: 'GET' | 'POST' | 'PUT' | 'DELETE';
    endpoint: string;
    queryParameters?: Record<string, string>;
    body?: Record<string, string>;
    headers?: Record<string, string>;
    authToken?: string
}

export type AccountCreationData = {
    email: string;
    password: string;
    firstName: string;
    lastName: string;
}