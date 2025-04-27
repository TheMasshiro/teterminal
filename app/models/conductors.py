import os
import sqlite3

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def get_connection():
    conn = sqlite3.connect(os.path.join(basedir, "app.db"))
    return conn


class Conductor:
    def __init__(
        self,
        conductor_name,
        conductor_id=None,
        bus_number=None,
        plate_number=None,
        vehicle_type=None,
    ):
        self.conductor_id = conductor_id
        self.conductor_name = conductor_name
        self.bus_number = bus_number
        self.plate_number = plate_number
        self.vehicle_type = vehicle_type

    def create_conductor(self):
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                create_query = """
                INSERT INTO bus_conductors (conductor_name, bus_number, plate_number, vehicle_type)
                VALUES (?, ?, ?, ?)
                """
                cur.execute(
                    create_query,
                    (
                        self.conductor_name,
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

    def update_driver(self, conductor_name, bus_number, plate_number):
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                update_query = """
                UPDATE bus_conductors
                SET conductor_name = ?, bus_number = ?, plate_number = ?
                WHERE driver_name = ?
                """
                cur.execute(
                    update_query,
                    (
                        conductor_name,
                        bus_number,
                        plate_number,
                        self.conductor_name,
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
                DELETE FROM bus_conductors
                WHERE driver_name = ? AND bus_number = ? AND plate_number = ?
                """
                cur.execute(
                    delete_query,
                    (self.conductor_name, self.bus_number, self.plate_number),
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
                SELECT * FROM bus_conductors WHERE conductor_name = ? AND vehicle_type = ?
                """
                cur.execute(get_query, (self.conductor_name, "Bus"))
                conductor_data = cur.fetchone()
                if not conductor_data:
                    return None

                return Conductor(
                    conductor_id=conductor_data[0],
                    conductor_name=conductor_data[1],
                    bus_number=conductor_data[2],
                    plate_number=conductor_data[3],
                    vehicle_type=conductor_data[4],
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
                CREATE TABLE IF NOT EXISTS bus_conductors (
                    conductor_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    conductor_name TEXT NOT NULL,
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
                CREATE INDEX IF NOT EXISTS idx_bus_conductors_bus_number
                    ON bus_conductors (bus_number);
                """
                plate_number = """
                CREATE INDEX IF NOT EXISTS idx_bus_conductors_plate_number
                    ON bus_conductors (plate_number);
                """
                driver_name = """
                CREATE INDEX IF NOT EXISTS idx_bus_conductors_conductor_name
                    ON bus_conductors (conductor_name);
                """
                cur.execute(bus_number)
                cur.execute(plate_number)
                cur.execute(driver_name)
                conn.commit()
        except sqlite3.DatabaseError as e:
            print(f"Error: {e}")
