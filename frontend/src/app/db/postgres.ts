import { Client } from 'pg'

export class Postgres {
    client: Client;

    constructor() {
        this.client = this._client
    };

    get _client() {
        return new Client();
    };

    async connect() {
        return await this.client.connect();
    };

    async close() {
        await this.client.end();
    };

};
