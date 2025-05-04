import os
import sqlite3

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def get_connection():
    conn = sqlite3.connect(os.path.join(basedir, "app.db"))
    return conn


class Reports:
    @staticmethod
    def return_report_db(type):
        try:
            with get_connection() as conn:
                if type.lower() == "bus":
                    number_type = "bus_number"
                    table_name = "bus_trips"
                elif type.lower() == "car":
                    number_type = "car_number"
                    table_name = "car_trips"
                else:
                    return None

                query = f"""
                    SELECT id, {number_type}, plate_number, trips, available, arrived, transit, maintenance, last_update
                    FROM {table_name}
                    WHERE today_date = DATE('now', 'localtime')
                """
                return conn, query

        except sqlite3.DatabaseError as e:
            print(f"Error: {e}")
            return None

    @staticmethod
    def get_trip_count(vehicle_number, plate_number, type):
        try:
            with get_connection() as conn:
                cur = conn.cursor()

                number_type = None
                if type.lower() == "bus":
                    number_type = "bus_number"
                    table_name = "bus_trips"
                elif type.lower() == "car":
                    number_type = "car_number"
                    table_name = "car_trips"
                else:
                    return None

                query = f"""
                    SELECT trips
                    FROM {table_name}
                    WHERE today_date = DATE('now', 'localtime') AND {number_type} = ? AND plate_number = ?
                """
                cur.execute(query, (vehicle_number, plate_number))
                result = cur.fetchone()
                return result[0] if result else 0

        except sqlite3.DatabaseError as e:
            print(f"Error: {e}")
            return None

    @staticmethod
    def get_statuses_count(vehicle_number, plate_number, type):
        try:
            with get_connection() as conn:
                cur = conn.cursor()

                number_type = None
                if type.lower() == "bus":
                    number_type = "bus_number"
                    table_name = "bus_trips"
                elif type.lower() == "car":
                    number_type = "car_number"
                    table_name = "car_trips"
                else:
                    return None

                query = f"""
                    SELECT available, arrived, transit, shift, maintenance
                    FROM {table_name}
                    WHERE today_date = DATE('now', 'localtime') AND {number_type} = ? AND plate_number = ?
                """
                cur.execute(query, (vehicle_number, plate_number))
                result = cur.fetchall()

                status_count = {
                    "available": 0,
                    "arrived": 0,
                    "transit": 0,
                    "shift": 0,
                    "maintenance": 0,
                }

                for row in result:
                    status_count["available"] += row[0]
                    status_count["arrived"] += row[1]
                    status_count["transit"] += row[2]
                    status_count["shift"] += row[3]
                    status_count["maintenance"] += row[4]

                return status_count

        except sqlite3.DatabaseError as e:
            print(f"Error: {e}")
            return None

    @staticmethod
    def reset_daily_counters(vehicle_number, plate_number, type):
        try:
            with get_connection() as conn:
                cur = conn.cursor()

                if type.lower() == "bus":
                    table_name = "bus_trips"
                    number_type = "bus_number"
                elif type.lower() == "car":
                    table_name = "car_trips"
                    number_type = "car_number"
                else:
                    return False

                reset_query = f"""
                UPDATE {table_name}
                SET trips = 0,
                    available = 0,
                    arrived = 0,
                    transit = 0,
                    shift = 0,
                    maintenance = 0,
                    today_date = DATE('now', 'localtime')
                WHERE DATE(today_date) != DATE('now', 'localtime') AND {number_type} = ? AND plate_number = ?
                """

                cur.execute(reset_query, (vehicle_number, plate_number))
                rows_affected = cur.rowcount
                conn.commit()

                return rows_affected > 0

        except sqlite3.DatabaseError as e:
            print(f"Error: {e}")
            return False

    @staticmethod
    def add_status(vehicle_number, plate_number, status, type):
        try:
            with get_connection() as conn:
                cur = conn.cursor()

                number_type = None
                table_name = None
                status_column = None

                if type.lower() == "bus":
                    number_type = "bus_number"
                    table_name = "bus_trips"
                elif type.lower() == "car":
                    number_type = "car_number"
                    table_name = "car_trips"
                else:
                    return False

                status = status.lower()
                if status == "available":
                    status_column = "available"
                elif status == "arrived at destination":
                    status_column = "arrived"
                elif status == "in transit":
                    status_column = "transit"
                elif status == "shift over":
                    status_column = "shift"
                elif status == "maintenance":
                    status_column = "maintenance"
                else:
                    return False

                update_query = f"""
                    UPDATE {table_name}
                    SET {status_column} = {status_column} + 1,
                        last_update = CURRENT_TIMESTAMP
                    WHERE {number_type} = ? AND plate_number = ? AND today_date = DATE('now', 'localtime')
                """

                cur.execute(update_query, (vehicle_number, plate_number))

                if status == "arrived at destination":
                    trip_query = f"""
                        UPDATE {table_name}
                        SET trips = trips + 1,
                            last_update = CURRENT_TIMESTAMP
                        WHERE {number_type} = ? AND plate_number = ? AND today_date = DATE('now', 'localtime')
                    """
                    cur.execute(trip_query, (vehicle_number, plate_number))

                conn.commit()
                return True

        except sqlite3.DatabaseError as e:
            print(f"Error: {e}")
            return False

    @staticmethod
    def create_bus_table() -> None:
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                reports_table = """
                CREATE TABLE IF NOT EXISTS bus_trips (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    bus_number TEXT,
                    plate_number TEXT,
                    today_date DATE DEFAULT CURRENT_DATE,
                    trips INTEGER DEFAULT 0,
                    available INTEGER DEFAULT 0,
                    arrived INTEGER DEFAULT 0,
                    transit INTEGER DEFAULT 0,
                    shift INTEGER DEFAULT 0,
                    maintenance INTEGER DEFAULT 0,
                    last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (bus_number) REFERENCES buses(bus_number) ON DELETE CASCADE,
                    FOREIGN KEY (plate_number) REFERENCES buses(plate_number) ON DELETE CASCADE
                );
                """
                cur.execute(reports_table)
                conn.commit()
        except sqlite3.DatabaseError as e:
            print(f"Error: {e}")

    @staticmethod
    def create_car_table() -> None:
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                reports_table = """
                CREATE TABLE IF NOT EXISTS car_trips (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    car_number TEXT,
                    plate_number TEXT,
                    today_date DATE DEFAULT CURRENT_DATE,
                    trips INTEGER DEFAULT 0,
                    available INTEGER DEFAULT 0,
                    arrived INTEGER DEFAULT 0,
                    transit INTEGER DEFAULT 0,
                    shift INTEGER DEFAULT 0,
                    maintenance INTEGER DEFAULT 0,
                    last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (car_number) REFERENCES cars(car_number) ON DELETE CASCADE,
                    FOREIGN KEY (plate_number) REFERENCES cars(plate_number) ON DELETE CASCADE
                );
                """
                cur.execute(reports_table)
                conn.commit()
        except sqlite3.DatabaseError as e:
            print(f"Error: {e}")

    @staticmethod
    def create_bus_trip_index() -> None:
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                bus_index = """
                CREATE INDEX IF NOT EXISTS idx_buses_trips ON bus_trips(bus_number, plate_number);
                """
                cur.execute(bus_index)
                conn.commit()
        except sqlite3.DatabaseError as e:
            print(f"Error: {e}")

    @staticmethod
    def create_car_trip_index() -> None:
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                bus_index = """
                CREATE INDEX IF NOT EXISTS idx_cars_trips ON car_trips(car_number, plate_number);
                """
                cur.execute(bus_index)
                conn.commit()
        except sqlite3.DatabaseError as e:
            print(f"Error: {e}")
