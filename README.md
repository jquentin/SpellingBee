# SpellingBee

This is a free, automated, textual version of the [New York Times' Spelling Bee game](https://www.nytimes.com/puzzles/spelling-bee).

Every day, it will serve a different puzzle the same for everyone.

## How to Play

 - Create words using the 7 letters provided.
 - Words must contain at least 3 letters.
 - Words must include the 1st letter (not necessarily in 1st place).
 - Letters can be used more than once.
 - There is at least 1 "pangram" for each puzzle. Pangrams are words that use all 7 letters.
 - Letters are unaccented, and words with non-alpha characters (like dash or apostrophe) are excluded.

## Usage

For simple default settings execution, just double-click spelling-bee-win.bat for Windows, spelling-bee-mac for Mac / Unix.

For more advanced usage and options, run spelling-bee.py with Python3.

## Options

 - -n \<count>: Will choose a puzzle only among those with <count> - 5 to <count> + 5 words
 - -l: Prints all puzzles and solutions, for debug purposes
 - -v: Verbose mode
 - -g \<language>: Sets the language to <language>. Uses ISO 639-1 codes. Currently available: en & fr
 - -w: Only loads the word list and creates the list of puzzles
 - -s \<letters>: Searches for the solutions to the puzzle with letters <letters> (mandatory letter first)
 - -d \<date>: Plays the puzzle for the date <date>
 - -u \<url>: Overrides the URL of the word list to <url>. Use with -w to recreate the puzzles with the new word list. Default word lists are provided for [English](http://www.mieliestronk.com/corncob_lowercase.txt) and [French](https://raw.githubusercontent.com/hbenbel/French-Dictionary/master/dictionary/dictionary.txt). Note that it will automatically remove accents and exclude words with non-alpha characters (like dash or apostrophe).
