import os
import sqlite3

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import login

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def get_connection():
    conn = sqlite3.connect(os.path.join(basedir, "app.db"))
    return conn


@login.user_loader
def load_user(id):
    return User.get_user(id)


class User(UserMixin):
    def __init__(self, id, username, name, email, password, is_admin=False):
        self.id = id
        self.username = username
        self.name = name
        self.email = email
        self.password = password
        self.is_admin = is_admin

    @staticmethod
    def get_user(id):
        try:
            with get_connection() as conn:
                cur = conn.cursor()

                cur.execute(
                    "SELECT * FROM admin WHERE id = ?",
                    (id,),
                )
                user_data = cur.fetchone()

                if user_data:
                    return User(
                        id=user_data[0],
                        username=user_data[1],
                        name=user_data[2],
                        email=user_data[3],
                        password=user_data[4],
                        is_admin=True,
                    )

                cur.execute(
                    "SELECT * FROM clients WHERE id = ?",
                    (id,),
                )
                user_data = cur.fetchone()

                if user_data:
                    return User(
                        id=user_data[0],
                        username=user_data[1],
                        name=user_data[2],
                        email=user_data[3],
                        password=user_data[4],
                        is_admin=False,
                    )

                return None
        except sqlite3.DatabaseError as e:
            print(f"Error: {e}")
            return None


class Admin:
    def __init__(self, username, password_hash, id=None, name=None, email=None):
        self.id = id
        self.username = username
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.is_admin = True

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def create_admin(self) -> bool:
        try:
            with get_connection() as conn:
                cur = conn.cursor()

                cur.execute("SELECT 1 FROM admin WHERE username = ?", (self.username,))
                if cur.fetchone():
                    return False

                create_query = """
                INSERT INTO admin (username, name, password_hash)
                VALUES (?, ?, ?)
                """
                cur.execute(
                    create_query,
                    (
                        self.username,
                        self.name,
                        self.password_hash,
                    ),
                )
                conn.commit()
                return True
        except sqlite3.IntegrityError as e:
            print(f"Error: {e}")
        except sqlite3.DatabaseError as e:
            print(f"Error: {e}")
        return False

    def get_admin(self):
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                get_query = """
                SELECT * FROM admin WHERE username = ?
                """
                cur.execute(get_query, (self.username,))
                user_data = cur.fetchone()
                if not user_data:
                    return None

                return Admin(
                    id=user_data[0],
                    username=user_data[1],
                    name=user_data[2],
                    email=user_data[3],
                    password_hash=user_data[4],
                )
        except sqlite3.DatabaseError as e:
            print(f"Error: {e}")
            return None

    def update_admin(self, email, new_password):
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                update_query = """
                UPDATE admin
                SET email = ?, password_hash = ?
                WHERE username = ?
                """
                cur.execute(
                    update_query,
                    (
                        email,
                        self.set_password(new_password),
                        self.username,
                    ),
                )
                conn.commit()
                return True
        except sqlite3.IntegrityError as e:
            print(f"Error: {e}")
        except sqlite3.DatabaseError as e:
            print(f"Error: {e}")
        return False

    def delete_admin(self):
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                delete_query = """
                DELETE FROM admin
                WHERE username = ?
                """
                cur.execute(delete_query, (self.username,))
                conn.commit()
                if cur.rowcount == 0:
                    return False
                return True
        except sqlite3.DatabaseError as e:
            print(f"Error: {e}")
        return False

    @staticmethod
    def create_table() -> None:
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                users_table = """
                CREATE TABLE IF NOT EXISTS admin (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE,
                    password_hash TEXT NOT NULL
                );
                """
                cur.execute(users_table)
                conn.commit()
        except sqlite3.DatabaseError as e:
            print(f"Error: {e}")


class Client:
    def __init__(self, username, name, email, password_hash, id=None):
        self.id = id
        self.username = username
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.is_admin = False

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def create_client(self) -> bool:
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                create_query = """
                INSERT INTO clients (username, name, email, password_hash)
                VALUES (?, ?, ?, ?)
                """
                cur.execute(
                    create_query,
                    (
                        self.username,
                        self.name,
                        self.email,
                        self.password_hash,
                    ),
                )
                conn.commit()
                return True
        except sqlite3.IntegrityError as e:
            print(f"Error: {e}")
        except sqlite3.DatabaseError as e:
            print(f"Error: {e}")
        return False

    def get_client(self):
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                get_query = """
                SELECT * FROM clients WHERE username = ?
                """
                cur.execute(get_query, (self.username,))
                user_data = cur.fetchone()
                if not user_data:
                    return None

                return Client(
                    id=user_data[0],
                    username=user_data[1],
                    name=user_data[2],
                    email=user_data[3],
                    password_hash=user_data[4],
                )
        except sqlite3.DatabaseError as e:
            print(f"Error: {e}")
            return None

    def update_admin(self, email, new_password):
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                update_query = """
                UPDATE clients
                SET email = ?, password_hash = ?
                WHERE username = ?
                """
                cur.execute(
                    update_query,
                    (
                        email,
                        self.set_password(new_password),
                        self.username,
                    ),
                )
                conn.commit()
                return True
        except sqlite3.IntegrityError as e:
            print(f"Error: {e}")
        except sqlite3.DatabaseError as e:
            print(f"Error: {e}")
        return False

    def delete_client(self):
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                delete_query = """
                DELETE FROM clients
                WHERE username = ?
                """
                cur.execute(delete_query, (self.username,))
                conn.commit()
                if cur.rowcount == 0:
                    return False
                return True
        except sqlite3.DatabaseError as e:
            print(f"Error: {e}")
        return False

    @staticmethod
    def create_table() -> None:
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                users_table = """
                CREATE TABLE IF NOT EXISTS clients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    password_hash TEXT NOT NULL
                );
                """
                cur.execute(users_table)
                conn.commit()
        except sqlite3.DatabaseError as e:
            print(f"Error: {e}")
