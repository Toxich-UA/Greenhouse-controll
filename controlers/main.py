import cherrypy
import os
import BaseConstants
from datetime import date, datetime
from munch import Munch
from dbworker import DBWorker
import sqlite3
import jsonprocessor as json
import json as js
from StatisticController import StatisticController as SC
from cherrypy.process.plugins import SignalHandler
import threading as th
from sensors_data import Sensors_data 
from networker import Networker
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('src'))
db = DBWorker()
networker = Networker()
statistic = None

fans_control_mode = True
pump_control_mode = True
lamps_control_mode = True


class ServerStart(object):

    def __init__(self):
        pass
        global statistic

        statistic = SC()
        statistic_method_thread = th.Timer(5.0, statistic.start_statistic_module)
        statistic_method_thread.start()

    @cherrypy.expose
    def index(self):
        tmpl = env.get_template(BaseConstants.INDEX)
        config = json.json2obj(open(BaseConstants.CONFIG).read())

        sensors = None
        peripherals = None

        connection = sqlite3.connect(BaseConstants.DB_STRING)
        greengouses = db.get_all_greenhouses(connection)
        connection.close
        for index, gh in enumerate(greengouses):
            gh = list(gh)
            sensors = statistic.get_sensors_data(gh[1])
            peripherals = json.json2obj(statistic.get_sensors_status(gh[1]))
            peripherals.fans = "ON" if peripherals.fans else "OFF"
            peripherals.pump = "ON" if peripherals.pump else "OFF"
            peripherals.lamps = "ON" if peripherals.lamps else "OFF"

            gh.append(sensors)
            gh.append(peripherals)
            greengouses[index] = gh

        return tmpl.render(gh=greengouses, peripheral=peripherals, config=config)

    @cherrypy.expose
    def greenhouse(self, ip):
        tmpl = env.get_template(BaseConstants.GREENHOUSE)
        ghConfig = json.json2obj(
            open("./configs/greenhouseConfig.json").read())
        config = json.json2obj(open(BaseConstants.CONFIG).read()).names

        connection = sqlite3.connect(BaseConstants.DB_STRING)
        data = db.get_greenhouse(connection, ip)
        connection.close
        sensors = statistic.get_sensors_data(ip)

        controls = json.json2obj(self.get_peripherals_status(ip))
        return tmpl.render(data=data, sensors=sensors, ghConfig=ghConfig, config=config, controls=controls)

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
    def status(self, ip):
        return json.dump(statistic.get_sensors_data(ip))

    @cherrypy.expose
    def toggle_fans(self, ip):
        data = networker.toggle_fans(ip)
        return data

    @cherrypy.expose
    def toggle_lamps(self, ip):
        data = networker.toggle_lamps(ip)
        return data

    @cherrypy.expose
    def toggle_pump(self, ip):
        data = networker.toggle_pump(ip)
        return data

    @cherrypy.expose
    def get_peripherals_status(self, ip):
        data = json.json2obj(networker.get_peripherals_status(ip))
        data.fans_control_mode = fans_control_mode
        data.pump_control_mode = pump_control_mode
        data.lamps_control_mode = lamps_control_mode
        return json.dump(data)

    @cherrypy.expose
    def set_control_mode(self, peripheral, status):
        global fans_control_mode
        global pump_control_mode
        global lamps_control_mode

        if (peripheral == "fans"):
            fans_control_mode = True if status == "true" else False
        if (peripheral == "pump"):
            pump_control_mode = True if status == "true" else False
        if (peripheral == "lamps"):
            lamps_control_mode = True if status == "true" else False

        return "200"

    @cherrypy.expose
    def get_logged_statistic_for_hour(self):
        connection = sqlite3.connect(BaseConstants.DB_STRING)
        greenhouses_data = db.get_all_greenhouses(connection)
        data = self.transform_data_from_db(connection, greenhouses_data, "hour")
        connection.close
        return json.dump(data)

    @cherrypy.expose
    def get_logged_statistic_for_day(self):
        connection = sqlite3.connect(BaseConstants.DB_STRING)
        greenhouses_data = db.get_all_greenhouses(connection)
        data = self.transform_data_from_db(connection, greenhouses_data, "day")
        connection.close
        return json.dump(data)


    def transform_data_from_db(self, connection, greenhouses_data, range):
        counter = 0
        data = Munch()
        dates = []
        air_temperature = []
        air_humidity = []
        soil_temperature = []
        soil_humidity = []
        for gh in greenhouses_data:
            ip = gh[1]
            for d in db.get_statistic(connection, ip, range):
                if (range == "day" and counter == 1):
                    counter = 0
                    continue
                dates.append(str(datetime.strptime(d[6], "%Y-%m-%d %H:%M:%S.%f").replace(microsecond=0)))
                air_temperature.append(d[2])
                air_humidity.append(d[3])
                soil_temperature.append(d[4])
                soil_humidity.append(d[5])
                counter = counter + 1
            
            data.labels = dates
            data.ip = gh[1]
            data.greenhouses = Munch()
            data.greenhouses.data = Munch()
            data.greenhouses.data.air_temperature = air_temperature
            data.greenhouses.data.air_humidity = air_humidity
            data.greenhouses.data.soil_temperature = soil_temperature
            data.greenhouses.data.soil_humidity = soil_humidity
        return data


    @cherrypy.expose
    def add_new_pump_activation_time(self, day, start, end):
        data = json.json2obj(open("./configs/greenhouseConfig.json").read())
        data.pump[day].append("{0}-{1}".format(start, end))

        with open("./configs/greenhouseConfig.json", 'w') as outfile:
            js.dump(data, outfile)
        return "200"


    def good_print(self, text):
        print("========================")
        print(text)
        print("========================")

    
@cherrypy.expose
class db_processing(object):

    @cherrypy.tools.accept(media='text/plain')
    def POST(self, ip, ghname, comment):
        global statistic
        connection = sqlite3.connect(BaseConstants.DB_STRING)
        data = (ip, ghname, comment)
        db.add_new_greenhouse(connection, data)
        connection.close
        statistic.running = False
        statistic = SC()
        return "200"

    def GET(self, ip):
        connection = sqlite3.connect(BaseConstants.DB_STRING)
        db.delete_greenhouse(connection, ip)
        connection.close
        return "200"

def shutdown(): 
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
cherrypy.config.update({'log.screen': False,
                        'server.socket_host': '0.0.0.0',
                        'log.access_file': './logs/access.txt',
                        'log.error_file': './logs/error.txt'})

signalhandler = SignalHandler(cherrypy.engine)
signalhandler.handlers['SIGTERM'] = shutdown
signalhandler.handlers['SIGHUP'] = shutdown
signalhandler.handlers['SIGQUIT'] = shutdown
signalhandler.handlers['SIGINT'] = shutdown
signalhandler.subscribe()



webapp = ServerStart()
webapp.db = db_processing()
cherrypy.quickstart(webapp, '/', config)

