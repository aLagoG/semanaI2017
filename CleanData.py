#!/usr/bin/env python
import re
from unidecode import unidecode
import json
import string
import sys


filename = 'results.json'

if len(sys.argv) > 1:
    filename = sys.argv[1].strip()

with open(filename) as f:
    data = json.load(f)
tweets = data['tweets']
emojis = ["😀", "😃", "😄", "😁", "😆", "😅", "😂", "🤣", "☺", "😊", "😇", "🙂", "🙃", "😉", "😌", "😍", "😘", "😗", "😙", "😖", "😫", "😩", "😤", "😠", "😡", "😶", "😐", "😑", "😯", "😦", "😧", "😮", "😲", "😵", "😳", "😱", "😨", "😰", "😢", "😥", "🤤", "😭", "😓", "😪", "😴", "🙄", "🤔", "🤥", "😬", "🤐", "🤢", "🤧", "😷", "🤒", "🤕", "😈", "👿", "😺", "😸", "😹", "👌", "👈", "👉",
          "👆", "👇", "☝", "✋", "🤚", "🖐", "🖖", "👋", "🤙", "💪", "🖕", "👀", "🤦‍♀", "🤷‍♂", "🤦‍♂", "🤷‍♀", "🙅", "❤", "💔", "🔥", "😹", "😻", "😼", "😽", "🙀", "😿", "😾", "🙌", "👏", "🙏", "👍", "👎", "👊", "✊", "✌", "🤘", "👈", "👉", "👌", "😸", "🤝", "🤛", "🤜", "😚", "😋", "😜", "😝", "😛", "🤑", "🤗", "🤓", "😎", "🤡", "🤠", "😏", "😒", "😞", "😔", "😟", "😕", "🙁", "☹", "😣"]
stopwords = set(["de", "la", "que", "el", "en", "y", "a", "los", "del", "se", "las", "por", "un", "para", "con", "una", "su", "al", "lo", "como", "mas", "pero", "sus", "le", "ya", "o", "este", "si", "porque", "esta", "entre", "cuando", "muy", "sin", "sobre", "tambien", "me", "hasta", "hay", "donde", "quien", "desde", "todo", "nos", "durante", "todos", "uno", "les", "ni", "contra", "otros", "ese", "eso", "ante", "ellos", "e", "esto", "mi", "antes", "algunos", "que", "unos", "yo", "otro", "otras", "otra", "el", "tanto", "esa", "estos", "mucho", "quienes", "nada", "muchos", "cual", "poco", "ella", "estar", "estas", "algunas", "algo", "nosotros", "mi", "mis", "tu", "te", "ti", "tu", "tus", "ellas", "nosotras", "vosostros", "vosostras", "os", "mio", "mia", "mios", "mias", "tuyo", "tuya", "tuyos", "tuyas", "suyo", "suya", "suyos", "suyas", "nuestro", "nuestra", "nuestros", "nuestras", "vuestro", "vuestra", "vuestros", "vuestras", "esos", "esas", "estoy", "estas", "esta", "estamos", "estais", "estan", "este", "estes", "estemos", "esteis", "esten", "estare", "estaras", "estara", "estaremos", "estareis", "estaran", "estaria", "estarias", "estariamos", "estariais", "estarian", "estaba", "estabas", "estabamos", "estabais", "estaban", "estuve", "estuviste", "estuvo", "estuvimos", "estuvisteis", "estuvieron", "estuviera", "estuvieras", "estuvieramos",
                 "estuvierais", "estuvieran", "estuviese", "estuvieses", "estuviesemos", "estuvieseis", "estuviesen", "estando", "estado", "estada", "estados", "estadas", "estad", "he", "has", "ha", "hemos", "habeis", "han", "haya", "hayas", "hayamos", "hayais", "hayan", "habre", "habras", "habra", "habremos", "habreis", "habran", "habria", "habrias", "habriamos", "habriais", "habrian", "habia", "habias", "habiamos", "habiais", "habian", "hube", "hubiste", "hubo", "hubimos", "hubisteis", "hubieron", "hubiera", "hubieras", "hubieramos", "hubierais", "hubieran", "hubiese", "hubieses", "hubiesemos", "hubieseis", "hubiesen", "habiendo", "habido", "habida", "habidos", "habidas", "soy", "eres", "es", "somos", "sois", "son", "sea", "seas", "seamos", "seais", "sean", "sere", "seras", "sera", "seremos", "sereis", "seran", "seria", "serias", "seriamos", "seriais", "serian", "era", "eras", "eramos", "erais", "eran", "fui", "fuiste", "fue", "fuimos", "fuisteis", "fueron", "fuera", "fueras", "fueramos", "fuerais", "fueran", "fuese", "fueses", "fuesemos", "fueseis", "fuesen", "sintiendo", "sentido", "sentida", "sentidos", "sentidas", "siente", "sentid", "tengo", "tienes", "tiene", "tenemos", "teneis", "tienen", "tenga", "tengas", "tengamos", "tengais", "tengan", "tendre", "tendras", "tendra", "tendremos", "tendreis", "tendran", "tendria", "tendrias"])
emojiRegex = re.compile("(" + "|".join(emojis) + ")")
whitespaceRegex = re.compile("\s+", re.MULTILINE)
urlRegex = re.compile("\s*http\S*", re.MULTILINE)
mentionsRegex = re.compile("((\s+|\W)@\S*|^@\S*)", re.MULTILINE)
punctuationRegex = re.compile("[{}]".format(string.punctuation + ','))
for tweet in tweets:
    tweet['emoji'] = emojiRegex.findall(tweet['text'])
    tweet['text'] = whitespaceRegex.sub(' ', unidecode(tweet['text'])).lower()
    tweet['text'] = urlRegex.sub('', tweet['text'])
    tweet['text'] = mentionsRegex.sub('', tweet['text'])
    tweet['text'] = punctuationRegex.sub('', tweet['text'])
    tweet['text'] = " ".join(
        [w for w in tweet['text'].split(" ") if w not in stopwords]).strip()

with open(filename.replace('.json', '_clean.json'), 'w') as f:
    f.write(json.dumps({"tweets": tweets}))
