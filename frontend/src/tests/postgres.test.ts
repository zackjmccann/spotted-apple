import { Postgres } from '../app/db/postgres'
import { beforeAll, expect } from 'vitest'

let pg = new Postgres()

beforeAll(() => {
    pg.connect()
})

afterAll(() => {
    pg.close();
})

describe('Connection to PostgreSQL server', async () => {
    it('should return 1 from a query output if the connection is established', async () => {
        let resultset = await pg.client.query(`SELECT 1 as test_value;`);
        expect(resultset.rows[0].test_value).toEqual(1);
    });
});