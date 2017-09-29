#!/usr/bin/env python

import json
from Tweets import *


def read_file(filename):
    with open(filename) as f:
        data = json.load(f)
    return data


def analizeTweetMax(tweet, dictionary):
    words = tweet.text_clean.split()
    if len(words) == 0:
        return 0
    result = 0
    for word in words:
        if word in dictionary:
            p = dictionary[word]['p']
            n = dictionary[word]['n']
            neutral = dictionary[word]['-']
            if p > n and p > neutral:
                result += p
            elif n > p and n > neutral:
                result -= n
    return result / len(words)


def analizeTweetAll(tweet, dictionary):
    words = tweet.text_clean.split()
    if len(words) == 0:
        return 0
    result = 0
    for word in words:
        if word in dictionary:
            p = dictionary[word]['p']
            n = dictionary[word]['n']
            neutral = dictionary[word]['-']
            result += p - n
    return result / len(words)


def analizeTweetComplement(tweet, dictionary):
    words = tweet.text_clean.split()
    if len(words) == 0:
        return 0
    result = 0
    for word in words:
        if word in dictionary:
            p = dictionary[word]['p']
            n = dictionary[word]['n']
            neutral = dictionary[word]['-']
            if p < n:
                p = 1 - n
            elif n < p:
                n = 1 - p
            result += p - n
    return result / len(words)


def correct(a, b):
    if (a > 0 and b > 0) or (a < 0 and b < 0):
        return True
    if a != 0 and 0 != b:
        return False
    return abs(a - b) <= 0.25


if __name__ == '__main__':

    data = read_json_file('650_completos.json')

    dictionaries = [
        read_file("combined_dictionary.json"), read_file("replaced_dictionary.json"), read_file(
            "average_dictionary.json"), read_file("our_dictionary.json")]

    methods = [analizeTweetMax, analizeTweetAll, analizeTweetComplement]

    for method in methods:
        print("################")
        for dictionary in dictionaries:
            count_correct = 0
            for tweet in data:
                if correct(tweet.polarity, method(tweet, dictionary)):
                    count_correct += 1
            print(count_correct / len(data))
