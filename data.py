import device
from leds import Leds 

class Input:

	def __init__(self, midi_id, cc):
		self.midi_id = midi_id
		self.cc = cc

knobs = [(176, i) for i in range(1, 9)]
knob_push_cc = [i for i in range(0, 8)] + [k for k in range(24, 32)]
buttons_one = [i for i in range(8, 24)]
buttons_two = [i for i in range(32, 48)]
buttons = buttons_one + buttons_two
knob_ccs = [i for i in range(1, 9)] + [k for k in range(11, 19)]
mc_knobs = [i for i in range(16, 24)]
button_midi_id = 144
stand_chan_ex = 128


class Knob():
	midi_id = 176
	k_one = 1
	k_two = 2
	k_three = 3
	k_four = 4
	k_five = 5
	k_six = 6
	k_seven = 7
	k_eight = 8
	k_sixteen = 18

class KnobPush():

	midi_id = 144 
	one = 0
	two = 1
	three = 2
	four = 3
	five = 4
	six = 5
	seven = 6
	eight = 7
	nine = 24
	ten = 25
	eleven = 26
	tweleve = 27
	thirteen = 28
	fourteen = 29
	fifteen  = 30
	sixteen = 31

class MC:
	button_id = 144
	midi_id = 144

	knob_id = 176
	k_one_p = 32
	k_two_p = 33
	k_three_p = 34
	k_four_p = 35
	k_five_p = 36
	k_six_p = 37
	k_seven_p = 38
	k_eight_p = 39

	knobs = [i for i in range(16, 24)]
	k_push = [i for i in range(32, 40)]
	# buttons = [b for b in range(89, 96)]
	buttons = [89, 90, 40, 41, 42, 43, 44, 45, 87, 88, 91, 92, 86, 93, 94, 95]
	bk_chan_ex = 128
	knob_led_cc = [i for i in range(48, 56)]
	fader_midi_id = 224
	fader = 0
	fader_chan_ex = 136

	layer_a = 84
	layer_b = 85
	layer_chan_ex = 128


	key_blank = 41
	lower_octave = 89
	raise_octave = 45
	key_dict = {
		'87': 60,
		'90': 61,
		'88': 62,
		'40': 63,
		'91': 64,
		'92': 65,
		'42': 66,
		'86': 67,
		'43': 68,
		'93': 69,
		'44': 70,
		'94': 71,
		'95': 72,
	}

	mapping ={
		89: "one",
		90: "two",
		40: "three",
		41: "four",
		42: "five",
		43: "six",
		44: "seven",
		45: "eight",
		87: "nine",
		88: "ten",
		91: "eleven",
		92: "twelve",
		86: "thirteen",
		93: "fourteen",
		94: "fifteen",
		95: "sixteen",

		# 32: "seventeen",
		# 33: "eighteen",
		# 34: "nineteen",
		# 35: "twenty",
		# 36: "twentyone",
		# 37: "twentytwo",
		# 38: "twentythree",
		# 39: "twentyfour",
		# 40: "twentyfive",
		# 41: "twentysix",
		# 42: "twentyseven",
		# 43: "twentyeight",
		# 44: "twentynine",
		# 45: "thirty",
		# 46: "thirtyone",
		# 47: "thirtytwo",
	}

	keyboard_leds = [0x5A, 0x28, 0x2A, 0x2B, 0x2C, 0x57, 0x58, 0x5B, 0x5C, 0x56, 0x5d, 0x5E, 0x5F]
	all_button_leds =      [0x59, 0x5A, 0x28, 0x29, 0x2A, 0x2B, 0x2C, 0x2D, 0x57, 0x58, 0x5B, 0x5C, 0x56, 0x5d, 0x5E, 0x5F]

	def init_leds(mode):
		for i in MC.all_button_leds:
			device.midiOutMsg(0x90, 0x00, i, 0x00)
		for i in MC.knob_led_cc:
			device.midiOutMsg(0xB0, 0x00, i, 0x00)
		device.midiOutMsg(0x90, 0x00, MC.layer_a, 0x7F)
		device.midiOutMsg(0x90, 0x00, MC.layer_b, 0x00)

		if mode == 6:
			for i in MC.keyboard_leds:
				device.midiOutMsg(0x90, 0x00, i, 0x7F)
		elif mode == 8:
			Leds.light_transport()


