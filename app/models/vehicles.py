import os
import sqlite3
from datetime import datetime, timedelta

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def get_connection():
    conn = sqlite3.connect(os.path.join(basedir, "app.db"))
    return conn


class Bus:
    def __init__(
        self,
        bus_number=None,
        plate_number=None,
        origin_terminal=None,
        destination=None,
        average_speed=None,
        status=None,
        departure_time=None,
        eta=None,
        distance=None,
        original_eta=None,
        id=None,
    ):
        self.id = id
        self.bus_number = bus_number
        self.plate_number = plate_number
        self.origin_terminal = origin_terminal
        self.destination = destination
        self.average_speed = average_speed
        self.status = status
        self.departure_time = departure_time
        self.eta = eta
        self.distance = distance
        self.original_eta = original_eta

    def add_bus(self):
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                create_query = """
                INSERT INTO buses (bus_number, plate_number, origin_terminal, destination, average_speed, status, distance, original_eta)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """
                cur.execute(
                    create_query,
                    (
                        self.bus_number,
                        self.plate_number,
                        self.origin_terminal,
                        self.destination,
                        self.average_speed,
                        self.status,
                        self.distance,
                        self.original_eta,
                    ),
                )

                bus_trip_query = """
                INSERT INTO bus_trips (bus_number, plate_number, trips, available, arrived, transit, shift, maintenance)
                VALUES (?, ?, 0, 0, 0, 0, 0, 0)
                """
                cur.execute(bus_trip_query, (self.bus_number, self.plate_number))

                conn.commit()
                return True
        except sqlite3.IntegrityError as e:
            print(f"Error: {e}")
        except sqlite3.DatabaseError as e:
            print(f"Error: {e}")
        return False

    def get_bus(self):
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                get_query = """
                SELECT * FROM buses WHERE bus_number = ? AND plate_number = ?
                """
                cur.execute(get_query, (self.bus_number, self.plate_number))
                vehicle_data = cur.fetchone()
                if not vehicle_data:
                    return None

                return Bus(
                    id=vehicle_data[0],
                    bus_number=vehicle_data[1],
                    plate_number=vehicle_data[2],
                    origin_terminal=vehicle_data[3],
                    destination=vehicle_data[4],
                    average_speed=vehicle_data[5],
                    status=vehicle_data[6],
                    departure_time=vehicle_data[7],
                    eta=vehicle_data[8],
                    distance=vehicle_data[9],
                    original_eta=vehicle_data[10],
                )
        except sqlite3.DatabaseError as e:
            print(f"Error: {e}")
            return None

    def update_bus(
        self,
        bus_number,
        plate_number,
        origin_terminal,
        destination,
        average_speed,
        status,
        distance,
        original_eta,
    ):
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                update_query = """
                UPDATE buses
                SET bus_number = ?, plate_number = ?, origin_terminal = ?, destination = ?, average_speed = ?, status = ?, distance = ?, original_eta = ?
                WHERE bus_number = ? AND plate_number = ?
                """
                cur.execute(
                    update_query,
                    (
                        bus_number,
                        plate_number,
                        origin_terminal,
                        destination,
                        average_speed,
                        status,
                        distance,
                        original_eta,
                        self.bus_number,
                        self.plate_number,
                    ),
                )
                conn.commit()
                return True
        except sqlite3.IntegrityError as e:
            print(f"Error: {e}")
        except sqlite3.DatabaseError as e:
            print(f"Error: {e}")
        return False

    def delete_bus(self):
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                delete_query = """
                DELETE FROM buses
                WHERE bus_number = ? AND plate_number = ?
                """
                cur.execute(delete_query, (self.bus_number, self.plate_number))
                conn.commit()
                if cur.rowcount == 0:
                    return False
                return True
        except sqlite3.DatabaseError as e:
            print(f"Error: {e}")
        return False

    @staticmethod
    def update_departure(bus_number, plate_number, status):
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                update_query = """
                UPDATE buses
                SET departure_time = ?
                WHERE bus_number = ? AND plate_number = ?
                """

                departure_time = None
                now = datetime.now()

                if status.lower() == "in transit":
                    departure_time = now.strftime("%I:%M %p - %d/%m/%y")
                elif status.lower() == "available":
                    departure_time = (now + timedelta(minutes=30)).strftime(
                        "%I:%M %p - %d/%m/%y"
                    )
                elif status.lower() == "arrived at destination":
                    departure_time = (now + timedelta(minutes=10)).strftime(
                        "%I:%M %p - %d/%m/%y"
                    )
                elif status.lower() == "shift over":
                    departure_time = (now + timedelta(hours=12)).strftime(
                        "%I:%M %p - %d/%m/%y"
                    )
                elif status.lower() == "maintenance":
                    departure_time = (now + timedelta(hours=48)).strftime(
                        "%I:%M %p - %d/%m/%y"
                    )

                cur.execute(
                    update_query,
                    (
                        departure_time,
                        bus_number,
                        plate_number,
                    ),
                )
                conn.commit()
                return True
        except sqlite3.IntegrityError as e:
            print(f"Error: {e}")
        except sqlite3.DatabaseError as e:
            print(f"Error: {e}")
        return False

    @staticmethod
    def update_eta(bus_number, plate_number, eta):
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                update_query = """
                UPDATE buses
                SET eta = ?
                WHERE bus_number = ? AND plate_number = ?
                """
                cur.execute(
                    update_query,
                    (
                        eta,
                        bus_number,
                        plate_number,
                    ),
                )
                conn.commit()
                return True
        except sqlite3.IntegrityError as e:
            print(f"Error: {e}")
        except sqlite3.DatabaseError as e:
            print(f"Error: {e}")
        return False

    @staticmethod
    def get_places(bus_number, plate_number):
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                get_query = """
                SELECT origin_terminal, destination
                FROM buses
                WHERE bus_number = ? AND plate_number = ?
                """
                cur.execute(
                    get_query,
                    (
                        bus_number,
                        plate_number,
                    ),
                )
                places = cur.fetchone()
                return places
        except sqlite3.DatabaseError as e:
            print(f"Error: {e}")
        return None

    @staticmethod
    def get_distance(bus_number, plate_number):
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                get_query = """
                SELECT distance
                FROM buses
                WHERE bus_number = ? AND plate_number = ?
                """
                cur.execute(
                    get_query,
                    (
                        bus_number,
                        plate_number,
                    ),
                )
                distance = cur.fetchone()
                return distance[0]
        except sqlite3.DatabaseError as e:
            print(f"Error: {e}")
        return None

    @staticmethod
    def update_status(bus_number, plate_number, status):
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                update_query = """
                UPDATE buses
                SET status = ?
                WHERE bus_number = ? AND plate_number = ?
                """
                cur.execute(
                    update_query,
                    (
                        status,
                        bus_number,
                        plate_number,
                    ),
                )
                conn.commit()
                return True
        except sqlite3.IntegrityError as e:
            print(f"Error: {e}")
        except sqlite3.DatabaseError as e:
            print(f"Error: {e}")
        return False

    @staticmethod
    def get_all_buses():
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                get_query = """
                SELECT * FROM buses;
                """
                cur.execute(get_query)
                buses_data = cur.fetchall()
                if not buses_data:
                    return []

                return [
                    Bus(
                        id=vehicle_data[0],
                        bus_number=vehicle_data[1],
                        plate_number=vehicle_data[2],
                        origin_terminal=vehicle_data[3],
                        destination=vehicle_data[4],
                        average_speed=vehicle_data[5],
                        status=vehicle_data[6],
                        departure_time=vehicle_data[7],
                        eta=vehicle_data[8],
                        distance=vehicle_data[9],
                        original_eta=vehicle_data[10],
                    )
                    for vehicle_data in buses_data
                ]
        except sqlite3.DatabaseError as e:
            print(f"Error: {e}")
            return []

    @staticmethod
    def create_table() -> None:
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                vehicle_table = """
                CREATE TABLE IF NOT EXISTS buses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    bus_number TEXT NOT NULL UNIQUE,
                    plate_number TEXT UNIQUE,
                    origin_terminal TEXT NOT NULL,
                    destination TEXT NOT NULL,
                    average_speed REAL,
                    status TEXT DEFAULT 'Available',
                    departure_time TEXT,
                    eta INTEGER DEFAULT 0,
                    distance FLOAT DEFAULT 0,
                    original_eta INTEGER DEFAULT 0,
                    last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """
                cur.execute(vehicle_table)
                conn.commit()
        except sqlite3.DatabaseError as e:
            print(f"Error: {e}")

    @staticmethod
    def create_index() -> None:
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                bus_index = """
                CREATE INDEX IF NOT EXISTS idx_buses ON buses(bus_number, plate_number);
                """
                cur.execute(bus_index)
                conn.commit()
        except sqlite3.DatabaseError as e:
            print(f"Error: {e}")


