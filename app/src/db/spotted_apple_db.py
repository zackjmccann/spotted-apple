import psycopg
import bcrypt
from db.postgres import Postgres

class SpottedAppleDB(Postgres):
    """A class to interact with the Spottle Apple Operational DB"""
    def __init__(self):
        super().__init__()

    def create_new_user(self, signup_form_entry: tuple):
        create_new_user_statement = 'INSERT INTO users (email, password) VALUES (%s, %s) RETURNING users.user_id'

        with self.conn.cursor() as cursor:
            try:
                email = signup_form_entry[0]
                password = self.hash_password(signup_form_entry[1])
                cursor.execute(create_new_user_statement, (email, password))
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

    def get_user(self, user_email: str):
        get_user_statement = 'SELECT * FROM users WHERE users.email = %s'
        with self.conn.cursor() as cursor:
            cursor.execute(get_user_statement, (user_email,))
            user = cursor.fetchall()[0]
            self.conn.commit()
            return user

    def insert_spotify_authorization_data(self, user_id: int, auth_code: str, refresh_token: str):
        # TODO: Should this overwrite existing data?
        spotify_auth_statement = """
        INSERT INTO spotify_authorizations (user_id, authorization_code, refresh_token)
        VALUES (%s, %s, %s)
        RETURNING spotify_authorizations.refresh_token;
        """

        with self.conn.cursor() as cursor:
            try:
                cursor.execute(spotify_auth_statement, (user_id, auth_code, refresh_token))
                entered_refresh_token = cursor.fetchall()[0][0]
                self.conn.commit()
                return entered_refresh_token
            except psycopg.errors.UniqueViolation as err:
                return err

    def check_for_spotify_access_token(user_id: int):
        spotify_auth_statement = """
        SELECT sa.refresh_token, MAX(sa.created)
        FROM spotify_authorizations sa
        WHERE sa.user_id = %s
        GROUP BY sa.refresh_token;
        """
        with self.conn.cursor() as cursor:
            cursor.execute(spotify_auth_statement, (user_id,))
            try:
                refresh_toke = cursor.fetchall()[0][0]
                self.conn.commit()
                return user
            except IndexError:
                return None

    @staticmethod
    def hash_password(entered_password: str):
        password = bytes(entered_password, 'utf-8')
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password, salt).hex()

    @staticmethod
    def verify_password(entered_password, password):
        return bcrypt.checkpw(bytes(entered_password, 'utf-8'),
                              bytes.fromhex(password))
