import { Postgres } from "./postgres";
import User from "./interfaces/user" // TODO: Target this import statement: import { User } from "@/app/lib/definitions"
import NewUser from "./interfaces/new-user"

export class Aloe extends Postgres {
    constructor() {
        super();
    };

    async getUser(column:string='user_id', userData:number | string): Promise<User> {
        const getUserQuery = {
            name: `get-user-${userData}`,
            text: `SELECT user_id, email, created
                   FROM users
                   WHERE ${column} = $1;`,
            values: [userData]
        }
        const resultset = await this.client.query(getUserQuery)
        return <User> {
            userId: Number(resultset.rows[0].user_id),
            email: resultset.rows[0].email,
            created: new Date(resultset.rows[0].created),
        }
    };

    async deleteUser(userId:number): Promise<Number | unknown> {
        try {
            const deleteUserQuery = {
                name: 'delete-new-user',
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

    async insertUser(newUser:NewUser): Promise<Number | unknown> {
        try {
            const insertNewUserQuery = {
                name: 'insert-new-user',
                text: `INSERT INTO users (email, password)
                       VALUES ($1, $2)
                       RETURNING users.user_id;`,
                values: [newUser.email, newUser.password],
              };
            
            const resultset = await this.client.query(insertNewUserQuery)
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
};