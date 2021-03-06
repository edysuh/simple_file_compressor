# Title:	huff.py
# Author:	Ethan Suh
# Date:		Tuesday, October 20, 2015 10:07:03 PM
# Info:		HW1 for EECS 214

from sys import * 
from bit_io import *
from tree import *

def get_arg():
	if len(argv) != 3:
		stderr.write('Usage: {} INFILE OUTFILE\n'.format(argv[0]))
		exit(2)
	
	infile = argv[1]
	outfile = argv[2]

	return infile, outfile

def convert_file_to_bytes(infile):
	reader = BitReader(infile)

	filesize = 0
	byte_list = []
	byte_freq = []
	
	while True:
		current_byte = reader.readbits(8)
	
		if current_byte == None:
			break
		if (current_byte in byte_list) == False:
			byte_list.append(current_byte)
			byte_freq.append(1)
		else:
			byte_freq[byte_list.index(current_byte)] += 1

		filesize += 1
	
	reader.close()

	return filesize, byte_list, byte_freq

def create_forest(byte_list, byte_freq):
	forest = []
	
	for i in range(0, len(byte_list)):
		new_tree = Tree()
		forest.append(new_tree)
		new_tree.set_data(byte_list[i])
		new_tree.set_weight(byte_freq[i])
	
	i = j = 0
	
	while len(forest) > 1:
		new_tree = Tree()
		forest[0].set_binary_code(0)
		forest[1].set_binary_code(1)
		new_tree.add_branch(forest[0])
		new_tree.add_branch(forest[1])
		new_tree.set_weight(forest[0].weight + forest[1].weight)
	
		j = 0
	 
		while j < len(forest):
			if new_tree.weight < forest[j].weight:
				forest.insert(j, new_tree)
				forest.pop(0)
				forest.pop(0)
				break
			elif j == len(forest)-1: 
				forest.append(new_tree)
				forest.pop(0)
				forest.pop(0)
			j += 1
	
	huffman_tree = forest[0]

	return huffman_tree

def set_binary(tree, leaf_val, leaf_bin, leaf_bin_count):
	if not tree.branches:
		leaf_val.append(tree.data)
		leaf_bin.append(int(tree.binary_path, 2))
		leaf_bin_count.append(len(tree.binary_path))
	else:
		tree.branches[0].set_binary_path(tree.binary_path)
		tree.branches[1].set_binary_path(tree.binary_path)
		set_binary(tree.branches[0], leaf_val, leaf_bin, leaf_bin_count)
		set_binary(tree.branches[1], leaf_val, leaf_bin, leaf_bin_count)

def gen_huff_file(filesize, huffman_tree, leaf_val, leaf_bin, leaf_bin_count, infile, outfile):
	reader2 = BitReader(infile)
	writer = BitWriter(outfile)
	
	writer.writebits(filesize, 32)

	todo = []
	todo.append(huffman_tree)
	
	serialized = ''
	
	while len(todo) > 0:
		current_node = todo.pop()
		if not current_node.branches:
			serialized += '1'
			serialized += str(current_node.data)
			writer.writebit(1)
			writer.writebits(current_node.data, 8)
		else:
			serialized += '0'
			writer.writebit(0)
			todo.append(current_node.branches[1])
			todo.append(current_node.branches[0])
	
	while True:
		current_byte = reader2.readbits(8)
	
		if current_byte == None:
			break
	
		for i in range(len(leaf_val)):
			if current_byte == leaf_val[i]:
				writer.writebits(leaf_bin[i], leaf_bin_count[i])
				break
	
	reader2.close()
	writer.close()

def main():
	infile, outfile = get_arg()

	filesize, byte_list, byte_freq = convert_file_to_bytes(infile)
	byte_freq, byte_list = (list(t) for t in zip(*sorted(zip(byte_freq, byte_list))))
	byte_freq.pop(0), byte_list.pop(0)

	huffman_tree = create_forest(byte_list, byte_freq)
	
	leaf_val = []
	leaf_bin = []
	leaf_bin_count = []

	set_binary(huffman_tree, leaf_val, leaf_bin, leaf_bin_count)

	gen_huff_file(filesize, huffman_tree, leaf_val, leaf_bin, leaf_bin_count, infile, outfile)

main()
