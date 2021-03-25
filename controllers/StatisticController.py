import sqlite3
import time
import schedule
import BaseConstants
from Greenhouse import Greenhouse
from GreenhouseController import GreenhouseController
import jsonprocessor as json
import json as js
from dbworker import DBWorker
from networker import Networker
from sensors_data import Sensors_data

db = DBWorker()
networker = Networker()
update_interval = 5
# It is a multiplier (interval * 5 second)
write_to_db_interval = 12 * update_interval


class StatisticController(object):
    greenhouse_controller = GreenhouseController()
    running = True

    def __init__(self):
        connection = sqlite3.connect(BaseConstants.DB_STRING)
        for gh in db.get_all_greenhouses(connection):
            self.greenhouse_controller.add_gh(gh[1])
        connection.close

    def start_statistic_module(self):
        schedule.every(update_interval).seconds.do(self.update_sensors_data)
        schedule.every(write_to_db_interval).seconds.do(self.log_all_data)
        while self.running:
            schedule.run_pending()
            time.sleep(1)

    def update_sensors_data(self):
        self.greenhouse_controller.update_all_gh_sensors_data()

    def log_all_data(self):
        connection = sqlite3.connect(BaseConstants.DB_STRING)
        for data in self.greenhouse_controller.get_raw_greenhouses_data():
            db.log_temperature_data(connection, data)
        connection.close