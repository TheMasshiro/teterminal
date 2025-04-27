from datetime import datetime, timedelta

from app.helpers import convert_time_format, get_municipalities, time_remaining


def updated_schedules(vehicles, type):
    vehicle_type = None
    vehicle_number = None
    scheduled_vehicles = []

    for vehicle in vehicles:
        if vehicle.distance is None:
            vehicle.distance = 0
        if type.lower() == "bus":
            vehicle_type = "bus_number"
            vehicle_number = vehicle.bus_number
        elif type.lower() == "car":
            vehicle_type = "car_number"
            vehicle_number = vehicle.car_number

        scheduled_vehicles.append(
            {
                vehicle_type: vehicle_number,
                "terminal": vehicle.origin_terminal,
                "destination": vehicle.destination,
                "distance": (vehicle.distance / 1000),
                "departure_time": vehicle.departure_time,
                "eta": convert_time_format(vehicle.eta),
                "status": vehicle.status,
            }
        )
    return scheduled_vehicles


def updated_availability(vehicles, type):
    vehicle_type = None
    vehicle_number = None
    available_vehicles = []

    for vehicle in vehicles:
        if vehicle.distance is None:
            vehicle.distance = 0
        if type.lower() == "bus":
            vehicle_type = "bus_number"
            vehicle_number = vehicle.bus_number
        elif type.lower() == "car":
            vehicle_type = "car_number"
            vehicle_number = vehicle.car_number

        available_vehicles.append(
            {
                vehicle_type: vehicle_number,
                "terminal": vehicle.origin_terminal,
                "destination": vehicle.destination,
                "distance": (vehicle.distance / 1000),
                "departure_time": vehicle.departure_time,
                "status": vehicle.status,
            }
        )
    return available_vehicles


def check_arrival(vehicles, vehicle_handler, type_name):
    CURRENT_TIME = datetime.now()
    for vehicle in vehicles:
        if type_name.lower() == "bus":
            vehicle_number = vehicle.bus_number
        elif type_name.lower() == "car":
            vehicle_number = vehicle.car_number
        else:
            continue

        if vehicle.departure_time and vehicle.eta <= 0 and vehicle.status:
            vehicle_departure_time = datetime.strptime(
                vehicle.departure_time, "%I:%M %p - %d/%m/%y"
            )

            if (
                CURRENT_TIME >= vehicle_departure_time
                and vehicle.status.lower() == "arrived at destination"
            ):
                vehicle_handler.update_eta(vehicle_number, vehicle.plate_number, 0)
                vehicle_handler.update_status(
                    vehicle_number, vehicle.plate_number, "Available"
                )
                vehicle_handler.update_departure(
                    vehicle_number, vehicle.plate_number, "Available"
                )
                vehicle.eta = 0
                vehicle.status = "Available"
                vehicle.departure_time = (CURRENT_TIME + timedelta(minutes=1)).strftime(
                    "%I:%M %p - %d/%m/%y"
                )


def display_availability(vehicles, vehicle_handler, type_name):
    CURRENT_TIME = datetime.now()
    for vehicle in vehicles:
        if type_name.lower() == "bus":
            vehicle_number = vehicle.bus_number
        elif type_name.lower() == "car":
            vehicle_number = vehicle.car_number
        else:
            continue

        if vehicle.departure_time and vehicle.eta <= 0 and vehicle.status:
            vehicle_departure_time = datetime.strptime(
                vehicle.departure_time, "%I:%M %p - %d/%m/%y"
            )

            if (
                CURRENT_TIME >= vehicle_departure_time
                and vehicle.status.lower() == "available"
            ):
                print("HELLO?")
                vehicle_handler.update_eta(vehicle_number, vehicle.plate_number, 0)
                vehicle_handler.update_status(
                    vehicle_number, vehicle.plate_number, "In Transit"
                )
                vehicle_handler.update_departure(
                    vehicle_number, vehicle.plate_number, "In Transit"
                )
                vehicle.eta = 0
                vehicle.status = "In Transit"
                vehicle.departure_time = CURRENT_TIME.strftime("%I:%M %p - %d/%m/%y")


def display_schedules(vehicles, vehicle_handler, type_name):
    CURRENT_TIME = datetime.now()
    for vehicle in vehicles:
        if type_name.lower() == "bus":
            vehicle_number = vehicle.bus_number
        elif type_name.lower() == "car":
            vehicle_number = vehicle.car_number
        else:
            continue

        if vehicle.original_eta is None:
            vehicle.original_eta = 0

        if vehicle.departure_time and vehicle.eta > 0 and vehicle.status:
            eta_minutes = time_remaining(vehicle.departure_time)
            current_eta = vehicle.original_eta - eta_minutes

            if vehicle.status.lower() == "in transit":
                vehicle_handler.update_eta(
                    vehicle_number, vehicle.plate_number, current_eta
                )
                vehicle.eta = current_eta

            if eta_minutes >= vehicle.original_eta or current_eta <= 0:
                vehicle_handler.update_status(
                    vehicle_number, vehicle.plate_number, "Arrived At Destination"
                )
                vehicle_handler.update_departure(
                    vehicle_number, vehicle.plate_number, "Arrived At Destination"
                )
                vehicle.status = "Arrived At Destination"
                vehicle.departure_time = (CURRENT_TIME + timedelta(minutes=1)).strftime(
                    "%I:%M %p - %d/%m/%y"
                )

        elif (
            (vehicle.eta == 0 or vehicle.eta is None)
            and vehicle.original_eta is not None
            and vehicle.status is not None
            and vehicle.status.lower() == "in transit"
        ):
            updated = vehicle_handler.update_eta(
                vehicle_number, vehicle.plate_number, vehicle.original_eta
            )
            if updated:
                vehicle.eta = vehicle.original_eta


def status_change(vehicle, form):
    if form.status.data.lower() == "in transit":
        vehicle.update_departure(
            form.vehicle_number.data,
            form.plate_number.data,
            form.status.data,
        )
    elif form.status.data.lower() == "available":
        vehicle.update_departure(
            form.vehicle_number.data,
            form.plate_number.data,
            form.status.data,
        )
    elif form.status.data.lower() == "arrived at destination":
        vehicle.update_departure(
            form.vehicle_number.data,
            form.plate_number.data,
            form.status.data,
        )
    elif form.status.data.lower() == "shift over":
        vehicle.update_departure(
            form.vehicle_number.data,
            form.plate_number.data,
            form.status.data,
        )
    elif form.status.data.lower() == "maintenance":
        vehicle.update_departure(
            form.vehicle_number.data,
            form.plate_number.data,
            form.status.data,
        )


def autofill_edit(vehicle, form):
    from_place = (
        vehicle.origin_terminal.split(", ") if vehicle.origin_terminal else ["", ""]
    )
    to_place = vehicle.destination.split(", ") if vehicle.destination else ["", ""]

    form.from_province.data = from_place[1]
    form.from_city.data = from_place[0]

    form.to_province.data = to_place[1]
    form.to_city.data = to_place[0]

    from_cities = get_municipalities(form.from_province.data)
    to_cities = get_municipalities(form.to_province.data)

    form.from_city.choices = [(city, city) for city in from_cities]
    form.to_city.choices = [(city, city) for city in to_cities]

    status = vehicle.status if vehicle.status else None
    form.status.data = status
