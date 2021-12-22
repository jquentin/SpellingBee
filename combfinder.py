#!/usr/bin/python3

import urllib.request
import pydoc

UNIQUE_LETTERS_COUNT = 7

def load_words():
#    urllib.request.urlretrieve("https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt", "words_alpha.txt")
    with open("words_alpha.txt") as word_file:
        valid_words = word_file.read().split()

    return [word for word in valid_words if len(word) >= 3]
    
    
english_words = load_words()
already_used = set()
    
def is_valid(word):
    has_7_letters = len(word) >= UNIQUE_LETTERS_COUNT and len(''.join(set(word))) == UNIQUE_LETTERS_COUNT
    if has_7_letters:
        other_words = set()
        for w in english_words:
            if w not in already_used and w != word and set(w).issubset(set(word)):
                other_words.add(w)
        if 10 <= len(other_words) <= 30:
            return (True, other_words)
    return (False, set())
    


fitting_words = []

for word in english_words:
    (valid, others) = is_valid(word)
    if valid:
        fitting_words.append(f"{''.join(set(word))} -> {len(others)+1}: {word},{','.join(others)}")
        already_used.add(word)


#fitting_words = list(filter(is_valid, english_words))
print(f"{len(fitting_words)} words with {UNIQUE_LETTERS_COUNT} unique letters:")

pydoc.pager('\n'.join(fitting_words))

#    for i in range(0, 100):
#        print(f"{fitting_words[i]} -> {''.join(set(fitting_words[i]))}")
