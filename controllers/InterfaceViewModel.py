import os
from networker import Networker
from dbworker import DBWorker
import sqlite3
import BaseConstants
from StatisticController import StatisticController
from InterfaceSensorsData import InterfaceSensorsData
import schedule
import jsonprocessor as json


db = DBWorker()
networker = Networker()
update_interval = 5

class InterfaceViewModel(object):
    statistic_controller = StatisticController()
    list_of_statistic_data = {}
    

    def __init__(self):
        connection = sqlite3.connect(BaseConstants.DB_STRING)
        for gh in db.get_all_greenhouses(connection):
            self.list_of_statistic_data[gh[1]] = InterfaceSensorsData(gh[1])
            self.update_sensors_map()
            self.create_greenhouse_config_file(gh[1])
        connection.close
        schedule.every(update_interval).seconds.do(self.update_sensors_map)

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(InterfaceViewModel, cls).__new__(cls)
        return cls.instance

    def update_sensors_map(self):
        for ip, value in self.list_of_statistic_data.items():

            value.sensors["temperature_a"] = self.statistic_controller.list_of_greenhouses_data[ip].dump().sensors.temperature[value.sensors_map["temperature_a"]]
            value.sensors["temperature_b"] = self.statistic_controller.list_of_greenhouses_data[ip].dump().sensors.temperature[value.sensors_map["temperature_b"]]
            value.sensors["temperature_c"] = self.statistic_controller.list_of_greenhouses_data[ip].dump().sensors.temperature[value.sensors_map["temperature_c"]]
            value.sensors["temperature_d"] = self.statistic_controller.list_of_greenhouses_data[ip].dump().sensors.temperature[value.sensors_map["temperature_d"]]
            value.sensors["temperature_e"] = self.statistic_controller.list_of_greenhouses_data[ip].dump().sensors.temperature[value.sensors_map["temperature_e"]]
            value.sensors["temperature_f"] = self.statistic_controller.list_of_greenhouses_data[ip].dump().sensors.temperature[value.sensors_map["temperature_f"]]
            value.sensors["humidity_a"] = self.statistic_controller.list_of_greenhouses_data[ip].dump().sensors.humidity[value.sensors_map["humidity_a"]]
            value.sensors["humidity_b"] = self.statistic_controller.list_of_greenhouses_data[ip].dump().sensors.humidity[value.sensors_map["humidity_b"]]
            value.sensors["humidity_c"] = self.statistic_controller.list_of_greenhouses_data[ip].dump().sensors.humidity[value.sensors_map["humidity_c"]]
            value.sensors["humidity_d"] = self.statistic_controller.list_of_greenhouses_data[ip].dump().sensors.humidity[value.sensors_map["humidity_d"]]
            value.sensors["humidity_e"] = self.statistic_controller.list_of_greenhouses_data[ip].dump().sensors.humidity[value.sensors_map["humidity_e"]]

    def set_sensors_map(self, ip, data):
        self.list_of_statistic_data[ip].sensors_map = data
        sensors = open("./sensors/{}_SensorsConfig.json".format(ip), "w+")
        json.dump(self.list_of_statistic_data[ip].sensors_map, sensors)
        sensors.close()

    def set_names_map(self, ip, data):
            self.list_of_statistic_data[ip].names_map = data
            names = open("./sensors/{}_NamesConfig.json".format(ip), "w+")
            json.dump(self.list_of_statistic_data[ip].names_map, names)
            names.close()

    def get_sensors(self, ip):
        return self.list_of_statistic_data[ip].sensors

    def get_sensors_map(self, ip):
        return self.list_of_statistic_data[ip].sensors_map

    def get_names(self, ip):
        return self.list_of_statistic_data[ip].names_map
        
    def add(self, ip):
        connection = sqlite3.connect(BaseConstants.DB_STRING)
        new_data = json.json2obj(networker.get_sensors_data(ip))
        self.list_of_statistic_data[ip] = InterfaceSensorsData(new_data)
        connection.close()

    def remove(self, ip):
        del self.list_of_statistic_data[ip]
        os.remove("./sensors/{}_SensorsConfig.json".format(ip))

    def create_greenhouse_config_file(self, ip):
        error = False
        try:
            open("./sensors/{}_NamesConfig.json".format(ip), "x")
            open("./sensors/{}_SensorsConfig.json".format(ip), "x")
        except:
            error = True
        if(error):
            names = open("./sensors/{}_NamesConfig.json".format(ip), "r").read()
            sensors = open("./sensors/{}_SensorsConfig.json".format(ip), "r").read()
            data = json.load(names)
            self.list_of_statistic_data[ip].names_map = data
            data = json.load(sensors)
            self.list_of_statistic_data[ip].sensors_map = data
        if(not error):
            names = open("./sensors/{}_NamesConfig.json".format(ip), "w+")
            json.dump(self.list_of_statistic_data[ip].names_map, names)
            names.close()
            sensors = open("./sensors/{}_SensorsConfig.json".format(ip), "w+")
            json.dump(self.list_of_statistic_data[ip].sensors_map, sensors)
            sensors.close()
