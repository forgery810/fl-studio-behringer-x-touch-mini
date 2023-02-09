import data as d
from action import Action
import channels
import ui 
import device
import mixer 
import channels 
import playlist
import plugins
import patterns
from utility import Utility
import midi
from config_layout import layout
from leds import Leds
from config import Config
import itertools
import plugindata as plg
from notes import Notes, Scales

class Dispatch:

	def __init__(self):
		self.chan_ex = 0
		self.channel = channels.selectedChannel()
		self.pattern = patterns.patternNumber()
		self.random_offset = 63
		self.seq_b_offset = 16
		if self.chan_ex == 138:
			self.xt = d.Standard()
		else:
			self.xt = d.MC()

class Process(Dispatch):

	def triage(self):

		if self.event.midiId == self.xt.button_id:
			if self.event.data1 in self.xt.buttons:
				Buttons.on_press(self)
			elif self.event.data1 in self.xt.k_push:
				Encoder.press(self)
			elif self.event.data1 == self.xt.layer_a and self.event.data2 > 0:
				Mode.set_layer(self, -1)
				# Mode.set_leds(self)
				self.event.handled = True
			elif self.event.data1 == self.xt.layer_b and self.event.data2 > 0:
				Mode.set_layer(self, 1)
				# Mode.set_leds(self)
				self.event.handled = True

		elif self.event.midiId == self.xt.knob_id and self.event.data1 in self.xt.knobs:
			Encoder.levels(self)

		elif self.event.midiId == self.xt.fader_midi_id and self.event.data1 == self.xt.fader:
			Fader.fade(self.event)
			self.event.handled = True

		elif self.event.midiId == 128:
			Mode.set_leds(self)

class Buttons(Process):

	step_to_edit = 0

	def on_press(self):

		if Mode.get_layer() == 2 and Mode.get_mode() != 8:  #  Modes 6 & 7, B transport layer
			if self.event.data2 > 0:
				Main.transport_act(self, self.event.data1 + 100)

		elif Mode.get_mode() == 6:  # keyboard
			Keys.decide(self)


		elif Mode.get_mode() == 7:	# sequencer
			if self.event.data2 > 0:
				print(f'seq status: {Mode.get_seq_status()}')
				if Mode.get_layer() == 0:
					if Mode.get_seq_status() == 'Pattern A':
						step = self.xt.buttons.index(self.event.data1)
					if Mode.get_seq_status() == 'Pattern B':
						step = self.xt.buttons.index(self.event.data1) + self.seq_b_offset

					if channels.getGridBit(channels.selectedChannel(), step) == 0:						
						channels.setGridBit(channels.selectedChannel(), step, 1)
						Mode.set_leds(self)
						self.event.handled = True
					else:															
						channels.setGridBit(channels.selectedChannel(), step, 0)
						Mode.set_leds(self)
						self.event.handled = True

				elif Mode.get_layer() == 1:
					if Mode.get_seq_status() == 'Pattern A':
						Buttons.step_to_edit = self.xt.buttons.index(self.event.data1)
						print(Buttons.step_to_edit)
						Mode.set_leds(self)
						Leds.blink_step(self.xt.all_button_leds[Buttons.step_to_edit])
						self.event.handled = True
					if Mode.get_seq_status() == 'Pattern B':
						Buttons.step_to_edit = self.xt.buttons.index(self.event.data1) + 16
						Mode.set_leds(self)
						Leds.blink_step(self.xt.all_button_leds[Buttons.step_to_edit - 16])
						self.event.handled = True

		elif Mode.get_mode() == 8:
			if self.event.data2 > 0:
				Main.transport_act(self, 20 * Mode.get_layer() + self.event.data1)

class Keys(Process):

	oct_iter = 2
	octave = [-36, -24, -12, 0, 12, 24, 36]

	def decide(self):
		if Mode.get_layer() == 0:

			if str(self.event.data1) in self.xt.key_dict.keys():
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
			channels.midiNoteOn(channels.selectedChannel(), Scales.scales[Scales.get_scale_choice()][self.xt.buttons.index(self.event.data1) + 24 + Notes.get_root_note()], self.event.data2)
			self.event.handled = True

	def play_note(self):
		channels.midiNoteOn(channels.selectedChannel(), self.xt.key_dict[str(self.event.data1)] + Keys.octave[Keys.oct_iter], self.event.data2)

