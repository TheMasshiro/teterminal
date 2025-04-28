from abc import ABC, abstractmethod
from typing import Any

from flask import render_template, request

from app.backend_helpers import (
    check_arrival,
    display_availability,
    display_schedules,
    updated_availability,
    updated_schedules,
    vehicle_statuses,
    vehicle_trips,
)
from app.models.users import User
from app.models.vehicles import Bus, Car


class MainInterface(ABC):
    @abstractmethod
    def index(self) -> Any:
        pass

    @abstractmethod
    def profile(self, username) -> Any:
        pass

    @abstractmethod
    def dashboard_admin(self) -> Any:
        pass

    @abstractmethod
    def dashboard_client(self) -> Any:
        pass

    @abstractmethod
    def availability(self) -> Any:
        pass

    @abstractmethod
    def reports(self) -> Any:
        pass

    @abstractmethod
    def schedules(self) -> Any:
        pass

    @abstractmethod
    def manage_clients(self) -> Any:
        pass

    @abstractmethod
    def manage_buses(self) -> Any:
        pass

    @abstractmethod
    def manage_cars(self) -> Any:
        pass

    @abstractmethod
    def schedules_cars(self) -> Any:
        pass

    @abstractmethod
    def schedules_buses(self) -> Any:
        pass

    @abstractmethod
    def available_cars(self) -> Any:
        pass

    @abstractmethod
    def available_buses(self) -> Any:
        pass


class Main(MainInterface):
    def index(self):
        return render_template("index.html", title="Home")

    def profile(self, username):
        return render_template(
            "main/profile.html", title=f"{username.title()}'s Profile"
        )

    def dashboard_admin(self):
        return render_template("main/dashboard.html", title="Dashboard")

    def dashboard_client(self):
        return render_template("main/dashboard.html", title="Dashboard")

    def availability(self):
        return render_template("main/available.html", title="Fleet Availability")

    def reports(self):
        buses = Bus.get_all_buses()
        cars = Car.get_all_cars()

        buses_status = vehicle_statuses(buses, "bus")
        cars_status = vehicle_statuses(cars, "car")

        bus_trips = vehicle_trips(buses, "bus")
        car_trips = vehicle_trips(cars, "car")

        return render_template(
            "main/reports.html",
            title="Daily Reports",
            buses=buses_status,
            cars=cars_status,
            bus_trips=bus_trips,
            car_trips=car_trips,
        )

    def schedules(self):
        return render_template("main/schedule.html", title="Fleet Schedules")

    def manage_clients(self):
        clients = User.get_all_users()
        if request.method == "GET":
            return render_template(
                "main/manage_clients.html", title="Manage Clients", clients=clients
            )
        return render_template("main/manage_clients.html", title="Manage Clients")

    def manage_buses(self):
        buses = Bus.get_all_buses()

        display_schedules(vehicles=buses, vehicle_handler=Bus, type_name="bus")
        check_arrival(vehicles=buses, vehicle_handler=Bus, type_name="bus")
        display_availability(vehicles=buses, vehicle_handler=Bus, type_name="bus")

        updated_buses = Bus.get_all_buses()

        if request.method == "GET":
            return render_template(
                "main/manage_buses.html", title="Manage Buses", buses=updated_buses
            )
        return render_template(
            "main/manage_buses.html", title="Manage Buses", buses=updated_buses
        )

    def manage_cars(self):
        cars = Car.get_all_cars()

        display_schedules(vehicles=cars, vehicle_handler=Car, type_name="car")
        check_arrival(vehicles=cars, vehicle_handler=Car, type_name="car")
        display_availability(vehicles=cars, vehicle_handler=Car, type_name="car")

        updated_cars = Car.get_all_cars()

        if request.method == "GET":
            return render_template(
                "main/manage_cars.html", title="Manage Cars", cars=updated_cars
            )
        return render_template(
            "main/manage_cars.html", title="Manage Cars", cars=updated_cars
        )

    def schedules_cars(self):
        cars = Car.get_all_cars()

        display_schedules(vehicles=cars, vehicle_handler=Car, type_name="car")
        check_arrival(vehicles=cars, vehicle_handler=Car, type_name="car")

        updated_cars = Car.get_all_cars()
        scheduled_cars = updated_schedules(vehicles=updated_cars, type="car")

        return render_template(
            "main/schedule_cars.html",
            title="Car Schedules",
            type="cars",
            cars=scheduled_cars,
        )

    def schedules_buses(self):
        buses = Bus.get_all_buses()

        display_schedules(vehicles=buses, vehicle_handler=Bus, type_name="bus")
        check_arrival(vehicles=buses, vehicle_handler=Bus, type_name="bus")

        updated_buses = Bus.get_all_buses()
        scheduled_buses = updated_schedules(vehicles=updated_buses, type="bus")

        return render_template(
            "main/schedule_buses.html",
            title="Bus Schedules",
            type="buses",
            buses=scheduled_buses,
        )

    def available_cars(self):
        cars = Car.get_all_cars()

        check_arrival(vehicles=cars, vehicle_handler=Car, type_name="car")
        display_availability(vehicles=cars, vehicle_handler=Car, type_name="car")

        updated_cars = Car.get_all_cars()
        available_cars = updated_availability(vehicles=updated_cars, type="car")

        return render_template(
            "main/available_cars.html",
            title="Available Cars",
            type="cars",
            cars=available_cars,
        )

    def available_buses(self):
        buses = Bus.get_all_buses()

        check_arrival(vehicles=buses, vehicle_handler=Bus, type_name="bus")
        display_availability(vehicles=buses, vehicle_handler=Bus, type_name="bus")

        updated_buses = Bus.get_all_buses()
        available_buses = updated_availability(vehicles=updated_buses, type="bus")

        return render_template(
            "main/available_buses.html",
            title="Available Buses",
            type="buses",
            buses=available_buses,
        )
