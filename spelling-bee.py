from browser import document, alert, html, load, window, timer
from browser.local_storage import storage
import urllib.request
import random
import datetime
import json
import hashlib
import unicodedata
import math
import time

load("bundle.js")

UNIQUE_LETTERS_COUNT = 7

CONGRATS_WORDS = ["Yes!", "Well done!", "Amazing!", "Fantastic!", "Fabulous!", "Wow!", "Perfect!"]
INCORRECT_WORDS = ["Incorrect word", "Nope", "Not a word", "That's not a thing", "What's that?"]
WRONG_LETTERS = ["Wrong letters", "That doesn't work", "Doesn't fit"]

DEFAULT_WORD_LISTS={
    "fr": "https://raw.githubusercontent.com/hbenbel/French-Dictionary/master/dictionary/dictionary.txt",
    "en": "http://www.mieliestronk.com/corncob_lowercase.txt",
    "de": "https://raw.githubusercontent.com/enz/german-wordlist/master/words"
}

DEFAULT_LANGUAGE = "en"

LOADING_BAR_LENGTH = 50

KEY_PANGRAMS = "pangrams"
KEY_OTHER_WORDS = "other_words"
KEY_LETTERS = "letters"
KEY_BEES = "bees"

WEEKDAYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]

ALL_TIMES_LEADERBOARD_ID = "all_time_points"
DAILY_LEADERBOARD_ID = "daily_points"

words_found = set()
pangrams_found = set()
letters_ordered = ""
word = ""

def hash(s: str):
    return hashlib.sha1(s.encode('utf-8')).hexdigest()[:6]

class Word:
    word: str
    letters: set

    def __init__(self, word: str, letters: set):
        self.word = word
        self.letters = letters

def today_key() -> str:
    return WEEKDAYS[day_of_week]

def yesterday_key() -> str:
    return WEEKDAYS[(day_of_week - 1) % 7]

def get_leaderboard_id(day_key: str) -> str:
    return f"{DAILY_LEADERBOARD_ID}_{day_key}_{language}"

def get_today_leaderboard_id() -> str:
    return get_leaderboard_id(today_key())

def get_yesterday_leaderboard_id() -> str:
    return get_leaderboard_id(yesterday_key())

def get_all_times_leaderboard_id() -> str:
    return f"{ALL_TIMES_LEADERBOARD_ID}_{language}"

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

    def show_letters(self):
        print(f"show_letters({self.letters})")
        other_letters = self.letters - set(self.center)
        res = f"{self.center.upper()}{''.join(random.sample(list(l.upper() for l in other_letters),len(other_letters)))}"
        print(res)
        return res

    def show_letters_ordered(self):
        other_letters = self.letters - set(self.center)
        res = f"{self.center}{''.join(sorted(list(other_letters)))}"
        return res

    @staticmethod
    def order_bee_letters(letters):
        res = f"{letters[0]}{''.join(sorted(letters[1:]))}"
        return res

    def __str__(self):
        return f"{self.show_letters()} -> {len(self.all_words())}: {','.join(self.pangrams)},{','.join(self.other_words)}"

    def all_words(self):
        return self.pangrams | self.other_words

    def is_pangram(self, word):
        return set(word) == self.letters


class HashedBee(Bee):

    def guess(self):
        words_count = len(self.all_words())
        words_found = set()
        pangrams_found = set()
        letters_ordered = self.show_letters()

    def try_guess(self, word):
        result = False
        word = word.lower()
        print(f"try_guess({word})")
        print(f"{letters_ordered}")
        hash_word = str(hash(word))
        if word == "":
            return
        elif len(word) < 4:
            feedback("Word too short", True, False)
        elif word in words_found:
            feedback("Word already found", True, False)
        elif self.center not in word:
            feedback(f"Word missing the central letter ({self.center})", True, False)
        elif hash_word in self.other_words:
            feedback(CONGRATS_WORDS[random.randint(0, len(CONGRATS_WORDS)-1)], False, False)
            words_found.add(word)
            result = True
        elif hash_word in self.pangrams:
            feedback("PANGRAM!", False, True)
            words_found.add(word)
            pangrams_found.add(word)
            result = True
        elif set(word).issubset(self.letters):
            feedback(INCORRECT_WORDS[random.randint(0, len(INCORRECT_WORDS)-1)], True, False)
        else:
            feedback(WRONG_LETTERS[random.randint(0, len(WRONG_LETTERS)-1)], True, False)
        clear_word()
        if result:
            window.submit_word(word, language)
        return result

    @staticmethod
    def create_from_dict(dict):
        return HashedBee(set(dict[KEY_LETTERS]), dict[KEY_LETTERS][0], set(dict[KEY_PANGRAMS]), set(dict[KEY_OTHER_WORDS]))

