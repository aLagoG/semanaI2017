#!/usr/bin/env python

import json
from Tweets import *
from random import choice
from metodos import *
from emojiAlgorithm import *

data = read_json_file('full_data.json')

d1 = read_file("combined_dictionary.json")
d2 = read_file("replaced_dictionary.json")

dicts = [d1,d2]

methods = [analizarTweet, analizarTweet2, analizarTweet3]

for i in range(20):
    tweet = choice(data)
    print(tweet.text)
    print("##################################")
    print(tweet.text_clean)
    for fn in methods:
        print(str(fn(tweet, d1))+"\t"+str(fn(tweet, d2)))
    if len(tweet.emoji) > 0:
        print("Emoji: "+str(analizeEmoji(tweet.emoji)))