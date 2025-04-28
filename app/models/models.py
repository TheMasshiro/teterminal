from app.models.reports import Reports
from app.models.vehicles import Bus, Car

from .users import User


def create_tables():
    User.create_table()
    User.create_index()
    Bus.create_table()
    Car.create_table()
    Bus.create_index()
    Car.create_index()

    Reports.create_bus_table()
    Reports.create_car_table()
    Reports.create_bus_trip_index()
    Reports.create_car_trip_index()