date = datetime.datetime.utcnow().date()
day_of_week = date.weekday()

if "language" in storage.keys() and storage["language"] in DEFAULT_WORD_LISTS.keys():
    language = storage["language"]
else:
    device_language = window.get_language()
    if device_language is not None and device_language[0:2] in DEFAULT_WORD_LISTS.keys():
        language = device_language[0:2]
    else:
        language = DEFAULT_LANGUAGE

for lang_flag in document.get(name="lang"):
    lang_flag.checked = lang_flag.value == language

print(f"language: {language}")

button1 = document["button1"]
button2 = document["button2"]
button3 = document["button3"]
button4 = document["button4"]
button5 = document["button5"]
button6 = document["button6"]
buttonC = document["buttonC"]
button1_text = button1.select("text")[0]
button2_text = button2.select("text")[0]
button3_text = button3.select("text")[0]
button4_text = button4.select("text")[0]
button5_text = button5.select("text")[0]
button6_text = button6.select("text")[0]
buttonC_text = buttonC.select("text")[0]
sb_hive_input_content = document.select(".sb-hive-input-content")[0]
sb_wordlist_items_pag = document.select(".sb-wordlist-items-pag")[0]
sb_recent_words = document.select(".sb-recent-words")[0]
sb_content_box = document.select(".sb-content-box")[0]
sb_message_box = document.select(".sb-message-box")[0]
progress_bar = document["progress-bar"]
progress_text = document["progress-text"]
leaderboard_btn = document["leaderboard-btn"]
leaderboard_modal = document["leaderboard-modal"]
account_modal = document["account-modal"]
email_modal = document["email-modal"]
scores_list_yesterday = document["scores-list-yesterday"]
scores_list_today = document["scores-list-today"]
scores_list_alltimes = document["scores-list-alltimes"]
username_txts = document.select("#username")
leaderboards_loading = document["leaderboards-loading"]


print(language)
window.rpc("GetTodaysBeeAndWordsFound", json.dumps({"language": language}), lambda bee_json: set_bee_and_start(bee_json.to_dict()))

def set_bee_and_start(bee_json):
    print(bee_json)
    global letters_ordered, bee, words_found
    bee = HashedBee.create_from_dict(bee_json["bee"])
    letters_ordered = bee.show_letters()
    print("Starting game")
    bee.guess()
    words_found = set(bee_json["wordsFound"])

    update_letters()
    update_word()
    update_word_list()
    update_email()
    load_and_update_username()
    window.rpc("GetYesterdaysBeeAndWordsFound", json.dumps({"language": language}), lambda bee_json: setup_yesterday(bee_json.to_dict()))

def setup_yesterday(bee_json):
    print(bee_json)
    yesterday_wordlist = document["yesterday-wordlist"]
    yesterday_wordlist.clear()
    for word in sorted(bee_json["bee"]["pangrams"]) + sorted(bee_json["bee"]["other_words"]):
        prefix = "&#9989;" if word in bee_json["wordsFound"] else "&#10060;"
        word_item = html.LI(f"{prefix} {word}")
        if len(set(word)) == 7:
            word_item.class_name = "rainbow-text"
        yesterday_wordlist <= word_item

def add_letter(letter: str):
    print(f"add_letter({letter.strip()})")
    global word
    word += letter.strip()
    update_word()

def button1clicked(event):
    global button1_text
    add_letter(button1_text.text)

def button2clicked(event):
    global button2_text
    add_letter(button2_text.text)

