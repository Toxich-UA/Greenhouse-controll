from jsonprocessor import json2obj

class SensorsDataViewModel(object):

    def __init__(self):
        pass


    sensors = json2obj({
        "temperature_a": {
            "val": 0,
            "change": "NONE"
        },
        "temperature_b": {
            "val": 0,
            "change": "NONE"
        },
        "temperature_c": {
            "val": 0,
            "change": "NONE"
        },
        "temperature_d": {
            "val": 0,
            "change": "NONE"
        },
        "temperature_e": {
            "val": 0,
            "change": "NONE"
        },
        "temperature_DH": {
            "val": 0,
            "change": "NONE"
        },
        "humidity_a": {
            "val": 0,
            "change": "NONE"
        },
        "humidity_b": {
            "val": 0,
            "change": "NONE"
        },
        "humidity_c": {
            "val": 0,
            "change": "NONE"
        },
        "humidity_d": {
            "val": 0,
            "change": "NONE"
        },
        "humidity_DH": {
            "val": 0,
            "change": "NONE"
        },
    })

    sensors_map = json2obj({
        "temperature_a": "OneWire_a",
        "temperature_b": "OneWire_b",
        "temperature_c": "OneWire_c",
        "temperature_d": "OneWire_d",
        "temperature_e": "OneWire_e",
        "temperature_DH": "DH22_temperature",
        "humidity_a": "a",
        "humidity_b": "b",
        "humidity_c": "c",
        "humidity_d": "d",
        "humidity_DH": "DH22_humidity",
    })

    names_map = json2obj({
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
    })
    peripherals = json2obj({
        "fans": "Нет данных",
        "pump": "Нет данных",
        "lamps": "Нет данных",
    })
