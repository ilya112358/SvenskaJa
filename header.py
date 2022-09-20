import configparser
import json
import signal
import sys

def initiate():
    """Set Ctrl-C handler. Read and return config."""
    def ctrlc_handler(signal, frame):
        print('\nCtrl-C pressed, exiting...')
        sys.exit(0)

    signal.signal(signal.SIGINT, ctrlc_handler)
    print('*** SvenskaJa ***')
    print('(press Ctrl-C to exit at any time)')
    config = configparser.ConfigParser()
    with open('config.ini') as f:
        config.read_file(f)
    return config

def infinitives(verbs):
    infs = [verb[0] for verb in verbs]
    list_verbs = '\nList of verbs in the word base:\n'
    cols = 6    # number of columns 
    if len(infs) < cols:   # no full lines
        l = -1
    else:
        for l in range(len(infs)//cols):
            line = '\n'
            for k in range(cols):  # full lines
                line += f'{infs[l*cols+k]:12}'
            list_verbs += line
    line = '\n'
    for k in range(len(infs)%cols):    # last (tail) line
        line += f'{infs[(l+1)*cols+k]:12}'
    list_verbs += line
    list_verbs += f'\n\n{len(verbs)} verbs loaded from the word base\n'
    print(list_verbs)
    return infs

def load(file):
    with open(file, encoding='utf-8') as f:
        return json.load(f)

def dump(file, obj):
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(obj, f)
