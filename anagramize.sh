# DESCRIPTION: Takes an input text paramater and outputs an ~_anagramized.txt text file where every vowel may be scrambled with an adjacent character. The result is readable to (about half of?) humans, but would take extra programming or resources for web keyword scanners (SPIES) to make good of.

# USAGE: run the script with one paramaeter, being the name of a text file in the same directory, to scramble. Results will appear in ~_anagramized.txt. ex.:
# ./thisScript.sh inputFile.txt

# OPTIONAL: Strip every character that isn't alphabetic or a space:
# gsed "s/[^[:alpha:] ]/ /g" $1 > tmp1.txt
# IF YOU DON'T DO THAT previous line, do this:
cat $1 > tmp1.txt
tr ' ' '\n' < tmp1.txt > tmp2.txt
printf "" > tmp3.txt

while read element
do
	# adapted from: http://stackoverflow.com/a/26326317 and http://www.theunixschool.com/2012/06/swap-every-2-lines-in-file.html
	echo $element | gsed 's/[aeiouyAEIOUY]/&\n/g' | gsed -n '{h;${p;q;};n;G;p;}' | tr -d '\n' > tmp1.txt
	scrambledWord=$( < tmp1.txt )
	echo "$scrambledWord " >> tmp3.txt
done < tmp2.txt

tr '\n' ' ' < tmp3.txt > $1\_anagramized.txt
gsed -i 's/  / /g' $1\_anagramized.txt
rm tmp1.txt tmp2.txt tmp3.txt