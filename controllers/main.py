from threading import Thread
import cherrypy
import os
import BaseConstants
from datetime import datetime
from munch import Munch
from dbworker import DBWorker
import sqlite3
import jsonprocessor as json
import json as js
from StatisticController import StatisticController as SC
from cherrypy.process.plugins import SignalHandler
from networker import Networker
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('src'))
db = DBWorker()
networker = Networker()

statistic = None
greenhouse_controller = None

class ServerStart(object):
    def __init__(self):
        global statistic
        global greenhouse_controller
        statistic = SC()
        greenhouse_controller = statistic.greenhouse_controller
        thread = Thread(target = statistic.start_statistic_module)
        thread.start()

    @cherrypy.expose
    def index(self):
        tmpl = env.get_template(BaseConstants.INDEX)
        sensors = None
        peripherals = None
        connection = sqlite3.connect(BaseConstants.DB_STRING)
        greengouses = db.get_all_greenhouses(connection)
        connection.close
        for index, gh in enumerate(greengouses):
            gh = list(gh)
            sensors = greenhouse_controller.get_greenhouse_data(gh[1])
            peripherals = greenhouse_controller.get_peripherals_status(gh[1])
            gh.append(sensors)
            gh.append(peripherals)
            greengouses[index] = gh
        return tmpl.render(gh=greengouses)

    @cherrypy.expose
    def greenhouse(self, ip):
        tmpl = env.get_template(BaseConstants.GREENHOUSE)
        
        ghConfig = greenhouse_controller.get_greenhouse_config(ip).get_peripheral()
        config = list(greenhouse_controller.get_days_name(ip))

        connection = sqlite3.connect(BaseConstants.DB_STRING)
        data = db.get_greenhouse(connection, ip)
        connection.close
        sensors = greenhouse_controller.get_greenhouse_data(ip)
        names = greenhouse_controller.get_names_map(ip)

        controls = greenhouse_controller.get_auto_controll_status(ip)


        return tmpl.render(data=data, sensors=sensors, ghConfig=ghConfig, config=config, controls=controls, names=names)

    @cherrypy.expose
    def settings(self):
        tmpl = env.get_template(BaseConstants.SETTINGS)
        connection = sqlite3.connect(BaseConstants.DB_STRING)
        gh = db.get_all_greenhouses(connection)
        connection.close
        return tmpl.render(gh=gh)

    @cherrypy.expose
    def statistic(self):
        tmpl = env.get_template(BaseConstants.STATISTIC)
        connection = sqlite3.connect(BaseConstants.DB_STRING)
        gh = db.get_all_greenhouses(connection)
        connection.close
        return tmpl.render(gh=gh)

    @cherrypy.expose
    def help(self):
        tmpl = env.get_template(BaseConstants.HELP)
        return tmpl.render()

    @cherrypy.expose
    def greenhouseSettings(self, ip):
        tmpl = env.get_template(BaseConstants.GH_CONFIG)
        sensors_map = greenhouse_controller.get_sensors_map(ip).items()
        names = greenhouse_controller.get_names_map(ip).items()
        return tmpl.render(names=names, sensors=sensors_map)

    @cherrypy.expose
    def update_greenhouse_names_and_sensors(self, ip, names, sensors_map):
        greenhouse_controller.update_names_map(ip, js.loads(names))
        greenhouse_controller.update_sensors_map(ip, js.loads(sensors_map))
        return "200"

    # REST api links
    @cherrypy.expose
    def status(self, ip):
        data = json.dump(greenhouse_controller.get_greenhouse_data(ip))
        return data

    @cherrypy.expose
    def toggle_peripheral_status(self, ip, peripheral):
        data = networker.toggle_peripheral_status(ip, peripheral)
        greenhouse_controller.update_peripherals(ip)
        return data

    @cherrypy.expose
    def get_peripherals_status(self, ip):
        data = json.json2obj(networker.get_peripherals_status(ip))
        peripherals = greenhouse_controller.get_auto_controll_status(ip)
        data.fans_controll_mode = peripherals.fans_auto_controll_mode
        data.pump_controll_mode = peripherals.pump_auto_controll_mode
        data.lamps_controll_mode = peripherals.lamps_auto_controll_mode
        return json.dump(data)

    @cherrypy.expose
    def set_control_mode(self, ip, peripheral, status):
        greenhouse_controller.update_auto_controll_status(ip, peripheral, status)

    @cherrypy.expose
    def get_logged_statistic(self, ip, range, date_start, date_end):
        connection = sqlite3.connect(BaseConstants.DB_STRING)
        data = self.transform_data_from_db(connection, ip, range, date_start, date_end)
        connection.close

        return json.dump(data)

    def transform_data_from_db(self, connection, ip, range, date_start, date_end):
        data = Munch()
        dates = []
        temperature_a = []
        temperature_b = []
        temperature_c = []
        temperature_d = []
        temperature_e = []
        temperature_DH = []
        humidity_a = []
        humidity_b = []
        humidity_c = []
        humidity_d = []
        humidity_DH = []
        
        for item in db.get_statistic(connection, ip, range, date_start, date_end):
            if(range == "hour"):
                dates.append(str(datetime.strptime(
                    item[13], "%Y-%m-%d %H:%M:%S.%f").replace(microsecond=0).time()))
            else:
                dates.append(str(datetime.strptime(
                    item[13], "%Y-%m-%d %H:%M:%S.%f").replace(microsecond=0)))
            temperature_a.append(item[2])
            temperature_b.append(item[3])
            temperature_c.append(item[4])
            temperature_d.append(item[5])
            temperature_e.append(item[6])
            temperature_DH.append(item[7])
            humidity_a.append(item[8])
            humidity_b.append(item[9])
            humidity_c.append(item[10])
            humidity_d.append(item[11])
            humidity_DH.append(item[12])


        data.labels = dates
        data.names = list(greenhouse_controller.get_names_map(ip).values())
        data.ip = ip
        data.greenhouses = Munch()
        data.greenhouses.temperature_a = temperature_a
        data.greenhouses.temperature_b = temperature_b
        data.greenhouses.temperature_c = temperature_c
        data.greenhouses.temperature_d = temperature_d
        data.greenhouses.temperature_e = temperature_e
        data.greenhouses.temperature_DH = temperature_DH
        data.greenhouses.humidity_a = humidity_a
        data.greenhouses.humidity_b = humidity_b
        data.greenhouses.humidity_c = humidity_c
        data.greenhouses.humidity_d = humidity_d
        data.greenhouses.humidity_DH = humidity_DH
        return data

    @cherrypy.expose
    def add_new_pump_activation_time(self, ip, start_end, day):
        greenhouse_controller.add_pump_activation_time(ip, start_end, day)
        return "200"
        

    @cherrypy.expose
    def remove_pump_activation_time(self, ip, start_end, day):
        greenhouse_controller.remove_pump_activation_time(ip, start_end, day)
        return "200"

    def good_print(self, text):
        print("========================")
        print(text)
        print("========================")

    @cherrypy.expose
    def set_new_fans_activation_temp(self, start, end, ip):
        greenhouse_controller.get_greenhouse_config(ip).set_fans(f"{start}-{end}")
        return "200"

    @cherrypy.expose
    def set_new_pump_activation_humidity(self, start, end, ip):
        greenhouse_controller.get_greenhouse_config(ip).set_pump_sensor(f"{start}-{end}")
        return "200"


@cherrypy.expose
class db_processing(object):

    @cherrypy.tools.accept(media='text/plain')
    def POST(self, ip, ghname, comment):
        connection = sqlite3.connect(BaseConstants.DB_STRING)
        data = (ip, ghname, comment)
        db.add_new_greenhouse(connection, data)
        greenhouse_controller.add_gh(ip, )
        connection.close
        return "200"

    def GET(self, ip):
        connection = sqlite3.connect(BaseConstants.DB_STRING)
        db.delete_greenhouse(connection, ip)
        greenhouse_controller.remove_gh(ip)
        connection.close
        return "200"


def shutdown():
    global statistic
    statistic.running = False
    cherrypy.engine.exit()


if __name__ == '__main__':
    config = {
        '/': {
            'tools.sessions.on': False,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/db': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'static'
        },
    }
cherrypy.config.update({'log.screen': True,
                        'server.socket_host': '0.0.0.0',
                        'log.access_file': './logs/access.txt',
                        'log.error_file': './logs/error.txt'})

signalhandler = SignalHandler(cherrypy.engine)
signalhandler.handlers['SIGINT'] = shutdown
signalhandler.subscribe()


webapp = ServerStart()
webapp.db = db_processing()
cherrypy.quickstart(webapp, '/', config)
