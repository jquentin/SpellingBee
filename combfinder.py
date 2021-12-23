#!/usr/bin/python3

import urllib.request
import pydoc
import random
import os
import sys
import getopt
import datetime

start_time = datetime.datetime.now()

UNIQUE_LETTERS_COUNT = 7

CONGRATS_WORDS = ["Yes!", "Well done!", "Amazing!", "Fantastic!", "Fabulous!", "Wow!", "Perfect!"]
INCORRECT_WORDS = ["Incorrect word", "Nope", "Not a word", "That's not a thing", "What's that?"]
WRONG_LETTERS = ["Wrong letters", "That doesn't work", "Doesn't fit"]

LOADING_BAR_LENGTH = 60

os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))

class Word:
    word: str
    letters: set
    
    def __init__(self, word: str, letters: set):
        self.word = word
        self.letters = letters

def load_words():
#    urllib.request.urlretrieve("https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt", "words_alpha.txt")
    with open("./words.txt") as word_file:
        valid_words = word_file.read().split()

    return [Word(word, set(word)) for word in valid_words if len(word) >= 3]

class Bee:
    letters: set
    center: str
    pangram: str
    other_words: set
    
    def __init__(self, letters: set, center: str, pangram: str, other_words: set):
        self.letters = letters
        self.center = center
        self.pangram = pangram
        self.other_words = other_words
        
    @staticmethod
    def create_bee(word: Word):
        res = set()
        has_7_letters = len(word.letters) == UNIQUE_LETTERS_COUNT
        if has_7_letters:
            all_other_words = set()
            for w in english_words:
                if w.letters.issubset(word.letters) and w.word != word.word:
                    all_other_words.add(w)
            for center in sorted(word.letters):
                other_words = set()
                for w in all_other_words:
                    if center in w.letters:
                        other_words.add(w.word)
                if 10 <= len(other_words) <= 20:
                    res.add(Bee(word.letters, center, word.word, other_words))
        return res
                
    @staticmethod
    def create_bees(words):
        bees = []
        index = 0
        for word in words:
            loading_rate = index / len(words)
            loading_bar = "["
            for i in range(0, LOADING_BAR_LENGTH):
                if i < loading_rate * LOADING_BAR_LENGTH:
                    loading_bar += "█"
                else:
                    loading_bar += " "
            loading_bar += "]"
            print(f"Loading: {loading_bar} {round(loading_rate * 100)}%", end = '\r')
            bee = Bee.create_bee(word)
            if bee is not None:
                bees.extend(list(bee))
            index += 1
        return bees
        
    def show_letters(self):
        other_letters = self.letters - set(self.center)
        return f"{self.center}{''.join(other_letters)}"
    
    def __str__(self):
        return f"{self.show_letters()} -> {len(self.other_words)+1}: {self.pangram},{','.join(self.other_words)}"
        
    def guess(self):
        words_count = len(self.other_words)+1
        print(f"{self.show_letters()} -> {words_count} words to find")
        words_found = set()
        while len(words_found) < words_count:
            word = input()
            if word in words_found:
                print("Word already found")
            elif self.center not in word:
                print("Word missing the central letter (1st letter)")
            elif word in self.other_words:
                print(CONGRATS_WORDS[random.randint(0, len(CONGRATS_WORDS)-1)])
                words_found.add(word)
            elif word == self.pangram:
                print("PANGRAM!")
                words_found.add(word)
            elif set(word).issubset(self.letters):
                print(INCORRECT_WORDS[random.randint(0, len(INCORRECT_WORDS)-1)])
            else:
                print(WRONG_LETTERS[random.randint(0, len(WRONG_LETTERS)-1)])
            print(f"{words_count - len(words_found)} words remaining")
        print("You found everything! Congratulations Jessica!")
          
print_all = False
search_bee = None

try:
    opts, args = getopt.getopt(sys.argv[1:], "ls:", ["list", "search"])
except getopt.GetoptError as err:
    print("error options")
    sys.exit(2)
for o, a in opts:
    if o == "-l":
        print_all = True
    elif o == "-s":
        search_bee = a
        
english_words = load_words()
bees = Bee.create_bees(english_words)

end_time = datetime.datetime.now()

print(f"Generated {len(bees)} bees in {(end_time - start_time).seconds}s from {len(english_words)} words")

if print_all:
    all_bees = ""
    index = 0
    for b in bees:
        all_bees += f"{index} - {b}\n"
        index += 1
    pydoc.pager(all_bees)
elif search_bee is not None:
    bee = [b for b in bees if b.letters == set(search_bee)][0]
    print(bee)
else:
    date = datetime.date.today()
    print(f"Spelling bee for {date}")
    seed = (date - datetime.datetime.utcfromtimestamp(0).date()).days
    print(f"Seed: {seed}")
    random.seed(seed)
    bee_index = random.randint(0, len(bees)-1)
    print(f"Bee number: {bee_index}")
    bee = bees[bee_index]
    bee.guess()

#fitting_words = list(filter(is_valid, english_words))
#print(f"{len(bees)} words with {UNIQUE_LETTERS_COUNT} unique letters:")

#pydoc.pager('\n'.join(str(b) for b in bees))

#    for i in range(0, 100):
#        print(f"{fitting_words[i]} -> {''.join(set(fitting_words[i]))}")
