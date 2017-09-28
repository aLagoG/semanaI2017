#!/usr/bin/env python

import json


class Tweet:

    emoji = []
    text = ""
    creation_date = None
    id = -1
    user = None

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
            self.user = User(data['user'])


class User:
    username = ''
    id = -1

    def __init__(self, data):
        if 'id' in data:
            self.id = data['id']
        if 'user_name' in data:
            self.username = data['user_name']


def read_json_file(filename):
    with open(filename, 'r') as file:
        data = json.load(file)['tweets']
    return [Tweet(obj) for obj in data]


def write_json_file(filename, data):
    with open(filename, 'w') as file:
        file.write(json.dumps({'tweets': data}
                              if isinstance(data, list) else data))
