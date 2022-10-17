#!/usr/bin/env python3
import os.path
import random
import re
import pyinputplus as pyip

import header
load, dump = header.load, header.dump

def input_verb(inf):
    """Input verb forms"""
    pres = pyip.inputStr('Presens? ').casefold()
    past = pyip.inputStr('Preteritum? ').casefold()
    supin = pyip.inputStr('Supinum? ').casefold()
    trans = pyip.inputStr('Translation? ').casefold()
    verb = [inf, pres, past, supin, trans]
    print(verb)
    return verb

def lookup():
    """Look up a verb from the list"""
    inf = pyip.inputStr('\nInfinitive? ').casefold()
    try:
        x = infs.index(inf)
    except ValueError:
        print('Not in the list!')
        return
    print(verbs[x])

def add_el():
    """Add a verb to the list"""
    inf = pyip.inputStr('\nInfinitive to add? ')
    if inf in infs:
        print('Already exists!')
        return
    verb = input_verb(inf)
    if pyip.inputYesNo('Add this entry? ') == 'no':
        return
    verbs.append(verb)
    rep = load(repbase)
    rep.insert(0, inf)
    dump(repbase, rep)
    dump(wordbase, verbs)
    print(f'[{inf}] added to wordbase and repbase')

def del_el():
    """Delete a verb from the list"""
    inf = pyip.inputStr('\nInfinitive to delete? ').casefold()
    try:
        x = infs.index(inf)
    except ValueError:
        print('Not in the list!')
        return
    print(verbs[x])
    if pyip.inputYesNo('Delete this entry? ') == 'no':
        return
    verbs.pop(x)
    rep = load(repbase)
    rep.remove(inf)
    dump(repbase, rep)
    dump(wordbase, verbs)
    print(f'[{inf}] deleted from wordbase and repbase')

def sortbase():
    """Sort wordbase by infinitives and save"""
    verbs.sort(key=lambda verb: verb[0])
    dump(wordbase, verbs)
    print('Word base sorted')

def makerep():
    """(Re)Create repetition base"""
    rep = [verb[0] for verb in verbs]
    random.shuffle(rep)
    print(f'\n{len(rep)} verbs prepared')
    if os.path.isfile(repbase):
        if pyip.inputYesNo(f'Rewrite existing {repbase}? ') == 'no':
            return
    dump(repbase, rep)
    print('Repetition base saved')

def export():
    """Export word base to text file"""
    lines = []
    for verb in verbs:
        lines.append(f"{' '.join(verb)}\n")
    if os.path.isfile(textbase):
        if pyip.inputYesNo(f'Rewrite existing {textbase}? ') == 'no':
            return
    with open(textbase, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print('Word base exported')

def import_verbs():
    """Import verbs from text file"""
    print(f'Adding with replacement from {textbase}')
    if pyip.inputYesNo('Proceed? ') == 'no':
        return
    with open(textbase, encoding='utf-8') as f:
        lines = f.readlines()
    rep = load(repbase)
    n_added, n_changed = 0, 0
    for line in lines:
        new_el = line.split()
        if len(new_el) < 4:
            print(f'Too few forms in: [{line.rstrip()}]')
            continue
        verb = []
        for i in range(4):
            word = new_el[i].lower()
            if not re.search('[^a-zöäå]', word):
                verb.append(word)
            else:
                print(f'Incorrect word: [{word}] in [{line.rstrip()}]')
                break
        if len(verb) < 4:
            continue
        verb.append(' '.join(new_el[4:]))    # multiword translation
        if verb[0] not in infs:
            verbs.append(verb)
            rep.insert(0, verb[0])  # into the next practice
            print(f'{verb} added')
            n_added += 1
        else:
            x = infs.index(verb[0])
            if verb != verbs[x]:
                verbs[x] = verb
                print(f'{verb} changed')
                n_changed += 1
    dump(repbase, rep)
    dump(wordbase, verbs)
    print(f'{n_added} verbs added, {n_changed} verbs changed')

if __name__ == "__main__":
    header.initiate()
    wordbase = 'wordbase.json'
    repbase = 'repbase.json'
    backbase = 'wordbase.bak'
    textbase = 'wordbase.txt'
    try:
        verbs = load(wordbase)
        dump(backbase, verbs)
    except FileNotFoundError:
        print('\nNo word base found! Add a verb or import from a text file!\n')
        verbs = []
    tasks = (lookup, del_el, add_el, sortbase, makerep, export, import_verbs)
    while True:
        infs = header.infinitives(verbs)
        inp = pyip.inputNum('Choose a number to:'
                            '\n[0] look up,'
                            '\n[1] delete,'
                            '\n[2] add new,'
                            '\n[3] sort,'
                            '\n[4] create repetition base,'
                            '\n[5] export base to text file,'
                            '\n[6] import verbs from text file,'
                            '\n[Ctrl-C] to exit\n',
                            min=0, max=6)
        tasks[inp]()
        input('Press Enter to return')
