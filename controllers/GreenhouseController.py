import sqlite3
import BaseConstants
from Greenhouse import Greenhouse
from PeripheralsControl import PeripheralsControl
from dbworker import DBWorker
from networker import Networker

networker = Networker()

class GreenhouseController(object):
    db = DBWorker()
    peripheral_control = PeripheralsControl()


    list_of_greenhouses = {}

    def __init__(self):
        connection = sqlite3.connect(BaseConstants.DB_STRING)
        greengouses = self.db.get_all_greenhouses(connection)
        connection.close()
        for gh in greengouses:
            ip = gh[1]
            self.add_gh(ip)
            for day, times in self.list_of_greenhouses[ip].config.get_pump_times().items():
                for time in times:
                    self.peripheral_control.add_pump_activation_time_by_day(ip, time, day)
        
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(GreenhouseController, cls).__new__(cls)
        return cls.instance

    def update_all_gh_sensors_data(self):
        for key in self.list_of_greenhouses:
            self.list_of_greenhouses[key].set_sensors_data()

    def is_data_valid(self, ip):
        return self.list_of_greenhouses[ip].is_data_valid()
    
    def get_greenhouse_data(self, ip):
        return self.list_of_greenhouses[ip].get_sensors_data()

    def get_peripherals_status(self, ip):
        return self.list_of_greenhouses[ip].get_peripherals_status()

    def get_names_map(self, ip):
        return self.list_of_greenhouses[ip].get_names_map()

    def get_sensors_map(self, ip):
        return self.list_of_greenhouses[ip].get_sensors_map()

    def get_greenhouse_config(self, ip):
        return self.list_of_greenhouses[ip].get_config()
    
    def get_days_name(self, ip):
        return self.list_of_greenhouses[ip].config.get_days_name()

    def update_sensors_map(self, ip, new_map):
        self.list_of_greenhouses[ip].update_sensors_map(new_map)

    def update_names_map(self, ip, new_map):
        self.list_of_greenhouses[ip].update_names_map(new_map)

    def add_pump_activation_time(self, ip, start_end, day):
        self.peripheral_control.add_pump_activation_time_by_day(ip, start_end, day)
        self.list_of_greenhouses[ip].config.add_pump_time(day, start_end)

    def remove_pump_activation_time(self, ip, start_end, day):
        self.peripheral_control.remove_pump_activation_time(ip, start_end, day)
        self.list_of_greenhouses[ip].config.remove_pump_time(day, start_end)

    def get_raw_greenhouses_data(self):
        data = []
        for key in self.list_of_greenhouses:
            if(self.list_of_greenhouses[key].is_data_valid()):
                data.append(self.list_of_greenhouses[key].last_raw_data)
        return data

    def get_auto_controll_status(self, ip):
        return self.list_of_greenhouses[ip].get_auto_controll_status()

    def update_auto_controll_status(self, ip, peripheral, status):
        self.list_of_greenhouses[ip].update_auto_controll_status(peripheral, status)

    def update_peripherals(self, ip):
        self.list_of_greenhouses[ip].update_peripherals_status()

    def add_gh(self, ip):
        self.list_of_greenhouses[ip] = Greenhouse(ip)

    def remove_gh(self, ip):
        self.list_of_greenhouses[ip].remove_config()
        del self.list_of_greenhouses[ip]