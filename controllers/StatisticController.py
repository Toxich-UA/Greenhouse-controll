import sqlite3
import time
import schedule
import BaseConstants
from GreenhouseController import GreenhouseController
from dbworker import DBWorker
from networker import Networker

db = DBWorker()
networker = Networker()
update_interval = 5
# It is a multiplier (interval * 5 second)
write_to_db_interval = 12 * update_interval


class StatisticController(object):
    greenhouse_controller = None
    running = True

    def __init__(self):
        self.greenhouse_controller = GreenhouseController()

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