def button3clicked(event):
    global button3_text
    add_letter(button3_text.text)

def button4clicked(event):
    global button4_text
    add_letter(button4_text.text)

def button5clicked(event):
    global button5_text
    add_letter(button5_text.text)

def button6clicked(event):
    global button6_text
    add_letter(button6_text.text)

def buttonCclicked(event):
    global buttonC_text
    add_letter(buttonC_text.text)

def update_word_list():
    global sb_wordlist_items_pag, sb_recent_words
    sb_wordlist_items_pag.clear()
    sb_recent_words.clear()
    progress_text.text = f"{len(words_found)}/{len(bee.all_words())} words found"
    progress_bar.style = {"width": f"{len(words_found)/len(bee.all_words()) * 100}%"}
    for word in sorted(words_found):
        word_item = html.LI(word)
        if bee.is_pangram(word):
            word_item.class_name = "rainbow-text"
            pangrams_found.add(word)
        sb_wordlist_items_pag <= word_item
        sb_recent_words <= word_item.clone()
    for index, pangram in enumerate(bee.pangrams):
        img_src = "star-full.png" if index < len(pangrams_found) else "star-empty.png"
        pos_x = (len(bee.pangrams) - index - 1) * 18 + 6
        document["progress-text-container"] <= html.IMG("", src=img_src, Class="pangram-star", style={"right": f"{pos_x}px"})

def button_enter_clicked(event):
    correct = bee.try_guess(word)
    if correct:
        update_word_list()
    clear_word()

def button_delete_clicked(event):
    global word
    word = word[:-1]
    update_word()

def button_shuffle_clicked(event):
    print("shuffle")
    global letters_ordered
    letters_ordered = bee.show_letters()
    update_letters()


def document_changed(event):
    match event.target.name:
        case "lang":
            language = event.target.value
            storage["language"] = event.target.value
            document.location.reload()
        case "username":
            window.change_username(event.target.value)
            print(f"username_changed to {event.target.value}")
            load_and_update_username()

def button_expand_wordlist_clicked(event):
    if "sb-expanded" in sb_content_box.class_name:
        sb_content_box.class_name = "sb-content-box"
        document["yesterday-button"].style.display = "Block"
    else:
        sb_content_box.class_name = "sb-content-box sb-expanded"
        document["yesterday-button"].style.display = "None"

def update_leaderboard(scores_list, scores):

    medals = ["&#129351;", "&#129352;", "&#129353;"]
    medal_index = -1
    last_score = -1
    for ind, score_entry in enumerate(scores):
        score = score_entry.to_dict()['score']
        username = score_entry.to_dict()['username']
        if score != last_score:
             medal_index = ind
             last_score = score
        medal = medals[medal_index] if medal_index < len(medals) else ""
        scores_list <= html.LI(f"{medal}{username}: {score}")

    leaderboards_loading.style.display = "none"

def button_leaderboard_clicked(event):
    print("leaderboard_clicked")
    leaderboard_modal.style.display = "block";

    scores_list_today.clear()
    scores_list_yesterday.clear()
    scores_list_alltimes.clear()

    window.list_scores(get_today_leaderboard_id(), lambda scores_today : update_leaderboard(scores_list_today, scores_today))
    window.list_scores(get_yesterday_leaderboard_id(), lambda scores_yesterday : update_leaderboard(scores_list_yesterday, scores_yesterday))
    window.list_scores(get_all_times_leaderboard_id(), lambda scores_all_times : update_leaderboard(scores_list_alltimes, scores_all_times))

    window.display_leaderboard("Today")
    leaderboards_loading.style.display = "inline"

def button_account_clicked(event):
    print("account_clicked")
    account_modal.style.display = "block"

def button_email_connect_clicked(event):
    print("account_clicked")
    email_modal.style.display = "block"

def button_modal_close_clicked(event):
    print("modal_close_clicked")
    close_modals()

def window_clicked(event):
    if "modal" in event.target.class_name:
        close_modals()

def close_modals():
    for modal in document.select(".modal"):
        modal.style.display = "none";

