
from PeripheralsControl import PeripheralsControl
from SensorsDataModel import SensorsDataModel
from jsonprocessor import json2obj
from networker import Networker
from Config import Config


class Greenhouse(object):
    config = None
    networker = None
    peripheral_control = None

    data_model = None
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
        self.data_model = SensorsDataModel()
        self.networker = Networker()
        self.config = Config(ip)
        self.peripheral_control = PeripheralsControl()
        self.data_model.names_map = self.config.get_names_map()
        self.data_model.sensors_map = self.config.get_sensors_map()
        self.data_model.sensors = self.config.get_sensors_data()
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
            if(self.pump_auto_controll_mode):
                self.update_pump_activation_time()
            else:
                self.peripheral_control.cancel_all_job(self.ip)
        if (peripheral == "lamps"):
            self.lamps_auto_controll_mode = True if status == "true" else False
        if (peripheral == "pump_by_humidity"):
            self.pump_auto_controll_by_humidity = True if status == "true" else False
            if(self.pump_auto_controll_by_humidity):
                self.peripheral_control.cancel_all_job(self.ip)
            else:
                self.update_pump_activation_time()

    def update_pump_activation_time(self):
        for day, times in self.config.get_pump_times().items():
            for time in times:
                self.peripheral_control.add_pump_activation_time_by_day(
                    self.ip, time, day)

    def get_peripherals_status(self):
        self.update_peripherals_status()
        return json2obj(self.data_model.peripherals)

    def get_sensors_map(self):
        return self.data_model.sensors_map

    def get_names_map(self):
        return self.data_model.names_map

    def get_config(self):
        return self.config

    def get_peripheral_status(self, peripheral):
        self.update_peripherals_status()
        if(peripheral == "pump"):
            if(self.data_model.peripherals.pump == "Нет данных"):
                return 0
            else:
                return self.data_model.peripherals.pump
        elif(peripheral == "fans"):
            if(self.data_model.peripherals.fans == "Нет данных"):
                return 0
            else:
                return self.data_model.peripherals.fans

    def update_peripherals_status(self):
        response = json2obj(self.networker.get_peripherals_status(self.ip))
        self.data_model.peripherals.fans = response.fans
        self.data_model.peripherals.pump = response.pump
        self.data_model.peripherals.lamps = response.lamps

    def is_data_valid(self):
        if(self.data_model.sensors.temperature_a.val != "Нет данных"):
            return True
        return False

    def get_sensors_data(self):
        return self.data_model.sensors

    def set_sensors_data(self):
        new_data = self.networker.get_sensors_data(self.ip)
        self.last_raw_data = new_data
        for key in self.data_model.sensors.keys():
            if(key.startswith("temperature")):
                self.data_model.sensors[key].change = self.compare(
                    new_data.sensors.temperature[self.data_model.sensors_map[key]].val, self.data_model.sensors[key].val)
                self.data_model.sensors[key].val = new_data.sensors.temperature[self.data_model.sensors_map[key]].val
            else:
                self.data_model.sensors[key].change = self.compare(
                    new_data.sensors.humidity[self.data_model.sensors_map[key]].val, self.data_model.sensors[key].val)
                self.data_model.sensors[key].val = new_data.sensors.humidity[self.data_model.sensors_map[key]].val
        self.update_peripherals_auto_controll_by_temperature()

    def update_peripherals_auto_controll_by_temperature(self):
        if(self.pump_auto_controll_mode):
            if(self.pump_auto_controll_by_humidity):
                # self.peripheral_control.cancel_all_job(self.ip)
                start, end = self.config.get_pump_sensor().split("-", 1)
                start = int(start)
                end = int(end)
                current_status = self.get_peripheral_status("pump")
                current_value = self.__get_humidity_min_value()

                if(current_value <= start):
                    if(not current_status):
                        self.peripheral_control.run_pump(self.ip)
                        self.pump_status = 1
                if(current_value >= end):
                    if(current_status):
                        self.peripheral_control.stop_pump(self.ip)
                        self.pump_status = 0

        if(self.fans_auto_controll_mode):
            start, end = self.config.get_fans_sensor().split("-", 1)
            start = int(start)
            end = int(end)
            current_status = self.get_peripheral_status("fans")
            current_temperature = self.__get_max_temperature()
            if(current_temperature >= start):
                if(not current_status):
                    self.peripheral_control.run_fans(self.ip)
                    self.fans_status = 1
            if(current_temperature <= end):
                if(current_status):
                    self.peripheral_control.stop_fans(self.ip)
                    self.fans_status = 0

    def __get_max_temperature(self):
        # Change it when controlling from three sensors will needed
        max = self.data_model.sensors["temperature_DH"].val
        return max

    def __get_humidity_min_value(self):
        min = 100
        for key, value in self.data_model.sensors.items():
            if(value.val < min):
                min = value.val
        return min

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
        self.data_model.sensors_map = new_map
        self.config.set_sensors_map(new_map)

    def update_names_map(self, new_map):
        self.data_model.names_map = new_map
        self.config.set_names_map(new_map)
