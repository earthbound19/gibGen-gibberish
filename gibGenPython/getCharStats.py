# DESCRIPTION
# Takes an input text file (and accepts one with an attempted wide acceptance of international (European) alphabet characters; in utf-8), extracts letter pair statistics and writes them to a database named <inputFileBaseName>.mkvch (.mkvch, because I may be using Markov chains? I'm not certain). Statistics are written to the database in the form et,3289 (<letter pair,how often the pair was found in the input text). The .mkvch database may then be used to generate statistically similar gibberish via gibGen.py. Note that statistics for spaces before and after letters are also in the database; this serves to terminate and begin generated words during recombobulation.

# USAGE
# python thisScript.py inputFile.txt

import sys			# allows reciept and parsing of command line arguments to script from a list of strings, sys.argv[].
import os			# for one count it one function
import codecs		# allows opening a file with utf-8 interpretation
import itertools	# for permutation/combination functions.
import re			# for regex functions.

# TO DO:
# Write a separate script which generates gibberish via an .mkvch file (which type of file this script creates by parsing an input text)
# include punctuation in this array? At a starting minimum will use a space character ' '.
# add instr. to print res. to text file via >
# add usage instr. -- for now input text is argv[1].
# make this accept specific cli opts via opts library? re: https://gist.github.com/dideler/2395703
# filter very common words out of imported text?
# adopt regex https://pypi.python.org/pypi/regex/ instead?

# NOT TO DO: calculate the least common factor of all letter pair occurances and divide them all by that to reduce the number space. First, this breaks the set if some of them are '1', and second, no. If the numbers get so huge that I have to get numPy, I might start considering that.

# MARKOV CHAIN DATABASE GENERATING ALGORITHM.

# What?! if I break up the below array definition over the wrong arbitrary sequence of newlines, it throws: '..line 24 SyntaxError: Non-UTF-8 code starting with '\xc5' in file getCharStats.py on line 24, but no encoding declared; see http://python.org/dev/peps/pep-0263/ for details' : TO DO: figure out why that is so--it feels risky of a bug in another environment (I get this on Windows invoking pythong from cygwin OR (I think) cmd) :
# Includes space because it will be used as a statistical beginning and ending of word marker:
alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','À','Á','Â','Ã','Ä','Å','Æ','Ç','È','É','Ê','Ë','Ì','Í','Î','Ï','Ð','Ñ','Ò','Ó','Ô','Õ','Ö','Ø','Ù','Ú','Û','Ü','Ý','Þ','ß','à','á','â','ã','ä','å','æ','ç','è','é','ê','ë','ì','í','î','ï','ð','ñ','ò','ó','ô','õ','ö','ø','ù','ú','û','ü','ý','þ','ÿ','Ł','ł','Ń','ń','Ņ','ņ','Ň','ň','Ŋ','ŋ','Ō','ō','Ŏ','ŏ','Ő','ő','Œ','œ','Ŕ','ŕ','Ŗ','ŗ','Ř','ř','Ś','ś','Ŝ','ŝ','Ş','ş','Š','š','Ţ','ţ','Ť','ť','Ŧ','ŧ','Ũ','ũ','Ū','ū','Ŭ','ŭ','Ů','ů','Ű','ű','Ŵ','ŵ','Ŷ','ŷ','Ÿ','Ź','ź','Ż','ż','Ž','ž','ſ','Α','Β','Γ','Δ','Ε','Ζ','Η','Θ','Ι','Κ','Λ','Μ','Ν','Ξ','Ο','Π','Ρ','Σ','Τ','Υ','Φ','Χ','Ψ','Ω','α','β','γ','δ','ε','ζ','η','θ','ι','κ','λ','μ',
'ν','ξ','ο','π','ρ','ς',
'σ','τ','υ','φ','χ','ψ',
'ω','А','Б','В','Г','Д','Е','Ж','З',
'И','Й','К','Л','М','Н','О','П','Р','С','Т','У','Ф','Х',
'Ц','Ч','Ш','Щ','Ъ','Ы','Ь','Э','Ю','Я','а','б',
'в','г','д','е','ж','з','и','й','к','л',
'м','н','о','п','р','с','т','у','ф','х',
'ц','ч','ш','щ','ъ','ы','ь','э','ю','я','Ỳ',' '
]

