from lifxlan import LifxLAN, Light
from lifxlan import ORANGE, RED, GOLD, COLD_WHITE, WARM_WHITE
import json


class Lifx:

    def __init__(self, no_blink=False):
        light_macs = json.load(open('light_macs.json', 'r')).get('lights')
        lan = LifxLAN()

        if light_macs is None:
            self.lights = lan.get_lights()
        else:
            self.lights = filter(lambda x: x.mac_addr in [mac['mac'] for mac in light_macs], lan.get_lights())

        self.prev_light_power_color = self.store_power_color()
        if not no_blink:
            print "Blink lights"

            for light in self.lights:
                power = light.get_power()
                light.set_power(0)
                light.set_power(power)

    def store_power_color(self):
        self.prev_light_power_color = [{'power': light.get_power(), 'color': light.get_color()} for light in self.lights]

    def restore_power_color(self):
        n = len(self.lights)
        for i in range(0, n):
            self.lights[i].set_power(self.prev_light_power_color[i]['power'])
            self.lights[i].set_color(self.prev_light_power_color[i]['color'])

    def set_power(self, power, duration=0):
        map(lambda x: x.set_power(power, duration), self.lights)

    def set_color(self, color):
        map(lambda x: x.set_color(color), self.lights)

    def alarm(self, n=5):
        print "Lifx Alarm"
        self.store_power_color()
        self.set_color((33, 55049, 19660, 2500))

        for i in range(0, n):
            self.set_power(0)
            self.set_power(1)

        self.restore_power_color()

    def turn_on(self):
        print "Lifx turn on"
        self.set_color((11499, 655, 22937, 2500))
        self.set_power(65535)

    def turn_off(self):
        print "Lifx turn off"
        self.set_power(0)








if __name__ == "__main__":
    lifx = Lifx()
    import pdb; pdb.set_trace()
