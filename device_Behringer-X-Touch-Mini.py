# name=Behringer X-Touch Mini
# Author: ts-forgery
# Version 0.01

import device
import channels
import midi

def OnInit():
	"""Function called when script starts"""
	if device.isAssigned():					
		print(device.getName())
		print(f"Port Number: {device.getPortNumber()}")
	else:
		print("Not assigned")

def  OnMidiMsg(event):
	"""Function called on every midi message sent by controller"""

	print(event.midiId, event.data1, event.data2, event.midiChan, event.midiChanEx)