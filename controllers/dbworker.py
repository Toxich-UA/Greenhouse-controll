import sqlite3
import datetime
import BaseConstants

class DBWorker(object):

    def __init__(self):
        connection = sqlite3.connect(BaseConstants.DB_STRING)
        cursor = connection.cursor()
        cursor.execute(BaseConstants.sql_create_greenhouse_table)
        cursor.execute(BaseConstants.sql_create_statistic_table)

    def add_new_greenhouse(self, conn, data):
        cursor = conn.cursor()
        cursor.execute(
            'INSERT OR IGNORE INTO Greenhouses(ip, name, comment) VALUES (?,?,?)', data)
        conn.commit()

    def get_all_greenhouses(self, conn):
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Greenhouses ORDER BY ip')
        return cursor.fetchall()

    def get_greenhouse(self, conn, ip):
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Greenhouses WHERE ip=?', (ip,))
        return cursor.fetchall()

    def get_statistic(self, conn, ip, range, date_start, date_end):
        cursor = conn.cursor()
        if (range == "hour"):
            cursor.execute("SELECT * FROM Statistic WHERE greenhouse_id=? AND id%2 = 0 AND datetime(date) >= datetime('now', '-1 hour')", (ip,))
        elif(range == "day"):
            cursor.execute("SELECT * FROM Statistic WHERE greenhouse_id=? AND id%10 = 0 AND date(date) == ?", (ip, date_start))
        elif(date_end != ""):
            cursor.execute("SELECT * FROM Statistic WHERE greenhouse_id=? AND id%10 = 0 AND date(date) >= ? AND date(date) <= ?", (ip, date_start, date_end))

        return cursor.fetchall()
    
    def delete_greenhouse(self, conn, ip):
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Greenhouses WHERE ip=?', (ip,))
        conn.commit()

    def log_temperature_data(self, conn, data):
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO Statistic (
            "greenhouse_id",
            "temperature_a",
            "temperature_b",
            "temperature_c",
            "temperature_d",
            "temperature_e",
            "temperature_DH",
            "humidity_a",
            "humidity_b",
            "humidity_c",
            "humidity_d",
            "humidity_DH",
            "date"
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                       (data.ip,
                       data.sensors.temperature.OneWire_a.val,
                       data.sensors.temperature.OneWire_b.val,
                       data.sensors.temperature.OneWire_c.val,
                       data.sensors.temperature.OneWire_d.val,
                       data.sensors.temperature.OneWire_e.val,
                       data.sensors.temperature.DH22_temperature.val,
                       data.sensors.humidity.a.val,
                       data.sensors.humidity.b.val,
                       data.sensors.humidity.c.val,
                       data.sensors.humidity.d.val,
                       data.sensors.humidity.DH22_humidity.val,
                       datetime.datetime.now()))
        conn.commit()
