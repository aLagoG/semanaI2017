#!/usr/bin/env python

import re

emociones = ['alegria', 'amor', 'sorpresa', 'neutral',
             'verguenza', 'aversion', 'miedo', 'tristeza', 'colera']
polaridad = [1, 1, 1 / 3, 0, -1 / 3, -1 / 3, -2 / 3, -1, -1]

emoji_map = {}


def generateMap():
    """
        Lee el archivo de la lista de emojis y genera un mapa con sus valores emocionales
    """
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
        values['polaridad'] = sum(
            [values[emociones[i]] * polaridad[i] for i in range(len(emociones))])
        if values['polaridad'] > 1:
            values['polaridad'] = 1
        elif values['polaridad'] < -1:
            values['polaridad'] = -1
        emoji_map[emoji] = values


generateMap()
emojis = ["😀", "😃", "😄", "😁", "😆", "😅", "😂", "🤣", "☺", "😊", "😇", "🙂", "🙃", "😉", "😌", "😍", "😘", "😗", "😙", "😖", "😫", "😩", "😤", "😠", "😡", "😶", "😐", "😑", "😯", "😦", "😧", "😮", "😲", "😵", "😳", "😱", "😨", "😰", "😢", "😥", "🤤", "😭", "😓", "😪", "😴", "🙄", "🤔", "🤥", "😬", "🤐", "🤢", "🤧", "😷", "🤒", "🤕", "😈", "👿", "😺", "😸", "😹", "👌", "👈", "👉",
          "👆", "👇", "☝", "✋", "🤚", "🖐", "🖖", "👋", "🤙", "💪", "🖕", "👀", "🤦‍♀", "🤷‍♂", "🤦‍♂", "🤷‍♀", "🙅", "❤", "💔", "🔥", "😹", "😻", "😼", "😽", "🙀", "😿", "😾", "🙌", "👏", "🙏", "👍", "👎", "👊", "✊", "✌", "🤘", "👈", "👉", "👌", "😸", "🤝", "🤛", "🤜", "😚", "😋", "😜", "😝", "😛", "🤑", "🤗", "🤓", "😎", "🤡", "🤠", "😏", "😒", "😞", "😔", "😟", "😕", "🙁", "☹", "😣"]


def analizeEmoji(input_list):
    """
        Toma una lista de emojis y regresa el analisis de sus valores emocionales
    """
    values = {x: 0.0 for x in emociones}
    values['polaridad'] = 0.0
    if len(input_list) == 0:
        return values
    for emoji in input_list:
        # print(emoji + ": " + str(emoji_map[emoji]))
        for key in emoji_map[emoji]:
            values[key] += emoji_map[emoji][key]
    values = {x: values[x] / len(input_list) for x in values}
    # print("completo: " + str(values))
    return values


if __name__ == "__main__":
    # si se llama desde linea de comandos permite analizar los emojis de un texto
    if len(ARGV) > 1:
        analize_string(ARGV[1])
    else:
        while 1:
            line = input(
                "Escribe el string que quieras analizar (q para salir): ").strip()
            if line == 'q':
                break
            analize_string(line)
