from data import fader, k, Knob, buttons, buttons_two, knobs, Button
import data as d
from action import Action
import channels
import ui 
import device
import mixer 
import channels 
import playlist
from utility import Utility
import midi
from config_layout import layout
from leds import Leds
from config import Config
import itertools
# from buttons import Buttons

class Dispatch:

	def __init__(self, event):
		self.event = event
		self.mapped_1 = Utility.mapvalues(self.event.data2, 0, 1, 0, 127)
		self.mapped_minus_1 = Utility.mapvalues(self.event.data2, -1, 1, 0, 127)		
		self.channel = channels.selectedChannel()
		self.track = mixer.trackNumber()

class Process(Dispatch):

	def triage(self):

		if self.event.midiId == 144 and self.event.data1 in d.buttons_two:
			print('layer b')
			Buttons.layer_b(self)

		
		elif self.event.midiId != 176 and Mode.get_mode() == 6 and self.event.data1 in d.buttons:
			print('mode 6')
			Keys.decide(self.event)

		elif self.event.midiId == 128:
			Mode.set_leds()

		elif self.event.midiId == Button.midi_id and self.event.data1 in d.buttons:
			print('b.press')
			b = Buttons(self.event)
			b.press()

		elif self.event.midiId == fader.midi_id and self.event.data1 == fader.cc:
			print('fader')
			Fader.fade(self.event)
			self.event.handled = True

		elif self.event.midiId == d.KnobPush.midi_id and self.event.data1 in d.knob_push_cc:	
			print('knob-control press')
			KnobControl.press(self)

		# elif Mode.get_mode() == 8:
		elif self.event.midiId == Knob.midi_id:
			print('knob levels')
			KnobControl.levels(self)

		elif self.event.midiId == 144 and self.event.data1 == 95 and self.event.event.midiChanEx == 128:
			device.midiOutMsg(0xB0, 0x00, 0x7F, 0x00)
			
class Buttons(Dispatch):

	def press(self):

		if Mode.get_mode() == 7:      						  # needs addressing
			if Mode.get_seq_status() == 'Pattern A':
				step = d.buttons_one.index(self.event.data1)
			elif Mode.get_seq_status() == 'Pattern B':
				step = d.buttons_one.index(self.event.data1) + 16

			if channels.getGridBit(channels.selectedChannel(), step) == 0:						
				channels.setGridBit(channels.selectedChannel(), step, 1)
				Mode.set_leds()
				self.event.handled = True
			else:															
				channels.setGridBit(channels.selectedChannel(), step, 0)
				self.event.handled = True
			
		elif Mode.get_mode() == 8:
			Main.decide(self.event)

	def layer_b(self):
		Main.decide(self.event)



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

	oct_iter = 2
	octave = [-36, -24, -12, 0, 12, 24, 36]

	def decide(event):
		if str(event.data1) in Keys.key_dict.keys():
			print('in key_dict')
			Keys.play_note(event)
			Leds.light_keys()
			event.handled = True

		elif event.data1 == 8 and event.midiId == 144:
			Keys.oct_iter -= 1
			if Keys.oct_iter < 0:
				print(len(Keys.octave))
				Keys.oct_iter = len(Keys.octave) - 1
			event.handled = True

		elif event.data1 == 15 and event.midiId == 144:
			Keys.oct_iter += 1
			if Keys.oct_iter == len(Keys.octave):
				print(len(Keys.octave))
				Keys.oct_iter = 0
			event.handled = True

		elif event.data1 == 11 and event.midiId == 144:
			Action.record()
			event.handled = True

	def play_note(event):
		channels.midiNoteOn(channels.selectedChannel(), Keys.key_dict[str(event.data1)] + Keys.octave[Keys.oct_iter], event.data2)

