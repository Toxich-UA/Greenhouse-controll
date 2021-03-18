

class InterfaceSensorsData(object):

    def __init__(self, ip):
        pass

    sensors = {
        "temperature_a": 0,
        "temperature_b": 0,
        "temperature_c": 0,
        "temperature_d": 0,
        "temperature_e": 0,
        "temperature_DH": 0,
        "humidity_a": 0,
        "humidity_b": 0,
        "humidity_c": 0,
        "humidity_d": 0,
        "humidity_DH": 0,
    }

    sensors_map = {
        "temperature_a": "DH22_temperature",
        "temperature_b": "OneWire_a",
        "temperature_c": "OneWire_b",
        "temperature_d": "OneWire_c",
        "temperature_e": "OneWire_d",
        "temperature_DH": "OneWire_e",
        "humidity_a": "DH22_humidity",
        "humidity_b": "a",
        "humidity_c": "b",
        "humidity_d": "c",
        "humidity_DH": "d",
    }

    names_map = {
        "temperature_a": "Датчик температуры 1",
        "temperature_b": "Датчик температуры 2",
        "temperature_c": "Датчик температуры 3",
        "temperature_d": "Датчик температуры 4",
        "temperature_e": "Датчик температуры 5",
        "temperature_DH": "Датчик температуры 6",
        "humidity_a": "Датчик влажности 1",
        "humidity_b": "Датчик влажности 2",
        "humidity_c": "Датчик влажности 3",
        "humidity_d": "Датчик влажности 4",
        "humidity_DH": "Датчик влажности 5",
    }
