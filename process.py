from data import fader, k, Knob, buttons, buttons_two, knobs, Button
import data as d
from action import Action
import channels
import ui 
import device
import mixer 
import channels 
import playlist
import plugins
from utility import Utility
import midi
from config_layout import layout
from leds import Leds
from config import Config
import itertools
import plugindata as plg
from notes import Notes, Scales
# from buttons import Buttons

class Dispatch:

	def __init__(self):
		self.event = 0
		self.chan_ex = 0
		# self.mapped_1 = Utility.mapvalues(self.event.data2, 0, 1, 0, 127)
		# self.mapped_minus_1 = Utility.mapvalues(self.event.data2, -1, 1, 0, 127)		
		self.channel = channels.selectedChannel()
		self.track = mixer.trackNumber()
		self.random_offset = 63
		if self.chan_ex == 138:
			self.mode = 'Standard'
			self.xt = d.Standard()

		else:
			self.mode = 'MC'
			self.xt = d.MC()
			print(Mode.layer_count)

class Process(Dispatch):

	def triage(self):

		if self.event.midiId == self.xt.button_id:
			if self.event.data1 in self.xt.buttons:
				Buttons.on_press(self)
			elif self.event.data1 in self.xt.k_push:
				KnobControl.press(self)
			elif self.event.data1 == 84 and self.event.data2 > 0:
				print('layer a')
				Mode.set_layer(self, -1)
				Mode.set_leds(self)
				self.event.handled = True
			elif self.event.data1 == self.xt.layer_b and self.event.data2 > 0:
				Mode.set_layer(self, 1)
				Mode.set_leds(self)
				self.event.handled = True

		elif self.event.midiId == self.xt.knob_id and self.event.data1 in self.xt.knobs:
			print('knob levels')
			KnobControl.levels(self)

		elif self.event.midiId == self.xt.fader_midi_id and self.event.data1 == self.xt.fader:
			Fader.fade(self.event)
			self.event.handled = True

		
		# elif self.event.midiId != 176 and Mode.get_mode() == 6 and self.event.data1 in d.buttons:
		# 	print('mode 6')
		# 	Keys.decide(self.event)

		elif self.event.midiId == 128:
			Mode.set_leds(self)

		# elif self.event.midiId == self.xt.button_id and self.event.data1 in self.xt.buttons:
		# 	print('b.press')
		# 	b = Buttons(self.event)
		# 	b.press()
		# elif Mode.get_mode() == 8:

		elif self.event.midiId == 144 and self.event.data1 == 95 and self.event.midiChanEx == 128:
			device.midiOutMsg(0xB0, 0x00, 0x7F, 0x00)

class Buttons(Dispatch):

	def on_press(self):
		print('button on_press')


		if Mode.get_layer() == 2:  # transport layer
			print('layer 2')
			if self.event.data2 > 0:
				Main.decide(self)

		elif Mode.get_mode() == 6:  # keyboard
			print('go keys')
			Keys.decide(self)


		elif Mode.get_mode() == 7:	# sequencer
			if self.event.data2 > 0:
				print(f'seq status: {Mode.get_seq_status()}')
				# if Mode.get_layer() == 0:
				if Mode.get_seq_status() == 'Pattern A':
					step = self.xt.buttons.index(self.event.data1)
				# elif Mode.get_layer() == 1:
				if Mode.get_seq_status() == 'Pattern B':
					step = self.xt.buttons.index(self.event.data1) + 16

				if channels.getGridBit(channels.selectedChannel(), step) == 0:						
					channels.setGridBit(channels.selectedChannel(), step, 1)
					Mode.set_leds(self)
					self.event.handled = True
				else:															
					channels.setGridBit(channels.selectedChannel(), step, 0)
					Mode.set_leds(self)
					self.event.handled = True
				
		elif Mode.get_mode() == 8:
			if self.event.data2 > 0:
				Main.decide(self)

	def layer_b(self):
		Main.decide(self)

