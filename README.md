Info
=====
This project offer greenhouse controll and monitoring functionality’s. There are using raspberry py (could be different pc) as main server, and NodeMcu with set of sensors like: DS18B20, DH22, and capacitive soil moisture sensor. This type of connections provide near to unlimited count of greenhouses to be connected.

Usage
=====
The POST request with a special code to
```http
    http://192.168.0.xxx/sensors
```

will return
```json
{
    "ip": "192.168.x.xxx",
    "sensors": {
        "temperature": {
            "DH22_temperature": {
                "val": "Нет данных",
                "change": "0"
            },
            "OneWire_a": {
                "val": "Нет данных",
                "change": "0"
            },
            "OneWire_b": {
                "val": "Нет данных",
                "change": "0"
            },
            "OneWire_c": {
                "val": "Нет данных",
                "change": "0"
            },
            "OneWire_d": {
                "val": "Нет данных",
                "change": "0"
            },
            "OneWire_e": {
                "val": "Нет данных",
                "change": "0"
            }
        },
        "humidity":{
            "DH22_humidity": {
                "val": "Нет данных",
                "change": "0"
            },
            "a": {
                "val": "Нет данных",
                "change": "0"
            },
            "b": {
                "val": "Нет данных",
                "change": "0"
            },
            "c": {
                "val": "Нет данных",
                "change": "0"
            },
            "d": {
                "val": "Нет данных",
                "change": "0"
            }

        } 
    },
    "status":{
        "fans": "No data",
        "pump": "No data",
        "lamps": "No data"
    }
}
```

Request to
```http
    http://192.168.0.xxx/peripherals
```
will return
```json
{
    "fans" : "OFF",
    "pump" : "ON",
    "lamps": "OFF"
}
```

Request to
```http
    http://192.168.0.xxx/peripherals/{peripheral}
```
will switch status of {peripheral} and return it as text ( ON / OFF )

Request to
```http
    http://192.168.0.xxx/peripherals/{peripheral}
```
with status key

will set the status of {peripheral} and return it as text ( ON / OFF )


Database
========
Server automaticaly makes request to all greenhouses every X minutes and add it data to the "Statistic" database.

Statistic
---------
```
ID | Greenhouse_ID | Air_temperature | Air_humidity | Soil_temperature | Soil_humidity
```

Greenhouse
----------
```
ID | IP | Greenhouse_ID | Comment
```