class Mode(Process):

	current_mode = Config.INIT_MODE
	seq_modes = ['Pattern B', 'Pattern A']
	seq = itertools.cycle(seq_modes)
	seq_status = 'Pattern A'
	modes = ['Keyboard', 'Transport', 'Sequencer']
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
			if Mode.get_layer() == 0:
				Leds.light_keys(self.xt.keyboard_leds)
			elif Mode.get_layer() == 1:
				Leds.light_button_range(self.xt.all_button_leds)

		elif Mode.get_mode() == 7 and Mode.get_layer() != 2:
			Leds.knobs_off()
			if Mode.get_seq_status() == 'Pattern A':
				Leds.light_quarter_knob(54, 1)
			elif Mode.get_seq_status() == 'Pattern B':
				Leds.light_quarter_knob(54, 2)
			Leds.light_steps(Mode.get_seq_status())
		elif Mode.get_mode() == 8 and Mode.get_layer() == 0:
			Leds.light_transport()
		else:
			Leds.off(self.xt.all_button_leds)

class Update():

	def light_control(event):
		if event and Mode.get_mode() == 7 and Mode.get_layer() != 2:
			Leds.light_steps(Mode.get_seq_status(), )
		elif event == 256 or event == 260:
			if Mode.get_mode() == 8 and Mode.get_layer() == 0:
				Leds.light_transport()
			elif Mode.get_layer() == 2 and Mode.get_mode() != 8:
				Leds.light_transport()

