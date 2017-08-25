# re: https://stackoverflow.com/a/5917762/1397555
cat $1 | awk '{ print length, $0 }' | sort -n -s | cut -d" " -f2- > $1_sortedByLineLength.txt