class Standard:

	button_id = 144
	k_one_p = 32
	k_two_p = 33
	k_three_p = 34
	k_four_p = 35
	k_five_p = 36
	k_six_p = 37
	k_seven_p = 38
	k_eight_p = 39

	knob_id = 176
	knobs = [i for i in range(1, 9)]
	k_one = 1
	k_two = 2
	k_three = 3
	k_four = 4
	k_five = 5
	k_six = 6
	k_seven = 7
	k_eight = 8
	k_sixteen = 18	
	layer_a = 'none'
	layer_b = 'none'

	buttons_one = [i for i in range(8, 24)]
	buttons_two = [i for i in range(32, 48)]
	buttons = buttons_one + buttons_two

	fader_midi_id = 176
	fader_cc = 9

	mapping ={
		8: "one",
		9: "two",
		10: "three",
		11: "four",
		12: "five",
		13: "six",
		14: "seven",
		15: "eight",
		16: "nine",
		17: "ten",
		18: "eleven",
		19: "twelve",
		20: "thirteen",
		21: "fourteen",
		22: "fifteen",
		23: "sixteen",

		32: "seventeen",
		33: "eighteen",
		34: "nineteen",
		35: "twenty",
		36: "twentyone",
		37: "twentytwo",
		38: "twentythree",
		39: "twentyfour",
		40: "twentyfive",
		41: "twentysix",
		42: "twentyseven",
		43: "twentyeight",
		44: "twentynine",
		45: "thirty",
		46: "thirtyone",
		47: "thirtytwo",
		}	
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

	keyboard_leds = [0x01, 0x02, 0x04, 0x05, 0x06, 0x08, 0x09, 0x0A, 0x0B, 0x0c, 0x0D, 0x0E, 0x0F]

class Button():
	midi_id = 144

fader = Input(176, 9)

k = {
	'one': {'turn': Input(176, 1),
			'push': Input(144, 0) },	
	'two': {'turn': Input(176, 2),
			'push': Input(144, 1) },	
	'three': {'turn': Input(176, 3),
			'push': Input(144, 2) },	
	'four': {'turn': Input(176, 4),
			'push': Input(144, 3) },	
	'five': {'turn': Input(176, 5),
			'push': Input(144, 4) },	
	'six': {'turn': Input(176, 6),
			'push': Input(144, 5) },	
	'seven': {'turn': Input(176, 7),
			'push': Input(144, 6) },
	'eight': {'turn': Input(176, 8),
			'push': Input(144, 7) },
	}

b = {
	'one': {}

}

mapping ={
	8: "one",
	9: "two",
	10: "three",
	11: "four",
	12: "five",
	13: "six",
	14: "seven",
	15: "eight",
	16: "nine",
	17: "ten",
	18: "eleven",
	19: "twelve",
	20: "thirteen",
	21: "fourteen",
	22: "fifteen",
	23: "sixteen",

	32: "seventeen",
	33: "eighteen",
	34: "nineteen",
	35: "twenty",
	36: "twentyone",
	37: "twentytwo",
	38: "twentythree",
	39: "twentyfour",
	40: "twentyfive",
	41: "twentysix",
	42: "twentyseven",
	43: "twentyeight",
	44: "twentynine",
	45: "thirty",
	46: "thirtyone",
	47: "thirtytwo",
	}


class Controller:

	 def __init__(self):
	 	self.midi_id
	 	self.cc 
	 	self.data2



# class KnobPush():
# 	midi_id = 144 
# 	one = Input(midi_id, 0)
# 	two = Input(midi_id, 1)
# 	three = Input(midi_id, 2)
# 	four = Input(midi_id, 3)
# 	five = Input(midi_id, 4)
# 	six = Input(midi_id, 5)
# 	seven = Input(midi_id, 6)
# 	eight = Input(midi_id, 7)	
# 	nine = Input(midi_id, 24)
# 	ten = Input(midi_id, 25)
# 	eleven = Input(midi_id, 26)
# 	tweleve = Input(midi_id, 27)
# 	thirteen = Input(midi_id, 28)
# 	fourteen = Input(midi_id, 29)
# 	fifteen  = Input(midi_id, 30)
# 	sixteen = Input(midi_id, 31)