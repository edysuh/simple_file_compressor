# simple_file_compressor

huff.py:

	convert_file_to_bytes(infile):
		- first we read the text file using the bit_io module
		- we count the number of bytes in the original text file and return it as filesize
		- we have two lists, one for byte_list, which holds the character data, and one for the frequency of the character in the text file (having two lists is slower than using the character code as a list index of its frequencies, but since it still ran in a reasonable amount of time, but we left it is as personal preference)
	
	create_forst(byte_list, byte_freq):
		- we create a tree node for each character using the class Tree declared in tree.py
		- we then go through the algorithm of creating a huffman tree, creating branches by pairing the lowest weight nodes, re-inserting it into our list of nodes, sorted by weight so that it will be paired when it is the lowest weight node again
		- we return the top of the tree as our huffman tree

	set_binary(tree, leaf_val, leaf_bin, leaf_bin_count):
		- set_binary() is a recursive function that takes the top of the huffman tree and three lists as arguments
		- it tranverses the tree by recursion, calling itself twice for each branch at every non-leaf node, while appending to the binary path, 0 for left branch, 1 for right branch
		- at each leaf, we store the character value, the binary code for the huffman tree, and the length of the binary code necessary for encoding with bit_io

	gen_huff_file(filesize, huffman_tree, leaf_val, leaf_bin, leaf_bin_count, infile, outfile):
		- writes the actual .huff file, starting with the 32 bits for the filesize, the level-order serialization used for decoding, and the encoded file using our huffman tree

puff.py:

	recreate_tree(infile):
		- the first 32 bits are the filesize
		- we have a todo queue that holds the child nodes of each node until we are ready to place it into the tree
		- recreates the barebone structure of the tree with the character data at the leaves
		- returns the top of the tree, the filesize, number of bits (the filesize and serialization) to skip when rereading the encoded file

	set_binary(tree, leaf_val, leaf_bin, leaf_bin_count):
		- this function is identical to the one in huff.py, but is rather used to fill in the rest of the node data in the tree

	gen_puff_file(huffman_tree, infile, filestart, filesize, outfile):
		- reads a bit of the encoded file at a time and follows the path down the tree until it hits a leaf and writes the character data 
		- continues to path down the tree for each prefix code until the end of the filesize


for testing, we generally just used print statements in each function confirming that the huffman tree was properly created, that prefix codes were actually unique, that puff was recreating the same tree and list of prefix codes, etc. 

our code currently still has a bug that skipped over one character ("7") in the decoded file when compared to the original hamlet.txt file. this issue continues to allude us despite our attempts at debugging the problem. 
