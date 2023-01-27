
class Input:

	def __init__(self, midi_id, cc):
		self.midi_id = midi_id
		self.cc = cc



knobs = [(176, i) for i in range(1, 9)]
knob_push_cc = [i for i in range(0, 8)] + [k for k in range(24, 32)]
buttons_one = [i for i in range(8, 24)]
buttons_two = [i for i in range(32, 48)]
# buttons_two = [(144, i) for i in range(32, 48)]
buttons = buttons_one + buttons_two
knob_ccs = [i for i in range(1, 9)] + [k for k in range(11, 19)]
class Knob():
	midi_id = 176
	one = Input(midi_id, 1)
	two = Input(midi_id, 2)
	three = Input(midi_id, 3)
	four = Input(midi_id, 4)
	five = Input(midi_id, 5)
	six = Input(midi_id, 6)
	seven = Input(midi_id, 7)
	eight = Input(midi_id, 8)
	sixteen = Input(midi_id, 18)


class KnobPush():
	midi_id = 144 
	one = Input(midi_id, 0)
	two = Input(midi_id, 1)
	three = Input(midi_id, 2)
	four = Input(midi_id, 3)
	five = Input(midi_id, 4)
	six = Input(midi_id, 5)
	seven = Input(midi_id, 6)
	eight = Input(midi_id, 7)	
	nine = Input(midi_id, 24)
	ten = Input(midi_id, 25)
	eleven = Input(midi_id, 26)
	tweleve = Input(midi_id, 27)
	thirteen = Input(midi_id, 28)
	fourteen = Input(midi_id, 29)
	fifteen  = Input(midi_id, 30)
	sixteen = Input(midi_id, 31)

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