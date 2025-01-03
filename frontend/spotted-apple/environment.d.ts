declare global {
    namespace NodeJS {
        interface ProcessEnv {
            NODE_ENV: 'development' | 'production';
            
            ORIGIN: string;
            CLIENT_ID: string;
            CLIENT_USERNAME: string;
            CLIENT_PASSWORD: string;
            
            AUTH_SERVER: string;
            AUTH_CLIENT_ID: string;
            AUTH_SECRET: string;
            
            OPS_SERVER: string;
            OPS_CLIENT_ID: string
            OPS_SECRET: string

            DEV_MODE: boolean;
        }
    }
};

export {};