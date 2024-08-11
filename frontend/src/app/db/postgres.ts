import postgres from 'postgres'

let db = postgres('postgres://', {
    username: process.env.POSTGRES_USER ?? 'postgres',
    password: process.env.POSTGRES_PASSWORD ?? 'postgres',
    host    : process.env.POSTGRES_HOST ?? 'localhost',
    port    : parseInt(process.env.POSTGRES_PORT!) ?? 5432,
    database: process.env.POSTGRES_DB ?? 'postgres',
    max: 10
  });


export async function connect() {
  return await db
}

export async function insert() {
  let test_email = 'unit_test_user@email.com'
  let test_password = 'unit_test_password'

  let insert_result = await db`
  INSERT INTO users (email, password)
  VALUES (${test_email}, ${test_password})
  RETURNING users.user_id
  `
  db.end()
  return insert_result[0].user_id

};

export * as db from './postgres';
