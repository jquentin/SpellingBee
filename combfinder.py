#!/usr/bin/python3

import urllib.request
import pydoc

UNIQUE_LETTERS_COUNT = 7

def load_words():
#    urllib.request.urlretrieve("https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt", "words_alpha.txt")
    with open("words_alpha.txt") as word_file:
        valid_words = word_file.read().split()

    return valid_words
    
def is_valid(word):
    return len(word) >= UNIQUE_LETTERS_COUNT and len(''.join(set(word))) == UNIQUE_LETTERS_COUNT
    



if __name__ == '__main__':
    english_words = load_words()
    fitting_words = list(filter(is_valid, english_words))
    print(f"{len(fitting_words)} words with {UNIQUE_LETTERS_COUNT} unique letters:")

    pydoc.pager('\n'.join(f"{word} -> {''.join(set(word))}" for word in fitting_words))

#    for i in range(0, 100):
#        print(f"{fitting_words[i]} -> {''.join(set(fitting_words[i]))}")
