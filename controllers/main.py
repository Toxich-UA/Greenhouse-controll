import cherrypy
import os
import BaseConstants
from datetime import datetime
from munch import Munch
from InterfaceViewModel import InterfaceViewModel
from dbworker import DBWorker
from PeripheralsControl import PeripheralsControl
import sqlite3
import jsonprocessor as json
import json as js
from StatisticController import StatisticController as SC
from cherrypy.process.plugins import SignalHandler
import threading as th
from networker import Networker
from jinja2 import Environment, FileSystemLoader


env = Environment(loader=FileSystemLoader('src'))
db = DBWorker()
networker = Networker()
peripheral_control = PeripheralsControl()
statistic = None
interface_view_model = None

fans_control_mode = True
pump_control_mode = True
lamps_control_mode = True


class ServerStart(object):

    def __init__(self):
        global statistic
        global interface_view_model
        connection = sqlite3.connect(BaseConstants.DB_STRING)
        greengouses = db.get_all_greenhouses(connection)
        for gh in greengouses:
            ip = gh[1]
            create_greenhouse_config_file(ip)
            with open("./configs/{}_Config.json".format(ip), 'r') as outfile:
                data = json.json2obj(outfile.read())
                for day in data.pump:
                    for time in data.pump[day]:
                        start, end = time.split("-", 1)
                        peripheral_control.set_pump_activation_time_by_day(
                            day, start, end, ip)
        statistic = SC()
        statistic_method_thread = th.Timer(
            5.0, statistic.start_statistic_module)
        statistic_method_thread.start()
        interface_view_model = InterfaceViewModel()

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
            sensors = interface_view_model.get_sensors(gh[1])
            peripherals = json.json2obj(statistic.get_sensors_status(gh[1]))
            peripherals.fans = "ON" if peripherals.fans == 1 else "OFF"
            peripherals.pump = "ON" if peripherals.pump == 1 else "OFF"
            peripherals.lamps = "ON" if peripherals.lamps == 1 else "OFF"
            gh.append(sensors)
            gh.append(peripherals)
            greengouses[index] = gh
        return tmpl.render(gh=greengouses, config=config)

    @cherrypy.expose
    def greenhouse(self, ip):
        tmpl = env.get_template(BaseConstants.GREENHOUSE)
        with open("./configs/{}_Config.json".format(ip), 'r') as outfile:
            ghConfig = json.json2obj(outfile.read())

        config = json.json2obj(open(BaseConstants.CONFIG).read()).names

        connection = sqlite3.connect(BaseConstants.DB_STRING)
        data = db.get_greenhouse(connection, ip)
        connection.close
        sensors = interface_view_model.get_sensors(ip)
        names = interface_view_model.get_names(ip)

        controls = json.json2obj(self.get_peripherals_status(ip))
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
        names = interface_view_model.get_names(ip).items()
        sensors = interface_view_model.get_sensors_map(ip).items()
        return tmpl.render(names=names, sensors=sensors)

    @cherrypy.expose
    def update_greenhouse_names_and_sensors(self, ip, names, sensors_map):
        interface_view_model.set_names_map(ip, js.loads(names))
        interface_view_model.set_sensors_map(ip, js.loads(sensors_map))

        return "200"

    # REST api links
    @cherrypy.expose
    def status(self, ip):
        data = json.dump(interface_view_model.get_sensors(ip))
        return data

    @cherrypy.expose
    def toggle_peripheral_status(self, ip, peripheral):
        data = networker.toggle_peripheral_status(ip, peripheral)
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
    def get_logged_statistic(self, ip, range):
        connection = sqlite3.connect(BaseConstants.DB_STRING)
        data = self.transform_data_from_db(connection, ip, range)
        connection.close
        return json.dump(data)

    def transform_data_from_db(self, connection, ip, range):
        counter = 0
        data = Munch()
        dates = []
        air_temperature = []
        air_humidity = []
        soil_temperature = []
        soil_humidity = []
        for item in db.get_statistic(connection, ip, range):
            if (range == "day" and counter == 1):
                counter = 0
                continue
            if(range == "hour"):
                dates.append(str(datetime.strptime(
                    item[6], "%Y-%m-%d %H:%M:%S.%f").replace(microsecond=0).time()))
            else:
                dates.append(str(datetime.strptime(
                    item[6], "%Y-%m-%d %H:%M:%S.%f").replace(microsecond=0)))

            air_temperature.append(item[2])
            air_humidity.append(item[3])
            soil_temperature.append(item[4])
            soil_humidity.append(item[5])
            counter = counter + 1

            data.labels = dates
            data.ip = ip
            data.greenhouses = Munch()
            data.greenhouses.air_temperature = air_temperature
            data.greenhouses.air_humidity = air_humidity
            data.greenhouses.soil_temperature = soil_temperature
            data.greenhouses.soil_humidity = soil_humidity
        return data

    @cherrypy.expose
    def add_new_pump_activation_time(self, day, start, end, ip):
        with open("./configs/{}_Config.json".format(ip), 'r') as outfile:
            data = json.json2obj(outfile.read())
            data.pump[day].append("{0}-{1}".format(start, end))
        with open("./configs/{}_Config.json".format(ip), 'w') as outfile:
            js.dump(data, outfile, indent=4, ensure_ascii=False)
        peripheral_control.set_pump_activation_time_by_day(ip, start, end, day)
        return "200"

    @cherrypy.expose
    def remove_pump_activation_time(self, day, start, end, ip):
        with open("./configs/{}_Config.json".format(ip), 'r') as outfile:
            data = json.json2obj(outfile.read())
            data.pump[day].remove("{0}-{1}".format(start, end))
        with open("./configs/{}_Config.json".format(ip), 'w') as outfile:
            js.dump(data, outfile, indent=4, ensure_ascii=False)
        peripheral_control.remove_pump_activation_time(day, start, end, ip)
        return "200"

    def good_print(self, text):
        print("========================")
        print(text)
        print("========================")

    @cherrypy.expose
    def set_new_fans_activation_time(self, start, end, ip):
        with open("./configs/{}_Config.json".format(ip), 'r+') as outfile:
            data = json.json2obj(outfile.read())
            data.fans = "{0}-{1}".format(start, end)
            outfile.seek(0)
            js.dump(data, outfile, indent=4, ensure_ascii=False)
        return "200"


@cherrypy.expose
class db_processing(object):

    @cherrypy.tools.accept(media='text/plain')
    def POST(self, ip, ghname, comment):
        global statistic
        connection = sqlite3.connect(BaseConstants.DB_STRING)
        data = (ip, ghname, comment)
        db.add_new_greenhouse(connection, data)
        statistic.add(ip)
        interface_view_model.add(ip)
        create_greenhouse_config_file(ip)
        connection.close
        return "200"

    def GET(self, ip):
        connection = sqlite3.connect(BaseConstants.DB_STRING)
        db.delete_greenhouse(connection, ip)
        connection.close
        statistic.remove(ip)
        interface_view_model.remove(ip)
        os.remove("./configs/{}_Config.json".format(ip))
        return "200"


def create_greenhouse_config_file(ip):
    error = False
    try:
        open("./configs/{}_Config.json".format(ip), "x")
    except:
        error = True
    if(not error):
        f = open("./configs/{}_Config.json".format(ip), "w+")
        f.write(open("./configs/greenhouseConfig.json", "r").read())
        f.close()


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
cherrypy.config.update({'log.screen': True,
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
