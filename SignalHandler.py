import json
from lifx import Lifx
from scapy.all import *
from datetime import datetime

class SignalHandler:

    def __init__(self):
        self.lifx = Lifx()
        self.macs = json.load(open("known_macs.json",'r'))['macs']
        self.recent_macs = []

    def is_mac_recent(self, mac_addr):
        return mac_addr in [mac['mac'] for mac in self.recent_macs]

    def clear_recent(self):
        self.recent_macs = []

    def clear_older_than(self, minutes):
        now = datetime.now().strftime('%s')
        temp = self.recent_macs
        for mac in temp:
            if int(now) - int(mac['time']) > minutes:
                self.remove_from_recent(mac['mac'])

    def add_to_recent(self, mac):
        if str(mac['mac']) not in [str(rmac['mac']) for rmac in self.recent_macs]:
            data = {
                "time": datetime.now().strftime('%s')
            }
            data.update(mac)
            self.recent_macs.append(data)

    def remove_from_recent(self, mac_addr):
        for i in range(0, len(self.recent_macs)):
            if mac_addr == self.recent_macs[i]:
                self.recent_macs = self.recent_macs[:i] + self.recent_macs[i+1:]
                break

    def handle_packet(self, pkt):
        if pkt[Dot11] is not None:
            this_device = None
            appear_action = None
            response = None

            for mac in self.macs:
                if mac['mac'] == pkt[Dot11].addr2:
                    this_device = mac['device']
                    appear_action = mac.get('appear_action')
                    disappear_action = mac.get('disappear_action')


                    break

            if this_device is None:
                return response

            if pkt[Dot11].subtype == 4L and pkt[Dot11].addr1 == "ff:ff:ff:ff:ff:ff": # Broadcast
                if appear_action == "alert" and not self.is_mac_recent(mac['mac']):
                    self.lifx.alarm()
                    self.add_to_recent(mac)
                if appear_action == "light_on" and not self.is_mac_recent(mac['mac']):
                    self.lifx.turn_on()
                    self.add_to_recent(mac)
                response = this_device + " is detected. Strength: " + str(-(256 - ord(pkt.notdecoded[-2:-1])))

            if pkt[Dot11].subtype == 10L: # Deauthenticate
                if disappear_action == "light_off":
                    self.remove_from_recent(mac['mac'])
                    self.lifx.turn_off()

            	response = this_device + " is disconnecting from a network..."
            # if pkt[Dot11].subtype == 11L: #
            # 	return this_device + " is here. Strength: " + str(-(256 - ord(pkt.notdecoded[-2:-1])))


        return response
