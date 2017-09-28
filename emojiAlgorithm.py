#!/usr/bin/env python
import re

emociones = ['alegria', 'amor', 'sorpresa', 'neutral',
             'verguenza', 'aversion', 'miedo', 'tristeza', 'colera']
positividad = [3, 3, 1, 0, -1, -1, -2, -3, -3]

emoji_map = {}


def generateMap():
    f = open('emojiList.csv', 'r')
    first = True
    reg = re.compile('^\d+$')
    for line in f:
        if first:
            first = False
            continue
        cols = line.split(',')
        emoji = cols[1].strip()
        values = {}
        for idx, val in enumerate(cols[2:]):
            val = val.strip() if reg.match(val) else '0'
            values[emociones[idx]] = float(val) / 100
        values['positividad'] = sum(
            [values[emociones[i]] * positividad[i] for i in range(len(emociones))])
        emoji_map[emoji] = values


generateMap()
emojis = ["😀", "😃", "😄", "😁", "😆", "😅", "😂", "🤣", "☺", "😊", "😇", "🙂", "🙃", "😉", "😌", "😍", "😘", "😗", "😙", "😖", "😫", "😩", "😤", "😠", "😡", "😶", "😐", "😑", "😯", "😦", "😧", "😮", "😲", "😵", "😳", "😱", "😨", "😰", "😢", "😥", "🤤", "😭", "😓", "😪", "😴", "🙄", "🤔", "🤥", "😬", "🤐", "🤢", "🤧", "😷", "🤒", "🤕", "😈", "👿", "😺", "😸", "😹", "👌", "👈", "👉",
          "👆", "👇", "☝", "✋", "🤚", "🖐", "🖖", "👋", "🤙", "💪", "🖕", "👀", "🤦‍♀", "🤷‍♂", "🤦‍♂", "🤷‍♀", "🙅", "❤", "💔", "🔥", "😹", "😻", "😼", "😽", "🙀", "😿", "😾", "🙌", "👏", "🙏", "👍", "👎", "👊", "✊", "✌", "🤘", "👈", "👉", "👌", "😸", "🤝", "🤛", "🤜", "😚", "😋", "😜", "😝", "😛", "🤑", "🤗", "🤓", "😎", "🤡", "🤠", "😏", "😒", "😞", "😔", "😟", "😕", "🙁", "☹", "😣"]

regexString = "(" + "|".join(emojis) + ")"
regex = re.compile(regexString)


def analize_string(steing):
    values = {x: 0.0 for x in emociones}
    values['positividad'] = 0.0
    matches = regex.findall(line)
    for emoji in matches:
        print(emoji + ": " + str(emoji_map[emoji]))
        for key in emoji_map[emoji]:
            values[key] += emoji_map[emoji][key]
    values = {x: values[x] / len(matches) for x in values}
    print("completo: " + str(values))


if __name__ == "__main__":
    if len(ARGV) > 1:
        analize_string(ARGV[1])
    else:
        while 1:
            line = input(
                "Escribe el string que quieras analizar (q para salir): ").strip()
            if line == 'q':
                break
            analize_string(line)