class Mode():

	current_mode = Config.INIT_MODE
	seq_modes = ['Pattern B', 'Pattern A']
	seq = itertools.cycle(seq_modes)
	seq_status = 'Pattern A'

	def set_mode_direct(mode):
		Mode.current_mode = mode
		Mode.set_leds()

	def set_leds():
		print('set_leds')
		if Mode.get_mode() == 6:
			Leds.light_keys()
		elif Mode.get_mode() == 7:
			Leds.light_steps(Mode.get_seq_status())
		elif Mode.get_mode() == 8:
			Leds.light_transport()
		else:
			Leds.off()

	def get_mode():
		return Mode.current_mode

	def set_seq():
		Mode.seq_status = next(Mode.seq)
		ui.setHintMsg(f'Seq Mode: {Mode.seq_status}')

	def get_seq_status():
		return Mode.seq_status

class Update():

	def light_control(event):
		print('update light_control')
		if event and Mode.get_mode() == 7:
			print('event and 7')
			Leds.light_steps(Mode.get_seq_status())
		elif Mode.get_mode() == 8:
			if event == 256 or event == 260:
				Leds.light_transport()

class KnobControl(Process):

	def press(self):

		if self.event.data1 == d.KnobPush.one.cc:
			Action.focus_channels()
			self.event.handled = True

		elif self.event.data1 == d.KnobPush.two.cc:
			Action.focus_mixer()
			self.event.handled = True

		elif self.event.data1 == d.KnobPush.three.cc:
			# device.midiOutMsg(0xB0, 0x00, 0x7F, 0x01)
			Leds.off()
			self.event.handled = True

		elif self.event.data1 == d.KnobPush.four.cc:
			# Leds.off()
			Leds.light_b()
			self.event.handled = True

		elif self.event.data1 == d.KnobPush.five.cc:
			Leds.off()
			self.event.handled = True

		elif self.event.data1 == d.KnobPush.six.cc:

			Mode.set_mode_direct(6)
			self.event.handled = True
		elif self.event.data1 == d.KnobPush.seven.cc:
			if Mode.get_mode() == 7:
				Mode.set_seq()
				self.event.handled = True
			else:
				Mode.set_mode_direct(7)
				self.event.handled = True

		elif self.event.data1 == d.KnobPush.eight.cc:
			Leds.off()
			Mode.set_mode_direct(8)
			self.event.handled = True		

	def levels(self):

		if self.event.data1 == d.Knob.one.cc:
			if ui.getFocused(midi.widMixer):
				mixer.setTrackVolume(self.track, self.mapped_1, 1)

			elif ui.getFocused(midi.widChannelRack):
				channels.setChannelVolume(self.channel, self.mapped_1, 1)

		elif self.event.data1 == d.Knob.two.cc:
			if ui.getFocused(midi.widMixer):
				mixer.setTrackPan(self.track, self.mapped_minus_1, 1)
			elif ui.getFocused(midi.widChannelRack):
				channels.setChannelPan(self.channel, self.mapped_minus_1, 1)

		elif self.event.data1 == d.Knob.three.cc:
			if ui.getFocused(midi.widChannelRack):
				mixer.linkChannelToTrack(channels.selectedChannel(), int(Utility.mapvalues(self.event.data2, 0, 125, 0, 127)))
			elif ui.getFocused(midi.widMixer):
				Action.set_mixer_route(int(Utility.mapvalues(self.event.data2, 0, 125, 0, 127)))
				ui.setHintMsg(f"Route Current Track to Track {int(Utility.mapvalues(self.event.data2, 0, 125, 0, 127))}")

class Fader():

	def fade(event):
		if ui.getFocused(0):
			mixer.setTrackNumber(int(Utility.mapvalues(event.data2, 0, 64, 0, 127)))
			ui.scrollWindow(midi.widMixer, mixer.trackNumber())

		elif ui.getFocused(1):
			channels.selectOneChannel(int(round(Utility.mapvalues(event.data2, channels.channelCount()-1, 0, 0, 127), 0)))			
			event.handled = True
		elif ui.getFocused(2):
			playlist.deselectAll()
			playlist.selectTrack(int(Utility.mapvalues(event.data2, 30, 1, 0, 127)))
			event.handled = True

class Main():	

	def decide(event):
			Action.call_func(layout[d.mapping[event.data1]])
			event.handled = True