import os

from dotenv import load_dotenv

from .users import Admin, Client

load_dotenv(".flaskenv")


def create_tables():
    username = os.environ.get("ADMIN_USERNAME")
    name = os.environ.get("NAME")
    password_hash = os.environ.get("PASSWORD")
    admin = Admin(username=username, name=name, password_hash=password_hash)

    admin.create_table()
    if admin.create_admin():
        Client.create_table()
        # TODO: Create tables for vehicles
