#!/usr/bin/env python3
import os.path
import random
import re
import sqlite3
import sys
import pyinputplus as pyip

import header
load, dump = header.load, header.dump

def lookup():
    """Ask for an infinitive, look it up, print, return with found entry."""
    inf = pyip.inputStr('\nInfinitive? ').casefold()
    entry = []
    if inf in infs:
        entry = verbs[infs.index(inf)]
        print(entry)
    else:
        print(f'[{inf}] is not in the wordbase')
    return inf, entry

def add_el():
    """Add a verb to the list"""
    inf, entry = lookup()
    if entry:
        if pyip.inputYesNo('Do you want to replace this entry? ') == 'no':
            return
    pres = pyip.inputStr('Presens? ').casefold()
    past = pyip.inputStr('Preteritum? ').casefold()
    supin = pyip.inputStr('Supinum? ').casefold()
    verb = [inf, pres, past, supin]
    print(verb)
    if pyip.inputYesNo('Add this entry? ') == 'no':
        return
    query = "INSERT OR REPLACE INTO VerbForms VALUES (?, ?, ?, ?)"
    cur.execute(query, (verb[0], verb[1], verb[2], verb[3]))
    con.commit()
    print(f'[{inf}] added to wordbase')

def del_el():
    """Delete a verb from the list"""
    inf, entry = lookup()
    if not entry:
        return
    if pyip.inputYesNo('Delete this entry? ') == 'no':
        return
    query = "DELETE FROM VerbForms WHERE Infinitive = ?"
    cur.execute(query, (inf,))
    con.commit()
    print(f'[{inf}] deleted from wordbase')

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

def loadbase():
    """Load wordbase from db. Return list of lists of verb forms."""
    verbs = []
    query = "SELECT * FROM VerbForms ORDER BY Infinitive"
    try:
        for row in cur.execute(query):
            verbs.append(list(row))
    except sqlite3.Error as e:
        if 'no such table' in str(e):
            query = """
                CREATE TABLE VerbForms (
                    Infinitive TEXT NOT NULL PRIMARY KEY,
                    Presens TEXT NOT NULL UNIQUE,
                    Preteritum TEXT NOT NULL UNIQUE,
                    Supinum TEXT NOT NULL UNIQUE
                )"""
            cur.execute(query)
            con.commit()
        else:
            print('\nERROR!', type(e), e)
            end()
    return verbs

def end():
    """Cleanup and exit"""
    con.close()
    print('Goodbye!')
    sys.exit(0)

if __name__ == "__main__":
    print('*** SvenskaJa ***')
    con = sqlite3.connect('wordbase.db')
    cur = con.cursor()
    tasks = (lookup, del_el, add_el, makerep, export, import_verbs, end)
    while True:
        verbs = loadbase()
        if not verbs:
            print('\nWord base is empty. '
                  'Add a verb or import from a text file!\n')
        infs = header.infinitives(verbs)
        inp = pyip.inputNum('Choose a number to:'
                            '\n[1] look up,'
                            '\n[2] delete,'
                            '\n[3] add new,'
                            '\n[4] create repetition base,'
                            '\n[5] export base to text file,'
                            '\n[6] import verbs from text file,'
                            '\n[7] to exit\n',
                            min=1, max=7)
        tasks[inp-1]()
        input('Press Enter to continue')
