import assembler233 as ass
from pathlib import Path
import argparse

def convert_file(input_file, suffix, convertF, output_file=None):
	input_file = Path(input_file)
	output_file = Path(output_file) if output_file else input_file.with_suffix('.' + suffix)

	input_stream = open(str(input_file), 'r')
	output_stream = open(str(output_file), 'w')
	convertF(input_stream, output_stream)
	
	input_stream.close()
	output_stream.close()
	
def assemble_file(asm_file, binary_file=None):
	convert_file(asm_file, 'binary', ass.assemble, binary_file)

def assemble_file_to_hex(asm_file, hex_file=None):
	convert_file(asm_file, 'hex', ass.assemble_to_hex, hex_file)

def binary_file_to_hex(binary_file, hex_file=None):
	convert_file(binary_file, 'hex', ass.binary_to_hex, hex_file)

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("input", help="the file to convert")
	parser.add_argument("-o", "--output", help="a file to write output to")
	parser.add_argument("-t", "--type", default="a2b",
						help="the type of conversion: [a2b] Assembly to binary, [a2h] Assembly to hex, [b2h] Binary to hex",
						choices=["a2b", "a2h", "b2h"])
	args = parser.parse_args()
	
	functions = {
		"a2b": assemble_file,
		"a2h": assemble_file_to_hex,
		"b2h": binary_file_to_hex
	}
	
	functions[args.type](args.input, args.output)
	