class Keys(Dispatch):

	oct_iter = 2
	octave = [-36, -24, -12, 0, 12, 24, 36]

	def decide(self):
		if Mode.get_layer() == 0:

			if str(self.event.data1) in self.xt.key_dict.keys():
				print('in key_dict')
				Keys.play_note(self)
				self.event.handled = True

			elif self.event.data2 > 0:
				if self.event.data1 == self.xt.lower_octave  and self.event.midiId == 144:
					Keys.oct_iter -= 1
					if Keys.oct_iter < 0:
						Keys.oct_iter = len(Keys.octave) - 1
					self.event.handled = True

				elif self.event.data1 == self.xt.raise_octave and self.event.midiId == 144:
					Keys.oct_iter += 1
					if Keys.oct_iter == len(Keys.octave):
						Keys.oct_iter = 0
					self.event.handled = True

				elif self.event.data1 == self.xt.key_blank and self.event.midiId == 144:
					Action.record()
					self.event.handled = True

		elif Mode.get_layer() == 1:
			channels.midiNoteOn(channels.selectedChannel(), Scales.scales[1][self.xt.buttons.index(self.event.data1) + 36], self.event.data2)
			self.event.handled = True
			# channels.midiNoteOn(channels.selectedChannel(), notes.scales[Modes.scale_iter][Modes.root_iter][event.data1-24], self.event.data2)

	def play_note(self):
		print('playnote')
		channels.midiNoteOn(channels.selectedChannel(), self.xt.key_dict[str(self.event.data1)] + Keys.octave[Keys.oct_iter], self.event.data2)

class Mode(Process):

	current_mode = Config.INIT_MODE
	seq_modes = ['Pattern B', 'Pattern A']
	seq = itertools.cycle(seq_modes)
	seq_status = 'Pattern A'
	modes = ['Keyboard', 'Transport', 'Sequencer']
	layers = ['A', 'B', 'C']
	current_layer = 'A'
	layer_count = 0

	def set_layer(self, val):
		Mode.layer_count = Mode.layer_count + val
		if Mode.layer_count < 0:
			Mode.layer_count = 2
		elif Mode.layer_count > 2:
			Mode.layer_count = 0
		Mode.set_leds(self)

	def get_layer():
		return Mode.layer_count

	def set_mode_direct(mode):
		Mode.current_mode = mode

	def get_mode():
		return Mode.current_mode

	def set_pattern_range(self):
		"""rotates between pattern a and pattern b"""

		if Mode.get_layer() <= 1:
			Mode.seq_status = next(Mode.seq)
			ui.setHintMsg(f'Seq Mode: {Mode.seq_status}')

	def get_seq_status():
		return Mode.seq_status

	def set_leds(self):
		Leds.off(self.xt.all_button_leds)
		Leds.light_layer(Mode.get_layer())
		if Mode.get_layer() == 2 and Mode.get_mode() != 8:
			print('light_transport')			
			Leds.light_transport()
		elif Mode.get_mode() == 6:
			print('mode 6')
			if Mode.get_layer() == 0:
				Leds.light_keys(self.xt.keyboard_leds)
			elif Mode.get_layer() == 1:
				print('all_button_leds')
				Leds.light_button_range(self.xt.all_button_leds)

		elif Mode.get_mode() == 7:
			if Mode.get_seq_status() == 'Pattern A':
				Leds.light_quarter_knob(self.event.data1 + 16, 1)
			else:
				Leds.light_quarter_knob(self.event.data1 + 16, 2)
			Leds.light_steps(Mode.get_seq_status())
		elif Mode.get_mode() == 8 and Mode.get_layer() == 0:
			print('mode 8 layer 0 ')
			Leds.light_transport()
		else:
			Leds.off(self.xt.all_button_leds)

class Update():

	def light_control(event):
		print('update light_control')
		if event and Mode.get_mode() == 7:
			print('event and 7')
			Leds.light_steps(Mode.get_seq_status(), )
		elif Mode.get_mode() == 8:
			if event == 256 or event == 260:
				Leds.light_transport()