class Car:
    def __init__(
        self,
        car_number=None,
        plate_number=None,
        origin_terminal=None,
        destination=None,
        average_speed=None,
        id=None,
        status=None,
        departure_time=None,
        distance=None,
        original_eta=None,
        eta=None,
    ):
        self.id = id
        self.car_number = car_number
        self.plate_number = plate_number
        self.origin_terminal = origin_terminal
        self.destination = destination
        self.average_speed = average_speed
        self.status = status
        self.departure_time = departure_time
        self.eta = eta
        self.distance = distance
        self.original_eta = original_eta

    def add_car(self):
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                create_query = """
                INSERT INTO cars (car_number, plate_number, origin_terminal, destination, average_speed, status, distance, original_eta)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """
                cur.execute(
                    create_query,
                    (
                        self.car_number,
                        self.plate_number,
                        self.origin_terminal,
                        self.destination,
                        self.average_speed,
                        self.status,
                        self.distance,
                        self.original_eta,
                    ),
                )

                car_trip_query = """
                INSERT INTO car_trips (car_number, plate_number, trips, available, arrived, transit, shift, maintenance)
                VALUES (?, ?, 0, 0, 0, 0, 0, 0)
                """
                cur.execute(car_trip_query, (self.car_number, self.plate_number))

                conn.commit()
                return True
        except sqlite3.IntegrityError as e:
            print(f"Error: {e}")
        except sqlite3.DatabaseError as e:
            print(f"Error: {e}")
        return False

    def get_car(self):
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                get_query = """
                SELECT * FROM cars WHERE car_number = ? AND plate_number = ?
                """
                cur.execute(get_query, (self.car_number, self.plate_number))
                vehicle_data = cur.fetchone()
                if not vehicle_data:
                    return None

                return Car(
                    id=vehicle_data[0],
                    car_number=vehicle_data[1],
                    plate_number=vehicle_data[2],
                    origin_terminal=vehicle_data[3],
                    destination=vehicle_data[4],
                    average_speed=vehicle_data[5],
                    status=vehicle_data[6],
                    departure_time=vehicle_data[7],
                    eta=vehicle_data[8],
                    distance=vehicle_data[9],
                    original_eta=vehicle_data[10],
                )
        except sqlite3.DatabaseError as e:
            print(f"Error: {e}")
            return None

    def update_car(
        self,
        car_number,
        plate_number,
        origin_terminal,
        destination,
        average_speed,
        status,
        distance,
        original_eta,
    ):
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                update_query = """
                UPDATE cars
                SET car_number = ?, plate_number = ?, origin_terminal = ?, destination = ?, average_speed = ?, status = ?, distance = ?, original_eta = ?
                WHERE car_number = ? AND plate_number = ?
                """
                cur.execute(
                    update_query,
                    (
                        car_number,
                        plate_number,
                        origin_terminal,
                        destination,
                        average_speed,
                        status,
                        distance,
                        original_eta,
                        self.car_number,
                        self.plate_number,
                    ),
                )
                conn.commit()
                return True
        except sqlite3.IntegrityError as e:
            print(f"Error: {e}")
        except sqlite3.DatabaseError as e:
            print(f"Error: {e}")
        return False

    def delete_car(self):
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                delete_query = """
                DELETE FROM cars
                WHERE car_number = ? AND plate_number = ?
                """
                cur.execute(delete_query, (self.car_number, self.plate_number))
                conn.commit()
                if cur.rowcount == 0:
                    return False
                return True
        except sqlite3.DatabaseError as e:
            print(f"Error: {e}")
        return False

    @staticmethod
    def update_departure(car_number, plate_number, status):
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                update_query = """
                UPDATE cars
                SET departure_time = ?
                WHERE car_number = ? AND plate_number = ?
                """

                departure_time = None
                now = datetime.now()

                if status.lower() == "in transit":
                    departure_time = now.strftime("%I:%M %p - %d/%m/%y")
                elif status.lower() == "available":
                    departure_time = (now + timedelta(minutes=30)).strftime(
                        "%I:%M %p - %d/%m/%y"
                    )
                elif status.lower() == "arrived at destination":
                    departure_time = (now + timedelta(minutes=10)).strftime(
                        "%I:%M %p - %d/%m/%y"
                    )
                elif status.lower() == "shift over":
                    departure_time = (now + timedelta(hours=12)).strftime(
                        "%I:%M %p - %d/%m/%y"
                    )
                elif status.lower() == "maintenance":
                    departure_time = (now + timedelta(hours=48)).strftime(
                        "%I:%M %p - %d/%m/%y"
                    )

                cur.execute(
                    update_query,
                    (
                        departure_time,
                        car_number,
                        plate_number,
                    ),
                )
                conn.commit()
                return True
        except sqlite3.IntegrityError as e:
            print(f"Error: {e}")
        except sqlite3.DatabaseError as e:
            print(f"Error: {e}")
        return False

    @staticmethod
    def update_eta(car_number, plate_number, eta):
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                update_query = """
                UPDATE cars
                SET eta = ?
                WHERE car_number = ? AND plate_number = ?
                """
                cur.execute(
                    update_query,
                    (
                        eta,
                        car_number,
                        plate_number,
                    ),
                )
                conn.commit()
                return True
        except sqlite3.IntegrityError as e:
            print(f"Error: {e}")
        except sqlite3.DatabaseError as e:
            print(f"Error: {e}")
        return False

    @staticmethod
    def get_places(car_number, plate_number):
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                get_query = """
                SELECT origin_terminal, destination
                FROM cars
                WHERE car_number = ? AND plate_number = ?
                """
                cur.execute(
                    get_query,
                    (
                        car_number,
                        plate_number,
                    ),
                )
                places = cur.fetchone()
                return places
        except sqlite3.DatabaseError as e:
            print(f"Error: {e}")
        return None

    @staticmethod
    def get_distance(car_number, plate_number):
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                get_query = """
                SELECT distance
                FROM cars
                WHERE car_number = ? AND plate_number = ?
                """
                cur.execute(
                    get_query,
                    (
                        car_number,
                        plate_number,
                    ),
                )
                distance = cur.fetchone()
                return distance[0]
        except sqlite3.DatabaseError as e:
            print(f"Error: {e}")
        return None

    @staticmethod
    def update_status(car_number, plate_number, status):
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                update_query = """
                UPDATE cars
                SET status = ?
                WHERE car_number = ? AND plate_number = ?
                """
                cur.execute(
                    update_query,
                    (
                        status,
                        car_number,
                        plate_number,
                    ),
                )
                conn.commit()
                return True
        except sqlite3.IntegrityError as e:
            print(f"Error: {e}")
        except sqlite3.DatabaseError as e:
            print(f"Error: {e}")
        return False

    @staticmethod
    def get_all_cars():
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                get_query = """
                SELECT * FROM cars;
                """
                cur.execute(get_query)
                cars_data = cur.fetchall()
                if not cars_data:
                    return []

                return [
                    Car(
                        id=vehicle_data[0],
                        car_number=vehicle_data[1],
                        plate_number=vehicle_data[2],
                        origin_terminal=vehicle_data[3],
                        destination=vehicle_data[4],
                        average_speed=vehicle_data[5],
                        status=vehicle_data[6],
                        departure_time=vehicle_data[7],
                        eta=vehicle_data[8],
                        distance=vehicle_data[9],
                        original_eta=vehicle_data[10],
                    )
                    for vehicle_data in cars_data
                ]
        except sqlite3.DatabaseError as e:
            print(f"Error: {e}")
            return []

    @staticmethod
    def create_table() -> None:
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                vehicle_table = """
                CREATE TABLE IF NOT EXISTS cars (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    car_number TEXT NOT NULL UNIQUE,
                    plate_number TEXT NOT NULL UNIQUE,
                    origin_terminal TEXT NOT NULL,
                    destination TEXT NOT NULL,
                    average_speed REAL,
                    status TEXT DEFAULT 'Available',
                    departure_time TEXT,
                    eta INTEGER DEFAULT 0,
                    distance FLOAT DEFAULT 0,
                    original_eta INTEGER DEFAULT 0,
                    last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """
                cur.execute(vehicle_table)
                conn.commit()
        except sqlite3.DatabaseError as e:
            print(f"Error: {e}")

    @staticmethod
    def create_index() -> None:
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                car_index = """
                CREATE INDEX IF NOT EXISTS idx_cars ON cars(car_number, plate_number);
                """
                cur.execute(car_index)
                conn.commit()
        except sqlite3.DatabaseError as e:
            print(f"Error: {e}")
