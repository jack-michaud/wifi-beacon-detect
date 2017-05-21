
from scapy.all import *
from SignalHandler import SignalHandler

sig = SignalHandler()

def detect(pkt):
	response = sig.handle_packet(pkt)
	if response is not None:
		print response

sniff(prn=detect, iface="mon0")
