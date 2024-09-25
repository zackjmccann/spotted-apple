import { Postgres } from "./postgres";
import User from "./interfaces/user" // TODO: Target this import statement: import { User } from "@/app/lib/definitions"
import UserAuthentication from "./interfaces/user-authentication"

export class AloeError extends Error {
    constructor(message: string) {
        super(message);
        this.name = 'AloeError';
    };
};

export class AloeExistingUserError extends AloeError {
    constructor(message: string = 'An account with that email already exists.') {
        super(message);
        this.name = 'AloeExistingUserError';
    };
};

export class Aloe extends Postgres {
    constructor() {
        super();
    };

    async getUser(column:string='user_id', userData:number | string): Promise<User> {
        const getUserQuery = {
            name: `get-user-${userData}`,
            text: `SELECT user_id, email, first_name, last_name, created, modified
                   FROM users
                   WHERE ${column} = $1;`,
            values: [userData]
        }
        const resultset = await this.client.query(getUserQuery)
        return <User> {
            userId: Number(resultset.rows[0].user_id),
            email: resultset.rows[0].email,
            firstName: resultset.rows[0].first_name,
            lastName: resultset.rows[0].last_name,
            created: new Date(resultset.rows[0].created),
            modified: new Date(resultset.rows[0].modified),
        }
    };

    async deleteUser(userId:number): Promise<Number | unknown> {
        try {
            const deleteUserQuery = {
                name: 'delete-user',
                text: `DELETE FROM users
                       WHERE user_id = $1
                       RETURNING users.user_id;`,
                values: [userId],
              };
            
            const resultset = await this.client.query(deleteUserQuery)
            return Number(resultset.rows[0].user_id);

        } catch (error) {
            if(error instanceof Error) {
                console.log(error.message);
                return -1;
            } else {
                return error;
            };
        };
    };

    async insertUser(user:User): Promise<Number> {
        try {
            const insertUserQuery = {
                name: 'insert-user',
                text: `INSERT INTO users (email, first_name, last_name)
                       VALUES ($1, $2, $3)
                       RETURNING users.user_id;`,
                values: [user.email, user.firstName, user.lastName],
              };

            const resultset = await this.client.query(insertUserQuery)
            return Number(resultset.rows[0].user_id);

        } catch (error: any) {
            if (error.message === 'duplicate key value violates unique constraint "users_email_key"') {
                throw new AloeExistingUserError;
            }
            const errorMessage = `Failed to insert user: ${error.message}`
            throw new AloeError(errorMessage);
        };
    };

    async getUserAuthentication(userId:number): Promise<UserAuthentication> {
        const getUserAuthenticationQuery = {
            name: `get-user-authentication-${userId}`,
            text: `SELECT auth_id, user_id, password, created, modified
                   FROM user_authentication
                   WHERE user_authentication.user_id = $1;`,
            values: [userId]
        }
        const resultset = await this.client.query(getUserAuthenticationQuery)
        return <UserAuthentication> {
            authId: Number(resultset.rows[0].auth_id),
            userId: Number(resultset.rows[0].user_id),
            password: resultset.rows[0].password,
            created: new Date(resultset.rows[0].created),
            modified: new Date(resultset.rows[0].modified),
        }
    };

    async insertUserAuthentication(userAuthentication:UserAuthentication): Promise<Number | unknown> {
        try {
            const insertUserAuthenticationQuery = {
                name: 'insert-user-authentication',
                text: `INSERT INTO user_authentication (user_id, password)
                       VALUES ($1, $2)
                       RETURNING user_authentication.auth_id;`,
                values: [userAuthentication.userId, userAuthentication.password],
              };

            const resultset = await this.client.query(insertUserAuthenticationQuery)
            return Number(resultset.rows[0].user_id);

        } catch (error: any) {
            const errorMessage = `Failed to insert user authentication: ${error.message}`
            throw new AloeError(errorMessage);
        };
    };

};