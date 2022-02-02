#!/usr/bin/python3

import urllib.request
import random
import os
import sys
import getopt
import datetime
import json
import hashlib
import unicodedata
import math
import time
import locale

UNIQUE_LETTERS_COUNT = 7

CONGRATS_WORDS = ["Yes!", "Well done!", "Amazing!", "Fantastic!", "Fabulous!", "Wow!", "Perfect!"]
INCORRECT_WORDS = ["Incorrect word", "Nope", "Not a word", "That's not a thing", "What's that?"]
WRONG_LETTERS = ["Wrong letters", "That doesn't work", "Doesn't fit"]

DEFAULT_WORD_LISTS={
    "fr": "https://raw.githubusercontent.com/hbenbel/French-Dictionary/master/dictionary/dictionary.txt",
    "en": "http://www.mieliestronk.com/corncob_lowercase.txt"
}

DEFAULT_LANGUAGE = "en"

LOADING_BAR_LENGTH = 50

KEY_PANGRAMS = "pangrams"
KEY_OTHER_WORDS = "other_words"
KEY_LETTERS = "letters"
KEY_BEES = "bees"

os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))

def cls():
    os.system('cls' if os.name=='nt' else 'clear')
    
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
    
def words_path():
    return f"words_{language}.txt"
        
def bees_path():
    return f"bees_{language}.txt"

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
        print(f"Downloading words: {loading_bar} {math.floor(loading_rate * 100)}%", end='\r')
    else:
        print(f"Downloading words: {loading_bar} 100%")

def load_words(url: str):
    urllib.request.urlretrieve(url, words_path(), show_progress)
    word_file = open(words_path())
    content = word_file.read()
    content = unicodedata.normalize('NFD', content).encode('ascii', 'ignore').decode("utf-8")
    word_file = open(words_path(), "w")
    word_file.write(content)
    words = content.split()
    res = []
    for word in words:
        if len(word) >= 4 and len(set(word)) <= 7 and "'" not in word and "-" not in word:
            res.append(Word(word, set(word)))
    return res

class Bee:
    letters: set
    center: str
    pangrams: set
    other_words: set
    
    def __init__(self, letters: set, center: str, pangrams: set, other_words: set):
        self.letters = letters
        self.center = center
        self.pangrams = pangrams
        self.other_words = other_words
        
    @staticmethod
    def create_bee(word: Word, words):
        res = set()
        if len(word.letters) == UNIQUE_LETTERS_COUNT:
            pangrams = set()
            all_other_words = set()
            for w in words:
                if w.letters == word.letters:
                    pangrams.add(w.word)
                elif w.letters.issubset(word.letters):
                    all_other_words.add(w)
            for center in sorted(word.letters):
                other_words = set()
                for w in all_other_words:
                    if center in w.letters:
                        other_words.add(w.word)
                res.add(Bee(word.letters, center, pangrams, other_words))
        return res
                
    @staticmethod
    def create_bees(words):
        bees = []
        index = 0
        used_letters = set()
        for word in words:
            loading_rate = index / len(words)
            loading_bar = get_loading_bar(loading_rate, LOADING_BAR_LENGTH)
            print(f"Generating bees: {loading_bar} {math.floor(loading_rate * 100)}%", end = '\r')
            if word.letters not in used_letters:
                bee = Bee.create_bee(word, words)
                if bee is not None:
                    bees.extend(list(bee))
                    used_letters.add(frozenset(word.letters))
            index += 1
        print(f"Generating bees: {loading_bar} 100%")
        return bees
        
    def show_letters(self):
        other_letters = self.letters - set(self.center)
        return f"{self.center}{''.join(random.sample(list(other_letters),len(other_letters)))}"
    
    def __str__(self):
        return f"{self.show_letters()} -> {len(self.other_words)+1}: {','.join(self.pangrams)},{','.join(self.other_words)}"
          
class HashedBee(Bee):
    
    def guess(self):
        words_count = len(self.other_words) + len(self.pangrams)
        words_found = set()
        pangrams_found = set()
        letters_ordered = self.show_letters()
        while len(words_found) < words_count:
            cls()
            print(f"{letters_ordered}")
            print(f"{len(words_found)}/{words_count} words found: {','.join(sorted(words_found))}")
            print(f"{len(pangrams_found)}/{len(self.pangrams)} pangrams found: {','.join(sorted(pangrams_found))}")
            word = input()
            hash_word = str(hash(word))
            if verbose:
                print(f"hash: {hash_word}")
            if word == "":
                continue
            elif word == "s" or word == "r":
                letters_ordered = self.show_letters()
                continue
            elif len(word) < 4:
                print("Word too short")
            elif word in words_found:
                print("Word already found")
            elif self.center not in word:
                print("Word missing the central letter (1st letter)")
            elif hash_word in self.other_words:
                print(CONGRATS_WORDS[random.randint(0, len(CONGRATS_WORDS)-1)])
                words_found.add(word)
            elif hash_word in self.pangrams:
                print("PANGRAM!")
                words_found.add(word)
                pangrams_found.add(word)
            elif set(word).issubset(self.letters):
                print(INCORRECT_WORDS[random.randint(0, len(INCORRECT_WORDS)-1)])
            else:
                print(WRONG_LETTERS[random.randint(0, len(WRONG_LETTERS)-1)])
            time.sleep(1)
        print("You found everything! Congratulations Jessica!")
    
    @staticmethod
    def create_from_dict(dict):
        return HashedBee(set(dict[KEY_LETTERS]), dict[KEY_LETTERS][0], set(dict[KEY_PANGRAMS]), set(dict[KEY_OTHER_WORDS]))
        
    
