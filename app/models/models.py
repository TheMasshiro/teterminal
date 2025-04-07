from app.models.vehicles import Bus, Car
from instance.config import Config

from .users import User


def create_tables():
    username = Config.ADMIN_USERNAME
    name = Config.NAME
    password_hash = Config.PASSWORD

    admin = User(username=username, name=name)
    admin.set_password(password_hash)
    admin.create_table()

    if admin.create_admin():
        admin.create_index()
        Bus.create_table()
        Car.create_table()
        Bus.create_index()
        Car.create_index()
