# Title:	htree.py
# Author:	Ethan Suh
# Date:		Tuesday, October 20, 2015 10:07:03 PM
# Info:		HW1 for EECS 214

class Tree:
	
	def __init__(self):
		self.weight = 0
		self.data = 0
		self.branches = []
		self.binary_code = -1
		self.binary_path = ''
	
	def set_data(self, data):
		self.data = data

	def set_weight(self, weight):
		self.weight = weight
	
	def add_branch(self, obj):
		self.branches.append(obj)

	def set_binary_code(self, b):
		self.binary_code = b

	def set_binary_path(self, s):
		self.binary_path = str(s) + str(self.binary_code)
