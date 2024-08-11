import { db } from "../app/db/postgres"
import { expect } from 'vitest'

let conn = await db.connect()
let test_email = 'unit_test_user@email.com'
let test_password = 'unit_test_password'

afterAll(async () => {
    conn.end()
});

describe('Postgres Connection', async () => {
    it('should establish a connection to the configured postgreSQL instance', async () => {
        let resultset = await conn`SELECT 1 as test_value;`;
        expect(resultset[0].test_value).toEqual(1);
    });
});

describe('insert new user', () => {
    it('should return the user_id of the newly inserted user', async () => {
        let test_id = await db.insert_user(test_email, test_password);
        expect(parseInt(test_id)).toBeGreaterThan(1);
    });
});

describe('insert existing user operation', () => {
    it('should return -1 due to a duplicate entry attempt', async () => {
        let test_id = await db.insert_user(test_email, test_password);
        expect(parseInt(test_id)).toEqual(-1);
    });
});

describe('get user by email', () => {
    it('should return the user data of the desired user', async () => {
        let user_data: db.UserData = await db.get_user_data_by_email(test_email);
        expect(user_data.email).toEqual(test_email);
    });
});

describe('delete existing user', () => {
    it('should return the user_id of the deleted user', async () => {
        let user_data: db.UserData = await db.get_user_data_by_email(test_email);
        let test_user_id = parseInt(user_data.user_id)
        let deleted_user_id = await db.delete_user(test_user_id);
        expect(parseInt(deleted_user_id)).toEqual(test_user_id);
    });
});
