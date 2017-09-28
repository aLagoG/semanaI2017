#!/usr/bin/env python

import json


class Tweet:

    emoji = []
    text = ""
    creation_date = None
    id = -1
    user = ""

    def __init__(self, data):
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

    def to_dict(self):
        return {'id': self.id, 'created_at': self.creation_date, 'user': self.user, 'text': self.text, 'emoji': self.emoji}


def read_json_file(filename):
    with open(filename, 'r') as file:
        data = json.load(file)['tweets']
    return [Tweet(obj) for obj in data]


def write_json_file(filename, data):
    with open(filename, 'w') as file:
        data = [x.to_dict() for x in data]
        file.write(json.dumps({'tweets': data}))
