import re
from collections import Counter
import numpy as np
import pandas as pd

w = []  # words
with open('sample.txt', 'r', encoding="utf8") as f:
    file_name_data = f.read()
    file_name_data = file_name_data.lower()
    w = re.findall('\w+', file_name_data)

v = set(w)  # vocabulary 
print(f"The first 10 words in our dictionary are:\n{w[:10]}")
print(f"The dictionary has {len(v)} words")


def get_count(words):
    word_count_dict = {}
    for word in words:
        if word in word_count_dict:
            word_count_dict[word] += 1
        else:
            word_count_dict[word] = 1
    return word_count_dict


word_count_dict = get_count(w)
print(f"There are {len(word_count_dict)} key-value pairs.")


def get_probs(word_count_dict):
    probs = {}
    m = sum(word_count_dict.values())
    for key in word_count_dict.keys():
        probs[key] = word_count_dict[key] / m
    return probs


def delete_letter(word):
    delete_list = []
    split_list = []
    for i in range(len(word)):
        split_list.append((word[0:i], word[i:]))
    for a, b in split_list:
        delete_list.append(a + b[1:])
    return delete_list


def switch_letter(word):
    split_l = []
    switch_l = []
    for i in range(len(word)):
        split_l.append((word[0:i], word[i:]))
    switch_l = [a + b[1] + b[0] + b[2:] for a, b in split_l if len(b) >= 2]
    return switch_l


def replace_letter(word):
    split_l = []
    replace_list = []
    for i in range(len(word)):
        split_l.append((word[0:i], word[i:]))
    alphabets = 'abcdefghijklmnopqrstuvwxyz'
    replace_list = [a + l + (b[1:] if len(b) > 1 else '') for a, b in split_l if b for l in alphabets]
    return replace_list


def insert_letter(word):
    split_l = []
    insert_list = []
    for i in range(len(word) + 1):
        split_l.append((word[0:i], word[i:]))
    letters = 'abcdefghijklmnopqrstuvwxyz'
    insert_list = [a + l + b for a, b in split_l for l in letters]
    return insert_list


def edit_one_letter(word, allow_switches=True):
    edit_set1 = set()
    edit_set1.update(delete_letter(word))
    if allow_switches:
        edit_set1.update(switch_letter(word))
    edit_set1.update(replace_letter(word))
    edit_set1.update(insert_letter(word))
    return edit_set1


def edit_two_letters(word, allow_switches=True):
    edit_set2 = set()
    edit_one = edit_one_letter(word, allow_switches=allow_switches)
    for w in edit_one:
        if w:
            edit_two = edit_one_letter(w, allow_switches=allow_switches)
            edit_set2.update(edit_two)
    return edit_set2


def get_corrections(word, probs, vocab, n=2):
    suggested_word = (
        [word] if word in vocab else
        list(edit_one_letter(word).intersection(vocab)) or
        list(edit_two_letters(word).intersection(vocab))
    )
    best_suggestion = [[s, probs[s]] for s in reversed(suggested_word)]
    return best_suggestion


my_word = input("Enter any word: ")
probs = get_probs(word_count_dict)
tmp_corrections = get_corrections(my_word, probs, v, 2)
for i, word_prob in enumerate(tmp_corrections):
    print(f"Word {i}: {word_prob[0]}, probability {word_prob[1]:.6f}")
