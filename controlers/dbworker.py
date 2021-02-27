import sqlite3
import datetime
import BaseConstants
from sqlite3 import Error


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

    def get_statistic(self, conn, ip, range):
        cursor = conn.cursor()
        if (range == "hour"):
            cursor.execute("SELECT * FROM Statistic WHERE greenhouse_id=? AND datetime(date) >=datetime('now', '+2 hours', '-1 hour')", (ip,))
        elif(range == "day"):
            cursor.execute("SELECT * FROM Statistic WHERE greenhouse_id=? AND datetime(date) >=datetime('now', '+2 hours', '-1 day')", (ip,))

        return cursor.fetchall()
    
    def get_statistic_for_hour(self, conn, ip):
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Statistic WHERE greenhouse_id=? AND datetime(date) >=datetime('now', '+2 hours', '-1 hour')", (ip,))
        return cursor.fetchall()

    def delete_greenhouse(self, conn, ip):
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Greenhouses WHERE ip=?', (ip,))
        conn.commit()

    def log_temperature_data(self, conn, data):
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Statistic (greenhouse_id, air_temperature, air_humidity, soil_temperature, soil_humidity, date) VALUES (?, ?, ?, ?, ?, ?)',
                       (data.ip, data.sensors.air.temperature.avg, data.sensors.air.humidity.val, data.sensors.soil.temperature.val, data.sensors.soil.humidity.avg, datetime.datetime.now()))
        conn.commit()