# Print an error and help message if no paramater 1 provided, then exit.
if len(sys.argv) < 2:
	print("ERROR: No input text provided for parameter 1 (parameter 1 empty).\n\nUSAGE: python thisScript.py inputFile.txt\n\nDESCRIPTION: Takes an input text file (and accepts one with an attempted wide acceptance of international (European) alphabet characters; in utf-8), extracts letter pair statistics and writes them to a database named <inputFileBaseName>.mkvch (.mkvch, because I may be using Markov chains? I'm not certain). Statistics are written to the database in the form et,3289 (<letter pair,how often the pair was found in the input text). The .mkvch database may then be used to generate statistically similar gibberish via gibGen.py. Note that statistics for spaces before and after letters are also in the database; this serves to terminate and begin generated words during recombobulation.")
	sys.exit()

# read file using UTF-8 interpretation, reading it into a string, and delete all newlines and assign it to an object 'data'; re: https://stackoverflow.com/a/14787896/1397555
		# DEPRECATED:
		# with open(sys.argv[1], 'r') as myfile:
with codecs.open(sys.argv[1],"r", encoding='utf-8') as myfile:
    data=myfile.read().replace('\n', '')

# OPTIONAL, lowercase everything in that string; there are reasons you might not want to do this (such as creating psuedo-proper nouns from statistics of what letters start (are capitalized) in a name:
# data = data.lower()

# create an object of all 2-permutations of alphabet characters (pairs), which is a *lot* of pairs, depending on the alphabet:
allAlpha2perms = list(itertools.permutations(alphabet, 2))
	# to test object (dev):
	# for element in allAlpha2perms:
		# print(element[0] + " and " + element[1])
	# or to access a list element in this--I think it's an array of lists? :
	# print(allAlpha2perms[12][1])	# Prints list element 1 in array allAlpha2perms index 12.

# search for all pairs in allAlpha2perms, counting matches, and write to stat file--it is *so nice* that itertools took care of permutations/nested looping for me:
	# I think we will want overlapping matches (which I think this script also isn't doing; TO DO: that), re:https://stackoverflow.com/a/11430936/1397555 ? For now I'm going to assume that and ask someone who would know or bend my brain figuring it.

# get file base name re: https://stackoverflow.com/a/678242/1397555
paramFileNameNoExt =  os.path.splitext(sys.argv[1])[0]
outfileName = paramFileNameNoExt + '.mkvch'
# TO DO: figure out if the following should be codecs.open? Seems to work anyway:
# Open a file for writing in utf-8 encoding:
outfile = open(outfileName , "w", encoding='utf-8') 

for element in allAlpha2perms:
	searchStr = element[0] + element[1]
	result = re.findall(searchStr, data)
			# re: https://stackoverflow.com/a/3895658/1397555
	resultLenStr = str(len(result))
	if ( len(result) > 0):
		outfile.write(result[0] + ',' + resultLenStr + "\n")
		# DEPRECATED, as it seems to choke in environments that don't know how to pipe many unicode characters (which I would guess is most environments, sad sad) :
		# print(result[0] + ',' + resultLenStr)

outfile.close()

print("DONE. Letter matching statistics for input file are written to: " + outfileName)

# DEV NOTES:
	# can sort via 'nix util of that name by column e.g.:
	# sort -k2 -n yourfile
	# change delimiter to comma with -t switch e.g. -t, re https://docstore.mik.ua/orelly/unix3/upt/ch22_03.htm
	# WORKING COMMAND; add to usage notes; sorts in descending order by number (2nd) column:
	# gsort -r -t, -k2 -n TheCompleteWorksOfWilliamShakespeare.mkvch > numericSortTemp.mkvch