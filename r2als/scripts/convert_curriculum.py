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
#
import re
import pprint

class CsvToModel:

	def validateComment(self, str):
		if str.find('#') < 0:
			return None
		else:
			return str
			# return re.sub(r'#', '', str)

	def removeSpecialChar(self, str):
		return re.sub('[\n\"]', '', str)

	def process(self):
		f_in= open('curriculum.csv', 'r')

		keys_string = f_in.readline()
		keys = keys_string.split(',')
		for i in range(len(keys)):
			keys[i] = self.removeSpecialChar(keys[i])

		# for key in keys:
		# 	print(key)
		lists = []
		for line in f_in:
			if self.validateComment(line) == None:
				values = line.split(',')
				tmp = {}
				for i in range(len(keys)):
					values[i] = self.removeSpecialChar(values[i])
					tmp[keys[i]] = values[i]
				lists.append(tmp)
			else:
				print(line)
		return lists


if __name__ == '__main__':
	f_out = open('curriculum.json', 'w')

	pp = pprint.PrettyPrinter(stream=f_out,indent=4)

	c2m = CsvToModel()
	lists = c2m.process()
	pp.pprint(lists)

	# pp.pprint(dataobject, logFile)

	#with open('curriculum.json', 'w') as out

	# pp.pprint(lists)

	# for v in values:
	# 	print(v+" ",end="")
	# print("")

	#
	# f_out.write("[")
	# for line in f_in:
	# 	f_out.write("{")
	# 	values = line.split(',')
	# 	for i in range(len(keys)):
	# 		if values[i] == "" and validateComment(values[i]) == None:
	# 			f_out.write("\t"+str(keys[i])+" : ''"+str(values[i])+"''")
	# 		else:
	# 			f_out.write(values[i])
	# 		# last loop
	# 		if len(keys) - i != 1:
	# 			f_out.write(",")
	#
	# 	#f_out.write(line, end='')
	# 	f_out.write("},")
	# f_out.write("]")
