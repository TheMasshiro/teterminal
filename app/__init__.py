import atexit
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from flask_login import LoginManager

from app.backend_helpers import (
    check_arrival,
    display_availability,
    display_schedules,
    reset_statuses,
)
from app.models.reports import Reports
from app.models.vehicles import Bus, Car
from instance.config import Config

app = Flask(__name__)
app.config.from_object(Config)
login = LoginManager(app)


def start_db():
    from app.models.models import create_tables

    return create_tables()


start_db()


def refresh_vehicle_statuses():
    print(f"[{datetime.now()}] Running background vehicle refresh...")

    buses = Bus.get_all_buses()
    cars = Car.get_all_cars()

    check_arrival(vehicles=buses, vehicle_handler=Bus, type_name="bus")
    check_arrival(vehicles=cars, vehicle_handler=Car, type_name="car")

    display_availability(vehicles=buses, vehicle_handler=Bus, type_name="bus")
    display_availability(vehicles=cars, vehicle_handler=Car, type_name="car")

    display_schedules(vehicles=buses, vehicle_handler=Bus, type_name="bus")
    display_schedules(vehicles=cars, vehicle_handler=Car, type_name="car")

    print(f"[{datetime.now()}] Vehicle refresh completed.")

    if reset_statuses(vehicles=buses, type="bus"):
        print(f"[{datetime.now()}] Buses Daily counters reset.")

    if reset_statuses(vehicles=cars, type="car"):
        print(f"[{datetime.now()}] Cars Daily counters reset.")


refresh_vehicle_statuses()

scheduler = BackgroundScheduler()
scheduler.add_job(func=refresh_vehicle_statuses, trigger="interval", seconds=60)
scheduler.start()

atexit.register(lambda: scheduler.shutdown())


from app.auth import auth_bp  # noqa: E402
from app.errors import errors_bp  # noqa: E402
from app.main import main_bp  # noqa: E402

app.register_blueprint(auth_bp)
app.register_blueprint(errors_bp)
app.register_blueprint(main_bp)
