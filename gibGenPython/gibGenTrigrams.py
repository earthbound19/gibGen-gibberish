# IN DEVELOPMENT; an extension or refactor of gibGenBigrams.py

# DESCRIPTION
# Generates (recombobulates) gibberish from a database of character pair statistics (bigrams). See comments at the top of getBigramStats.py to get such a database. Writes results to gibber_out.txt

# USAGE
# python gibGenTrigrams.py -d [source database.mkvch] -c [count of words to generate]
# For example:
# python gibGenTrigrams.py -d ../databases/onomatopoeiaTri.mkvch -c 500

# TO DO
# make log file optional (which means make a log function and refactor to pass it strings conditionally)
# dump recombobulation var to file when it gets to certain huge size, then continue filling it.
# make gibberish dump file name partly based on timestamp.

# import sys            # comment out for release; only for development.
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
    args.database = '../databases/tenOldestSpokenLanguagesNamesTri.mkvch'
if args.count:
    print('Letter groups to create number ' + args.count + ' specified.')
else:
    args.count = 2000

# READ database into var data
with codecs.open(args.database, 'r', encoding='utf-8') as inputFile:
    reader = csv.reader(inputFile)
    data = list(reader)        # for TRIGRAMS e.g. data[0] == ['aaa', '4426'], data[0][0] is: aaa, data[0][1] is: 4426.
inputFile.close

# open run log file for writing.
logFile = codecs.open('gibGen_py_log.txt', 'w', encoding='utf-8')


recombobulation = ''
# seed mustStartWith var with space ' ' (or for trigrams make that a double space '  ')
mustStartWith = '  '
genNumPhonemes = int(args.count)
charMatchesList = list()

# loop as many times as genNumPhonemes var:
for i in range(0, genNumPhonemes):
    charMatchesList.clear()       # This list of lists is cleared at each outer loop iteration.
    addedFreq = 0                 # So is this.
    # logFile.write('-- SEARCHING for match candidates from data where where mustStartWith is \'' + mustStartWith + '\' . . .\n')
    # It may turn out that using for loops is the most legible and fast way to do this, re https://stackoverflow.com/a/1156143/1397555 :
        # LOOK FOR the whole set of possible matches for mustStartWith and add them to a list of lists charMatchesList; summing the occurances given from the source .mkvch into addedFreq to be used later.
    for pair, freq in data:
        partA = pair[0] + pair[1]        # For BIGRAM use, pair[0] is e.g. 'a', the first character in pair; for TRIGRAM use, (pair[0][0] + pair[0][1]) would be both e.g. 'ab'.
        if partA == mustStartWith:
            addedFreq = int(addedFreq + int(freq))
            tmpTuple = [pair, int(freq)]
            charMatchesList.append(tmpTuple)
            # logFile.write('added ' + str(tmpTuple) + ' at pair \'' + pair + '\', freq ' + freq + ', addedFreq ' + str(addedFreq) + '\n')

    # WITH charMatchesList populated with matches copied from var data[lists], randomly pick one of the pairs by first character in pair matching mustStartWith, accounting for statistical frequency (akin to data[0][1] == 4426). If there will not be a match (akin to data[0][0][0] == 'aa') for mustStartWith, pick any first letter (or for trigrams or further, letters) from any pair in the whole data list of lists.

    # IF A MATCH WAS FOUND (addedFreq != 0), assign it to nextLetter for later recombobulation.
    if addedFreq != 0:
        PRND = randint(0, addedFreq)
        # logFile.write('Selected PRND ' + str(PRND) + ' from range 0,' + str(addedFreq) + '\n')
        freqIterAdd = 0
        for idx, list in enumerate(charMatchesList):
            # logFile.write('at enumerate list ' + str(list) + ' idx ' + str(idx) + '; list[1] ' + str(list[1]) + '; PRND ' + str(PRND) + '\n')
            # logFile.write('freqIterAdd ' + str(freqIterAdd) + ' . . . ')
            freqIterAdd += int(list[1])
            # logFile.write('now incremented to ' + str(freqIterAdd) + '\n')
            if freqIterAdd >= PRND:
                pickedPair = str( charMatchesList[ (idx - 1) ] )
                nextLetter = pickedPair[4]      # Originally goofed that as ~[3] + ~[4]
                # logFile.write('mustStartWith is \'' + mustStartWith + '\' . . .\n')
                logFile.write('!-- FROM pickedPair ' + pickedPair + ' PICK nextLetter \'' + nextLetter + '\' at freqIterAdd (' + str(freqIterAdd) + ') >= PRND (' + str(PRND) + '); \n')
                # for BIGRAM use: mustStartWith = nextLetter
                # for TRIGRAM use:
                mustStartWith = (pickedPair[3] + pickedPair[4])
                # logFile.write('mustStartWith is now \'' + mustStartWith + '\'\n')
                break
    # IF A MATCH WAS NOT FOUND (addedFreq == 0), terminate the word by setting nextLetter to ' ', and set mustStartWith to a random selection from the entire data set of first letters (that appear in a group).
    else:
        nextLetter = ' '
        dataLen = len(data)
        PRND = randint(0, (dataLen - 1) )
        logFile.write('--! No match starts with \'' + mustStartWith + '\'; terminated word and picking mustStartWith val from data set . . .\n')
        # for BIGRAM: mustStartWith = data[ (PRND) ][0][0]
        # for TRIGRAM:
        mustStartWith = ( data[ (PRND) ][0][0] + data[ (PRND) ][0][1] )
        logFile.write('PICKED new value \'' + mustStartWith + '\' for mustStartWith.\n')

    # WHATEVER HAPPENED for the value of addedFreq, we covered all possible cases to assign to nextLetter, so can do this now:
    recombobulation = (recombobulation + nextLetter)
# for loop ends


logFile.close

# Write generated gibberish to file.
gibberFileName = 'gibber_out.txt'
gibberFile = codecs.open(gibberFileName, 'w', encoding='utf-8')
gibberFile.write(recombobulation)
gibberFile.close

print('\nO frabjous day!\nDONE. Wrote gibberish to ' + gibberFileName + '.\n')

# print(recombobulation)