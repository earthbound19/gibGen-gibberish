# IN DEVELOPMENT. At this writing has a fatal bug. Prematurely adapted from gibGenBigrams.py (before I realised this propogates a fatal bug from that).

# DESCRIPTION
# Generates (recombobulates) gibberish from a database of character triples statistics (trigrams). See comments at the top of getBigramStats.py to get such a database. Writes results to gib.txt

# USAGE
# python3 thisScript.py -d [source database.mkvch] -c [count of words to generate]

# NOTES: This may only work with python3. Also, the only source database I have producing useful output at this writing is databases/TheJabberwocky.mkvch, at this writing. TO DO: fix that: maybe by having this work statistically on trigrams instead of bigrams.

# TO DO
# pick new random mustStartWith if triplet is '<letter><space><triplet>'?
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
    args.database = '../databases/tenOldestSpokenLanguagesNamesTri.mkvch'
if args.count:
    print('Letter groups to create number ' + args.count + ' specified.')
else:
    args.count = 2000

# READ database into var data
with codecs.open(args.database, 'r', encoding='utf-8') as inputFile:
    reader = csv.reader(inputFile)
    data = list(reader)
inputFile.close

dataLen = len(data)

# open gibberish generation output file for writing
logFile = codecs.open('gibGen_py_log.txt', 'w', encoding='utf-8')


recombobulation = ''
# seed mustStartWith var with spaces '  '
mustStartWith = '  '
genNumPhonemes = int(args.count)
frequencySum = 0
charMatchList = list()      # This will be a list of lists!

# loop as many times as genNumPhonemes var:
for i in range(0, genNumPhonemes):
    # logFile.write('frequencySum is ' + str(frequencySum) + '\n')
    # logFile.write('-- FINDING next phoneme where mustStartWith is \'' + mustStartWith + '\'\n')
            # It may turn out that using for loops is the most legible and fast way to do this, re https://stackoverflow.com/a/1156143/1397555 :
    # LOOK FOR the whole set of possible matches for mustStartWith and add them to a list of lists charMatchList; summing the occurances given from the source .mkvch into frequencySum to be used later.
    for pair, idx in data:
        partA = pair[0] + pair[1]        # pair[0] is e.g. 'a', the first character in pair; (pair[0][0] + pair[0][1]) would be both, e.g. 'ab'.
        # logFile.write('partA is \'' + partA + '\' where pair is \'' + pair + '\' and pair[0] and [1] are ' + pair[0] + ' and ' + pair[1] + '; mustStartWith is \'' + mustStartWith + '\'\n')
        if partA == mustStartWith:
            frequencySum = (frequencySum + int(idx))
            # logFile.write('frequencySum incremented to ' + str(frequencySum) + '\n')
            tmpTuple = [pair, frequencySum]
            charMatchList.append(tmpTuple)
            logFile.write('appended ' + str(tmpTuple) + ', pair \'' + pair + '\' freq. (idx) ' + idx + ' frequencySum ' + str(frequencySum) + '\n')

    # WITH charMatchList populated with matches copied from var data[lists], randomly pick one of the pairs by first character in pair matching mustStartWith, accounting for statistical frequency (akin to data[0][1] == 4426). If there will not be a match (akin to data[0][0][0] == 'a') for mustStartWith, pick any first letter from any pair in the whole data list of lists.

    # IF A MATCH WAS FOUND (frequencySum != 0), assign it to nextLetter for later recombobulation.
    # logFile.write('frequencySum before nonzero check is ' + str(frequencySum) + '\n')
    if frequencySum != 0:
        PRND = randint(0, frequencySum)
        # logFile.write('\t\t\t\tSelected PRND ' + str(PRND) + ' from range 0,' + str(frequencySum) + '\n')
        for idx, pair in enumerate(charMatchList):
            # idx == iteration in loop, pair e.g. == [' aa', 10], pair[0] == ' aa', pair[1] == 10 (frequency 10 for "pair") TO DO: learn, would a third var listing in the for enumeration get the second list item in the list at charMatchList(idx)?
            # logFile.write('\t\t\t\tPAIR[1] val ' + str(pair[1]) + '\n')
            if pair[1] >= PRND:
                pickedPair = str( charMatchList[ idx ] )       # e.g. [' ai', 61]
                nextLetter = (pickedPair[4])                                # e.g. 'i'
                logFile.write('PICKED \'' + nextLetter + '\' from \'' + mustStartWith + '\' > \'' + pickedPair + '\'\n')
                # logFile.write('\t\tadded:\n\'' + nextLetter + '\' from mustStartWith \'' + mustStartWith + '\' in \'' + pickedPair + '\' at frequency >= list item ' + str(pair[1]) + '\n')
                mustStartWith = (pickedPair[3] + pickedPair[4])             # e.g. 'ai'
                logFile.write('\t\t\t\tmustStartWith val now \'' + mustStartWith + '\'\n')
                break
    else:           # IF A MATCH WAS NOT FOUND (frequencySum == 0), terminate the word by setting nextLetter to ' ', and set mustStartWith to a random selection from the entire data set of first letters (that appear in a group).
        # TO DO: test this else case (force it to happen)
        logFile.write('frequencySum in else case block is ' + str(frequencySum) + '\n')
        logFile.write('else case encountered where no match was found!\n')
        nextLetter = ' '
        PRND = randint(0, (dataLen - 1) )
        logFile.write('--! No match starts with \'' + mustStartWith + '\'; terminated word and picking mustStartWith val from data set . . .\n')
        mustStartWith = ( data[ (PRND) ][0][1] + data[ (PRND) ][0][2] )
        logFile.write('PICKED new value \'' + mustStartWith + '\' for mustStartWith where data[ PRND ][0] val is \'' + str(data[ PRND ][0]) + '\'\n')

    # WHATEVER HAPPENED for the value of frequencySum, we covered all possible cases to assign to nextLetter, so can do this now:
    # COMMENT OUT these logFile.write lines of code if you don't want your log file to massively grow--! :
    logFile.write('\'' + recombobulation + '\' += \'' + nextLetter + '\':\n\'')
    recombobulation = (recombobulation + nextLetter)
    logFile.write(recombobulation + '\'\n')
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