# importing libraries
import os
import re
import sys
from collections import Counter

# creating a class merchant guide for galaxy
class Galaxy_convert:
    # Now creating a key value pair dictionary
	ROE = dict(
		I = 1,
		V = 5,
		X = 10,
		L = 50,
		C = 100,
		D = 500,
		M = 1000
	)
# function to convert the roman to the numbers
	@staticmethod
	def galaxy_convert_roman(symbols):
		if not Galaxy_convert.galaxy_check_roman(symbols):
			return None
		# getting the number value for Roman numerals
		numbers = [ Galaxy_convert.ROE[s] for s in symbols ]
		for i in range(len(numbers)-1):
			if numbers[i] < numbers[i+1]:
				numbers[i] = -numbers[i]
		return sum(numbers)

# function to check the roman numerals
	@staticmethod
	def galaxy_check_roman(sym_inp):
		'''

		:param symbols:
		:return: this returns the symbol for the repeating regular expression, this counts the counter and return the symbols
		'''
		if not sym_inp and not isinstance(sym_inp, str):
			return False
		# now getting the counter over the symbols
		galaxy_cnt = Counter(sym_inp)
		if galaxy_cnt['I'] > 3:
			return False
		if galaxy_cnt['X'] > 4 or (galaxy_cnt['X'] == 4 and not re.match(r'\w*XXX[IV]X', sym_inp)):
			return False
		if galaxy_cnt['C'] > 4 or (galaxy_cnt['C'] == 4 and not re.match(r'\w*CCC[IVXL]C', sym_inp)):
			return False
		if galaxy_cnt['M'] > 4 or (galaxy_cnt['M'] == 4 and not re.match(r'\w*MMM[IVXLCD]M', sym_inp)):
			return False
		if galaxy_cnt['D'] > 1 or galaxy_cnt['L'] > 1 or galaxy_cnt['V'] > 1:
			return False
		# Now checking the value for other set of the input symbols
		for i in range(len(sym_inp)-1):
			if sym_inp[i] == 'I' and not sym_inp[i+1] in ['I', 'V', 'X']:
				return False
			elif sym_inp[i] == 'X' and not sym_inp[i+1] in ['I', 'V', 'X', 'L', 'C']:
				return False
			elif sym_inp[i] == 'V' and not sym_inp[i+1] in ['I']:
				return False
			elif sym_inp[i] == 'L' and not sym_inp[i+1] in ['I', 'V' ,'X']:
				return False
			elif sym_inp[i] == 'D' and not sym_inp[i+1] in ['I', 'V', 'X', 'L', 'C']:
				return False
	# getting the value for symbols for the input file
		return True


class Galaxy_auto:
	"""
	This class traverses automatically, and works with the key value pair over the dictionary
	"""
	gm = {}

	def galaxy_put(self, key, subkey=None, value=None):
		if key and subkey and value:
			if key in self.gm:
				self.gm[key][subkey] = value
			else:
				self.gm[key] = { subkey: value }
		elif key and value:
			self.gm[key] = value
	# this is used to get the key value pairs for dictionary
	def galaxy_get(self, key, subkey=None):
		return self.gm.get(key) if not subkey else self.gm.get(key) and self.gm[key].get(subkey)


class Reader(Galaxy_auto):
	"""
	The reader here reads the data from the file, and gets the conversion for the data in the file
	"""

	default_answer = 'I have no idea what you are talking about'
	def __init__(self, glxy=None):
		self.glxy = glxy

    # function to take the input for the message and perform conversion
	def __call__(self, galaxy_msg):

		if not self.galaxy_is_question(galaxy_msg):
			self.galaxy_learn(galaxy_msg)
		else:
			ans = self.getting_answer(galaxy_msg)
			if hasattr(self.glxy, '__call__'):
				self.glxy(ans)
# check the input is question or not
	def galaxy_is_question(self, galaxy_msg):
		"""
		Is the input has how much or how many
		"""
		return galaxy_msg and re.match(r'how (?:much|many)', galaxy_msg)

	def galaxy_convert(self, galaxy_symbols):
		"""
		This converts the symbols to numbers
		"""
		if not galaxy_symbols or not isinstance(galaxy_symbols, list):
			return None
		roman = [ self.galaxy_get('NUMBERS', s) for s in galaxy_symbols if self.galaxy_get('NUMBERS') and s in self.galaxy_get('NUMBERS') ]
		return None if len(galaxy_symbols) != len(roman) else Galaxy_convert.galaxy_convert_roman(''.join(roman))

	def galaxy_learn(self, glxy_msg):
		"""
		This reads the message input and perform conversion
		"""
		if not glxy_msg or not isinstance(glxy_msg, str):
			return
		words = glxy_msg.split()
		if re.match(r'\w+ is [IVXL]',glxy_msg):
			self.galaxy_put('NUMBERS', words[0], words[-1])
		elif re.match(r'(?:\w+ )*\w+ is \d+ Credits', glxy_msg):
			# getting the credits
			symbols = re.findall(r'((?:\w+ )*)\w+ is \d+ Credits', glxy_msg)
			number = symbols and self.galaxy_convert(symbols[0].split())
			if number:
				self.galaxy_put('UNITS', words[-4], float(words[-2])/number)

	def getting_answer(self, glxy_msg):
		"""
		Reader gets the answer for the input
		"""
		if not glxy_msg or not isinstance(glxy_msg, str):
			return self.default_answer
		if re.match(r'how much', glxy_msg):
			symbols = re.findall(r'how much is ((?:\w+ )+)', glxy_msg)
			number = symbols and self.galaxy_convert(symbols[0].split())
			if number:
				return '{0} is {1}'.format(' '.join(symbols), number)
		elif re.match('how many Credits', glxy_msg):
			symbols = re.findall(r'how many Credits is ((?:\w+ )+)\w+', glxy_msg)
			number = symbols and self.galaxy_convert(symbols[0].split())
			#getting the matched units using the regular expression matching from the input
			glxy_matched_unit = re.findall(r'how many Credits is (?:(?:\w+ )+)(\w+)', glxy_msg)
			unit = glxy_matched_unit and glxy_matched_unit[0]
			if number and self.galaxy_get('UNITS', unit):
				return '{0} {1} is {2:.0f} Credits'.format(' '.join(symbols), unit, number*self.galaxy_get('UNITS', unit))
		return self.default_answer


@Reader
def process(msg):
	print(msg)


if __name__ == '__main__':
	Galaxy_file = sys.argv[1] if len(sys.argv) > 1 else 'input1.txt'
	if not os.path.isfile(Galaxy_file):
		print("Check the file name: {file}".format(file=Galaxy_file))
		exit(1)
	print(__doc__)
	# taking the file as the input
	with open(Galaxy_file) as f:
		for line in f:
			process(line)
