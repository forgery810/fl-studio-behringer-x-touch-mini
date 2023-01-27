import device
import channels
import patterns
import transport
import ui

class Leds:

	keyboard = [0x01, 0x02, 0x04, 0x05, 0x06, 0x08, 0x09, 0x0A, 0x0B, 0x0c, 0x0D, 0x0E, 0x0F]

	def light_keys():
		print('light_keys')
		for i in Leds.keyboard:
			device.midiOutMsg(0x90, 0x00, i, 0x01)

	def off():
		for i in range(0, 17):
			device.midiOutMsg(0x90, 0x00, i, 0x00)

	def light_steps(seq_mode):
		LedsMC.light_all_buttons()
		print('light_steps')
		if seq_mode == 'Pattern A':
			start = 0
			end = 16
			Leds.one_encoder_led(7, 1)
		elif seq_mode == 'Pattern B':
			start = 16
			end = 33
			Leds.all_one_knob(7)
		
		for c, i in enumerate(range(start, end)):
			if channels.getGridBit(channels.selectedChannel(), i) == 1:
				device.midiOutMsg(0x90, 0x00, c, 0x01)
			else:
				device.midiOutMsg(0x90, 0x00, c, 0x00)

	def all_one_knob(knob_num):
		 device.midiOutMsg(0xB0, 0x00, 8 + knob_num, 27) # Light Knob 7 led 4

	def one_encoder_led(knob_num, led_num):
		device.midiOutMsg(0xB0, 0x00, 8 + knob_num, led_num)

	def light_transport():
		print('light_transport')
		if transport.isRecording():
			device.midiOutMsg(0x90, 0x00, 0x0F, 1)
		if ui.isLoopRecEnabled():
			device.midiOutMsg(0x90, 0x00, 0x0C, 1)
		else:
			device.midiOutMsg(0x90, 0x00, 0x0C, 0)
		if transport.isPlaying():
			device.midiOutMsg(0x90, 0x00, 0x0E, 1)
			device.midiOutMsg(0x90, 0x00, 0x0D, 0)
		else:
			device.midiOutMsg(0x90, 0x00, 0x0E, 0)
			device.midiOutMsg(0x90, 0x00, 0x0D, 1)

	def light_b():
		device.midiOutMsg(0x90, 0x00, 0x21, 0x01) # Lights button 16
	# device.midiOutMsg(176, 0, 15, 2)
	# device.midiOutMsg(0xC0, 0x00, 0x09, 0x05)

# Buttons
	# device.midiOutMsg(0x90, 0x00, 0x0F, 0x01) # Lights button 16
# midiId = 0x90
# channel = 0x00
# velocity
# 0 - off
# 1 - on 
# 2 - blinking 



# Knobs
	# device.midiOutMsg(0xB0, 0x00, 0x0F, 0x04) # Light Knob 7 led 4
# velcity
# all_off = 0x00
# 1-13 = indiviual leds
# 14-26 - blinking
# 27 all_on
# 28 - all blinking

	# device.midiOutMsg(0xB0, 0x00, 0x7F, 0x00) # Standard Mode
	# device.midiOutMsg(0xB0, 0x00, 0x7F, 0x01) # MC Mode


		# device.midiOutMsg(0xC0, 0x00, 0x00, 0x00) layer a
			# device.midiOutMsg(0xC0, 0x00, 0x01, 0x00) layer b 

	# device.midiOutMsg(0xC0, 0x00, 0x00, 0x00)
	# device.midiOutMsg(176, 0, 15, 2)
	# device.midiOutMsg(0xC0, 0x00, 0x09, 0x05)
	# device.midiOutMsg(0x90, 0x00, 0x0F, 0x01) # Lights button 16
	# device.midiOutMsg(0xB0, 0x00, 0x0F, 0x04) # Light Knob 7 led 4
	# device.midiOutMsg(0xB0, 0x00, 0x7F, 0x00) # Standard Mode
	# device.midiOutMsg(0xB0, 0x00, 0x7F, 0x01) # MC Mode



class LedsMC:

	buttons = [0x59, 0x5A, 0x28, 0x29, 0x2A, 0x2B, 0x2C, 0x2D,  0x57, 0x58, 0x5B, 0x5C, 0x56, 0x5D, 0x5E, 0x5F]

	def light_all_buttons():
		for i in LedsMC.buttons:
			device.midiOutMsg(0x90, 0x00, i, 127)