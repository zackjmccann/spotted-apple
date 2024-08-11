import { db } from "../app/db/postgres"
import { expect, test } from 'vitest'

let conn = await db.connect()

afterAll(async () => {
    conn.end()
});

describe('Postgres Connection', async () => {
    it('should establish a connection to the configured postgreSQL instance', async () => {
        let resultset = await conn`SELECT 1 as test_value;`;
        expect(resultset[0].test_value).toEqual(1);
    });
});

describe('Postgres INSERT operation', () => {
    it('should insert data into a postgreSQL instance', async () => {
        let test_id = await db.insert();
        expect(parseInt(test_id)).toBeGreaterThan(1);
    });
});
