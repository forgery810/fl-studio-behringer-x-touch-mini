from data import fader, k, Knob, buttons, buttons_two, knobs, Button
import data as d
from action import Action
import channels
import ui 
import mixer 
import channels 
import playlist
from utility import Utility
import midi
from config_layout import layout
from leds import Leds
# from buttons import Buttons

class Dispatch:

	def __init__(self, event):
		self.event = event

class Process(Dispatch):

	def triage(self):
		# print(ks)
		if Mode.get_mode() == 6 and self.event.data1 in d.buttons:
			if self.event.midiId == 144:
				Keys.play_note(self.event)

		if self.event.midiId == 128:
			Mode.set_leds()
			print('128')
			# Leds.light_steps()

		elif self.event.midiId == Button.midi_id and self.event.data1 in d.buttons:
			print('button') 
			b = Buttons(self.event)
			b.press()

		elif self.event.midiId == fader.midi_id and self.event.data1 == fader.cc:
			Fader.fade(self.event)

		elif self.event.midiId == Button.midi_id and self.event.data1 in d.knob_push_cc:
			Knob.press(self.event)


class Buttons(Dispatch):

	def press(self):
		print('press')
		if Mode.get_mode() == 6:
			Keys.play_note(self.event)
			Mode.set_leds()

		elif Mode.get_mode() == 7:      						  # sets step as long as param edit not active
			if channels.getGridBit(channels.selectedChannel(), self.event.data1 - 8) == 0:						
				channels.setGridBit(channels.selectedChannel(), self.event.data1 - 8, 1)
				Mode.set_leds()
				self.event.handled = True
			else:															
				channels.setGridBit(channels.selectedChannel(), self.event.data1 - 8, 0)
				self.event.handled = True
			
		elif Mode.get_mode() == 8:
			print('decide')
			Main.decide(self.event)

class Fader():

	def fade(event):
		if ui.getFocused(0):
			mixer.setTrackNumber(int(Utility.mapvalues(event.data2, 0, 64, 0, 127)))
			ui.scrollWindow(midi.widMixer, mixer.trackNumber())
		elif ui.getFocused(1):
			channels.selectOneChannel(int(round(Utility.mapvalues(event.data2, channels.channelCount()-1, 0, 0, 127), 0)))			
		elif ui.getFocused(2):
			playlist.deselectAll()
			playlist.selectTrack(int(Utility.mapvalues(event.data2, 30, 1, 0, 127)))


class Keys:
	key_dict = {
		'16': 60,
		'9': 61,
		'17': 62,
		'10': 63,
		'18': 64,
		'19': 65,
		'12': 66,
		'20': 67,
		'13': 68,
		'21': 69,
		'14': 70,
		'22': 71,
		'23': 72,
	}

	def play_note(event):
		channels.midiNoteOn(channels.selectedChannel(), Keys.key_dict[str(event.data1)], event.data2)

class Mode():
	current_mode = 8

	def set_mode_direct(mode):
		Mode.current_mode = mode
		Mode.set_leds()

	def set_leds():
		print('set_leds')
		if Mode.get_mode() == 6:
			Leds.light_keys()
		elif Mode.get_mode() == 7:
			Leds.light_steps()
		else:
			Leds.off()



	def get_mode():
		return Mode.current_mode

class Main():	

	def decide(event):
			Action.call_func(layout[d.mapping[event.data1]])
			event.handled = True


class Update():
	def light_control(event):
		print('update light_control')
		if event and Mode.get_mode() == 7:
			print('event and 7')
			Leds.light_steps()

class Knob():

	def press(event):
		if event.data1 == d.KnobPush.eight.cc:
			Mode.set_mode_direct(8)
			event.handled = True			
		elif event.data1 == d.KnobPush.one.cc:
			Action.focus_channels()
			event.handled = True
		elif event.data1 == d.KnobPush.two.cc:
			Action.focus_mixer()
			event.handled = True
		elif event.data1 == d.KnobPush.six.cc:
			Mode.set_mode_direct(6)
			event.handled = True
		elif event.data1 == d.KnobPush.seven.cc:
			Mode.set_mode_direct(7)
			event.handled = True

		# elif event.data1 == d.KnobPush..cc:
