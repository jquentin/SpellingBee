#!/usr/bin/python3

import urllib.request
import pydoc

UNIQUE_LETTERS_COUNT = 7

def load_words():
#    urllib.request.urlretrieve("https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt", "words_alpha.txt")
    with open("words_alpha.txt") as word_file:
        valid_words = word_file.read().split()

    return [word for word in valid_words if len(word) >= 3]

class Bee:
    letters: set
    pangram: str
    other_words: set
    
    def __init__(self, letters: set, pangram: str, other_words: set):
        self.letters = letters
        self.pangram = pangram
        self.other_words = other_words
        
    @staticmethod
    def create_bee(word: str):
        has_7_letters = len(word) >= UNIQUE_LETTERS_COUNT and len(''.join(set(word))) == UNIQUE_LETTERS_COUNT
        if has_7_letters:
            other_words = set()
            for w in english_words:
                if w != word and set(w).issubset(set(word)):
                    other_words.add(w)
            if 10 <= len(other_words) <= 30:
                return Bee(set(word), word, other_words)
        return None
                
    @staticmethod
    def create_bees(words):
        bees = []
        for word in words:
            bee = Bee.create_bee(word)
            if bee is not None:
                bees.append(bee)
        return bees
    
    def __str__(self):
        return f"{''.join(self.letters)} -> {len(self.other_words)+1}: {self.pangram},{','.join(self.other_words)}"
        
english_words = load_words()
bees = Bee.create_bees(english_words)

#fitting_words = list(filter(is_valid, english_words))
#print(f"{len(bees)} words with {UNIQUE_LETTERS_COUNT} unique letters:")

pydoc.pager('\n'.join(str(b) for b in bees))

#    for i in range(0, 100):
#        print(f"{fitting_words[i]} -> {''.join(set(fitting_words[i]))}")
