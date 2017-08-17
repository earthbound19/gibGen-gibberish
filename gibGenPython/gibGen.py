# IN DEVELOPMENT; Essential functionalty complete (I think)! See "TO DO" section.

# DESCRIPTION
# Generates (recombobulates) gibberish from a database of word pairing statistics. See comments at the top of getCharStats.py to get such a database. Writes results to gib.txt

# USAGE
# thisScript.py -s [source database.mkvch] -c [count of words to generate]

# NOTES: This may only work with python3. Also, the only source database I have producing useful output at this writing is databases/TheJabberwocky.mkvch, at this writing. TO DO: fix that: maybe by having this work statistically on trigrams instead of bigrams.

# TO DO
# if no match found in loop in prior letter match iteration, terminate word (print a space), and randomly pick a new letter to start another word. AND/OR (potentially two different problems, and maybe only this second one is a valid problem), whatever condition leads to the problem in the log noted in this writing in charactersThatBreakIAEgibGen.txt -- fix that.
# make it write to files (instead of stdout), as stdout will fail on some unicode chars.
# make log file optional (which means make a log function and refactor to pass it strings conditionally)
# dump recombobulation var to file when it gets to certain huge size, then continue filling it.
# make gibberish dump file name partly based on timestamp.

import sys			# comment out for release; only for development.
import itertools
import codecs		# allows opening a file with utf-8 
from random import randint
import csv          # to allow reading database into an array of lists or summat wut format
import argparse     # to parse terminal arguments

# Set up and make use of command line arguments; use defaults if none passed.
argParser = argparse.ArgumentParser()
argParser.add_argument("-s", "--source", help="source .mkvch database filename")
argParser.add_argument("-c", "--count", help="how many letter groups to create")
args = argParser.parse_args()
if args.source:
    print('Source db ' + args.source + ' specified.')
else:
    args.source = 'databases/TheJabberwocky.mkvch'
if args.count:
    print('Letter groups to create number ' + args.count + ' specified.')
else:
    args.count = 1000

with codecs.open(args.source, 'r', encoding='utf-8') as inputFile:
    reader = csv.reader(inputFile)
    data = list(reader)		# I've verified that will write back to a file the exact same structure of a source database, if parsed correctly.
inputFile.close

# open gibberish generation output file for writing; TO DO: generate this file name based on source database and date?
logFile = codecs.open('gibGen_py_log.txt', 'w', encoding='utf-8')

recombobulation = ''
# seed mustStartWith var with space ' '
mustStartWith = ' '
genNumPhonemes = int(args.count)
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
        # FIX to go here? :
        if PRND == 0:
            logFile.write('ERROR: Oh teh noes! It picked zero! Something wrong . . .\n wheh matchedPairs len ' + str(pickedPair))
        if pair[1] >= PRND:
            pickedPair = str( matchedPairs[ (idx - 1) ] ); nextLetter = pickedPair[3]; logFile.write('! ----------- PICK for pair ' + pickedPair + ' at num ' + str(pair[1]) + '!\n'); recombobulation = (recombobulation + nextLetter); mustStartWith = nextLetter; break
            # ; print(pickedPair + ' \'' + nextLetter + '\'')
    # reset frequencySum for the next iteration of the outmost loop:
    frequencySum = 0
# for loop ends

logFile.close

# Write generated gibberish to file.
gibberFileName = 'gibber_out.txt'
gibberFile = codecs.open(gibberFileName, 'w', encoding='utf-8')
gibberFile.write(recombobulation)
gibberFile.close

print('\nO frabjous day!\nDONE. Wrote gibberish to ' + gibberFileName + '.\n')

# print(recombobulation)