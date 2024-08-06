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

    def upsert_access_token_data(self, user_id, account, access_token_info):
        upsert_access_token_data_statement = """
        INSERT INTO access_tokens (
                                    access_token_id,
                                    account,
                                    user_id,
                                    access_token,
                                    token_type,
                                    scope,
                                    expiration_time,
                                    refresh_token
                                  )
        VALUES (%s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP + %s * interval '1 second', %s)
        ON CONFLICT (access_token_id)
        DO UPDATE
            SET access_token = EXCLUDED.access_token,
                token_type = EXCLUDED.token_type,
                scope = EXCLUDED.scope,
                expiration_time = EXCLUDED.expiration_time,
                refresh_token = EXCLUDED.refresh_token,
                modified = CURRENT_TIMESTAMP
        RETURNING access_tokens.access_token;
        """
        with self.conn.cursor() as cursor:
            try:
                access_token_id = account + '_' + str(user_id)
                access_token = access_token_info.get('access_token')
                token_type = access_token_info.get('token_type')
                scope = access_token_info.get('scope')
                expires_in = access_token_info.get('expires_in')
                refresh_token = access_token_info.get('refresh_token')

                cursor.execute(
                    upsert_access_token_data_statement,
                    (access_token_id, account, user_id, access_token, token_type, scope, expires_in, refresh_token)
                    )
                access_token = cursor.fetchall()[0][0]
                self.conn.commit()
                return access_token
            except psycopg.errors.UniqueViolation as err:
                return err

    def get_access_token(self, access_token_id: str) -> str:
        access_token_statement = 'SELECT access_token FROM access_tokens WHERE access_token_id = %s;'
        with self.conn.cursor() as cursor:
            try:
                cursor.execute(access_token_statement, (access_token_id,))
                access_token = cursor.fetchall()[0][0]
                self.conn.commit()
                return access_token
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
