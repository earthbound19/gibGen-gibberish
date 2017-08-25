# IN DEVELOPMENT. At this writing has a fatal bug.

# DESCRIPTION
# Generates (recombobulates) gibberish from a database of character pair statistics (bigrams). See comments at the top of getBigramStats.py to get such a database. Writes results to gib.txt

# USAGE
# python3 thisScript.py -d [source database.mkvch] -c [count of words to generate]

# NOTES: This may only work with python3. Also, the only source database I have producing useful output at this writing is databases/TheJabberwocky.mkvch, at this writing. TO DO: fix that: maybe by having this work statistically on trigrams instead of bigrams.

# TO DO
# make log file optional (which means make a log function and refactor to pass it strings conditionally)
# dump recombobulation var to file when it gets to certain huge size, then continue filling it.
# make gibberish dump file name partly based on timestamp.

# import sys            # comment out for release; only for development.
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
    args.database = '../databases/tenOldestSpokenLanguagesNamesBi.mkvch'
if args.count:
    print('Letter groups to create number ' + args.count + ' specified.')
else:
    args.count = 2000

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
addedFreq = 0
charMatchesList = list()      # This will be a list of lists!
# loop as many times as genNumPhonemes var:
for i in range(0, genNumPhonemes):
    # logFile.write('-- SEARCHING for match candidates from data where where mustStartWith is \'' + mustStartWith + '\' . . .\n')
    # It may turn out that using for loops is the most legible and fast way to do this, re https://stackoverflow.com/a/1156143/1397555 :
        # LOOK FOR the whole set of possible matches for mustStartWith and add them to a list of lists charMatchesList; summing the occurances given from the source .mkvch into addedFreq to be used later.
    for pair, freq in data:
        partA = pair[0]        # pair[0] is e.g. 'a', the first character in pair; (pair[0][0] + pair[0][1]) would be both e.g. 'ab'.
        if partA == mustStartWith:
            addedFreq = int(addedFreq + int(freq))
            tmpTuple = [pair, int(freq)]
            charMatchesList.append(tmpTuple)
            # logFile.write('added ' + str(tmpTuple) + ' at pair \'' + pair + '\', freq ' + freq + ', addedFreq ' + str(addedFreq) + '\n')

    # WITH charMatchesList populated with matches copied from var data[lists], randomly pick one of the pairs by first character in pair matching mustStartWith, accounting for statistical frequency (akin to data[0][1] == 4426). If there will not be a match (akin to data[0][0][0] == 'a') for mustStartWith, pick any first letter from any pair in the whole data list of lists.

    # IF A MATCH WAS FOUND (addedFreq != 0), assign it to nextLetter for later recombobulation.
    if addedFreq != 0:
        PRND = randint(0, addedFreq)
        logFile.write('Selected PRND ' + str(PRND) + ' from range 0,' + str(addedFreq) + '\n')
        freqIterAdd = 0
        for idx, list in enumerate(charMatchesList):
            # logFile.write('at enumerate list ' + str(list) + ' idx ' + str(idx) + '; list[1] ' + str(list[1]) + '; PRND ' + str(PRND) + '\n')
            # logFile.write('freqIterAdd ' + str(freqIterAdd) + ' incremented to ')
            freqIterAdd += int(list[1])
            # logFile.write('freqIterAdd incremented to ' + str(freqIterAdd) + '\n')
            if freqIterAdd >= PRND:
                pickedPair = str( charMatchesList[ (idx - 1) ] )
                nextLetter = pickedPair[3]
                logFile.write('PICK nextLetter \'' + nextLetter + '\' from pickedPair ' + pickedPair + ' at freqIterAdd (' + str(freqIterAdd) + ') >= PRND (' + str(PRND) + ')\n')
                # logFile.write('mustStartWith was \'' + mustStartWith + '\'; is now \'')
                mustStartWith = nextLetter
                # logFile.write(mustStartWith + '\'\n')
                break
    # IF A MATCH WAS NOT FOUND (addedFreq == 0), terminate the word by setting nextLetter to ' ', and set mustStartWith to a random selection from the entire data set of first letters (that appear in a group).
    else:
        nextLetter = ' '
        dataLen = len(data)
        PRND = randint(0, (dataLen - 1) )
        logFile.write('--! No match starts with \'' + mustStartWith + '\'; terminated word and picking mustStartWith val from data set . . .\n')
        mustStartWith = data[ (PRND) ][0][0]
        logFile.write('PICKED new value \'' + mustStartWith + '\' for mustStartWith.\n')

    # WHATEVER HAPPENED for the value of addedFreq, we covered all possible cases to assign to nextLetter, so can do this now:
    recombobulation = (recombobulation + nextLetter)
    # reset addedFreq for the next iteration of the outmost loop:
    addedFreq = 0
# for loop ends


logFile.close

# Write generated gibberish to file.
gibberFileName = 'gibber_out.txt'
gibberFile = codecs.open(gibberFileName, 'w', encoding='utf-8')
gibberFile.write(recombobulation)
gibberFile.close

print('\nO frabjous day!\nDONE. Wrote gibberish to ' + gibberFileName + '.\n')

# print(recombobulation)