class KnobControl(Process):

	link_chan = 0

	def press(self):

		if self.event.data2 > 0:

			if self.event.data1 == self.xt.k_one_p:
				if ui.getFocused(midi.widMixer):
					Action.focus_channels()
				elif ui.getFocused(midi.widChannelRack):
					Action.focus_mixer()
				else:
					Action.focus_channels()
				self.event.handled = True

			elif self.event.data1 == self.xt.k_two_p:
				Action.open_channel()
				self.event.handled = True

			elif self.event.data1 == self.xt.k_three_p:
				device.midiOutMsg(0xB0, 0x00, 0x7F, 0x01)	# change to mc mode
				self.event.handled = True

			elif self.event.data1 == self.xt.k_four_p:
				# Leds.off()
				Leds.knobs_off()
				Leds.light_b()
				self.event.handled = True

			elif self.event.data1 == self.xt.k_five_p:
				Leds.knobs_off()
				self.event.handled = True

			elif self.event.data1 == self.xt.k_six_p:
				print('press knob 6')
				# Leds.light_keys(self.xt.keyboard_leds)
				Leds.light_one_knob(self.event.data1 + 16)
				Mode.set_mode_direct(6)
				Mode.set_leds(self)
				self.event.handled = True

			elif self.event.data1 == self.xt.k_seven_p:
				Leds.knobs_off()
				print(f'layer: {Mode.get_layer()}')
				if Mode.get_layer() <= 2 and Mode.get_mode() == 7:
					Mode.set_pattern_range(self)
					Mode.set_leds(self)
					self.event.handled = True
				else:
					print('set_direct_7')
					Mode.set_mode_direct(7)
					Mode.set_leds(self)
					self.event.handled = True

			elif self.event.data1 == self.xt.k_eight_p:
				print('mode 8')
				# Leds.off(self.xt.all_button_leds)
				Leds.light_one_knob(self.event.data1 + 16)
				Mode.set_mode_direct(8)
				Mode.set_leds(self)
				self.event.handled = True		

	def levels(self):

		# if self.event.data1 == d.Knob.sixteen.cc:
		# 	Action.random_offset = self.event.data2

		if ui.getFocused(5) and plugins.isValid(channels.channelNumber()): 

			plugin = plugins.getPluginName(channels.selectedChannel())	
			param_count = plugins.getParamCount(channels.selectedChannel())
			if plugin in plg.plugin_dict:
				param = plg.plugin_dict[plugin][self.xt.knobs.index(self.event.data1)]
				print('has plugin')	
				param_value =  KnobControl.level_adjust(self.event.data2, plugins.getParamValue(param, channels.selectedChannel()))		                                                                           																		
				plugins.setParamValue(param_value, param, channels.selectedChannel())
				self.event.handled = True
		
			else:	
				param = self.event.data1 - 15
				param_value =  KnobControl.level_adjust(self.event.data2, plugins.getParamValue(param, channels.selectedChannel()))	
				plugins.setParamValue(param_value, param, self.channel)
				self.event.handled = True

		if self.event.data1 == self.xt.knobs[0]:
			if ui.getFocused(midi.widMixer):
				mixer.setTrackVolume(self.track, KnobControl.level_adjust(self.event.data2, mixer.getTrackVolume(self.track)))

			elif ui.getFocused(midi.widChannelRack):
				channels.setChannelVolume(self.channel, KnobControl.level_adjust(self.event.data2, channels.getChannelVolume(self.channel)))

		elif self.event.data1 == self.xt.knobs[1]:
			if ui.getFocused(midi.widMixer):
				mixer.setTrackPan(self.track, self.mapped_minus_1, 1)
			elif ui.getFocused(midi.widChannelRack):
				channels.setChannelPan(self.channel, KnobControl.level_adjust(self.event.data2, channels.getChannelPan(self.channel)))

		elif self.event.data1 == self.xt.knobs[2]:
			link = KnobControl.channel_link(self.event.data2)
			if ui.getFocused(midi.widChannelRack):
				mixer.linkChannelToTrack(channels.selectedChannel(), link)
			elif ui.getFocused(midi.widMixer):
				Action.set_mixer_route(link)
				ui.setHintMsg(f"Route Current Track to Track {link}")

	def level_adjust(cc, current_level):
		if cc >= 65:
			return round(current_level - .025, 5)
		elif cc <= 15:
			return round(current_level + .025, 5)

	def channel_link(cc):

		tracks = [i for i in range(0, 128)]
		if cc >= 65:
			if KnobControl.link_chan > 0:
				KnobControl.link_chan -= 1
		elif KnobControl.link_chan < 127:
			KnobControl.link_chan += 1
		return tracks[KnobControl.link_chan]

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

class Main(Dispatch):	

	def decide(self):
		# use index in list rather than event
			Action.call_func(layout[self.xt.mapping[self.event.data1]])
			self.event.handled = True