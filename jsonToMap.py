#!/usr/bin/env python

import json
import csv


def read_file(filename):
    with open(filename) as f:
        data = json.load(f)
    return data


def write_csv(filename, data):
    with open('tweets.csv', 'w') as f:
        writer = csv.writer(
            f, delimiter=',', quoting=csv.QUOTE_MINIMAL, quotechar='"')
        writer.writerow(['id', 'text', 'positivity'])
        for tweet in data:
            writer.writerow([tweet['id'], tweet['text']])
    print("Done")


if __name__ == "__main__":
    data = read_file('results.json')['tweets']
    write_csv('tweets.csv', data)
