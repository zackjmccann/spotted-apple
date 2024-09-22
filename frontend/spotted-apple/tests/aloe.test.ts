import { Aloe } from '../db/aloe'
import { afterAll, beforeAll, expect, describe, it } from 'vitest'
import User from "../db/interfaces/user"

let db = new Aloe()
let testEmail = 'unit_test_user@email.com'
let testFirstName = 'unit_test_first'
let testLastName = 'unit_test_last'
let testPassword = 'unit_test_password'

beforeAll(() => {
    db.connect()
})

afterAll(() => {
    db.close();
})

describe('Get test user', async () => {
    it('should return the user_id, email, and created at timestamp for the db test user', async () => {
        let testUserId = parseInt(process.env.TEST_USER_ID!)
        let testUserEmail = process.env.TEST_USER_EMAIL
        let testUser = await db.getUser('user_id', testUserId)
        expect(testUser.userId).toEqual(testUserId);
        expect(testUser.email).toEqual(testUserEmail);
        expect(testUser.created).toBeTypeOf('object');
    });
});

describe('Insert user', async () => {
    it('should return the user_id of the newly inserted user', async () => {
        let newUser = <User> {
            email: testEmail,
            firstName: testFirstName,
            lastName: testLastName,
        };

        let newUserId = await db.insertUser(newUser)
        expect(newUserId).toBeGreaterThan(1);
    });
});

describe('Insert existing user', async () => {
    it('should return -1 due to the presented user already existing in the users relation', async () => {
        let newUser = <User> {
            email: testEmail,
            firstName: testFirstName,
            lastName: testLastName,
        };

        let newUserId = await db.insertUser(newUser)
        expect(newUserId).toBeLessThan(0);
    });
});

describe('Delete user', async () => {
    it('should return the user_id for the deleted user', async () => {
        let testUser = await db.getUser('email', testEmail)
        let deletedTestUserId = await db.deleteUser(testUser.userId)
        expect(deletedTestUserId).toEqual(testUser.userId);
    });
});

describe('Get User Authentication record', async () => {
    it('should return the user_authentication record for the provide user', async () => {
        let testUserId = parseInt(process.env.TEST_USER_ID!)
        let testUser = await db.getUser('user_id', testUserId)
        let testUserAuthentication = await db.getUserAuthentication(testUser.userId)
        expect(testUserAuthentication.authId).toEqual(parseInt(process.env.TEST_USER_ID!));
        expect(testUserAuthentication.password).toEqual(process.env.TEST_USER_PASSWORD);
    });
});
