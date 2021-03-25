SECRET_KEY = "8Synbt9N7p5yttx8"

# HTML
INDEX = "index.html"
GREENHOUSE = "greenhouse.html"
SETTINGS = "settings.html"
STATISTIC = "statistic.html"
HELP = "help.html"

GH_CONFIG = "greenhouseSettings.html"


# JSON
CONFIG = '{"peripherals": {"pump_time": {"Monday": [],"Tuesday": [],"Wednesday": [],"Thursday": [],"Friday": [],"Saturday": [],"Sunday": []},"pump_sensor": "","fans": ""},"names_map": {"temperature_a": "Датчик температуры 1","temperature_b": "Датчик температуры 2","temperature_c": "Датчик температуры 3","temperature_d": "Датчик температуры 4","temperature_e": "Датчик температуры 5","temperature_DH": "Датчик температуры 6","humidity_a": "Датчик влажности 1","humidity_b": "Датчик влажности 2","humidity_c": "Датчик влажности 3","humidity_d": "Датчик влажности 4","humidity_DH": "Датчик влажности 5"},"sensors_map": {"temperature_a": "OneWire_a","temperature_b": "OneWire_b","temperature_c": "OneWire_c","temperature_d": "OneWire_d","temperature_e": "OneWire_e","temperature_DH": "DH22_temperature","humidity_a": "a","humidity_b": "b","humidity_c": "c","humidity_d": "d","humidity_DH": "DH22_humidity"}}'
NO_CONNECTION = '{"ip": "192.168.x.xxx","sensors": {"temperature": {"DH22_temperature": {"val": "Нет данных","change": "0"},"OneWire_a": {"val": "Нет данных","change": "0"},"OneWire_b": {"val": "Нет данных","change": "0"},"OneWire_c": {"val": "Нет данных","change": "0"},"OneWire_d": {"val": "Нет данных","change": "0"},"OneWire_e": {"val": "Нет данных","change": "0"}},"humidity":{"DH22_humidity": {"val": "Нет данных","change": "0"},"a": {"val": "Нет данных","change": "0"},"b": {"val": "Нет данных","change": "0"},"c": {"val": "Нет данных","change": "0"},"d": {"val": "Нет данных","change": "0"}}},"status":{"fans": "Нет данных","pump": "Нет данных","lamps": "Нет данных"}}'
BASE_GH_CONFIG_PATH = "./configs/{}_config.json"


# DB
DB_STRING = "./DB/GreenhouseControl.db"

sql_create_greenhouse_table = """ CREATE TABLE IF NOT EXISTS Greenhouses (
                                        id	integer,
                                        ip	text NOT NULL UNIQUE,
                                        name	text,
                                        comment	text,
                                        PRIMARY KEY(id AUTOINCREMENT)
                                    ); """
sql_create_statistic_table = """ CREATE TABLE IF NOT EXISTS "Statistic" (
                                    "id"	integer,
                                    "greenhouse_id"	text NOT NULL,
                                    "temperature_a"	INTEGER,
                                    "temperature_b"	INTEGER,
                                    "temperature_c"	INTEGER,
                                    "temperature_d"	INTEGER,
                                    "temperature_e"	INTEGER,
                                    "temperature_DH"	INTEGER,
                                    "humidity_a"	INTEGER,
                                    "humidity_b"	INTEGER,
                                    "humidity_c"	INTEGER,
                                    "humidity_d"	INTEGER,
                                    "humidity_DH"	INTEGER,
                                    "date"	timestamp,
                                    PRIMARY KEY("id" AUTOINCREMENT)
                                ); """
