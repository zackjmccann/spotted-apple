import psycopg
from db.postgres import Postgres

class SpottedAppleDB(Postgres):
    """A class to interact with the Spottle Apple Operational DB"""
    def __init__(self):
        super().__init__()

    def create_new_user(self, signup_form_entry: tuple):
        create_new_user_statement = 'INSERT INTO users (email, password) VALUES (%s, %s) RETURNING users.user_id'

        with self.conn.cursor() as cursor:
            try:
                cursor.execute(create_new_user_statement, signup_form_entry)
                new_user_id = cursor.fetchall()[0][0]
                self.conn.commit()
                return new_user_id
            except psycopg.errors.UniqueViolation as err:
                return err

    def delete_user(self, user_email: str): # TODO: Should this be 'user_id'?
        delete_user_statement = 'DELETE FROM users WHERE users.email = %s RETURNING users.email;'
        with self.conn.cursor() as cursor:
            try:
                cursor.execute(delete_user_statement, (user_email,))
                deleted_user = cursor.fetchall()[0][0]
                self.conn.commit()
                return deleted_user
            except psycopg.errors.UniqueViolation as err:
                return err
