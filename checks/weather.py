import requests
import json

class Task:

    def __init__(self, settings):
        self.SETTINGS = settings
        self.TIME     = ["morning", "night"]

        self.ICE        = (34511, 11796, 22937, 2500)
        self.LIGHT_BLUE = (37991, 32767, 22937, 2500)
        self.BLUE       = (45292, 59636, 22937, 2500)
        self.YELLOW     = (6004, 22281, 22937, 2500)
        self.ORANGE     = (3340, 45874, 22937, 2500)
        self.RED        = (226, 63568, 22937, 2500)

    def get_current_bedford_weather(self):
        url = "http://api.apixu.com/v1/current.json?key=1b99c03e5bef42528bb01428172905&q=Bedford, NH"
        return json.loads(requests.get(url).text)

    def get_current_temp(self):
        return self.get_current_bedford_weather()['current']['temp_f']

    def get_tomorrow_bedford_weather(self):
        url = "http://api.apixu.com/v1/forecast.json?key=1b99c03e5bef42528bb01428172905&q=Bedford, NH&days=2"
        return json.loads(requests.get(url).text)['forecast']['forecastday'][1]

    def get_tomorrow_temp(self):
        return self.get_tomorrow_bedford_weather()['day']['avgtemp_f']

    def main(self, lifx):
        if self.SETTINGS['time'] == "morning":
            temp = self.get_current_temp(sel)
        elif self.SETTINGS['time'] == "night":
            temp = self.get_tomorrow_temp()

        print "Setting weather color: " + str(temp) + " degrees"

        if temp < 32:
            lifx.set_color(self.BLUE)
            return
        if temp < 40:
            lifx.set_color(self.LIGHT_BLUE)
            return
        if temp < 55:
            lifx.set_color(self.ICE)
            return
        if temp < 60:
            lifx.set_color(self.YELLOW)
            return
        if temp < 80:
            lifx.set_color(self.ORANGE)
            return
        else:
            lifx.set_color(self.RED)
            return

        return

