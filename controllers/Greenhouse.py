
from SensorsDataModel import SensorsDataModel
from jsonprocessor import json2obj
from networker import Networker
from Config import Config


class Greenhouse(object):
    config = None
    networker = None

    data_viewmodel = None
    last_raw_data = None
    ip = None
    fans_auto_controll_mode = False
    pump_auto_controll_mode = False
    lamps_auto_controll_mode = False
    pump_auto_controll_by_humidity = False

    fans_status = False
    pump_status = False
    lamps_status = False

    def __init__(self, ip):
        self.ip = ip
        self.data_viewmodel = SensorsDataModel()
        self.networker = Networker()
        self.config = Config(ip)
        self.data_viewmodel.names_map = self.config.get_names_map()
        self.data_viewmodel.sensors_map = self.config.get_sensors_map()
        self.data_viewmodel.sensors = self.config.get_sensors_data()
        self.set_sensors_data()
        self.update_peripherals_status()

    def get_auto_controll_status(self):
        return json2obj({"fans_auto_controll_mode": self.fans_auto_controll_mode,
                "pump_auto_controll_mode": self.pump_auto_controll_mode,
                "lamps_auto_controll_mode": self.lamps_auto_controll_mode,
                "pump_auto_controll_by_humidity": self.pump_auto_controll_by_humidity
                })

    def update_auto_controll_status(self, peripheral, status):
        if (peripheral == "fans"):
            self.fans_auto_controll_mode = True if status == "true" else False
        if (peripheral == "pump"):
            self.pump_auto_controll_mode = True if status == "true" else False
        if (peripheral == "lamps"):
            self.lamps_auto_controll_mode = True if status == "true" else False
        if (peripheral == "pump_by_humidity"):
            self.pump_auto_controll_by_humidity = True if status == "true" else False

    def get_peripherals_status(self):
        self.update_peripherals_status()
        return json2obj(self.data_viewmodel.peripherals)

    def get_sensors_map(self):
        return self.data_viewmodel.sensors_map

    def get_names_map(self):
        return self.data_viewmodel.names_map

    def get_config(self):
        return self.config

    def update_peripherals_status(self):
        response = json2obj(self.networker.get_peripherals_status(self.ip))
        self.data_viewmodel.peripherals.fans = response.fans
        self.data_viewmodel.peripherals.pump = response.pump
        self.data_viewmodel.peripherals.lamps = response.lamps

    def is_data_valid(self):
        if(self.data_viewmodel.sensors.temperature_a.val != "Нет данных"):
            return True
        return False

    def get_sensors_data(self):
        return self.data_viewmodel.sensors

    def set_sensors_data(self):
        new_data = self.networker.get_sensors_data(self.ip)
        self.last_raw_data = new_data
        for key in self.data_viewmodel.sensors.keys():
            if(key.startswith("temperature")):
                self.data_viewmodel.sensors[key].change = self.compare(
                    new_data.sensors.temperature[self.data_viewmodel.sensors_map[key]].val, self.data_viewmodel.sensors[key].val)
                self.data_viewmodel.sensors[key].val = new_data.sensors.temperature[self.data_viewmodel.sensors_map[key]].val
            else:
                self.data_viewmodel.sensors[key].change = self.compare(
                    new_data.sensors.humidity[self.data_viewmodel.sensors_map[key]].val, self.data_viewmodel.sensors[key].val)
                self.data_viewmodel.sensors[key].val = new_data.sensors.humidity[self.data_viewmodel.sensors_map[key]].val

    def compare(self, new, old):
        if(type(new) == str or type(old) == str):
            return 0
        if(new == None or old == None):
            return 0
        if(new > old):
            return 1
        elif (new < old):
            return -1
        return 0

    def remove_config(self):
        self.config.remove_config_file()

    def update_sensors_map(self, new_map):
        self.data_viewmodel.sensors_map = new_map
        self.config.set_sensors_map(new_map)

    def update_names_map(self, new_map):
        self.data_viewmodel.names_map = new_map
        self.config.set_names_map(new_map)
