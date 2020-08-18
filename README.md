# GibGen-gibberish

Tools to create nonsense from sense; recombobulators.

See the [README.md](gibGenPython/README.md) in ./gibGenPython to get started (it will point you to other things to read).

At this writing this repository includes other (undocumented?) tools and scripts useful for preparing corpuses to generate gibberish.

This repository may eventaully host source code for various recombobulators I have coded and/or ganked over the years.

----

# PREVIOUS NOTES
..which I may need to correct and/or integrate into the above--and I think replace mentioned tools that were removed:

This is a collection of algorithmic/statistical gibberish generators. I authored one of these from scratch, and the others are from sources which are clearly public, and I release all of the work in this folder to the Public Domain. 09/03/2015 05:38:24 PM -RAH

This documentation is lacking, and possibly inaccurate, so you know. TO DO: fix that. 03/20/2016 10:55:04 PM -RAH

### QUICK SETUP AND USE
Copy your text corpus from which to generate gibberish into the _corpus folder, then copy and paste whatever you will from that into pyMarkovGibGen/gibbersource.txt, and from that folder, run the command:
Python _runMarkovGen.py

And behold the results in so many files named e.g.:
pyMarkovGibGen\generated_IAE_gibberish__2016_01_02__02_33_12__707556.txt
--the file name will vary by the date and time it happens to be at the moment the gibberish is generated.

Python must be installed and in your PATH for this to work. If it makes a difference, this was coded and tested with Python 3.1

## Contents of subfolder pyMarkovGibGen

A few horked and adapted implimentations of markov chain analysis/generation to make up new words and/or nonsense paragrpahs. At this writing, they span using Python 2 and 3 and you'll have to sort that out.

For example, markovgen.py is my modification of a script I found (notes in source code), to generate gibberish paragraphs or fake essays from a source corpus in gibbersource.txt. To run from the .py file, it and gibbersource.txt must be in python's PATH.

In Windows, you can copy these with runMarkovgen.py to the Python install directory, and double-click that run~ python script. However that will bring up a window that generates paragraphs and the immediately vanishes. To capture the gibberish to a text file, bring up a console in the Python directory (or make sure Python is in your %PATH%), and and run this command:

Python _runMarkovGen.py

--which will write gibberish to the pyMarkovGibGen\_generated_gibberish.txt file.

Anything you wish to keep must be copied out of that result text file before you run the script again, as the result file is overwritten from the start on every run of the batch.

You may donate Public Domain texts to the _corpus directory. Copy and paste any text from the corpus into e.g. pyMarkovGibGen\gibbersource.txt (and then save the file), and then execute _runMarkovGen.py as explained.

It would be great to implement this program as a web page where visitors can save and share results.

---
### REVISION HISTORY

- pyMarkovGibGen\_runMarkovGen.py v1 INITIAL RELEASE
GibbGen\GibbGenCPP\bin\1.0-functional\gibbgen_DOS.exe resurrected functional first version of that. 09/03/2015 05:29:15 PM -RAH
- Changed _runMarkovGen.py to output so many (configurable by editing the script) date and microsecond-stamped gibberish files, which may be edited for syntax and "cohesiveness" and/or "clarity," etc. and later incorporated into other works. A major expansion of gibbersource.txt with an exhaustive (though incomplete) compendium of announcements on the e-flux mailing list (a perhaps incomparable trove of nonsensical International Art English). Tweaked random range of output gibberish words, and removed README.md mention that I fear to include such for Copyright reasons; as it is used *both* for purposes of farce *and* instruction (in what kind of language to avoid like the plague if you want to be friendly to your audience). 01/02/2016 12:48:31 AM -RAH