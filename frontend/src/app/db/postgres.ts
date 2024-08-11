import postgres, { PostgresError } from 'postgres'

let db = postgres('postgres://', {
    username: process.env.POSTGRES_USER ?? 'postgres',
    password: process.env.POSTGRES_PASSWORD ?? 'postgres',
    host    : process.env.POSTGRES_HOST ?? 'localhost',
    port    : parseInt(process.env.POSTGRES_PORT!) ?? 5432,
    database: process.env.POSTGRES_DB ?? 'postgres',
    max: 10
  });

export interface UserData {
  // TODO: Change types
  user_id: string,
  email: string,
  created: string
};

export async function connect() {
  return await db
}

export async function insert_user(email:string, password: string) {
  try {
    let insert_result = await db`
    INSERT INTO users (email, password)
    VALUES (${email}, ${password})
    RETURNING users.user_id
    `
    return insert_result[0].user_id

  } catch (err) {
    if(err.name == 'PostgresError' &&
      err.message == `duplicate key value violates unique constraint "users_email_key"`) {
      console.log(`User "${email}" already exists.`);
      return -1;
    };

  };
};

export async function delete_user(user_id: number) {
  try {
    let insert_result = await db`
    DELETE FROM users 
    WHERE users.user_id = ${user_id}
    RETURNING users.user_id;
    `
    return insert_result[0].user_id

  } catch (err) {
      return err;
  };
};

export async function get_user_data_by_email(email:string): Promise<UserData> {
  let user_result = await db`
  SELECT user_id, email, created
  FROM users 
    WHERE email = ${email};
  `
  return <UserData> user_result[0]
};

export * as db from './postgres';