class Encoder(Process):

	link_chan = 0

	def press(self):

		if self.event.data2 > 0:

			if self.event.data1 == self.xt.k_one_p:
				Action.call_func(layout['knob_one'])
				self.event.handled = True

			elif self.event.data1 == self.xt.k_two_p:
				Action.call_func(layout['knob_two'])
				self.event.handled = True

			elif self.event.data1 == self.xt.k_three_p:
				Action.call_func(layout['knob_three'])
				self.event.handled = True

			elif self.event.data1 == self.xt.k_four_p:
				Action.call_func(layout['knob_four'])
				self.event.handled = True

			elif self.event.data1 == self.xt.k_five_p:
				Action.call_func(layout['knob_five'])
				self.event.handled = True

			elif self.event.data1 == self.xt.k_six_p:
				Leds.light_one_knob(self.event.data1 + 16)
				Mode.set_mode_direct(6)
				Mode.set_leds(self)
				self.event.handled = True

			elif self.event.data1 == self.xt.k_seven_p:
				Leds.knobs_off()
				if Mode.get_layer() <= 2 and Mode.get_mode() == 7:
					Mode.set_pattern_range(self)
					Mode.set_leds(self)
					self.event.handled = True
				else:
					Mode.set_mode_direct(7)
					Mode.set_leds(self)
					self.event.handled = True

			elif self.event.data1 == self.xt.k_eight_p:
				Leds.light_one_knob(self.event.data1 + 16)
				Mode.set_mode_direct(8)
				Mode.set_leds(self)
				self.event.handled = True		

	def levels(self):

		if ui.getFocused(5) and plugins.isValid(channels.channelNumber()): 

			plugin = plugins.getPluginName(channels.selectedChannel())	
			param_count = plugins.getParamCount(channels.selectedChannel())
			if plugin in plg.plugin_dict:
				param = plg.plugin_dict[plugin][self.xt.knobs.index(self.event.data1)]
				param_value =  Utility.level_adjust(self.event.data2, plugins.getParamValue(param, channels.selectedChannel()), .025)		                                                                           																		
				plugins.setParamValue(param_value, param, channels.selectedChannel())
				self.event.handled = True
		
			else:	
				param = self.event.data1 - 15
				param_value =  Utility.level_adjust(self.event.data2, plugins.getParamValue(param, channels.selectedChannel()), .025)	
				plugins.setParamValue(param_value, param, self.channel)
				self.event.handled = True

		# elif self.event.data1 == self.xt.knobs[3] and Mode.get_mode() != 7:
		# 	shift = Shifter()
		# 	if self.event.data2 == 65:
		# 		shift.back()
		# 	elif self.event.data2 == 1:
		# 		shift.forward()

		elif Mode.get_mode() == 7 and self.event.data1 < 23:  		# < 23 ignores shift and lets knob 8 adjust random offset

			if Mode.get_layer() == 0 and self.event.data1 == self.xt.knobs[3]:
				shift = Shifter()
				if self.event.data2 == 65:
					shift.back()
				elif self.event.data2 == 1:
					shift.forward()			 
			elif Mode.get_layer() == 1:
				Encoder.edit_parameter(self)

			elif Mode.get_layer() == 2:
				Encoder.set_random(self) 



		elif Mode.get_mode() == 6 and Mode.get_layer() == 1:
			if self.event.data1 == self.xt.knobs[0] or self.event.data1 == self.xt.knobs[1]:
				Encoder.set_random(self)

		elif self.event.data1 == self.xt.knobs[0]:
			if ui.getFocused(midi.widMixer):
				mixer.setTrackVolume(mixer.trackNumber(), Utility.level_adjust(self.event.data2, mixer.getTrackVolume(mixer.trackNumber()), 0.025))

			elif ui.getFocused(midi.widChannelRack):
				channels.setChannelVolume(self.channel, Utility.level_adjust(self.event.data2, channels.getChannelVolume(self.channel), 0.025))

		elif self.event.data1 == self.xt.knobs[1]:
			if ui.getFocused(midi.widMixer):
				mixer.setTrackPan(mixer.trackNumber(), Utility.level_adjust(self.event.data2, mixer.getTrackPan(mixer.trackNumber()), 0.05))
			elif ui.getFocused(midi.widChannelRack):
				channels.setChannelPan(self.channel, Utility.level_adjust(self.event.data2, channels.getChannelPan(self.channel), 0.025))

		elif self.event.data1 == self.xt.knobs[2]:
			link = Encoder.channel_link(self.event.data2)
			if ui.getFocused(midi.widChannelRack):
				mixer.linkChannelToTrack(channels.selectedChannel(), link)
			elif ui.getFocused(midi.widMixer):
				Action.set_mixer_route(link)
				ui.setHintMsg(f"Route Current Track to Track {link}")


		elif self.event.data1 == self.xt.knobs[7]:
			Action.set_random_offset(Utility.level_adjust(self.event.data2, Action.get_random_offset(), 5))
			if Action.get_random_offset() < 0:
				Action.set_random_offset(0)
			elif Action.get_random_offset() > 127:
				Action.set_random_offset(127)
			ui.setHintMsg(f'Random Offset: {Action.get_random_offset()}')

	def edit_parameter(self):
			param_knob = self.xt.knobs.index(self.event.data1)
			param_value = channels.getCurrentStepParam(self.channel, Buttons.step_to_edit, param_knob)
			channels.showGraphEditor(True, param_knob, Buttons.step_to_edit, channels.selectedChannel())
																						# bool temporary, long param, long step, long index, (long globalIndex* = 1)			
			if param_knob == midi.pModX or param_knob == midi.pModY: 					#long index, long patNum, long step, long param, long value, (long globalIndex = 0)
				channels.setStepParameterByIndex(self.channel, self.pattern, Buttons.step_to_edit, param_knob, int(Utility.level_adjust(self.event.data2, param_value,  1)), 1)

			elif param_knob == midi.pFinePitch:	
				channels.setStepParameterByIndex(self.channel, self.pattern, Buttons.step_to_edit, param_knob, int(Utility.level_adjust(self.event.data2, param_value,  1)), 1)

			else:
				channels.setStepParameterByIndex(self.channel, self.pattern, Buttons.step_to_edit, param_knob, int(Utility.level_adjust(self.event.data2, param_value, 1)), 1)

	def set_random(self):
		if self.event.data1 == self.xt.knobs[0]:
			root = Utility.level_adjust(self.event.data2, Notes.get_root_note(), 1)
			if root < 0:
				root = 0
			if root > 11:
				root = 11
			Notes.set_root_note(root)	
			ui.setHintMsg(f'{Notes.root_name(Notes.get_root_note())} {Scales.scale_name(Scales.get_scale_choice())}')

		elif self.event.data1 == self.xt.knobs[1]:
			scale = Utility.level_adjust(self.event.data2, Scales.get_scale_choice(), 1)
			if scale < 0:
				scale = 0
			if scale >= len(Scales.scales):
				scale = len(Scales.scales) - 1
			Scales.set_scale(scale)
			ui.setHintMsg(f'{Notes.root_name(Notes.get_root_note())} {Scales.scale_name(Scales.get_scale_choice())}')

		elif self.event.data1 == self.xt.knobs[2]:
			lower = Utility.level_adjust(self.event.data2, Notes.get_lower_limit(), 1)
			if lower < 0:
				lower = 0
			elif lower > 50:
				lower = 50
			Notes.set_lower_limit(lower)
			ui.setHintMsg(f'Lower Limit: {Notes.get_lower_limit()}')
			self.event.handled = True

		elif self.event.data1 == self.xt.knobs[3]:
			upper = Utility.level_adjust(self.event.data2, Notes.get_upper_limit(), 1)
			if upper > 0:
				upper = 0
			elif upper < -50:
				upper = -50
			Notes.set_upper_limit(upper)
			ui.setHintMsg(f'Upper Limit: {Notes.get_upper_limit()}')
			self.event.handled = True

	def channel_link(cc):

		tracks = [i for i in range(0, 128)]
		if cc >= 65:
			if Encoder.link_chan > 0:
				Encoder.link_chan -= 1
		elif Encoder.link_chan < 127:
			Encoder.link_chan += 1
		return tracks[Encoder.link_chan]

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

