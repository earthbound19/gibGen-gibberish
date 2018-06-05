# DESCRIPTION
# Reminds you every 50 minutes to get up and stretch, by way of three random words proncounced by randomly chosen voices (Mac only). Records the statements to ~.m4a files and opens them in default sound player. If you pass the script a string parameter (see USAGE), it terminates immediately (without looping every 50 minutes).

# DEPENDENCIES
# The Mac "say" command, and gnu corutils shuf (here as gshuf via homebrew coreutils).

# USAGE
# Invoke this script to be seranated every 50 minutes by random voices speaking random words (to remind you to get up and stretch--and the words are all fetched by a random word web API, if the service is up). OR: invoke this script with one parameter $1, being any random word you'd like recored and played by any random Mac system voice.

while [ 1 ]
do

# IF no parameter provided, retrieve a random word and assign it to a word variable. Otherwise, assign $1 to word.
if [ -z ${1+x} ]
	then
	param_passed=TRUE
	curl -s http://www.setgetgo.com/randomword/get.php > wut.txt
  word1=$(<./wut.txt)
  curl -s http://www.setgetgo.com/randomword/get.php > wut.txt
  word2=$(<./wut.txt)
  curl -s http://www.setgetgo.com/randomword/get.php > wut.txt
  word3=$(<./wut.txt)
	rm ./wut.txt
  word="$word1, $word2, $word3"
  wordForFileName="$word1"_"$word2"_"$word3"
	else
	word=$1
	wordForFileName=$1
fi

echo The word or phrase to render is\: $word
# exit

# IF THE FOLLOWING text file does not exist:
if ! [ -a sayVoices.txt ]
then
  # CREATE TEXT FILE listing available voices for the say command, then
  # USE TEXT FILE as array source for random voice selection:
  # re: http://stackoverflow.com/a/30103783
    # for voice in `say -v '?' | awk '{print $1}'`; do say -v "$voice" "Hello, my name is $voice."; done
for voice in `say -v '?' | awk '{print $1}'`; do echo $voice >> sayVoices.txt; done
  # // OR:
  # to list available voices:
  # say -v '?' > sayVoices.txt
  # -- and then in a text editor that supports regex search/replace, use the following regex to isolate voices from that text file line per line if run on every line:
  # (^[^\t ]{1,}).*$
fi

# SELECT A RANDOM voice to render the word with;
# requires corutils from "brew install coreutils" :
voice=`cat ./sayVoices.txt | gshuf -n 1`
echo chosen voice is $voice.

# RENDER the actual file:
say "$word\!" -o "exc_""$voice""_$wordForFileName.aif"
# OPTIONALLY ADD IT TO and open and play it in iTunes:
open "exc_""$voice""_$wordForFileName.aif"

# IF A PARAMETER was passed to the script, exit. Otherwise this block will not execute, and the infinite while loop will continue.
if [ -z ${param_passed+x} ]
	then
	exit
fi

sleep 6
done
