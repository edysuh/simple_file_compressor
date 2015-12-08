# Title:	puff.py
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

def recreate_tree(infile):
	reader = BitReader(infile)

	filesize = reader.readbits(32)

	top_of_tree = Tree()

	todo = []
	todo.append(top_of_tree)
	
	filestart = 0

	while len(todo) > 0:
		current_bit = reader.readbit()
		print(current_bit)
		filestart += 1
	
		current_node = todo.pop()
	
		if current_bit == 0:
			new_branch0 = Tree()
			new_branch1 = Tree()
			new_branch0.set_binary_code(0)
			new_branch1.set_binary_code(1)
			current_node.add_branch(new_branch0)
			current_node.add_branch(new_branch1)
			todo.append(current_node.branches[1])
			todo.append(current_node.branches[0])
			print(todo)
		elif current_bit == 1:
			current_node.set_data(reader.readbits(8))
			filestart += 8
			print(current_node.data)
			print("do leaves have branches?:", current_node.branches)
			print(todo)

	reader.close()
	
	return top_of_tree, filesize, filestart

def set_binary(tree, leaf_val, leaf_bin, leaf_bin_count):

	if not tree.branches:
		print('LEAF:', 'data=', tree.data, 'weight=', tree.weight,'binarypath=',  tree.binary_path)
		leaf_val.append(tree.data)
		leaf_bin.append(int(tree.binary_path, 2))
		leaf_bin_count.append(len(tree.binary_path))
	else:
		print('data=', tree.data, 'weight=', tree.weight,'binarypath=',  tree.binary_path)
		tree.branches[0].set_binary_path(tree.binary_path)
		tree.branches[1].set_binary_path(tree.binary_path)
		set_binary(tree.branches[0], leaf_val, leaf_bin, leaf_bin_count)
		set_binary(tree.branches[1], leaf_val, leaf_bin, leaf_bin_count)

def gen_puff_file(huffman_tree, infile, filestart, filesize, outfile):
	reader = BitReader(infile)
	reader.readbits(32 + filestart)
	writer = BitWriter(outfile)

	current_node = huffman_tree

	i = 0
	while i < filesize:
		if not current_node.branches:
			writer.writebits(current_node.data, 8)
			current_node = huffman_tree
			i += 1
		else:
			current_bit = reader.readbit()
			current_node = current_node.branches[current_bit]
	
	reader.close()
	writer.close()

def main():
	infile, outfile = get_arg()
	huffman_tree, filesize, filestart = recreate_tree(infile)
	
	leaf_val = []
	leaf_bin = []
	leaf_bin_count = []

	set_binary(huffman_tree, leaf_val, leaf_bin, leaf_bin_count)
	
	for i in range(len(leaf_val)):
		print('leaf_val=', leaf_val[i], 'leaf_bin=', leaf_bin[i], 'count=', leaf_bin_count[i])

	print(filestart, filesize)
	gen_puff_file(huffman_tree, infile, filestart, filesize, outfile)

main()
