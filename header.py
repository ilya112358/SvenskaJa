import json
import signal
import sys

def initiate():
    """Set Ctrl-C handler"""
    def ctrlc_handler(signal, frame):
        print('\nCtrl-C pressed, exiting...')
        sys.exit(0)

    signal.signal(signal.SIGINT, ctrlc_handler)
    print('*** SvenskaJa ***')
    print('(press Ctrl-C to exit at any time)')

def infinitives(verbs):
    """Fill infs. Print infs. Return infs."""
    if not verbs:   # word base empty
        return []
    infs = [verb[0] for verb in verbs]
    list_verbs = '\nList of verbs in the word base:\n'
    width = len(max(infs, key=len)) + 3 # 3 spaces wider than the longest
    line = '\n'
    for inf in infs:
        line += f'{inf:{width}}'
        if len(line) > (80-width):  # rows are 80 chars max
            list_verbs += line
            line = '\n'
    if len(line) > 1:   # add tailing row
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