def button_email_submit_clicked(event):
    window.connect_email(document["email-input"].value, document["password-input"].value)
    timer.set_timeout(on_email_submit_complete, 1000)

def button_yesterday_clicked(event):
    print("button_yesterday_clicked")
    document["yesterday-modal"].style.display = "Block"

def button_report_clicked(event):
    document["report-modal"].style.display = "Block"

def button_info_clicked(event):
    document["info-modal"].style.display = "Block"

def button_report_submit_clicked(event):
    word = document["report-word-input"].value
    shouldExist = document["report-to-add"].checked
    window.rpc("ReportWord", json.dumps({"word": word, "language": language, "shouldExist": shouldExist}), lambda response: print("word reported"))
    close_modals()
    clear_report_modal()

def clear_report_modal():
    document["report-to-add"].checked = True
    document["report-to-remove"].checked = False
    document["report-word-input"].value = ""

def on_email_submit_complete():
    if window.error == "":
        update_email()
        load_and_update_username()
        close_modals()
    else:
        document["email-error-txt"].text = window.error
        document["email-error-txt"].style.display = "block"

def clear_word():
    print("clear_word")
    global word
    word = ""
    update_word()

def update_word():
    global sb_hive_input_content
    print(f"update label to {word}")
    sb_hive_input_content.clear()
    sb_hive_input_content.class_name = "sb-hive-input-content" if word == "" else "sb-hive-input-content non-empty"
    for letter in word:
        sb_hive_input_content <= html.SPAN(letter.strip(), Class="sb-input-bright" if letter.lower() == bee.center else "")

def update_letters():
    global button1_text, button2_text, button3_text, button4_text, button5_text, button6_text, buttonC_text
    button1_text.text = letters_ordered[1]
    button2_text.text = letters_ordered[2]
    button3_text.text = letters_ordered[3]
    button4_text.text = letters_ordered[4]
    button5_text.text = letters_ordered[5]
    button6_text.text = letters_ordered[6]
    buttonC_text.text = letters_ordered[0]

def update_username(username):
    print("update_username")
    for username_txt in username_txts:
        username_txt.value = username
        username_txt.text = username

def update_email():
    if "email" in storage:
        document["email-txt"].text = storage["email"]
        document["email-connect-btn"].style.display = "None"
    else:
        document["email-txt"].text = "None"
        document["email-connect-btn"].style.display = "Block"

def load_and_update_username():
    print("load_and_update_username")
    window.update_user(update_username)

def feedback(msg, isError, isPangram):
    class_name = "sb-message-box"
    if isPangram:
        class_name += " pangram-message"
    elif isError:
        class_name += " error-message"
    else:
        class_name += " success-message"
    sb_message_box.class_name = class_name
    sb_message_box.clear()
    sb_message_box <= html.SPAN(msg, Class="sb-message")

button1.bind("click", button1clicked)
button2.bind("click", button2clicked)
button3.bind("click", button3clicked)
button4.bind("click", button4clicked)
button5.bind("click", button5clicked)
button6.bind("click", button6clicked)
buttonC.bind("click", buttonCclicked)
document["button_enter"].bind("click", button_enter_clicked)
document["button_delete"].bind("click", button_delete_clicked)
document["button_shuffle"].bind("click", button_shuffle_clicked)
document.select(".sb-toggle-expand")[0].bind("click", button_expand_wordlist_clicked)
leaderboard_btn.bind("click", button_leaderboard_clicked)
window.bind('click', window_clicked)
document["account-btn"].bind('click', button_account_clicked)
document["email-connect-btn"].bind('click', button_email_connect_clicked)
document["email-submit"].bind('click', button_email_submit_clicked)
document["yesterday-button"].bind('click', button_yesterday_clicked)
document["report-button"].bind('click', button_report_clicked)
document["report-submit"].bind('click', button_report_submit_clicked)
document["info-button"].bind('click', button_info_clicked)

document.bind('change', document_changed)

clear_report_modal()

print(".modal_close_btn")
for close_btn in document.select(".modal-close-btn"):
    print(close_btn)
    close_btn.bind('click', button_modal_close_clicked)

