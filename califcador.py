#!/usr/bin/env python

import json
from Tweets import *
from random import choice
from metodos import *
from emojiAlgorithm import *

data = read_json_file('full_data.json')

d1 = read_file("combined_dictionary.json")
d2 = read_file("replaced_dictionary.json")
d3 = read_file("average_dictionary.json")
dicts = [d1,d2,d3]

methods = [analizarTweet, analizarTweet2, analizarTweet3]

for i in range(20):
    tweet = choice(data)
    print(tweet.text)
    print("##################################")
    print(tweet.text_clean)
    for fn in methods:
        print("\t".join([str(fn(tweet,dic) ) for dic in dicts]))
    if len(tweet.emoji) > 0:
        print("Emoji: "+str(analizeEmoji(tweet.emoji)))