import os
import BaseConstants
import jsonprocessor as json


class Config(object):
    base_config = None
    ip = None

    def __init__(self, ip):
        self.ip = ip
        if(not os.path.exists(BaseConstants.BASE_GH_CONFIG_PATH.format(ip))):
            with open(BaseConstants.BASE_GH_CONFIG_PATH.format(ip), 'w') as outfile:
                self.base_config = json.json2obj(BaseConstants.CONFIG)
                json.dump(json.json2obj(BaseConstants.CONFIG), outfile)
        else:
            with open(BaseConstants.BASE_GH_CONFIG_PATH.format(ip), 'r') as config:
                self.base_config = json.json2obj(config.read())

    def get_peripheral(self):
        return self.base_config.peripherals

    def get_names_map(self):
        return self.base_config.names_map

    def get_sensors_map(self):
        return self.base_config.sensors_map

    def get_pump_times(self):
        return self.base_config.peripherals.pump_time
    
    def get_days_name(self):
        return self.base_config.peripherals.pump_time.keys()

    def add_pump_time(self, day, time_stamp):
        self.base_config.peripherals.pump_time[day].append(time_stamp)
        self.save_to_file()

    def remove_pump_time(self, day, time_stamp):
        self.base_config.peripherals.pump_time[day].remove(time_stamp)
        self.save_to_file()

    def set_pump_sensor(self, value):
        self.base_config.peripherals.pump_sensor = value
        self.save_to_file()

    def set_fans(self, value):
        self.base_config.peripherals.fans = value
        self.save_to_file()

    def set_names_map(self, new_data):
        self.base_config.names_map = new_data
        self.save_to_file()

    def set_sensors_map(self, new_data):
        self.base_config.sensors_map = new_data
        print("---------------------")
        print(self.base_config.sensors_map)
        print("---------------------")
        self.save_to_file()

    def remove_config_file(self):
        os.remove(BaseConstants.BASE_GH_CONFIG_PATH.format(self.ip))

    def save_to_file(self):
        with open(BaseConstants.BASE_GH_CONFIG_PATH.format(self.ip), 'w') as outfile:
            json.dump(self.base_config, outfile)
