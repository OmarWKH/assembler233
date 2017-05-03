# refer to Hack's assmebler.py for original what-if/to-do
import io
import re
from contextlib import contextmanager

def assemble_to_hex(asm_input_stream, hex_output_stream):
	binary = assemble(asm_input_stream, io.StringIO())
	return binary_to_hex(binary, hex_output_stream)

def binary_to_hex(binary_input_stream, hex_output_stream):
	binary_input_stream.seek(0) # start from the beginning
	
	for line in binary_input_stream.readlines():
		translation = format(int(line, 2), '04x')
		hex_output_stream.write(translation + '\n')
	
	binary_input_stream.close()
	return hex_output_stream

def assemble(asm_input_stream, binary_output_stream):
	asm_input_stream.seek(0) # start from the beginning
	
	symbols = {
		'R0':		0,
		'R1':		1,
		'R2':		2,
		'R3':		3,
		'R4':		4,
		'R5':		5,
		'R6':		6,
		'R7':		7,
	}
	symbols.update(find_labels(asm_input_stream))
	
	count = 0
	for line in valid_lines(asm_input_stream):
		if not line.startswith('('):
			try:
				instruction = translate(line, symbols, count)
				binary_output_stream.write(instruction + '\n')
				count += 1
			except Exception as e:
				message = 'Error at line {0}: {1}'.format(count, line)
				raise LanguageError(message)
	
	asm_input_stream.close()
	return binary_output_stream
	
def valid_lines(input_stream):
	for line in input_stream:
		if not line.isspace():
			line = line.strip()
			if not is_comment(line):
				yield line
	input_stream.seek(0) # go back to start of stream

def find_labels(asm_input_stream):
	labels = {}
	count = 0
	for line in valid_lines(asm_input_stream):
		match = re.match(r'[(](?P<label>[a-zA-Z_.$:][\w.$:]*)[)]', line)
		if match:
			label = match.group('label')
			labels[label] = count
		else:
			count += 1
	return labels

def register(symbols, symbol):
	return symbols[symbol.upper()]

def translate(instruction, symbols, count):
	instruction = instruction.split()
	f = type_function(instruction[0])
	translation = f(instruction, symbols, count)
	return f(instruction, symbols, count)

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
	rd = register(symbols, instruction[1])
	rs = register(symbols, instruction[2])
	rt = register(symbols, instruction[3])
	f = fcode(instruction[0])
	return "{0:05b}{1:03b}{2:03b}{3:03b}{4:02b}".format(op, rs, rd, rt, f)

def translate_i(instruction, symbols, count):
	op = opcode(instruction[0])
	rd = register(symbols, instruction[1])
	rs = register(symbols, instruction[2])
	im5 = int(instruction[3])
	return "{0:05b}{1:03b}{2:03b}{3:05b}".format(op, rs, rd, im5 % (1 << 5))

def translate_jr(instruction, symbols, count):
	op = opcode(instruction[0])
	rs = register(symbols, instruction[1])
	return "{0:05b}{1:03b}00000000".format(op, rs)

def translate_lw(instruction, symbols, count):
	op = opcode(instruction[0])
	rd = register(symbols, instruction[1])
	rs = register(symbols, instruction[2])
	return "{0:05b}{1:03b}{2:03b}00000".format(op, rs, rd)

def translate_sw(instruction, symbols, count):
	op = opcode(instruction[0])
	rt = register(symbols, instruction[1])
	rs = register(symbols, instruction[2])
	return "{0:05b}{1:03b}000{2:03b}00".format(op, rs, rt)

def translate_b(instruction, symbols, count):
	op = opcode(instruction[0])
	rs = register(symbols, instruction[1])
	label = instruction[2]
	target = symbols[label]
	im8 = relative_count(count, target)
	return "{0:05b}{1:03b}{2:08b}".format(op, rs, im8 % (1 << 8))

def translate_j(instruction, symbols, count):
	op = opcode(instruction[0])
	im11 = 0
	if op >= 30: # j or jal
		label = instruction[1]
		target = symbols[label]
		im11 = relative_count(count, target)
	else:
		im11 = int(instruction[1])
	
	return "{0:05b}{1:011b}".format(op, im11 % (1 << 11))

def relative_count(current, target):
	return target - current;
	
def is_comment(instruction):
	return instruction.startswith('//') or instruction.startswith('#')

class LanguageError(Exception):
	pass
