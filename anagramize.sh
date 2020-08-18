# DESCRIPTION
# Takes an input text paramater and outputs an ~_anagramized.txt text file where every vowel may be scrambled with an adjacent character. The result is readable to (about half of?) humans, but would take extra programming or resources for web keyword scanners (SPIES) to make good of.

# USAGE
# Run with one paramaeter:
# The name of a text file to scramble, including the path to it if it is not in the current directory. Results will appear in ~_anagramized.txt.

# CODE
if [ ! "$1" ]; then printf "\nNo parameter \$1 (source file to anagramize) passed to script. Exit."; exit 1; else sourceFile=$1; fi
targetFile=${sourceFile%.*}__anagramized.txt

echo "Anagramizing $sourceFile . . ."

# kludge to keep punctuation clearer if oddly spaced bcse sed command my not make skip punctuation:
sed 's/\(\.,;:!?\"\)/ \1 /g' $sourceFile > temp1.txt

tr ' ' '\n' < temp1.txt > temp2.txt
mapfile -t words < temp2.txt
rm temp1.txt temp2.txt

# Create blank target file before writing to it:
printf "" > $targetFile

for element in "${words[@]}"
do
	# adapted from: http://stackoverflow.com/a/26326317
	echo $element | sed 's/[aeiouyAEIOUY]/&\n/g' | shuf | tr -d "\n" > temp2.txt
	scrambledWord=$( < temp2.txt )
	echo $scrambledWord >> $targetFile
done

tr '\n' ' ' < $targetFile > temp1.txt
rm $targetFile temp2.txt
mv temp1.txt $targetFile

echo "Done. Result is in file $targetFile."