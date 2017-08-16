# IN DEVELOPMENT; incomplete and possibly buggy.

# DESCRIPTION
# Generates (recombobulates) gibberish from a database of word pairing statistics. See comments at the top of getCharStats.py to get such a database. Writes results to gib.txt

# USAGE
# thisScript.py inputDatabase.mkvch [How many words to generate]

# TO DO
# use sys.argv[1] for input file.
# if no match found in loop in prior letter match iteration, terminate word.
# after ' ' termination, pick new random first letter.
# make range of random next letter pair pick reflect total of num stats in second pair (after ,) in src database.
# make it write to files (instead of stdout) after algo base developed (stdout will fail on some unicode chars.)

import sys			# comment out for release; only for development.
import itertools
import codecs		# allows opening a file with utf-8 
from random import randint

# read database into an array of lists or summat wut format
import csv
with codecs.open('test.mkvch', 'r', encoding='utf-8') as inputFile:
    reader = csv.reader(inputFile)
    data = list(reader)		# I've verified that will write back to a file the exact same structure of a source database, if parsed correctly.
inputFile.close

# seed mustStartWith var with space ' '
mustStartWith = ' '
	# loop as many times as genNumPhonemes var:
genNumPhonemes = 25
mustStartWithListMatches = list()

# open gibberish generation output file for writing; TO DO: generate this file name based on source database and date?
outputFile = codecs.open('wut.txt', 'w', encoding='utf-8')

# find pair that starts with mustStartWith; and it may turn out that using for loops is the most legible and fast way to do this, re https://stackoverflow.com/a/1156143/1397555 :
			# e.g. data[0] is "printed" by python as: ('a', 'g')
			# -- and data[0][0] is: 'a' and data[0][1] is: 'g'
foo = 'bor'      # frequencySum = (frequencySum + str(idx))
frequencySum = 0
for pair, idx in data:            # e.g. a list within the data list, ('a', 'g')
	partA = pair[0]               # the first character in pair; pair[0][0] + pair[0][1] would be both.
	if partA == mustStartWith:
		mustStartWithListMatches.append(partA); frequencySum = (frequencySum + int(idx)); outputFile.write('appended partA value \'' + partA + '\' to array from pair \'' + pair + '\' with frequency ' + idx + '\nfrequencySum: ' + str(frequencySum) + '\n')
	# TO DO:
	# re-seed mustStartWith using second letter of that written pair
	# previous two steps in loop until loop ends

mustStartWithListMatchesLength = len(mustStartWithListMatches)
# outputFile.write('\n\nvalues in mustStartWithListMatches:\n')
# for element in mustStartWithListMatches:
#     outputFile.write(element + '\n')

outputFile.close

# print(mustStartWithListMatchesLength)