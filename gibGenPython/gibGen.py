# IN DEVELOPMENT; Essential functionalty complete (I think)! See "TO DO" section.

# DESCRIPTION
# Generates (recombobulates) gibberish from a database of word pairing statistics. See comments at the top of getCharStats.py to get such a database. Writes results to gib.txt

# USAGE
# thisScript.py -s [source database.mkvch] -c [count of words to generate]

# NOTES: This may only work with python3. Also, the only source database I have producing useful output at this writing is databases/TheJabberwocky.mkvch, at this writing. TO DO: fix that: maybe by having this work statistically on trigrams instead of bigrams.

# TO DO
# Well, shucks. It seems that bigram statistics alone including spaces isn't going to end words very often (like, extremely not often). Force statistical inflation of space character ' ' (for word endings) AND/OR compile word length stats and employ them for artificial cutoff. Maybe this wouldn't be a problem with trigrams. With bigrams it's clearly a problem.
# make log file optional (which means make a log function and refactor to pass it strings conditionally)
# dump recombobulation var to file when it gets to certain huge size, then continue filling it.
# make gibberish dump file name partly based on timestamp.

import sys            # comment out for release; only for development.
import itertools
import codecs        # allows opening a file with utf-8 
from random import randint
import csv          # to allow reading database into an array of lists or summat wut format
import argparse     # to parse terminal arguments

# Set up and make use of command line arguments; use defaults if none passed.
argParser = argparse.ArgumentParser()
argParser.add_argument("-d", "--database", help="database (source).mkvch database filename")
argParser.add_argument("-c", "--count", help="how many letter groups to create")
args = argParser.parse_args()
if args.database:
    print('Source db ' + args.database + ' specified.')
else:
    args.database = 'databases/IAE.mkvch'
if args.count:
    print('Letter groups to create number ' + args.count + ' specified.')
else:
    args.count = 1000

# READ database into var data
with codecs.open(args.database, 'r', encoding='utf-8') as inputFile:
    reader = csv.reader(inputFile)
    data = list(reader)        # e.g. data[0] == ['aa', '4426'], data[0][0] is: aa, data[0][1] is: 4426. I've verified that this object list data[lists] will write back to a file the exact same structure of a source database, if parsed correctly.
inputFile.close

# open gibberish generation output file for writing; TO DO: generate this file name based on source database and date?
logFile = codecs.open('gibGen_py_log.txt', 'w', encoding='utf-8')


recombobulation = ''
# seed mustStartWith var with space ' '
mustStartWith = ' '
genNumPhonemes = int(args.count)
frequencySum = 0
firstCharMatchedList = list()      # This will be a list of lists!
# loop as many times as genNumPhonemes var:
for i in range(0, genNumPhonemes):
    logFile.write('---------- FINDING next phoneme ---------- \n')
    # It may turn out that using for loops is the most legible and fast way to do this, re https://stackoverflow.com/a/1156143/1397555 :
        # LOOK FOR the whole set of possible matches for mustStartWith and add them to a list of lists firstCharMatchedList; summing the occurances given from the source .mkvch into frequencySum to be used later.
    for pair, idx in data:
        partA = pair[0]        # pair[0] is e.g. 'a', the first character in pair; (pair[0][0] + pair[0][1]) would be both e.g. 'ab'.
        if partA == mustStartWith:      # Previously, some other unknown indent characters for the next lines, Python hated (and tried to tell me, but the error messages mystified me), as everything else here was something else (tabs? is?).
            frequencySum = (frequencySum + int(idx))
            tmpTuple = [pair, frequencySum]
            firstCharMatchedList.append(tmpTuple); logFile.write('appended partA value \'' + partA + '\' from pair \'' + pair + '\' with frequency ' + idx + '\nfrequencySum: ' + str(frequencySum) + '\n')
    # WITH FIRSTCHARMATCHEDLIST populated with matches copied from var data[lists], randomly pick one of the pairs by first character in pair matching mustStartWith, accounting for statistical frequency (akin to data[0][1] == 4426). If there will not be a match (akin to data[0][0][0] == 'a') for mustStartWith, pick any first letter from any pair in the whole data list of lists.

        # IF A MATCH WAS FOUND (frequencySum != 0), assign it to nextLetter for later recombobulation.
    if frequencySum != 0:
        PRND = randint(0, frequencySum)
        logFile.write('Selected PRND ' + str(PRND) + ' from range 0,' + str(frequencySum) + '\n')
        for idx, pair in enumerate(firstCharMatchedList):
            # idx == iteration in loop, pair e.g. == [' a', 630737], pair[0] == ' a', pair[1] == 630737. TO DO: learn, would a third var listing in the for enumeration get the second list item in the list at firstCharMatchedList(idx)?
            if pair[1] >= PRND:
                pickedPair = str( firstCharMatchedList[ (idx - 1) ] )
                nextLetter = pickedPair[3]
                logFile.write('! ----------- PICK \'' + nextLetter + '\' for pair ' + pickedPair + ' at num ' + str(pair[1]) + '!\n')
                break
        # IF A MATCH WAS NOT FOUND (frequencySum == 0), terminate the word by setting nextLetter to ' ', and set mustStartWith to a random selection from the entire data set of first letters (that appear in a group).
    else:
        print('YO!')
        nextLetter = ' '
        dataLen = len(data)
        PRND = randint(0, (dataLen - 1) )
        logFile.write('No match starts with \'' + mustStartWith + '\'; terminated word and picking mustStartWith val from data set . . .\n'); mustStartWith = data[ (PRND) ][0][0]
        logFile.write('PICKED new value \'' + mustStartWith + '\' for mustStartWith.\n')

    # WHATEVER HAPPENED for the value of frequencySum, we covered all possible cases to assign to nextLetter, so can do this now:
    recombobulation = (recombobulation + nextLetter)
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