import os
import sqlite3

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def get_connection():
    conn = sqlite3.connect(os.path.join(basedir, "app.db"))
    return conn


class CarDriver:
    def __init__(
        self,
        driver_name,
        driver_id=None,
        car_number=None,
        plate_number=None,
        vehicle_type=None,
    ):
        self.driver_id = driver_id
        self.driver_name = driver_name
        self.car_number = car_number
        self.plate_number = plate_number
        self.vehicle_type = vehicle_type

    def create_driver(self):
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                create_query = """
                INSERT INTO car_drivers (driver_name, car_number, plate_number, vehicle_type)
                VALUES (?, ?, ?, ?)
                """
                cur.execute(
                    create_query,
                    (
                        self.driver_name,
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

    def update_driver(self, driver_name, car_number, plate_number, vehicle_type):
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                update_query = """
                UPDATE car_drivers
                SET driver_name = ?, car_number = ?, plate_number = ?, vehicle_type = ?
                WHERE driver_name = ?
                """
                cur.execute(
                    update_query,
                    (
                        driver_name,
                        car_number,
                        plate_number,
                        vehicle_type,
                        self.driver_name,
                    ),
                )
                conn.commit()
                return True
        except sqlite3.IntegrityError as e:
            print(f"Error: {e}")
        except sqlite3.DatabaseError as e:
            print(f"Error: {e}")
        return False

    def delete_driver(self):
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                delete_query = """
                DELETE FROM car_drivers
                WHERE driver_name = ? AND car_number = ? AND plate_number = ?
                """
                cur.execute(
                    delete_query, (self.driver_name, self.car_number, self.plate_number)
                )
                conn.commit()
                if cur.rowcount == 0:
                    return False
                return True
        except sqlite3.DatabaseError as e:
            print(f"Error: {e}")
        return False

    def get_driver(self):
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                get_query = """
                SELECT * FROM car_drivers WHERE driver_name = ? AND vehicle_type = ?
                """
                cur.execute(get_query, (self.driver_name, "Car"))
                driver_data = cur.fetchone()
                if not driver_data:
                    return None

                return CarDriver(
                    driver_id=driver_data[0],
                    driver_name=driver_data[1],
                    car_number=driver_data[2],
                    plate_number=driver_data[3],
                    vehicle_type=driver_data[4],
                )
        except sqlite3.DatabaseError as e:
            print(f"Error: {e}")
            return None

    def get_all_drivers(self):
        pass

    @staticmethod
    def create_table() -> None:
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                users_table = """
                CREATE TABLE IF NOT EXISTS car_drivers (
                    driver_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    driver_name TEXT NOT NULL,
                    car_number TEXT NOT NULL,
                    plate_number TEXT NOT NULL,
                    vehicle_type TEXT DEFAULT 'Car',
                    FOREIGN KEY (car_number) REFERENCES cars(car_number) ON DELETE CASCADE,
                    FOREIGN KEY (plate_number) REFERENCES cars(plate_number) ON DELETE CASCADE
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
                car_number = """
                CREATE INDEX IF NOT EXISTS idx_car_drivers_car_number
                    ON car_drivers (car_number);
                """
                plate_number = """
                CREATE INDEX IF NOT EXISTS idx_car_drivers_plate_number
                    ON car_drivers (plate_number);
                """
                driver_name = """
                CREATE INDEX IF NOT EXISTS idx_car_drivers_driver_name
                    ON car_drivers (driver_name);
                """
                cur.execute(car_number)
                cur.execute(plate_number)
                cur.execute(driver_name)
                conn.commit()
        except sqlite3.DatabaseError as e:
            print(f"Error: {e}")


class BusDriver:
    def __init__(
        self,
        driver_name,
        driver_id=None,
        bus_number=None,
        plate_number=None,
        vehicle_type=None,
    ):
        self.driver_id = driver_id
        self.driver_name = driver_name
        self.bus_number = bus_number
        self.plate_number = plate_number
        self.vehicle_type = vehicle_type

    def create_driver(self):
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                create_query = """
                INSERT INTO bus_drivers (driver_name, bus_number, plate_number, vehicle_type)
                VALUES (?, ?, ?, ?)
                """
                cur.execute(
                    create_query,
                    (
                        self.driver_name,
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

    def update_driver(self, driver_name, bus_number, plate_number, vehicle_type):
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                update_query = """
                UPDATE bus_drivers
                SET driver_name = ?, bus_number = ?, plate_number = ?, vehicle_type = ?
                WHERE driver_name = ?
                """
                cur.execute(
                    update_query,
                    (
                        driver_name,
                        bus_number,
                        plate_number,
                        vehicle_type,
                        self.driver_name,
                    ),
                )
                conn.commit()
                return True
        except sqlite3.IntegrityError as e:
            print(f"Error: {e}")
        except sqlite3.DatabaseError as e:
            print(f"Error: {e}")
        return False

    def delete_driver(self):
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                delete_query = """
                DELETE FROM bus_drivers
                WHERE driver_name = ? AND bus_number = ? AND plate_number = ?
                """
                cur.execute(
                    delete_query, (self.driver_name, self.bus_number, self.plate_number)
                )
                conn.commit()
                if cur.rowcount == 0:
                    return False
                return True
        except sqlite3.DatabaseError as e:
            print(f"Error: {e}")
        return False

    def get_driver(self):
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                get_query = """
                SELECT * FROM bus_drivers WHERE driver_name = ? AND vehicle_type = ?
                """
                cur.execute(get_query, (self.driver_name, "bus"))
                driver_data = cur.fetchone()
                if not driver_data:
                    return None

                return BusDriver(
                    driver_id=driver_data[0],
                    driver_name=driver_data[1],
                    bus_number=driver_data[2],
                    plate_number=driver_data[3],
                    vehicle_type=driver_data[4],
                )
        except sqlite3.DatabaseError as e:
            print(f"Error: {e}")
            return None

    def get_all_drivers(self):
        pass

    @staticmethod
    def create_table() -> None:
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                users_table = """
                CREATE TABLE IF NOT EXISTS bus_drivers (
                    driver_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    driver_name TEXT NOT NULL,
                    bus_number TEXT NOT NULL,
                    plate_number TEXT NOT NULL,
                    vehicle_type TEXT DEFAULT 'Bus',
                    FOREIGN KEY (bus_number) REFERENCES buses(bus_number) ON DELETE CASCADE,
                    FOREIGN KEY (plate_number) REFERENCES buses(plate_number) ON DELETE CASCADE
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
                bus_number = """
                CREATE INDEX IF NOT EXISTS idx_bus_drivers_bus_number
                    ON bus_drivers (bus_number);
                """
                plate_number = """
                CREATE INDEX IF NOT EXISTS idx_bus_drivers_plate_number
                    ON bus_drivers (plate_number);
                """
                driver_name = """
                CREATE INDEX IF NOT EXISTS idx_bus_drivers_driver_name
                    ON bus_drivers (driver_name);
                """
                cur.execute(bus_number)
                cur.execute(plate_number)
                cur.execute(driver_name)
                conn.commit()
        except sqlite3.DatabaseError as e:
            print(f"Error: {e}")
