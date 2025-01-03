export type Cookie = {
    name: string;
    value: string;
    httpOnly?: boolean;
    secure?: boolean;
    sameSite?: 'lax' | 'strict' | 'none';
    expires?: Object;
    maxAge?: number;
}