from app.models.conductors import Conductor
from app.models.drivers import BusDriver, CarDriver
from app.models.vehicles import Bus, Car

from .users import User


def create_tables():
    User.create_table()
    User.create_index()
    Bus.create_table()
    Car.create_table()
    Bus.create_index()
    Car.create_index()
    BusDriver.create_table()
    CarDriver.create_table()
    Conductor.create_table()
    BusDriver.create_index()
    CarDriver.create_index()
    Conductor.create_index()
