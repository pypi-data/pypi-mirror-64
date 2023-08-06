# Copyright © 2019 Noel Kaczmarek
import json
import os


def load(file):
    try:
        if os.path.isfile(file):
            with open(file) as f:
                return json.load(f)
        raise Exception('File not found')
    except Exception as e:
        print('Error while loading config: ', e)
        exit()


def save(file, config):
    try:
        with open(file, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print('Error while saving config to \'%s\': %s' % (file, e))
