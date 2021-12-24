#!/usr/bin/python3

import urllib.request
import pydoc
import random
import os
import sys
import getopt
import datetime
import json
import hashlib

UNIQUE_LETTERS_COUNT = 7

CONGRATS_WORDS = ["Yes!", "Well done!", "Amazing!", "Fantastic!", "Fabulous!", "Wow!", "Perfect!"]
INCORRECT_WORDS = ["Incorrect word", "Nope", "Not a word", "That's not a thing", "What's that?"]
WRONG_LETTERS = ["Wrong letters", "That doesn't work", "Doesn't fit"]

LOADING_BAR_LENGTH = 60

os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))
    
def get_loading_bar(loading_rate, bar_length):
    loading_bar = "["
    for i in range(0, bar_length):
        if i < loading_rate * bar_length:
            loading_bar += "█"
        else:
            loading_bar += " "
    loading_bar += "]"
    return loading_bar

def hash(s: str):
    return hashlib.sha1(s.encode('utf-8')).hexdigest()[:6]

class Word:
    word: str
    letters: set
    
    def __init__(self, word: str, letters: set):
        self.word = word
        self.letters = letters
        

def show_progress(block_num, block_size, total_size):
            
    loading_rate = block_num * block_size / total_size
    loading_bar = get_loading_bar(loading_rate, LOADING_BAR_LENGTH)
    if loading_rate < 1:
        print(f"Downloading words: {loading_bar} {round(loading_rate * 100)}%", end='\r')
    else:
        print(f"Downloading words: {loading_bar} 100%")

def load_words():
    urllib.request.urlretrieve("http://www.mieliestronk.com/corncob_lowercase.txt", "words.txt", show_progress)
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
    def create_bee(word: Word, words):
        res = set()
        has_7_letters = len(word.letters) == UNIQUE_LETTERS_COUNT
        if has_7_letters:
            all_other_words = set()
            for w in words:
                if w.letters.issubset(word.letters) and w.word != word.word:
                    all_other_words.add(w)
            for center in sorted(word.letters):
                other_words = set()
                for w in all_other_words:
                    if center in w.letters:
                        other_words.add(w.word)
                res.add(Bee(word.letters, center, word.word, other_words))
        return res
                
    @staticmethod
    def create_bees(words):
        bees = []
        index = 0
        for word in words:
            loading_rate = index / len(words)
            loading_bar = get_loading_bar(loading_rate, LOADING_BAR_LENGTH)
            print(f"Generating bees: {loading_bar} {round(loading_rate * 100)}%", end = '\r')
            bee = Bee.create_bee(word, words)
            if bee is not None:
                bees.extend(list(bee))
            index += 1
        print(f"Generating bees: {loading_bar} 100%")
        return bees
        
    def show_letters(self):
        other_letters = self.letters - set(self.center)
        return f"{self.center}{''.join(random.sample(other_letters,len(other_letters)))}"
    
    def __str__(self):
        return f"{self.show_letters()} -> {len(self.other_words)+1}: {self.pangram},{','.join(self.other_words)}"
        
#    def hashed_str(self):
#        return f"{self.show_letters()} -> {','.join(str(hash(w)) for w in self.other_words)}"
        
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
          
class HashedBee(Bee):
    
    def guess(self):
        words_count = len(self.other_words)+1
        print(f"{self.show_letters()} -> {words_count} words to find")
        words_found = set()
        while len(words_found) < words_count:
            word = input()
            if word == "":
                continue
            elif word == "s" or word == "r" or word == "i":
                print(f"{self.show_letters()} -> {words_count - len(words_found)} words remaining")
                print(f"Words found: {','.join(words_found)}")
                continue
            hash_word = str(hash(word))
            if verbose:
                print(f"hash: {hash_word}")
            if word in words_found:
                print("Word already found")
            elif self.center not in word:
                print("Word missing the central letter (1st letter)")
            elif hash_word in self.other_words:
                print(CONGRATS_WORDS[random.randint(0, len(CONGRATS_WORDS)-1)])
                words_found.add(word)
            elif hash_word == self.pangram:
                print("PANGRAM!")
                words_found.add(word)
            elif set(word).issubset(self.letters):
                print(INCORRECT_WORDS[random.randint(0, len(INCORRECT_WORDS)-1)])
            else:
                print(WRONG_LETTERS[random.randint(0, len(WRONG_LETTERS)-1)])
            print(f"{words_count - len(words_found)} words remaining")
        print("You found everything! Congratulations Jessica!")
    
    @staticmethod
    def create_from_dict(dict):
        return HashedBee(set(dict["letters"]), dict["letters"][0], dict["pangram"], set(dict["other_words"]))
        
    
print_all = False
write_file = False
verbose = False
search_bee = None

try:
    opts, args = getopt.getopt(sys.argv[1:], "lwvs:", ["list", "write", "verbose", "search"])
except getopt.GetoptError as err:
    print("error options")
    sys.exit(2)
for o, a in opts:
    if o == "-l":
        print_all = True
    if o == "-w":
        write_file = True
    if o == "-v":
        verbose = True
    elif o == "-s":
        search_bee = a
        
def generate_bees():
    start_time = datetime.datetime.now()
    english_words = load_words()
    bees = Bee.create_bees(english_words)
    end_time = datetime.datetime.now()
    print(f"Generated {len(bees)} bees in {(end_time - start_time).seconds}s from {len(english_words)} words")
    return bees

def read_hashed_bees():
    print("Reading bees file")
    word_file = open("./bees.txt")
    json_data = json.load(word_file)
    bees = [HashedBee.create_from_dict(bee_dict) for bee_dict in json_data["bees"]]
    print(f"Read {len(bees)} hashed bees from file")
    return bees
    
def write_bees_file():
    bees = generate_bees()
    dict = {"bees": []}
    for b in bees:
        bee_dict = {"letters": b.show_letters(), "pangram": hash(b.pangram), "other_words": []}
        for w in b.other_words:
            bee_dict["other_words"].append(hash(w))
        dict["bees"].append(bee_dict)
    print("Writing bees file")
    with open("./bees.txt", "w") as word_file:
        json.dump(dict, word_file, indent = 1)

if write_file:
    write_bees_file()
elif print_all:
    bees = generate_bees()
    all_bees = ""
    index = 0
    for b in bees:
        all_bees += f"{index} - {b.hashed_str()}\n"
        index += 1
    pydoc.pager(all_bees)
elif search_bee is not None:
    bees = generate_bees()
    bee = [b for b in bees if b.center == search_bee[0] and b.letters == set(search_bee)][0]
    print(bee)
else:
    if not os.path.exists("./bees.txt"):
        print("First time playing -> generating bees file. This might take a couple minutes.")
        write_bees_file()
    bees = read_hashed_bees()
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
