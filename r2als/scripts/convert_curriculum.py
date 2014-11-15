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

from r2als.libs.logs import Log
l = Log('convert_curriculum').getLogger()


class CsvToModel:

	def __init__(self):
		self.COMMENT_SYMBOL = "#"
		self.SPLIT_SYMBOL = ":"
		self.MULTI_FIELD_SYMBOL = "*"
		# Format of head
		self.HEADER_LISTS = ['faculty','department','year','required_num_year','num_semester','*subject_groups','*branches','*categories','*prerequisites']
		# END_HEADER = "END_HEADER"

	def hasComment(self, str):
		if str.find(self.COMMENT_SYMBOL) < 0:
			return False
		else:
			return True

	def hasCommentRow(self, row):
		for r in row:
			if self.hasComment(r):
				return True
		return False

	def hasMultiField(self, str):
		if str.find(self.MULTI_FIELD_SYMBOL) < 0:
			return False
		else:
			return True

	def removeMultiFieldSymbol(self, str):
		return re.sub('['+self.MULTI_FIELD_SYMBOL+']', '', str)

	def validateFormatCurriculumFile(self, text, index):
		for i in range(len(self.HEADER_LISTS)):
			if text == self.HEADER_LISTS[i] and index == i:
				return True
		return False

	# def validateStudiedGroup(self, studied_groups, str):
	# 	for studied_group in studied_groups:
	# 		if str == studied_group :
	# 			return True
	# 	return False

	def process(self, url, has_header):
		subjects = []
		info = {}
		multiField = []
		if has_header :
			shift_row = len(self.HEADER_LISTS)
		else:
			shift_row = 0

		with open(url, 'r',encoding="utf-8") as f:
			reader = csv.reader(f)
			i = 0
			for row in reader:
				if i < shift_row:
					if self.validateFormatCurriculumFile(row[0], i) == False:
						l.error("Header line "+str(i+1)+" must is '"+self.HEADER_LISTS[i]+"'")
						return None
					else :
						if self.hasMultiField(self.HEADER_LISTS[i]):
							elements = row[1].split(self.SPLIT_SYMBOL)
							header = self.removeMultiFieldSymbol(self.HEADER_LISTS[i])
							info[header] = []
							for element in elements:
								info[header].append(element)
						else:
							info[self.HEADER_LISTS[i]] = row[1]


				elif i == shift_row :
					# keys
					for j in range(len(row)):
						multiField.append(self.hasMultiField(row[j]))
						row[j] = self.removeMultiFieldSymbol(row[j])
					keys = row
				elif self.hasCommentRow(row):
					l.info("Importing : " + row[0])
				else :
					#value
					tmp = {}
					for j in range(len(keys)):
						if row[j] != '':
							if multiField[j] == True :
								tmp[keys[j]] = []
								elements = row[j].split(self.SPLIT_SYMBOL)
								for element in elements:
									tmp[keys[j]].append(element)
							else :
								if has_header and keys[j] == 'studied_group' and row[j] not in info['studied_groups']:
									l.error("studied group : '"+row[j]+"'isn't allowed in header list("+str(info['studied_groups'])+")")
								tmp[keys[j]] = row[j]
					subjects.append(tmp)
				i = i + 1
		return {
			'subjects': subjects,
			'info': info
		}

def printInstruction():
	print("Convert csv file of curriculum to object")
	print("usage: convert_curriculum.py [path]")

if __name__ == '__main__':
	#print(len(sys.argv))



	if len(sys.argv) != 2:
		printInstruction()
		exit()

	path = sys.argv[1]

	f_out = open('curriculum.json', 'w')

	pp = pprint.PrettyPrinter(stream=f_out,indent=4)

	lists = CsvToModel().process(path, True)
	pp.pprint(lists)
	f_out.close()
