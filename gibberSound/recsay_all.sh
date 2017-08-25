# re: http://stackoverflow.com/a/13939247/1397555
while read gibLine
do
# echo blar $gibLine
./recsayLocalSRC.sh $gibLine
  # done < gibbersource.txt
done < randomWords.txt
