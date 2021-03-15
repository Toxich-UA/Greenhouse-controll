# Other
SECRET_KEY = "8Synbt9N7p5yttx8"

# HTML
INDEX = "index.html"
GREENHOUSE = "greenhouse.html"
SETTINGS = "settings.html"
STATISTIC = "statistic.html"
HELP = "help.html"
GH_CONFIG = "greenhouseSettings.html"

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
