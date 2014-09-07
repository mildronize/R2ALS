#!/usr/bin/env python
'''
convert_curriculum
Description#   This program allows to convert csv file to JSON format for curriculum data
Developer#     Thada Wangthammang
'''
# The format of curriculum data
# First row is key in each elements of list of JSON Object
# Another rows are value in JSON Object

# Note: The string that includes with '#' is a description of data or comment

# * is multi field

import pprint
import csv
import re
import sys

COMMENT_SYMBOL = "#"
SPLIT_SYMBOL = ":"
MULTI_FIELD_SYMBOL = "*"

class CsvToModel:

	def hasComment(self, str):
		if str.find(COMMENT_SYMBOL) < 0:
			return False
		else:
			return True

	def hasCommentRow(self, row):
		for r in row:
			if self.hasComment(r):
				return True
		return False

	def hasMultiField(self, str):
		if str.find(MULTI_FIELD_SYMBOL) < 0:
			return False
		else:
			return True

	def removeMultiFieldSymbol(self, str):
		return re.sub('['+MULTI_FIELD_SYMBOL+']', '', str)

	# def removeSpecialChar(self, str):
	# 	return re.sub('[\n\"]', '', str)

	# def process(self):
	# 	f_in= open('curriculum.csv', 'r')
	#
	# 	keys_string = f_in.readline()
	# 	keys = keys_string.split(';')
	# 	for i in range(len(keys)):
	# 		keys[i] = self.removeSpecialChar(keys[i])
	#
	# 	# for key in keys:
	# 	# 	print(key)
	# 	lists = []
	# 	for line in f_in:
	# 		if self.validateComment(line) == None:
	# 			values = line.split(';')
	# 			tmp = {}
	# 			for i in range(len(keys)):
	# 				values[i] = self.removeSpecialChar(values[i])
	# 				tmp[keys[i]] = values[i]
	# 			lists.append(tmp)
	# 		else:
	# 			print(line)
	# 	return lists

	def process(self, url):
		lists = []
		multiField = []
		with open(url, 'r',encoding="utf-8") as f:
			reader = csv.reader(f)
			i = 0
			for row in reader:
				if i == 0:
					for j in range(len(row)):
						multiField.append(self.hasMultiField(row[j]))
						row[j] = self.removeMultiFieldSymbol(row[j])
					keys = row
				elif self.hasCommentRow(row):
					print(row)
				else :
					tmp = {}
					for j in range(len(keys)):
						if row[j] != '':
							if multiField[j] == True :
								tmp[keys[j]] = []
								elements = row[j].split(SPLIT_SYMBOL)
								for element in elements:
									tmp[keys[j]].append(element)
							else :
								tmp[keys[j]] = row[j]
					lists.append(tmp)
				i = i + 1
		return lists

def printInstruction():
	print("Convert csv file of curriculum to object")
	print("usage: convert_curriculum.py [path]")

if __name__ == '__main__':
	#print(len(sys.argv))

	if len(sys.argv) != 2:
		printInstruction()
		exit()

	#print(str(sys.argv))
	path = sys.argv[1]

	f_out = open('curriculum.json', 'w')

	pp = pprint.PrettyPrinter(stream=f_out,indent=4)

	lists = CsvToModel().process(path)
	pp.pprint(lists)
	f_out.close()
