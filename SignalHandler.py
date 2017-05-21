import json
from scapy.all import *

class SignalHandler:

    def __init__(self):
        self.macs = json.load(open("known_macs.json",'r'))['macs']

    def handle_packet(self, pkt):
        if pkt[Dot11] is not None:
            this_device = None

            for mac in self.macs:
                if mac['mac'] == pkt[Dot11].addr2:
                    this_device = mac['device']
                    break

            if this_device is None:
                return

            if pkt[Dot11].subtype == 4L and pkt[Dot11].addr1 == "ff:ff:ff:ff:ff:ff": # Broadcast
            	return this_device + " is detected. Strength: " + str(-(256 - ord(pkt.notdecoded[-2:-1])))
            if pkt[Dot11].subtype == 10L: # Deauthenticate
            	return this_device + " is disconnecting from a network..."
            if pkt[Dot11].subtype == 11L: #
            	return this_device + " is here. Strength: " + str(-(256 - ord(pkt.notdecoded[-2:-1])))
        return
