import { Aloe } from '../db/aloe'
import { expect, describe, it } from 'vitest'
import NewUser from "../db/interfaces/new-user"

let db = new Aloe()
let testEmail = 'unit_test_user@email.com'
let testPassword = 'unit_test_password'

describe('Authentication with backend server', async () => {
    it('should return status code of 200 for authorized access', async () => {
        let testUserId = parseInt(process.env.TEST_USER_ID!)
        let testUserEmail = process.env.TEST_USER_EMAIL
        let response = await db.sendRequest(
            'GET',
            '/users/get',
            {'id': testUserId.toString()}
        );
        let status = response.status
        expect(status).toEqual(201);
    });
});

describe('Get user', async () => {
    it('should return the id, email, first and last names, and created at timestamp for the entered user id', async () => {
        let testUserId = parseInt(process.env.TEST_USER_ID!)
        let user = await db.getUser(testUserId)
        expect(user.email).toBeTypeOf('string');
    });
});

describe('Get nonexistent user', async () => {
    it('should throw an error', async () => {
        let nonexistentUserId = -99
        await expect(db.getUser(nonexistentUserId))
        .rejects.toThrow('No user found with provided id');
    });
});

// describe('Insert user', async () => {
//     it('should return the user_id of the newly inserted user', async () => {
//         let newUser = <NewUser> {
//             email: testEmail,
//             password: testPassword,
//         };

//         let newUserId = await db.insertUser(newUser)
//         expect(newUserId).toBeGreaterThan(1);
//     });
// });

// describe('Insert existing user', async () => {
//     it('should return -1 due to the presented user already existing in the users relation', async () => {
//         let newUser = <NewUser> {
//             email: testEmail,
//             password: testEmail,
//         };

//         let newUserId = await db.insertUser(newUser)
//         expect(newUserId).toBeLessThan(0);
//     });
// });

// describe('Delete user', async () => {
//     it('should return the user_id for the deleted user', async () => {
//         let testUser = await db.getUser('email', testEmail)
//         let deletedTestUserId = await db.deleteUser(testUser.userId)
//         expect(deletedTestUserId).toEqual(testUser.userId);
//     });
// });
