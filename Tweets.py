#!/usr/bin/env python

import json


class Tweet:
    """
        Representa un tweet con los valores necesarios para analisis
    """
    emoji = []
    text = ""
    text_clean = ""
    creation_date = None
    id = -1
    user = ""
    polarity = 0

    def __init__(self, data):
        """
            Genera los valores del tweet desde un mapa
        """
        if 'emoji' in data:
            self.emoji = data['emoji']
        if 'text' in data:
            self.text = data['text']
        if 'created_at' in data:
            self.creation_date = data['created_at']
        if 'id' in data:
            self.id = data['id']
        if 'user' in data:
            if isinstance(data['user'], dict):
                if 'user_name' in data['user']:
                    self.user = data['user']['user_name']
            else:
                self.user = data['user']
        if 'text_clean' in data:
            self.text_clean = data['text_clean']
        if 'polarity' in data:
            self.polarity = data['polarity']

    def set_polarity(self, data):
        """
            Convierte la polaridad de texto a numero
        """
        self.polarity = 1 if data == 'p' else -1 if data == 'n' else 0

    def to_dict(self):
        """
            Genera un diccionario de los valores del tweet
        """
        return {'id': self.id, 'created_at': self.creation_date, 'user': self.user, 'text': self.text, 'text_clean': self.text_clean, 'emoji': self.emoji, 'polarity': self.polarity}


def read_json_file(filename):
    """
        Lee un archivo json y regresa una lista de tweets
    """
    with open(filename, 'r') as file:
        data = json.load(file)['tweets']
    return [Tweet(obj) for obj in data]


def write_json_file(filename, data):
    """
        Recibe una lista de tweets y lo guarda en un archivo json
    """
    with open(filename, 'w') as file:
        data = [x.to_dict() for x in data]
        file.write(json.dumps({'tweets': data}))
