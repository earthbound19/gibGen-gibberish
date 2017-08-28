sort $1 > oot1.txt
uniq $1 > oot2.txt
rm $1
mv oot2.txt $1
rm oot1.txt