#Other
SECRET_KEY = "8Synbt9N7p5yttx8"

# HTML
INDEX = "index.html"
GREENHOUSE = "greenhouse.html"
SETTINGS = "settings.html"
STATISTIC = "statistic.html"
HELP = "help.html"

# JSON
CONFIG = "./configs/config.json"
NO_CONNECTION = "./configs/no_connection.json"


# DB
DB_STRING = "./DB/GreenhouseControl.db"

sql_create_greenhouse_table = """ CREATE TABLE IF NOT EXISTS Greenhouses (
                                        id	integer,
                                        ip	text NOT NULL UNIQUE,
                                        name	text,
                                        comment	text,
                                        PRIMARY KEY(id AUTOINCREMENT)
                                    ); """
sql_create_statistic_table = """ CREATE TABLE IF NOT EXISTS Statistic (
                                        id integer,
                                        greenhouse_id text NOT NULL,
                                        air_temperature integer,
                                        air_humidity integer,
                                        soil_temperature integer,
                                        soil_humidity integer,
                                        date timestamp,
                                        PRIMARY KEY(id AUTOINCREMENT)
                                    ); """
