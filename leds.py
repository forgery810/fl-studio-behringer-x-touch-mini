import device
import channels
import patterns
import transport
import ui

class LedsMC:

	buttons = [0x59, 0x5A, 0x28, 0x29, 0x2A, 0x2B, 0x2C, 0x2D, 0x57, 0x58, 0x5B, 0x5C, 0x56, 0x5D, 0x5E, 0x5F]

	def light_all_buttons():
		for i in LedsMC.buttons:
			device.midiOutMsg(0x90, 0x00, i, 127)

class Leds:

	def blink_step(step):
		device.midiOutMsg(0x90, 0x00, step, 0x01)

	def light_layer(layer):
		if layer == 0:
			device.midiOutMsg(0x90, 0x00, 0x54, 127)
			device.midiOutMsg(0x90, 0x00, 0x55, 0)
		elif layer == 1:
			device.midiOutMsg(0x90, 0x00, 0x54, 127)
			device.midiOutMsg(0x90, 0x00, 0x55, 127)
		elif layer == 2:
			device.midiOutMsg(0x90, 0x00, 0x55, 127)
			device.midiOutMsg(0x90, 0x00, 0x54, 0)

	def light_one_knob(knob):
		Leds.knobs_off()
		device.midiOutMsg(0xB0, 0x00, knob, 127)

	def light_keys(keys):
		for i in keys:
			device.midiOutMsg(0x90, 0x00, i, 127)

	def knobs_off():
		for i in range(48, 56):
			device.midiOutMsg(0xB0, 0x00, i, 0)

	def off(buttons):
		# device.midiOutMsg(0x90, 0x00, 45, 0)
		for i in buttons:
			device.midiOutMsg(0x90, 0x00, i, 0x00)

	def light_quarter_knob(knob, side):
		print(knob)
		if side == 1:
			device.midiOutMsg(0xB0, 0x00, knob, 38)
		elif side == 2:
			device.midiOutMsg(0xB0, 0x00, knob, 91)

	def light_steps(seq_mode, leds=LedsMC.buttons):
		if seq_mode == 'Pattern A':
			offset = 0
		elif seq_mode == 'Pattern B':
			offset = 16
		
		for c, i in enumerate(leds):
			if channels.getGridBit(channels.selectedChannel(), c + offset) == 1:
				device.midiOutMsg(0x90, 0x00, i, 0x7F)
			else:
				device.midiOutMsg(0x90, 0x00, i, 0x00)

	def all_one_knob(knob_num):
		 device.midiOutMsg(0xB0, 0x00, 8 + knob_num, 27) # Light Knob 7 led 4

	def one_encoder_led(knob_num, led_num):
		device.midiOutMsg(0xB0, 0x00, 8 + knob_num, led_num)
			
	def light_transport():
		print('light_transporttt')
		if transport.isRecording():
			# device.midiOutMsg(0x90, 0x00, 0x0F, 1)
			device.midiOutMsg(0x90, 0x00, 0x5F, 127)
		else:
			device.midiOutMsg(0x90, 0x00, 0x5F, 0)
		if ui.isLoopRecEnabled():
			# device.midiOutMsg(0x90, 0x00, 0x0C, 1)
			device.midiOutMsg(0x90, 0x00, 0x56, 127)
		else:
			# device.midiOutMsg(0x90, 0x00, 0x0C, 0)
			device.midiOutMsg(0x90, 0x00, 0x56, 0)
		if transport.isPlaying():
			# device.midiOutMsg(0x90, 0x00, 0x0E, 1)
			device.midiOutMsg(0x90, 0x00, 0x5E, 1)
			# device.midiOutMsg(0x90, 0x00, 0x0D, 0)
			device.midiOutMsg(0x90, 0x00, 0x5D, 0)
		else:
			# device.midiOutMsg(0x90, 0x00, 0x0E, 0)
			device.midiOutMsg(0x90, 0x00, 0x5E, 127)
			device.midiOutMsg(0x90, 0x00, 0x5E, 0)
			# device.midiOutMsg(0x90, 0x00, 0x0D, 1)
			device.midiOutMsg(0x90, 0x00, 0x5D, 127)

	def light_button_range(buttons):
		for i in buttons:
			device.midiOutMsg(0x90, 0x00, i, 0x7F)
	def light_b():
		device.midiOutMsg(0x90, 0x00, 0x21, 0x01) # Lights button 16
	# device.midiOutMsg(176, 0, 15, 2)
	# device.midiOutMsg(0xC0, 0x00, 0x09, 0x05)
