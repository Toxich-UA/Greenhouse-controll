

class Sensors_data (object):
    data = None

    def __init__(self, new_data):
        self.data = new_data
        self.set_change(new_data)
        
    
    def set_change(self, new_data):
        temp = new_data

        temp.sensors.air.temperature.a.change = self.compare(
            new_data.sensors.air.temperature.a.val, self.data.sensors.air.temperature.a.val)
        temp.sensors.air.temperature.b.change = self.compare(
            new_data.sensors.air.temperature.b.val, self.data.sensors.air.temperature.b.val)
        temp.sensors.air.temperature.c.change = self.compare(
            new_data.sensors.air.temperature.c.val, self.data.sensors.air.temperature.c.val)
        temp.sensors.air.humidity.change = self.compare(
            new_data.sensors.air.humidity.val, self.data.sensors.air.humidity.val)

        temp.sensors.soil.humidity.a.change = self.compare(
            new_data.sensors.soil.humidity.a.val, self.data.sensors.soil.humidity.a.val)
        temp.sensors.soil.humidity.b.change = self.compare(
            new_data.sensors.soil.humidity.b.val, self.data.sensors.soil.humidity.b.val)
        temp.sensors.soil.humidity.c.change = self.compare(
            new_data.sensors.soil.humidity.c.val, self.data.sensors.soil.humidity.c.val)
        temp.sensors.soil.temperature.change = self.compare(
            new_data.sensors.soil.temperature.val, self.data.sensors.soil.temperature.val)
        
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
