import requests
import logging
import BaseConstants
import jsonprocessor as json



class Networker(object):
    logger = logging.getLogger(__name__)

    def __request(self, ip, path, status=None):
        request_string = "http://{0}:80/{1}".format(ip, path)
        data = None
        try:
            if(status == None):
                data = requests.post(request_string, data={
                    "key": BaseConstants.SECRET_KEY}, verify=False, timeout=2).text
            else:
                data = requests.post(request_string, data={
                    "key": BaseConstants.SECRET_KEY, "status": status}, verify=False, timeout=2).text
        except:
            self.logger.debug("Greenhouse on {} is not responding".format(ip))
            return False

        return data

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Networker, cls).__new__(cls)
        return cls.instance

    def get_sensors_data(self, ip):
        data = self.__request(ip, "sensors")
        if (data):
            try:
                status = json.json2obj(data)
            except:
                status = json.json2obj(BaseConstants.NO_CONNECTION)
                status.ip = ip
                self.logger.info("Json got wrong object")
        else:
            status = json.json2obj(BaseConstants.NO_CONNECTION)
            status.ip = ip
        return status

    def toggle_peripheral_status(self, ip, peripheral_name):
        data = self.__request(ip, f"peripherals/{peripheral_name}")
        if (not(data)):
            return 'Нет данных'
        return data

    def set_peripheral_status(self, ip, peripheral_name, status):
        data = self.__request(ip, f"peripherals/{peripheral_name}", status)
        if (not(data)):
            return 'Нет данных'
        return data

    def get_peripherals_status(self, ip):
        data = self.__request(ip, "peripherals")
        if (not(data)):
            return '''{
                        "fans": "Нет данных",
                        "pump": "Нет данных",
                        "lamps": "Нет данных"
                    }'''
        return data
