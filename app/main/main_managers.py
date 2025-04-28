from abc import ABC, abstractmethod
from typing import Any

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user

from app.backend_helpers import add_status_count, autofill_edit, status_change
from app.forms import AddBus, AddCar, EditBus, EditCar, EditClient, UpdateProfile
from app.helpers import calculate_eta, geocode_place, get_distance, get_municipalities
from app.models.users import User
from app.models.vehicles import Bus, Car


class MainInterface(ABC):
    @abstractmethod
    def add_vehicle(self, type) -> Any:
        pass

    @abstractmethod
    def edit_vehicle(self, bus_number, car_number, plate_number, type) -> Any:
        pass

    @abstractmethod
    def delete_vehicle(self, bus_number, car_number, plate_number, type) -> Any:
        pass

    @abstractmethod
    def edit_client(self, client_username) -> Any:
        pass

    @abstractmethod
    def delete_client(self, client_username) -> Any:
        pass

    @abstractmethod
    def update_profile(self, username) -> Any:
        pass


class Manager(MainInterface):
    def add_vehicle(self, type):
        if current_user.user_type != "admin":
            flash("You don't have permission to add vehicles.", "danger")
            return redirect(url_for("main.dashboard_client"))

        if type == "bus":
            form = AddBus()

            from_cities = get_municipalities(form.from_province.data)
            to_cities = get_municipalities(form.to_province.data)

            form.from_city.choices = [(city, city) for city in from_cities]
            form.to_city.choices = [(city, city) for city in to_cities]

            if form.validate_on_submit():
                terminal = f"{form.from_city.data}, {form.from_province.data}"
                destination = f"{form.to_city.data}, {form.to_province.data}"

                try:
                    geocoded_terminal = geocode_place(terminal)
                    geocoded_destination = geocode_place(destination)

                    distance = get_distance(geocoded_terminal, geocoded_destination)
                    if distance is None:
                        flash(
                            "The calculated distance is too far to process. Please check the locations and try again.",
                            "danger",
                        )
                        return redirect(url_for("main.add_vehicle", type=type))

                    original_eta = calculate_eta(
                        distance_km=distance,
                        average_speed=form.avg_speed.data,
                        buffer_factor=1.6,
                    )

                except (ValueError, TypeError):
                    flash("An error has occurred", "danger")
                    return redirect(url_for("main.add_vehicle", type=type))

                bus = Bus(
                    bus_number=form.vehicle_number.data,
                    plate_number=form.plate_number.data,
                    origin_terminal=terminal,
                    destination=destination,
                    average_speed=form.avg_speed.data,
                    status=form.status.data,
                    distance=distance,
                    original_eta=original_eta,
                )
                if not bus.add_bus():
                    flash("This bus is already registered in the system.", "danger")
                    return redirect(url_for("main.add_vehicle", type=type))

                status_change(vehicle=Bus, form=form)
                add_status_count(
                    vehicle_number=form.vehicle_number.data,
                    plate_number=form.plate_number.data,
                    status=form.status.data,
                    type="bus",
                )

                flash("Created", "success")
                return redirect(url_for("main.manage_buses"))

            return render_template(
                "main/add_vehicle.html", form=form, type=type, title="Add Bus"
            )
        else:
            form = AddCar()

            from_cities = get_municipalities(form.from_province.data)
            to_cities = get_municipalities(form.to_province.data)

            form.from_city.choices = [(city, city) for city in from_cities]
            form.to_city.choices = [(city, city) for city in to_cities]

            if form.validate_on_submit():
                terminal = f"{form.from_city.data}, {form.from_province.data}"
                destination = f"{form.to_city.data}, {form.to_province.data}"

                try:
                    geocoded_terminal = geocode_place(terminal)
                    geocoded_destination = geocode_place(destination)

                    distance = get_distance(geocoded_terminal, geocoded_destination)
                    if distance is None:
                        flash(
                            "The calculated distance is too far to process. Please check the locations and try again.",
                            "danger",
                        )
                        return redirect(url_for("main.add_vehicle", type=type))

                    original_eta = calculate_eta(
                        distance_km=distance,
                        average_speed=form.avg_speed.data,
                        buffer_factor=1.3,
                    )

                except (ValueError, TypeError):
                    flash("An error has occurred", "danger")
                    return redirect(url_for("main.add_vehicle", type=type))

                car = Car(
                    car_number=form.vehicle_number.data,
                    plate_number=form.plate_number.data,
                    origin_terminal=terminal,
                    destination=destination,
                    average_speed=form.avg_speed.data,
                    status=form.status.data,
                    distance=distance,
                    original_eta=original_eta,
                )
                if not car.add_car():
                    flash("This car is already registered in the system.", "danger")
                    return redirect(url_for("main.add_vehicle", type=type))

                status_change(vehicle=Car, form=form)
                add_status_count(
                    vehicle_number=form.vehicle_number.data,
                    plate_number=form.plate_number.data,
                    status=form.status.data,
                    type="car",
                )

                flash("Created", "success")
                return redirect(url_for("main.manage_cars"))
            return render_template(
                "main/add_vehicle.html", form=form, type=type, title="Add Car"
            )

    def edit_vehicle(self, bus_number, car_number, plate_number, type):
        if current_user.user_type != "admin":
            flash("You don't have permission to edit vehicles.", "danger")
            return redirect(url_for("main.dashboard_client"))

        if type == "bus":
            form = EditBus()

            from_cities = get_municipalities(form.from_province.data)
            to_cities = get_municipalities(form.to_province.data)

            form.from_city.choices = [(city, city) for city in from_cities]
            form.to_city.choices = [(city, city) for city in to_cities]

            bus = Bus(
                bus_number=bus_number,
                plate_number=plate_number,
            )
            vehicle = bus.get_bus()
            if not vehicle:
                flash("Bus not found.", "error")
                return redirect(url_for("main.manage_buses"))

            places = bus.get_places(bus_number, plate_number)
            if places is None:
                places = ["", ""]

            if request.method == "GET":
                autofill_edit(vehicle=vehicle, form=form)

            if form.validate_on_submit():
                terminal = f"{form.from_city.data}, {form.from_province.data}"
                destination = f"{form.to_city.data}, {form.to_province.data}"
                distance = None
                original_eta = None

                if terminal == destination:
                    flash("Terminal and destination cannot be the same.", "danger")
                    return redirect(
                        url_for(
                            "main.edit_vehicle",
                            bus_number=bus_number,
                            car_number="null",
                            plate_number=plate_number,
                            type=type,
                        )
                    )

                if places[0] != terminal or places[1] != destination:
                    try:
                        geocoded_terminal = geocode_place(terminal)
                        geocoded_destination = geocode_place(destination)

                        distance = get_distance(geocoded_terminal, geocoded_destination)
                        if distance is None:
                            flash(
                                "The calculated distance is too far to process. Please check the locations and try again.",
                                "danger",
                            )
                            return redirect(
                                url_for(
                                    "main.edit_vehicle",
                                    bus_number=bus_number,
                                    car_number="null",
                                    plate_number=plate_number,
                                    type=type,
                                )
                            )

                        original_eta = calculate_eta(
                            distance_km=distance,
                            average_speed=form.avg_speed.data,
                            buffer_factor=1.6,
                        )

                    except (ValueError, TypeError):
                        flash("An error has occurred", "danger")
                        return redirect(
                            url_for(
                                "main.edit_vehicle",
                                bus_number=bus_number,
                                car_number="null",
                                plate_number=plate_number,
                                type=type,
                            )
                        )
                else:
                    distance = bus.get_distance(bus_number, plate_number)
                    if distance is None:
                        distance = 0

                    original_eta = calculate_eta(
                        distance_km=distance,
                        average_speed=form.avg_speed.data,
                        buffer_factor=1.6,
                    )

                if not bus.update_bus(
                    bus_number=form.vehicle_number.data,
                    plate_number=form.plate_number.data,
                    origin_terminal=terminal,
                    destination=destination,
                    average_speed=form.avg_speed.data,
                    status=form.status.data,
                    distance=distance,
                    original_eta=original_eta,
                ):
                    flash("This bus is already registered in the system.", "danger")
                    return redirect(
                        url_for(
                            "main.edit_vehicle",
                            bus_number=bus_number,
                            car_number="null",
                            plate_number=plate_number,
                            type=type,
                        )
                    )

                Bus.update_eta(form.vehicle_number.data, form.plate_number.data, 0)
                status_change(vehicle=Bus, form=form)
                add_status_count(
                    vehicle_number=form.vehicle_number.data,
                    plate_number=form.plate_number.data,
                    status=form.status.data,
                    type="bus",
                )

                flash("Updated", "success")
                return redirect(url_for("main.manage_buses"))

            return render_template(
                "main/edit_vehicle.html",
                vehicle=vehicle,
                form=form,
                type=type,
                title="Edit Bus",
            )
        else:
            form = EditCar()

            from_cities = get_municipalities(form.from_province.data)
            to_cities = get_municipalities(form.to_province.data)

            form.from_city.choices = [(city, city) for city in from_cities]
            form.to_city.choices = [(city, city) for city in to_cities]

            car = Car(
                car_number=car_number,
                plate_number=plate_number,
            )
            vehicle = car.get_car()
            if not vehicle:
                flash("Car not found.", "error")
                return redirect(url_for("main.manage_buses"))

            places = car.get_places(car_number, plate_number)
            if places is None:
                places = ["", ""]

            if request.method == "GET":
                autofill_edit(vehicle=vehicle, form=form)

            if form.validate_on_submit():
                terminal = f"{form.from_city.data}, {form.from_province.data}"
                destination = f"{form.to_city.data}, {form.to_province.data}"
                distance = None
                original_eta = None

                if terminal == destination:
                    flash("Terminal and destination cannot be the same.", "danger")
                    return redirect(
                        url_for(
                            "main.edit_vehicle",
                            bus_number="null",
                            car_number=car_number,
                            plate_number=plate_number,
                            type=type,
                        )
                    )

                if places[0] != terminal or places[1] != destination:
                    try:
                        geocoded_terminal = geocode_place(terminal)
                        geocoded_destination = geocode_place(destination)

                        distance = get_distance(geocoded_terminal, geocoded_destination)
                        if distance is None:
                            flash(
                                "The calculated distance is too far to process. Please check the locations and try again.",
                                "danger",
                            )
                            return redirect(
                                url_for(
                                    "main.edit_vehicle",
                                    bus_number="null",
                                    car_number=car_number,
                                    plate_number=plate_number,
                                    type=type,
                                )
                            )

                        original_eta = calculate_eta(
                            distance_km=distance,
                            average_speed=form.avg_speed.data,
                            buffer_factor=1.3,
                        )

                    except (ValueError, TypeError):
                        flash("An error has occurred", "danger")
                        return redirect(
                            url_for(
                                "main.edit_vehicle",
                                bus_number="null",
                                car_number=car_number,
                                plate_number=plate_number,
                                type=type,
                            )
                        )
                else:
                    distance = car.get_distance(car_number, plate_number)
                    if distance is None:
                        distance = 0

                    original_eta = calculate_eta(
                        distance_km=distance,
                        average_speed=form.avg_speed.data,
                        buffer_factor=1.6,
                    )

                if not car.update_car(
                    car_number=form.vehicle_number.data,
                    plate_number=form.plate_number.data,
                    origin_terminal=terminal,
                    destination=destination,
                    average_speed=form.avg_speed.data,
                    status=form.status.data,
                    distance=distance,
                    original_eta=original_eta,
                ):
                    flash("This car is already registered in the system.", "danger")
                    return redirect(
                        url_for(
                            "main.edit_vehicle",
                            bus_number="null",
                            car_number=car_number,
                            plate_number=plate_number,
                            type=type,
                        )
                    )

                Car.update_eta(form.vehicle_number.data, form.plate_number.data, 0)
                status_change(vehicle=Car, form=form)
                add_status_count(
                    vehicle_number=form.vehicle_number.data,
                    plate_number=form.plate_number.data,
                    status=form.status.data,
                    type="car",
                )

                flash("Updated", "success")
                return redirect(url_for("main.manage_cars"))
            return render_template(
                "main/edit_vehicle.html",
                vehicle=vehicle,
                form=form,
                type=type,
                title="Edit Car",
            )

    def delete_vehicle(self, bus_number, car_number, plate_number, type):
        if current_user.user_type != "admin":
            flash("You don't have permission to delete vehicles.", "danger")
            return redirect(url_for("main.dashboard_client"))
        if type == "bus":
            if Bus(bus_number=bus_number, plate_number=plate_number).delete_bus():
                flash(f"Bus no. {bus_number} has been deleted.", "success")
            else:
                flash(f"Failed to delete bus no. {bus_number}.", "danger")
            return redirect(url_for("main.manage_buses"))
        else:
            if Car(car_number=car_number, plate_number=plate_number).delete_car():
                flash(f"Car no. {car_number} has been deleted.", "success")
            else:
                flash(f"Failed to delete car no. {car_number}.", "danger")
            return redirect(url_for("main.manage_cars"))

    def edit_client(self, client_username):
        client = User.get_user_username(client_username)
        form = EditClient()
        if form.validate_on_submit():
            client = User(username=client_username)
            if not client.update_user(
                form.first_name.data,
                form.last_name.data,
                form.new_password.data,
            ):
                flash("An error has occurred", "danger")
                return redirect(url_for("main.manage_clients"))
            flash("Edited", "success")
            return redirect(url_for("main.manage_clients"))
        return render_template(
            "main/edit_client.html",
            client=client,
            form=form,
            page="edit_client",
            title="Edit Client",
        )

    def delete_client(self, client_username):
        if current_user.user_type != "admin":
            flash("You don't have permission to delete clients.", "danger")
            return redirect(url_for("main.dashboard_client"))
        if User(username=client_username).delete_user():
            flash(f"Client {client_username} has been deleted.", "success")
        else:
            flash(f"Failed to delete client {client_username}.", "danger")
        return redirect(url_for("main.manage_clients"))

    def update_profile(self, username):
        if current_user.user_type == "admin":
            user = User(username=username)
            get_user = user.get_admin()
        else:
            user = User(username=username)
            get_user = user.get_specific_user()
        if get_user is None:
            return redirect(url_for("main.profile", username=current_user.username))

        form = UpdateProfile()
        if current_user.user_type == "admin":
            form.first_name.data = "Administrator"

        if form.validate_on_submit():
            if not user.update_user(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                new_password=form.new_password.data,
            ):
                flash("An error has occurred", "danger")
                return redirect(url_for("main.update_profile", username=username))

            flash("Updated", "success")
            return redirect(url_for("main.profile", username=username))

        return render_template(
            "main/update_profile.html", form=form, title="Update Profile"
        )
