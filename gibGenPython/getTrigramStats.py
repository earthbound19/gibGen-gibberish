# DESCRIPTION
# Takes an input text file (and accepts one with an attempted wide acceptance of international (European) alphabet characters; in utf-8), extracts letter pair statistics and writes them to a database named <inputFileBaseName>.mkvch (.mkvch after Markov chains). Statistics are written to the database in the form et,3289 (<letter pair,frequency the pair appeared). The .mkvch database may then be used to generate statistically similar gibberish via gibGenTrigrams.py. Note that statistics for spaces before and after letters are also in the database; this serves to terminate and begin generated words during recombobulation. Dashes and single quotes (apostraphes) are also included.

# USAGE
# python getTrigramStats.py inputFile.txt

# NOTES
# - This may only work with python3.
# - If you use this against a list of words that are one per line with no space at the end, you'll get a database with no terminating space characters, and therefore words generated from it will never terminate. To avoid this, add a space character to the end of every line. (If you replace all newlines with spaces, you'll get trigrams that are letter-space-letter, which will skew trigram stats.)

import sys                           # allows reciept and parsing of command line arguments to script from a list of strings, sys.argv[].
import os                            # for one count it one function
import codecs                        # allows opening a file with utf-8 interpretation
from itertools import product        # for permutation with repetition, re: https://stackoverflow.com/a/3100016/1397555
import re                            # for regex functions.

# TO DO:
# - Accept characters from this list without error: ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿŁłŃńŅņŇňŊŋŌōŎŏŐőŒœŔŕŖŗŘřŚśŜŝŞşŠšŢţŤťŦŧŨũŪūŬŭŮůŰűŴŵŶŷŸŹźŻżŽžſΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩαβγδεζηθικλμνξοπρςστυφχψωАБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдежзийклмнопрстуфхцчшщъыьэюяỲA̧a̧B̧b̧ÇçḈḉÇ̇ç̇ḐḑȨȩȨ̇ȩ̇ḜḝƏ̧ə̧Ɛ̧ɛ̧ĢģḨḩI̧i̧Ɨ̧ɨ̧ĶķĻļM̧m̧ŅņO̧o̧Ɔ̧ɔ̧Q̧q̧ŖŗŞşſ̧ß̧ŢţU̧u̧X̧x̧Z̧z̧AĀBCČDEĒFGĢHIĪJKĶLĻMNŅOPRSŠTUŪVZŽaābcčdeēfgģhiījkķlļmnņoprsštuūvzž
# - Paramaterize alphabet support (import from text file of characters separated by newlines)
# - Separate script to generate an alphabet from a corpus?
# - Optionally filter very common words out of imported text?
# - Manually remove double-space '  ' from resulting letter pairs array (it is always the last item)?

# NOT TO DO: calculate the least common factor of all letter pair occurances and divide them all by that to reduce the number space. First, this breaks the set if some of them are '1', and second, no. If the numbers get so huge that I have to get numPy, I might start considering that.

# ~
# MARKOV CHAIN DATABASE GENERATING ALGORITHM.

# OPTIONS: 1) a more extensive alphabet for texts from a variety of European languages other than English OR 2) narrow alphabet from smaller and *ethnocentric* ACSII code page. Both alphabets include a space character because it will be used as a statistical beginning and ending of word marker. For extensive alphabet uncomment the next line and comment out the line after it; for narrow alphabest visa-versa:
# alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿĀāČčĒēĢģĪīĶķĻļŁłŃńŅņŇňŊŋŌōŎŏŐőŒœŔŕŖŗŘřŚśŜŝŞşŠšŢţŤťŦŧŨũŪūŬŭŮůŰűŴŵŶŷŸŹźŻżŽžſƆƏƐƗȨȩɔəɛɨΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩαβγδεζηθικλμνξοπρςστυφχψωАБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдежзийклмнопрстуфхцчшщъыьэюяḈḉḐḑḜḝḨḩỲ '-"
alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'- "

# Print an error and help message if no paramater 1 provided, then exit.
if len(sys.argv) < 2:
    print("ERROR: No input text provided for parameter 1 (parameter 1 empty).\n\nSee USAGE in the source code comments of this script.")
    sys.exit()

# read file using UTF-8 interpretation, replace all newlines with spaces, and write the result to an object 'data'; re: https://stackoverflow.com/a/14787896/1397555
with codecs.open(sys.argv[1],"r", encoding='utf-8') as myfile:
    data=myfile.read().replace('\n', ' ')

# OPTIONAL, lowercase everything in that string; there are reasons you might not want to do this (such as creating psuedo-proper nouns from statistics of what letters start (are capitalized) in a name:
# data = data.lower()

# create an object of all 2-permutations of alphabet characters (pairs), which is a *lot* of pairs, depending on the alphabet:
# allAlpha3perms = list(itertools.permutations(alphabet, 2)); note that if you want 3-character permutations you can change the 2 in this next call to 3, or 4 for 4-char permutations etc; although you may have to refactor code following that to accomodate:
allAlpha3perms = product(alphabet, repeat = 3)
        # to test object (dev), unindent and uncomment the next two lines, but expect your console (and thus python--? where it doesn't choke if you don't try printing in the loop!) may choke on unicode characters it doesn't know how to print:
        # for element in allAlpha3perms:
            # print(element[0] + " and " + element[1])

# search source .txt file against all pairs in allAlpha3perms, counting matches, and write to stat file--it is *so nice* that itertools took care of permutations/nested looping for me:
# first get file base name re: https://stackoverflow.com/a/678242/1397555
        # or to access a list element in this, as it is a list of lists:
        # print(allAlpha3perms[12][1])    # Prints list element 1 in array allAlpha3perms index 12.
paramFileNameNoExt =  os.path.splitext(sys.argv[1])[0]
outfileName = paramFileNameNoExt + 'Tri.mkvch'
# TO DO: figure out if the following should be codecs.open? Seems to work anyway:
# Open a file for writing in utf-8 encoding:
outfile = codecs.open(outfileName , "w", encoding='utf-8') 
for element in allAlpha3perms:
    searchStr = element[0] + element[1] + element[2]
    result = re.findall(searchStr, data)
            # re: https://stackoverflow.com/a/3895658/1397555
    resultLenStr = str(len(result))
    if ( len(result) > 0):
        outfile.write(result[0] + ',' + resultLenStr + "\n")
        # DEPRECATED, as it seems to choke in environments that don't know how to pipe many unicode characters (which I would guess is most environments, sad sad) :
        # print(result[0] + ',' + resultLenStr)
outfile.close()

print("\nDONE. Letter matching statistics for input file are written to: " + outfileName)

# DEV NOTES:
    # can sort via 'nix util of that name by column e.g.:
    # sort -k2 -n yourfile
    # change delimiter to comma with -t switch e.g. -t, re https://docstore.mik.ua/orelly/unix3/upt/ch22_03.htm
    # WORKING COMMAND; add to usage notes; sorts in descending order by number (2nd) column:
    # gsort -r -t, -k2 -n TheCompleteWorksOfWilliamShakespeare.mkvch > numericSortTemp.mkvch