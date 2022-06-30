# Takes input words and outputs modified gibberish alternatives for them. The results can be funny :)
# Tweaked from this source: http://pythonfiddle.com/gibberish-word-generator/
# If you have python installed and in your path, run this file from a console.
# -RAH 05/02/2014 11:38:45 PM

gibberish = 'idig'
gibberish1 = 'uddag'
gibberish2 = 'uvug'
gibberish3 = 'uthug'

original = raw_input('Enter a word:')

if original.isalpha() and len(original) <= 35:
    first_letter = original[0]
    rest_of_word = original[1:]
    whole_word = original[0:]
    new_word = first_letter + gibberish + rest_of_word
    vowel_word = gibberish + original
    vowel_word1 = gibberish1 + original
    vowel_word2 = gibberish2 + original
    vowel_word3 = gibberish3 + original
    if first_letter == "a" or first_letter == "e" or first_letter == "i" or first_letter == "o" or first_letter == "u":
        print vowel_word
        print vowel_word1
        print vowel_word2
        print vowel_word3
    else:
        print first_letter + gibberish + rest_of_word
        print first_letter + gibberish1 + rest_of_word
        print first_letter + gibberish2 + rest_of_word
        print first_letter + gibberish3 + rest_of_word
else:
    print "Invalid answer"