# IN DEVELOPMENT; Essential functionalty complete (I think)! See "TO DO" section.

# DESCRIPTION
# Generates (recombobulates) gibberish from a database of word pairing statistics. See comments at the top of getCharStats.py to get such a database. Writes results to gib.txt

# USAGE
# thisScript.py inputDatabase.mkvch [How many words to generate]

# TO DO
# use sys.argv[1] for input file.
# if no match found in loop in prior letter match iteration, terminate word.
# make it write to files (instead of stdout), as stdout will fail on some unicode chars.

import sys			# comment out for release; only for development.
import itertools
import codecs		# allows opening a file with utf-8 
from random import randint

# read database into an array of lists or summat wut format
import csv
with codecs.open('databases_corpora/TheJabberwocky.mkvch', 'r', encoding='utf-8') as inputFile:
    reader = csv.reader(inputFile)
    data = list(reader)		# I've verified that will write back to a file the exact same structure of a source database, if parsed correctly.
inputFile.close

# open gibberish generation output file for writing; TO DO: generate this file name based on source database and date?
logFile = codecs.open('gibGen_py_log.txt', 'w', encoding='utf-8')

recombobulation = ''
# seed mustStartWith var with space ' '
mustStartWith = ' '
genNumPhonemes = 13500
frequencySum = 0
matchedPairs = list()      # This will be a list of lists!
# loop as many times as genNumPhonemes var:
for i in range(0, genNumPhonemes):
    logFile.write('---------- GENERATING phoneme------------\n')
    # find pair that starts with mustStartWith; and it may turn out that using for loops is the most legible and fast way to do this, re https://stackoverflow.com/a/1156143/1397555 :
    			# e.g. data[0] is "printed" by python as: ('a', 'g')
    			# -- and data[0][0] is: 'a' and data[0][1] is: 'g'
    for pair, idx in data:            # e.g. a list within the data list, ('a', 'g')
    	partA = pair[0]               # the first character in pair; pair[0][0] + pair[0][1] would be both.
    	if partA == mustStartWith:
    		frequencySum = (frequencySum + int(idx)); tmpTuple = [pair, frequencySum]; matchedPairs.append(tmpTuple); logFile.write('appended partA value \'' + partA + '\' from pair \'' + pair + '\' with frequency ' + idx + '\nfrequencySum: ' + str(frequencySum) + '\n')
    # With matchedPairs populated from iterated items pair, randomly pick one of the pairs accounting for statistical frequency of pair occurances indexed from .mkvch database. 
    PRND = randint(0, frequencySum)
    # Reset frequencySum for the following for loop:
    frequencySum = 0
    logFile.write('Selected num ' + str(PRND) + ' from range 0,' + str(frequencySum) + '\n')
    for idx, pair in enumerate(matchedPairs):       # TO DO: learn, would a third var listing there get the second list item in the list at matchedPairs(idx)?
        if pair[1] >= PRND:
            pickedPair = str( matchedPairs[ (idx - 1) ] ); nextLetter = pickedPair[3]; logFile.write('! ----------- PICK for pair ' + pickedPair + ' at num ' + str(pair[1]) + '!\n'); recombobulation = (recombobulation + nextLetter); mustStartWith = nextLetter; break
            # ; print(pickedPair + ' \'' + nextLetter + '\'')
    # reset frequencySum for the next iteration of the outmost loop:
    frequencySum = 0
# for loop ends

logFile.close

print(recombobulation)

# print(mustStartWithListMatchesLength)