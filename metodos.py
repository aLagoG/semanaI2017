#!/usr/bin/env python

import json
from Tweets import *


def read_file(filename):
    with open(filename) as f:
        data = json.load(f)
    return data


def analizarTweet(tweet, diccionario):
    polaridadtotal = 0

    sentence = tweet.text.split(" ")
    for word in sentence:
        polaridad = 0
        confiabilidad = 0
        if word in diccionario:
            p = diccionario[word]["p"]
            n = diccionario[word]["n"]
            neutral = diccionario[word]["-"]
            total = p + n + neutral

            if (p > n and p > neutral):
                polaridad = 1
                confiabilidad = (p * 100) / total
            elif (n > p and n > neutral):
                polaridad = -1
                confiabilidad = (n * 100) / total
            else:
                polaridad = 0
                confiabilidad = neutral / total
        polaridadtotal += confiabilidad * polaridad
    valor = polaridadtotal / len(sentence)
    return valor


def analizarTweet2(tweet, diccionario):
    polaridadtotal = 0
    polaridadpositiva = 0
    polaridadnegativa = 0

    sentence = tweet.text.split(" ")
    for word in sentence:
        if word in diccionario:
            p = diccionario[word]["p"]
            n = diccionario[word]["n"]
            neutral = diccionario[word]["-"]
            total = p + n + neutral

            polaridadpositiva = polaridadpositiva + (p * 100) / total
            polaridadnegativa = polaridadnegativa - (n * 100) / total

            polaridadtotal = polaridadpositiva + polaridadnegativa

    valor = polaridadtotal / len(sentence)
    return valor


def analizarTweet3(tweet, diccionario):
    polaridadtotal = 0
    polaridadpositiva = 0
    polaridadnegativa = 0

    sentence = tweet.text.split(" ")
    for word in sentence:
        if word in diccionario:
            p = diccionario[word]["p"]
            n = diccionario[word]["n"]
            neutral = diccionario[word]["-"]
            total = p + n + neutral
            if p > n:
                n += neutral
            elif n > p:
                p += neutral

            polaridadpositiva = polaridadpositiva + (p * 100) / total
            polaridadnegativa = polaridadnegativa - (n * 100) / total

            polaridadtotal = polaridadpositiva + polaridadnegativa

    valor = polaridadtotal / len(sentence)
    return valor


if __name__ == '__main__':

    data = read_json_file('650_completos.json')

    d1 = read_file("combined_dictionary.json")
    d2 = read_file("replaced_dictionary.json")

    m1d1 = {tweet.id: analizarTweet(tweet, d1) for tweet in data}
    m1d2 = {tweet.id: analizarTweet(tweet, d2) for tweet in data}

    scoreM1D1 = sum([1 if m1d1[tweet.id] * tweet.polarity >=
                     0 else 0 for tweet in data]) / len(data)
    scoreM1D2 = sum([1 if m1d2[tweet.id] * tweet.polarity >=
                     0 else 0 for tweet in data]) / len(data)

    print("Metodo #1")
    print(scoreM1D1)
    print(scoreM1D2)

    m2d1 = {tweet.id: analizarTweet2(tweet, d1) for tweet in data}
    m2d2 = {tweet.id: analizarTweet2(tweet, d2) for tweet in data}

    scoreM2D1 = sum([1 if m2d1[tweet.id] * tweet.polarity >=
                     0 else 0 for tweet in data]) / len(data)
    scoreM2D2 = sum([1 if m2d2[tweet.id] * tweet.polarity >=
                     0 else 0 for tweet in data]) / len(data)
    print("Metodo #2")
    print(scoreM2D1)
    print(scoreM2D2)

    m3d1 = {tweet.id: analizarTweet3(tweet, d1) for tweet in data}
    m3d2 = {tweet.id: analizarTweet3(tweet, d2) for tweet in data}

    scoreM3D1 = sum([1 if m3d1[tweet.id] * tweet.polarity >=
                     0 else 0 for tweet in data]) / len(data)
    scoreM3D2 = sum([1 if m3d2[tweet.id] * tweet.polarity >=
                     0 else 0 for tweet in data]) / len(data)
    print("Metodo #3")
    print(scoreM3D1)
    print(scoreM3D2)
