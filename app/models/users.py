import os
import sqlite3
from hashlib import md5

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import login

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def get_connection():
    conn = sqlite3.connect(os.path.join(basedir, "app.db"))
    return conn


@login.user_loader
def load_user(id):
    print("load user is working fine")
    return User.get_user(id)


class User(UserMixin):
    def __init__(
        self,
        username,
        id=None,
        email=None,
        name=None,
        password_hash=None,
        user_type=None,
    ):
        self.id = id
        self.username = username
        self.email = email
        self.name = name
        self.password_hash = password_hash
        self.user_type = user_type

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        if self.password_hash is None:
            return False
        return check_password_hash(self.password_hash, password)

    def avatar(self, size=128):
        email = self.email
        if self.email is None:
            email = "admin@email.com"
        if email is None:
            return None
        digest = md5(email.lower().encode("utf-8")).hexdigest()
        return f"https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}"

    def create_admin(self):
        try:
            with get_connection() as conn:
                cur = conn.cursor()

                cur.execute("SELECT 1 FROM users WHERE username = ?", (self.username,))
                if cur.fetchone():
                    return False

                create_query = """
                INSERT INTO users (username, name, password_hash, user_type)
                VALUES (?, ?, ?, ?)
                """
                cur.execute(
                    create_query,
                    (self.username, self.name, self.password_hash, "admin"),
                )
                conn.commit()
                return True
        except sqlite3.IntegrityError as e:
            print(f"Error: {e}")
        except sqlite3.DatabaseError as e:
            print(f"Error: {e}")
        return False

    def create_user(self):
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                create_query = """
                INSERT INTO users (username, name, email, password_hash)
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

    def get_admin(self):
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                get_query = """
                SELECT * FROM users WHERE username = ? AND user_type = ?
                """
                cur.execute(get_query, (self.username, "admin"))
                user_data = cur.fetchone()
                if not user_data:
                    return None

                return User(
                    id=user_data[0],
                    username=user_data[1],
                    name=user_data[2],
                    email=user_data[3],
                    password_hash=user_data[4],
                    user_type=user_data[5],
                )
        except sqlite3.DatabaseError as e:
            print(f"Error: {e}")
            return None

    def get_specific_user(self):
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                get_query = """
                SELECT * FROM users WHERE username = ? AND user_type = ?
                """
                cur.execute(get_query, (self.username, "client"))
                user_data = cur.fetchone()
                if not user_data:
                    return None

                return User(
                    id=user_data[0],
                    username=user_data[1],
                    name=user_data[2],
                    email=user_data[3],
                    password_hash=user_data[4],
                    user_type=user_data[5],
                )
        except sqlite3.DatabaseError as e:
            print(f"Error: {e}")
            return None

    def update_user(self, name, email, new_password):
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                update_query = """
                UPDATE users
                SET name = ?, email = ?, password_hash = ?
                WHERE username = ?
                """
                cur.execute(
                    update_query,
                    (
                        name,
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

    def delete_user(self):
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                delete_query = """
                DELETE FROM users
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
    def get_user(id):
        with get_connection() as conn:
            cur = conn.cursor()

            cur.execute(
                "SELECT * FROM users WHERE id = ?",
                (id,),
            )
            user_data = cur.fetchone()

            if user_data is None:
                return None

            print(user_data)
            if user_data[5] == "admin":
                print("admin")
                return User(
                    id=1,
                    username=user_data[1],
                    name=user_data[2],
                    email=user_data[3],
                    password_hash=user_data[4],
                    user_type=user_data[5],
                )

            print("user")
            return User(
                id=user_data[0],
                username=user_data[1],
                name=user_data[2],
                email=user_data[3],
                password_hash=user_data[4],
                user_type=user_data[5],
            )

    @staticmethod
    def get_user_username(username):
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                get_query = """
                SELECT * FROM users WHERE username = ?
                """
                cur.execute(get_query, (username,))
                user_data = cur.fetchone()
                if not user_data:
                    return None

                return User(
                    id=user_data[0],
                    username=user_data[1],
                    name=user_data[2],
                    email=user_data[3],
                    password_hash=user_data[4],
                    user_type=user_data[5],
                )
        except sqlite3.DatabaseError as e:
            print(f"Error: {e}")
            return None

    @staticmethod
    def get_user_email(email):
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                get_query = """
                SELECT * FROM users WHERE email = ?
                """
                cur.execute(get_query, (email,))
                user_data = cur.fetchone()
                if not user_data:
                    return None

                return User(
                    id=user_data[0],
                    username=user_data[1],
                    name=user_data[2],
                    email=user_data[3],
                    password_hash=user_data[4],
                    user_type=user_data[5],
                )
        except sqlite3.DatabaseError as e:
            print(f"Error: {e}")
            return None

    @staticmethod
    def create_table() -> None:
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                users_table = """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE,
                    password_hash TEXT NOT NULL,
                    user_type TEXT DEFAULT client
                );
                """
                cur.execute(users_table)
                conn.commit()
        except sqlite3.DatabaseError as e:
            print(f"Error: {e}")

    @staticmethod
    def create_index() -> None:
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                user_index = """
                CREATE INDEX IF NOT EXISTS idx_users ON users(username, user_type);
                """
                cur.execute(user_index)
                conn.commit()
        except sqlite3.DatabaseError as e:
            print(f"Error: {e}")
