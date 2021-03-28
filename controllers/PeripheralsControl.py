import time
import schedule
from networker import Networker

networker = Networker()


class PeripheralsControl(object):

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(PeripheralsControl, cls).__new__(cls)
        return cls.instance
        
    def add_pump_activation_time_by_day(self, ip, start_end, day):
        start, end = start_end.split("-", 1)
        if(day == "Monday"):
            schedule.every().monday.at(start).do(self.run_pump, ip).tag(f'{ip}-{day}-{start}-{end}', 'monday', ip)
            schedule.every().monday.at(end).do(self.stop_pump, ip).tag(f'{ip}-{day}-{start}-{end}', 'monday', ip)
        if(day == "Tuesday"):
            schedule.every().tuesday.at(start).do(self.run_pump, ip).tag(f'{ip}-{day}-{start}-{end}', 'tuesday', ip)
            schedule.every().tuesday.at(end).do(self.stop_pump, ip).tag(f'{ip}-{day}-{start}-{end}', 'tuesday', ip)
        if(day == "Wednesday"):
            schedule.every().wednesday.at(start).do(self.run_pump, ip).tag(f'{ip}-{day}-{start}-{end}', 'wednesday', ip)
            schedule.every().wednesday.at(end).do(self.stop_pump, ip).tag(f'{ip}-{day}-{start}-{end}', 'wednesday', ip)
        if(day == "Thursday"):
            schedule.every().thursday.at(start).do(self.run_pump, ip).tag(f'{ip}-{day}-{start}-{end}', 'thursday', ip)
            schedule.every().thursday.at(end).do(self.stop_pump, ip).tag(f'{ip}-{day}-{start}-{end}', 'thursday', ip)
        if(day == "Friday"):
            schedule.every().friday.at(start).do(self.run_pump, ip).tag(f'{ip}-{day}-{start}-{end}', 'friday', ip)
            schedule.every().friday.at(end).do(self.stop_pump, ip).tag(f'{ip}-{day}-{start}-{end}', 'friday', ip)
        if(day == "Saturday"):
            schedule.every().saturday.at(start).do(self.run_pump, ip).tag(f'{ip}-{day}-{start}-{end}', 'saturday', ip)
            schedule.every().saturday.at(end).do(self.stop_pump, ip).tag(f'{ip}-{day}-{start}-{end}', 'saturday', ip)
        if(day == "Sunday"):
            schedule.every().sunday.at(start).do(self.run_pump, ip).tag(f'{ip}-{day}-{start}-{end}', 'sunday', ip)
            schedule.every().sunday.at(end).do(self.stop_pump, ip).tag(f'{ip}-{day}-{start}-{end}', 'sunday', ip)
        print(f"Pump activation on {day} in {start_end} was added!")
    
    def remove_pump_activation_time(self, ip, start_end, day):
        start, end = start_end.split("-", 1)
        tag = f"{ip}-{day}-{start}-{end}"
        schedule.clear(tag)
        print(f"Time on {day} at {start}-{end} in {ip} was removed.")

    def cancel_all_job(self, ip):
        schedule.clear(ip)
        print(f"All jobs for {ip} was canceled!")

    def run_pump(self, ip):
        networker.set_peripheral_status(ip, "pump", "ON")
        print(f'Pump is running on {ip}')

    def stop_pump(self, ip):
        networker.set_peripheral_status(ip, "pump", "OFF")
        print(f'Pump is stoped on {ip}')

    def run_fans(self, ip):
        networker.set_peripheral_status(ip, "fans", "ON")
        print(f'Fans is running on {ip}')

    def stop_fans(self, ip):
        networker.set_peripheral_status(ip, "fans", "OFF")
        print(f'Fans is stoped on {ip}')

