

class Sensors_data (object):
    data = None

    def __init__(self, new_data):
        self.data = new_data
        self.set_change(new_data)
        
    
    def set_change(self, new_data):
        temp = new_data
        temp.sensors.temperature.DH22_temperature.change = self.compare(
            new_data.sensors.temperature.DH22_temperature.val, self.data.sensors.temperature.DH22_temperature.val)
        temp.sensors.temperature.OneWire_a.change = self.compare(
            new_data.sensors.temperature.OneWire_a.val, self.data.sensors.temperature.OneWire_a.val)
        temp.sensors.temperature.OneWire_b.change = self.compare(
            new_data.sensors.temperature.OneWire_b.val, self.data.sensors.temperature.OneWire_b.val)
        temp.sensors.temperature.OneWire_c.change = self.compare(
            new_data.sensors.temperature.OneWire_c.val, self.data.sensors.temperature.OneWire_c.val)
        temp.sensors.temperature.OneWire_d.change = self.compare(
            new_data.sensors.temperature.OneWire_d.val, self.data.sensors.temperature.OneWire_d.val)
        temp.sensors.temperature.OneWire_e.change = self.compare(
            new_data.sensors.temperature.OneWire_e.val, self.data.sensors.temperature.OneWire_c.val)

        temp.sensors.humidity.DH22_humidity.change = self.compare(
            new_data.sensors.humidity.DH22_humidity.val, self.data.sensors.humidity.DH22_humidity.val)
        temp.sensors.humidity.a.change = self.compare(
            new_data.sensors.humidity.a.val, self.data.sensors.humidity.a.val)
        temp.sensors.humidity.b.change = self.compare(
            new_data.sensors.humidity.b.val, self.data.sensors.humidity.b.val)
        temp.sensors.humidity.c.change = self.compare(
            new_data.sensors.humidity.c.val, self.data.sensors.humidity.c.val)
        temp.sensors.humidity.d.change = self.compare(
            new_data.sensors.humidity.d.val, self.data.sensors.humidity.d.val)
        
        self.data = temp

    def compare(self, new, old):
        if(type(new) == str or type(old) == str):
            return "0"
        if(new == None or old == None):
            return "0"
        if(new > old):
            return "UP"
        elif (new < old):
            return "DOWN"
        return "0"

    def dump(self):
        return self.data
