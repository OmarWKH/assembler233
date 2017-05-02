# refer to Hack's assmebler.py for original what-if/to-do
from pathlib import Path
import re
from contextlib import contextmanager

def assemble_to_hex(asm_file):
	return binary_to_hex(assemble(asm_file))

def binary_to_hex(binary_text):
	output = ''
	for line in valid_lines(binary_text):
		translation = format(int(line, 2), '04x')
		output += (translation + '\n')
	return output

def assemble(asm_text):
	symbols = {}
	#symbols.update(find_labels(asm_text))
	output = ''
	count = 0
	for line in valid_lines(asm_text):
		if not line.startswith('('):
			instruction = translate(line, symbols, count)
			output += (instruction + '\n')
			count += 1
	return output
	
def valid_lines(text):
	for line in text.splitlines():
		if not line.isspace():
			line = line.strip()
			if not is_comment(line):
				yield line

def find_labels(asm_text):
	labels = {}
	count = 0
	for line in valid_lines(asm_text):
		match = re.match(r'[(](?P<label>[a-zA-Z_.$:][\w.$:]*)[)]', line)
		if match:
			label = match.group('label')
			labels[label] = count
		else:
			count += 1
	return labels

def translate(instruction, symbols, count):
	instruction = instruction.split()
	f = type_function(instruction[0])
	try:
		translation = f(instruction, symbols, count)
		return f(instruction, symbols, count)
	except Exception as e:
		print('Error on line', count, ': ', instruction)
		raise e

def type_function(x):
	return {
		'ADD': translate_r,
		'RSUB': translate_r,
		'SLT': translate_r,
		'AND': translate_r,
		'OR': translate_r,
		'XOR': translate_r,
		'NOR': translate_r,
		'ADDI': translate_i,
		'RSUBI': translate_i,
		'SLTI': translate_i,
		'ANDI': translate_i,
		'ORI': translate_i,
		'XORI': translate_i,
		'NORI': translate_i,
		'JR': translate_jr,
		'LW': translate_lw,
		'SW': translate_sw,
		'BEQZ': translate_b,
		'BNEZ': translate_b,
		'SET': translate_j,
		'SSET': translate_j,
		'J': translate_j,
		'JAL': translate_j
	}[x.upper()]

def opcode(x):
	return {
		'ADD': 0,
		'RSUB': 0,
		'SLT': 0,
		'AND': 1,
		'OR': 1,
		'XOR': 1,
		'NOR': 1,
		'ADDI': 4,
		'RSUBI': 5,
		'SLTI': 6,
		'ANDI': 8,
		'ORI': 9,
		'XORI': 10,
		'NORI': 11,
		'JR': 3,
		'LW': 16,
		'SW': 20,
		'BEQZ': 24,
		'BNEZ': 25,
		'SET': 28,
		'SSET': 29,
		'J': 30,
		'JAL': 31
	}[x.upper()]

def fcode(x):
	return {
		'ADD': 0,
		'RSUB': 1,
		'SLT': 2,
		'AND': 0,
		'OR': 1,
		'XOR': 2,
		'NOR': 3
	}[x.upper()]

def translate_r(instruction, symbols, count):
	op = opcode(instruction[0])
	rd = int(instruction[1])
	rs = int(instruction[2])
	rt = int(instruction[3])
	f = fcode(instruction[0])
	return "{0:05b}{1:03b}{2:03b}{3:03b}{4:02b}".format(op, rs, rd, rt, f)

def translate_i(instruction, symbols, count):
	op = opcode(instruction[0])
	rd = int(instruction[1])
	rs = int(instruction[2])
	im5 = int(instruction[3])
	return "{0:05b}{1:03b}{2:03b}{3:05b}".format(op, rs, rd, im5 % (1 << 5))

def translate_jr(instruction, symbols, count):
	op = opcode(instruction[0])
	rs = int(instruction[1])
	return "{0:05b}{1:03b}00000000".format(op, rs)

def translate_lw(instruction, symbols, count):
	op = opcode(instruction[0])
	rd = int(instruction[1])
	rs = int(instruction[2])
	return "{0:05b}{1:03b}{2:03b}00000".format(op, rs, rd)

def translate_sw(instruction, symbols, count):
	op = opcode(instruction[0])
	rt = int(instruction[1])
	rs = int(instruction[2])
	return "{0:05b}{1:03b}000{2:03b}00".format(op, rs, rt)

def translate_b(instruction, symbols, count):
	op = opcode(instruction[0])
	rs = int(instruction[1])
	# label = instruction[2]
	# im8 = symbols[label]
	im8 = int(instruction[2])
	return "{0:05b}{1:03b}{2:08b}".format(op, rs, im8 % (1 << 8))

def translate_j(instruction, symbols, count):
	op = opcode(instruction[0])
	im11 = int(instruction[1])
	'''
	im11 = 0
	if op >= 30: # j or jal
		label = instruction[1]
		im11 = symbols[label]
	else:
		im11 = int(instruction[1])
	'''
	
	return "{0:05b}{1:011b}".format(op, im11 % (1 << 11))

def is_comment(instruction):
	return instruction.startswith('//') or instruction.startswith('#')

class LanguageError(Exception):
	pass