class Main(Process):	

	def transport_act(self, offset_event):
		# use index in list rather than event
			Action.call_func(layout[self.xt.mapping[offset_event]])
			self.event.handled = True

class Shifter():

	def __init__(self):
		self.channel = channels.selectedChannel()
		self.pattern = []
		self.pat_num = patterns.patternNumber()
		self.pat_len = patterns.getPatternLength(self.pat_num)
		self.p_str = self.pattern_to_string() 	
		self.p_int = self.str_to_int(self.p_str)
		self.formatted = 0
		self.list_outgoing = []

	def back(self):
		self.formatted = format(self.shift_left(), self.get_format())	
		self.list_outgoing = self.str_to_list()
		if len(self.list_outgoing) > self.pat_len:
			self.list_outgoing.pop(0)
		self.write_to_pattern()

	def forward(self):
		self.formatted = format(self.shift_right(), self.get_format())	
		self.list_outgoing = self.str_to_list()
		if len(self.list_outgoing) > self.pat_len:
			self.list_outgoing.pop(0)
		self.write_to_pattern()

	def pattern_to_string(self):
		"""takes current pattern, appends to list, return string of list"""
		for bit in range(0, self.pat_len):
			self.pattern.append(str(channels.getGridBit(self.channel, bit)))
		return (''.join(self.pattern))

	def str_to_int(self, pattern):
		"""takes pattern as string of numbers and returns int"""

		return int(pattern, 2)	

	def get_format(self):
		"""gets patterns num and returns appropriate string to format in into bits"""

		length = patterns.getPatternLength(self.pat_num) + 2
		return f'#0{length}b'

	def shift_left(self):

		out = (self.p_int << 1) | (self.p_int >> (self.pat_len - 1))
		return out

	def shift_right(self):

		out = (self.p_int >> 1) | (self.p_int << (self.pat_len - 1)) & self.max_bits(self.pat_len)
		return out

	def str_to_list(self):
		"""takes string and returns list without first two characters'b0' """

		out_list = []
		for i in self.formatted[2:]:
			out_list.append(int(i))
		return out_list

	def write_to_pattern(self):
		"""writes bit shifted pattern to approriate channel"""

		inx = 0
		if patterns.patternNumber() == self.pat_num:
			for i in range(patterns.getPatternLength(self.pat_num)):    # clear pattern
				channels.setGridBit(self.channel, i, 0)
			for step in self.list_outgoing:
				channels.setGridBit(self.channel, inx, step)
				inx += 1

	def max_bits(self, num):
		"""returns the maximun integer based on num in bits"""

		max_num = (1 << num) - 1
		return max_num