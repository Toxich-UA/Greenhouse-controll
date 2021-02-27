import requests
import logging
import BaseConstants
import jsonprocessor as json

logger = logging.getLogger('networker')


class Networker(object):

    def __request(self, ip, path):
        request_string = "http://{0}:80/{1}".format(ip, path)
        data = None
        try:
            data = requests.post(request_string, data={
                                 "key": BaseConstants.SECRET_KEY}, verify=False, timeout=2).text
        except:
            logger.error("Greenhouse on {} is not responding".format(ip))
            return False

        return data

    def get_sensors_data(self, ip):
        data = self.__request(ip, "sensors")
        
        if (data):
            status = json.json2obj(data)
        else:
            status = json.json2obj(open(BaseConstants.NO_CONNECTION).read())
            status.ip = ip
        return status

    def toggle_fans(self, ip):
        data = self.__request(ip, "peripheral/fans")
        if (not(data)):
            return 'Нет данных'
        return data

    def toggle_pump(self, ip):
        data = self.__request(ip, "peripheral/pump")
        if (not(data)):
            return 'Нет данных'
        return data

    def toggle_lamps(self, ip):
        data = self.__request(ip, "peripheral/lamps")
        if (not(data)):
            return 'Нет данных'
        return data

    def get_peripherals_status(self, ip):
        data = self.__request(ip, "peripherals")
        if (not(data)):
            return '{"fans" : "Нет данных","pump" : "Нет данных"}'
        return data
