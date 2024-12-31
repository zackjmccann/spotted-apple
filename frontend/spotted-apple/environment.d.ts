declare global {
    namespace NodeJS {
        interface ProcessEnv {
            NODE_ENV: 'development' | 'production';
            DEV_MODE: boolean;
            APP_ID: string; // TODO: Fix this
            ORIGIN: string;
            CLIENT_USERNAME: string;
            CLIENT_PASSWORD: string;
            AUTH_SERVER: string;
            AUTH_CLIENT_ID: string;
            AUTH_SECRET: string;
            OPS_SERVER: string;
        }
    }
};

export {};