print_all = False
write_file = False
verbose = False
search_bee = None
diff_min = 10
diff_max = 50
date = datetime.date.today()
url = None

if locale.getlocale()[0] is None:
    locale.setlocale(locale.LC_ALL, '')
if locale.getlocale()[0] is not None and locale.getlocale()[0][0:2] in DEFAULT_WORD_LISTS.keys():
    language = locale.getlocale()[0][0:2]
else:
    language = DEFAULT_LANGUAGE

try:
    opts, args = getopt.getopt(sys.argv[1:], "n:lwvg:s:d:u:m:M:", ["words-count", "list", "write", "verbose", "language", "search", "date", "url", "min", "max"])
except getopt.GetoptError as err:
    print("error options")
    sys.exit(2)
for o, a in opts:
    if o == "-n":
        diff = int(a)
        diff_min = diff - 5
        diff_max = diff +5
    if o == "-l":
        print_all = True
    if o == "-w":
        write_file = True
    if o == "-v":
        verbose = True
    elif o == "-g":
        language = a
    elif o == "-s":
        search_bee = a
    elif o == "-d":
        date = datetime.date.fromisoformat(a)
    elif o == "-u":
        url = a
    elif o == "-m":
        url = diff_min = int(a)
    elif o == "-M":
        url = diff_max = int(a)
        
def generate_bees():
    start_time = datetime.datetime.now()
    words = load_words(DEFAULT_WORD_LISTS[language])
    bees = Bee.create_bees(words)
    end_time = datetime.datetime.now()
    print(f"Generated {len(bees)} bees in {(end_time - start_time).seconds}s from {len(words)} words")
    return bees

def read_hashed_bees():
    print("Reading bees file")
    word_file = open(bees_path())
    json_data = json.load(word_file)
    bees = [HashedBee.create_from_dict(bee_dict) for bee_dict in json_data[KEY_BEES] if diff_min <= len(bee_dict[KEY_OTHER_WORDS]) <= diff_max]
    print(f"Read {len(bees)} hashed bees with {diff_min} to {diff_max} words")
    return bees
    
def write_bees_file():
    bees = generate_bees()
    dict = {KEY_BEES: []}
    print("Creating bees dictionary")
    for b in bees:
        if diff_min <= len(b.other_words) <= diff_max:
            bee_dict = {KEY_LETTERS: b.show_letters(), KEY_PANGRAMS: [], KEY_OTHER_WORDS: []}
            for w in b.other_words:
                bee_dict[KEY_OTHER_WORDS].append(hash(w))
            for w in b.pangrams:
                bee_dict[KEY_PANGRAMS].append(hash(w))
            dict[KEY_BEES].append(bee_dict)
    print("Writing bees file")
    with open(bees_path(), "w") as word_file:
        json.dump(dict, word_file, indent = 1)

if write_file:
    write_bees_file()
elif print_all:
    bees = generate_bees()
    all_bees = ""
    index = 0
    for b in bees:
        all_bees += f"{index} - {str(b)}\n"
        index += 1
    pydoc.pager(all_bees)
elif search_bee is not None:
    bees = generate_bees()
    bee = [b for b in bees if b.center == search_bee[0] and b.letters == set(search_bee)][0]
    print(bee)
else:
    if not os.path.exists(bees_path()):
        print(f"First time playing in lang={language} -> generating bees file. This might take a few minutes.")
        write_bees_file()
    bees = read_hashed_bees()
    print(f"Spelling bee for {date}")
    seed = (date - datetime.datetime.utcfromtimestamp(0).date()).days
    print(f"Seed: {seed}")
    random.seed(seed)
    bee_index = random.randint(0, len(bees)-1)
    print(f"Bee number: {bee_index}")
    bee = bees[bee_index]
    print("Starting game")   
    time.sleep(1)
    bee.guess()

#fitting_words = list(filter(is_valid, english_words))
#print(f"{len(bees)} words with {UNIQUE_LETTERS_COUNT} unique letters:")

#pydoc.pager('\n'.join(str(b) for b in bees))

#    for i in range(0, 100):
#        print(f"{fitting_words[i]} -> {''.join(set(fitting_words[i]))}")
