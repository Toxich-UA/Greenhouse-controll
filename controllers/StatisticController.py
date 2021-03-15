import sqlite3
import time
import schedule
import BaseConstants
import jsonprocessor as json
import json as js
from dbworker import DBWorker
from networker import Networker
from sensors_data import Sensors_data

db = DBWorker()
networker = Networker()
update_interval = 5
# It is a multiplier (interval * 5 second)
write_to_db_interval = 2 * update_interval
counter = 0


class StatisticController(object):
    list_of_greenhouses_data = {}
    running = True

    def __init__(self):
        connection = sqlite3.connect(BaseConstants.DB_STRING)
        for gh in db.get_all_greenhouses(connection):
            new_data = json.json2obj(networker.get_sensors_data(gh[1]))
            self.list_of_greenhouses_data[gh[1]] = Sensors_data(new_data)
        connection.close

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(StatisticController, cls).__new__(cls)
        return cls.instance

    def start_statistic_module(self):
        schedule.every(update_interval).seconds.do(self.update_sensors_data_file)
        schedule.every(write_to_db_interval).seconds.do(self.log_all_data)
        while self.running:
            schedule.run_pending()
            time.sleep(1)

    def update_sensors_data_file(self):
        for key in self.list_of_greenhouses_data:
            self.list_of_greenhouses_data[key].set_change(
                networker.get_sensors_data(self.list_of_greenhouses_data[key].data.ip))
        self.write_to_files()

    def log_all_data(self):
        connection = sqlite3.connect(BaseConstants.DB_STRING)
        for key in self.list_of_greenhouses_data:
            if (self.list_of_greenhouses_data[key].data.sensors.temperature.DH22_temperature.val != "Нет данных"):
                db.log_temperature_data(
                    connection, self.list_of_greenhouses_data[key].data)
        connection.close

    def write_to_files(self):
        for key in self.list_of_greenhouses_data:
            try:
                with open("./sensors/{}.json".format(key), 'w') as file:
                    file.write(
                        js.dumps(self.list_of_greenhouses_data[key].dump(), indent=4))
            except:
                print("==========================")
                print("Writing to file went wrong")
                print("==========================")

    def get_sensors_data(self, ip):
        try:
            # with open("./sensors/{}.json".format(ip), 'r') as file:
            #     data = json.json2obj(js.loads(file.read())).sensors
            data = self.list_of_greenhouses_data[ip].dump().sensors
        except:
            file = open(BaseConstants.NO_CONNECTION, "r")
            data = json.json2obj(js.loads(file.read())).sensors
            file.close()
            print("==========================")
            print("Get sensors data went wrong")
            print("==========================")
        return data

    def get_sensors_status(self, ip):
        try:
            # with open("./sensors/{}.json".format(ip), 'r') as file:
            #     data = json.json2obj(js.loads(file.read())).status
            data = self.list_of_greenhouses_data[ip].dump().status
        except:
            file = open(BaseConstants.NO_CONNECTION, "r")
            data = json.json2obj(js.loads(file.read())).status
            file.close()
            print("==========================")
            print("Get sensors status went wrong")
            print("==========================")
        return data

    def add(self, ip):
        connection = sqlite3.connect(BaseConstants.DB_STRING)
        new_data = json.json2obj(networker.get_sensors_data(ip))
        self.list_of_greenhouses_data[ip] = Sensors_data(new_data)
        connection.close()

    def remove(self, ip):
        del self.list_of_greenhouses_data[ip]
