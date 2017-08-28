# gibGenPython

This is a set of scripts to invent new gibberish words from existing sense (or nonsense) words. The invented words are generated randomly based on the character pairing statistics (bigrams and trigrams supported at this writing) of any corpus you provide. Unicode (UTF-) is supported, or many characters from alphabets around the world are. Björk? You betcha.

# Prerequisites
Python 3. For some included text processing scripts, a 'nix environment such as Linux, Mac or Cygwin.

# Usage

Create your own or use a provided character statistics database (in the .mkvch format, some in the [../_reference](../_reference) folder.

To create your own, copy and paste a corpus of words into a text file in the same PATH as the [getTrigramStats.py](getTrigramStats.py) script (in this folder), then follow the `# USAGE` instructions in that script. Then also see `# DESCRIPTION` and `# USAGE` in [gibGenTrigrams.py](gibGenTrigrams.py). You can use the scripts for bigrams also, but trigrams produce superior results. 