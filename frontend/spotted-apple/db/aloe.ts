import { Postgres } from "./postgres";
import User from "./interfaces/user" // TODO: Target this import statement: import { User } from "@/app/lib/definitions"
import UserAuthentication from "./interfaces/user-authentication"

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

    async insertUser(user:User): Promise<Number | unknown> {
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

        } catch (error) {
            if(error instanceof Error) {
                console.log(error.message);
                return -1;
            } else {
                return error;
            };
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

};