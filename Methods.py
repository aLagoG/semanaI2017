#!/usr/bin/env python

from Tweets import *
from Emoji import *
from unidecode import unidecode
import string


def read_file(filename):
    with open(filename) as f:
        data = json.load(f)
    return data


def methodMax(tweet, dictionary):
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


def methodAll(tweet, dictionary):
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


def methodComplement(tweet, dictionary):
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


def analizeTweet(tweet):
    # todo elegir metodo correcto y diccionario correcto
    text_polarity = methodComplement(
        tweet, read_file("replaced_dictionary.json"))
    emoji_info = analizeEmoji(tweet.emoji)
    emoji_info['polaridad'] = text_polarity
    return emoji_info


stopwords = set(["de", "la", "que", "el", "en", "y", "a", "los", "del", "se", "las", "por", "un", "para", "con", "una", "su", "al", "lo", "como", "mas", "pero", "sus", "le", "ya", "o", "este", "si", "porque", "esta", "entre", "cuando", "muy", "sin", "sobre", "tambien", "me", "hasta", "hay", "donde", "quien", "desde", "todo", "nos", "durante", "todos", "uno", "les", "ni", "contra", "otros", "ese", "eso", "ante", "ellos", "e", "esto", "mi", "antes", "algunos", "que", "unos", "yo", "otro", "otras", "otra", "el", "tanto", "esa", "estos", "mucho", "quienes", "nada", "muchos", "cual", "poco", "ella", "estar", "estas", "algunas", "algo", "nosotros", "mi", "mis", "tu", "te", "ti", "tu", "tus", "ellas", "nosotras", "vosostros", "vosostras", "os", "mio", "mia", "mios", "mias", "tuyo", "tuya", "tuyos", "tuyas", "suyo", "suya", "suyos", "suyas", "nuestro", "nuestra", "nuestros", "nuestras", "vuestro", "vuestra", "vuestros", "vuestras", "esos", "esas", "estoy", "estas", "esta", "estamos", "estais", "estan", "este", "estes", "estemos", "esteis", "esten", "estare", "estaras", "estara", "estaremos", "estareis", "estaran", "estaria", "estarias", "estariamos", "estariais", "estarian", "estaba", "estabas", "estabamos", "estabais", "estaban", "estuve", "estuviste", "estuvo", "estuvimos", "estuvisteis", "estuvieron", "estuviera", "estuvieras", "estuvieramos",
                 "estuvierais", "estuvieran", "estuviese", "estuvieses", "estuviesemos", "estuvieseis", "estuviesen", "estando", "estado", "estada", "estados", "estadas", "estad", "he", "has", "ha", "hemos", "habeis", "han", "haya", "hayas", "hayamos", "hayais", "hayan", "habre", "habras", "habra", "habremos", "habreis", "habran", "habria", "habrias", "habriamos", "habriais", "habrian", "habia", "habias", "habiamos", "habiais", "habian", "hube", "hubiste", "hubo", "hubimos", "hubisteis", "hubieron", "hubiera", "hubieras", "hubieramos", "hubierais", "hubieran", "hubiese", "hubieses", "hubiesemos", "hubieseis", "hubiesen", "habiendo", "habido", "habida", "habidos", "habidas", "soy", "eres", "es", "somos", "sois", "son", "sea", "seas", "seamos", "seais", "sean", "sere", "seras", "sera", "seremos", "sereis", "seran", "seria", "serias", "seriamos", "seriais", "serian", "era", "eras", "eramos", "erais", "eran", "fui", "fuiste", "fue", "fuimos", "fuisteis", "fueron", "fuera", "fueras", "fueramos", "fuerais", "fueran", "fuese", "fueses", "fuesemos", "fueseis", "fuesen", "sintiendo", "sentido", "sentida", "sentidos", "sentidas", "siente", "sentid", "tengo", "tienes", "tiene", "tenemos", "teneis", "tienen", "tenga", "tengas", "tengamos", "tengais", "tengan", "tendre", "tendras", "tendra", "tendremos", "tendreis", "tendran", "tendria", "tendrias"])
emojiRegex = re.compile("(" + "|".join(emojis) + ")")
whitespaceRegex = re.compile("\s+", re.MULTILINE)
urlRegex = re.compile("\s*http\S*", re.MULTILINE)
mentionsRegex = re.compile("((\s+|\W)@\S*|^@\S*)", re.MULTILINE)
punctuationRegex = re.compile("[{}]".format(string.punctuation + ','))


def cleanTweet(tweet):
    tweet.emoji = emojiRegex.findall(tweet.text)
    tweet.text_clean = whitespaceRegex.sub(
        ' ', unidecode(tweet.text)).lower()
    tweet.text_clean = urlRegex.sub('', tweet.text_clean)
    tweet.text_clean = mentionsRegex.sub('', tweet.text_clean)
    tweet.text_clean = punctuationRegex.sub('', tweet.text_clean)
    tweet.text_clean = " ".join(
        [w for w in tweet.text_clean.split(" ") if w not in stopwords]).strip()


if __name__ == '__main__':

    data = read_json_file('650_completos.json')

    dictionaries = [
        read_file("combined_dictionary.json"), read_file("replaced_dictionary.json"), read_file(
            "average_dictionary.json"), read_file("our_dictionary.json"), read_file("nltk_dictionary.json")]
    dictionary_names = ["Combined", "Replaced", "Average", "Ours", "Spain"]

    methods = [methodMax, methodAll, methodComplement]
    method_names = ["Max", "All", "Complement"]

    for m_idx, method in enumerate(methods):
        print("\nMethod: " + method_names[m_idx])
        for d_idx, dictionary in enumerate(dictionaries):
            count_correct = 0
            for tweet in data:
                if correct(tweet.polarity, method(tweet, dictionary)):
                    count_correct += 1
            print("Dictionary: " +
                  dictionary_names[d_idx] + "\tScore: " + str(count_correct / len(data)))
    print("\nMethod: Emoji")
    count = 0
    count_correct = 0
    for tweet in data:
        if len(tweet.emoji) > 0:
            count += 1
            value = analizeEmoji(tweet.emoji)['polaridad']
            if correct(value, tweet.polarity):
                count_correct += 1
    print("Score: " + str(count_correct / count))