#!/usr/bin/env python

from Methods import *
import sys


def text2Tweet(text):
    tweet = Tweet({'text': text})
    cleanTweet(tweet)
    return tweet


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit()
    tweet = text2Tweet(sys.argv[1])
    result = analizeTweet(tweet)
    for key in result:
        print(key + ": " + str(result[key]))
