import os
import sqlite3

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def get_connection():
    conn = sqlite3.connect(os.path.join(basedir, "app.db"))
    return conn


class Bus:
    def __init__(
        self,
        bus_number,
        plate_number,
        origin_terminal,
        destination,
        average_speed,
        status=None,
        id=None,
    ):
        self.id = id
        self.bus_number = bus_number
        self.plate_number = plate_number
        self.origin_terminal = origin_terminal
        self.destination = destination
        self.average_speed = average_speed
        self.status = status

    def add_bus(self):
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                create_query = """
                INSERT INTO busses (bus_number, plate_number, origin_terminal, destination, average_speed, status)
                VALUES (?, ?, ?, ?, ?, ?)
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
                    ),
                )
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
                SELECT * FROM busses WHERE bus_number = ? AND plate_number = ?
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
                )
        except sqlite3.DatabaseError as e:
            print(f"Error: {e}")
            return None

    def update_bus(
        self,
        bus_number,
        plate_number,
    ):
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                update_query = """
                UPDATE busses
                SET bus_number = ?, plate_number = ?
                WHERE bus_number = ?
                """
                cur.execute(
                    update_query,
                    (bus_number, plate_number, self.bus_number),
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
                DELETE FROM busses
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

    def update_destination(self, destination):
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                update_query = """
                UPDATE busses
                SET destination = ?
                WHERE bus_number = ? and plate_number = ?
                """
                cur.execute(
                    update_query,
                    (destination, self.bus_number, self.plate_number),
                )
                conn.commit()
                return True
        except sqlite3.DatabaseError as e:
            print(f"Error: {e}")
        return False

    def update_origin(self, origin_terminal):
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                update_query = """
                UPDATE busses
                SET origin_terminal = ?
                WHERE bus_number = ? and plate_number = ?
                """
                cur.execute(
                    update_query,
                    (origin_terminal, self.bus_number, self.plate_number),
                )
                conn.commit()
                return True
        except sqlite3.DatabaseError as e:
            print(f"Error: {e}")
        return False

    def update_average_speed(self, average_speed):
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                update_query = """
                UPDATE busses
                SET average_speed = ?
                WHERE bus_number = ? and plate_number = ?
                """
                cur.execute(
                    update_query,
                    (average_speed, self.bus_number, self.plate_number),
                )
                conn.commit()
                return True
        except sqlite3.DatabaseError as e:
            print(f"Error: {e}")
        return False

    def update_status(self, status):
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                update_query = """
                UPDATE busses
                SET status = ?
                WHERE bus_number = ? and plate_number = ?
                """
                cur.execute(
                    update_query,
                    (status, self.bus_number, self.plate_number),
                )
                conn.commit()
                return True
        except sqlite3.DatabaseError as e:
            print(f"Error: {e}")
        return False

    @staticmethod
    def create_table() -> None:
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                users_table = """
                CREATE TABLE IF NOT EXISTS busses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    bus_number TEXT NOT NULL UNIQUE,
                    plate_number TEXT UNIQUE,
                    origin_terminal TEXT NOT NULL,
                    destination TEXT NOT NULL,
                    average_speed REAL,
                    status TEXT DEFAULT 'At Terminal',
                    last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
                bus_index = """
                CREATE INDEX IF NOT EXISTS idx_cars ON busses(bus_number, plate_number);
                """
                cur.execute(bus_index)
                conn.commit()
        except sqlite3.DatabaseError as e:
            print(f"Error: {e}")


class Car:
    def __init__(
        self,
        car_number,
        plate_number,
        origin_terminal,
        destination,
        average_speed,
        id=None,
        status=None,
    ):
        self.id = id
        self.car_number = car_number
        self.plate_number = plate_number
        self.origin_terminal = origin_terminal
        self.destination = destination
        self.average_speed = average_speed
        self.status = status

    def add_car(self):
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                create_query = """
                INSERT INTO clients (car_number, plate_number, origin_terminal, destination, average_speed, status)
                VALUES (?, ?, ?, ?, ?, ?)
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
                    ),
                )
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
                )
        except sqlite3.DatabaseError as e:
            print(f"Error: {e}")
            return None

    def update_car(
        self,
        car_number,
        plate_number,
    ):
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                update_query = """
                UPDATE cars
                SET car_number = ?, plate_number = ?
                WHERE car_number = ?
                """
                cur.execute(
                    update_query,
                    (car_number, plate_number, self.car_number),
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

    def update_destination(self, destination):
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                update_query = """
                UPDATE cars
                SET destination = ?
                WHERE car_number = ? and plate_number = ?
                """
                cur.execute(
                    update_query,
                    (destination, self.car_number, self.plate_number),
                )
                conn.commit()
                return True
        except sqlite3.DatabaseError as e:
            print(f"Error: {e}")
        return False

    def update_origin(self, origin_terminal):
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                update_query = """
                UPDATE cars
                SET origin_terminal = ?
                WHERE car_number = ? and plate_number = ?
                """
                cur.execute(
                    update_query,
                    (origin_terminal, self.car_number, self.plate_number),
                )
                conn.commit()
                return True
        except sqlite3.DatabaseError as e:
            print(f"Error: {e}")
        return False

    def update_average_speed(self, average_speed):
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                update_query = """
                UPDATE cars
                SET average_speed = ?
                WHERE car_number = ? and plate_number = ?
                """
                cur.execute(
                    update_query,
                    (average_speed, self.car_number, self.plate_number),
                )
                conn.commit()
                return True
        except sqlite3.DatabaseError as e:
            print(f"Error: {e}")
        return False

    def update_status(self, status):
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                update_query = """
                UPDATE cars
                SET status = ?
                WHERE car_number = ? and plate_number = ?
                """
                cur.execute(
                    update_query,
                    (status, self.car_number, self.plate_number),
                )
                conn.commit()
                return True
        except sqlite3.DatabaseError as e:
            print(f"Error: {e}")
        return False

    @staticmethod
    def create_table() -> None:
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                users_table = """
                CREATE TABLE IF NOT EXISTS cars (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    car_number TEXT NOT NULL UNIQUE,
                    plate_number TEXT NOT NULL UNIQUE,
                    origin_terminal TEXT NOT NULL,
                    destination TEXT NOT NULL,
                    average_speed REAL,
                    status TEXT DEFAULT 'At Terminal',
                    last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
                car_index = """
                CREATE INDEX IF NOT EXISTS idx_cars ON cars(car_number, plate_number);
                """
                cur.execute(car_index)
                conn.commit()
        except sqlite3.DatabaseError as e:
            print(f"Error: {e}")
