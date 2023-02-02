import device
from leds import Leds 

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

	mapping = {
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

		109: "seventeen",
		110: "eighteen",
		60: "nineteen",
		61: "twenty",
		62: "twentyone",
		63: "twentytwo",
		64: "twentythree",
		65: "twentyfour",
		107: "twentyfive",
		108: "twentysix",
		111: "twentyseven",
		112: "twentyeight",
		106: "twentynine",
		113: "thirty",
		114: "thirtyone",
		115: "thirtytwo",

		129: "thirtythree",
		13: "thirtyfour",
		80: "thirtyfive",
		81: "thirtysix",
		82: "thirtyseven",
		83: "thirtyeight",
		84: "thirtynine",
		85: "forty",
		127: "fortyone",
		128: "fortytwo",
		131: "fortythree",
		131: "fortyfour",
		126: "fortyfive",
		133: "fortysix",
		134: "fortyseven",
		135: "fortyeight",
	}

	mapping_b = {
		89: "one_b",
		90: "two_b",
		40: "three_b",
		41: "four_b",
		42: "five_b",
		43: "six_b",
		44: "seven_b",
		45: "eight_b",
		87: "nine_b",
		88: "ten_b",
		91: "eleven_b",
		92: "twelve_b",
		86: "thirteen_b",
		93: "fourteen_b",
		94: "fifteen_b",
		95: "sixteen_b",
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
