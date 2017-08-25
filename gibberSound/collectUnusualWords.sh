# re a stackoverflow answer abt illegal byte sequence in tr:
export LC_CTYPE=C

while [ 1 ]
do
  # TO DO: pregenerate so many bytes and nibble off the string in each loop.
# tmp=`cat /dev/urandom | tr -dc '0-9' | head -c 5`
  # trim off any leading zeros that would cause errors:
# numStr=`echo $tmp | sed 's/^0\{1,\}//'`
# rndNum=$(( ($numStr % 15) + 6 ))     # generates random result in range (n2) to (n2 + (n1 - 1))
# echo Retrieving random word of length $rndNum . . .

# OPTION involving previous lines of code in this do loop, if you uncomment them:
# word=`curl -s http://www.setgetgo.com/randomword/get.php?len=$rndNum`

# OPTION that allows the server to dispense words at random (independent of length consideration):
word=`curl -s http://www.setgetgo.com/randomword/get.php`
echo $word
printf "$word\n" >> unusualWordsCollecting.txt
# Else the service be overwhelemed and ban me:
sleep 3
done
