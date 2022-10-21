#!/usr/bin/env python3
import random
import re
import sqlite3
import sys
import pyinputplus as pyip

import header

def lookup():
    """Ask for an infinitive, look it up, print, return with found entry."""
    inf = pyip.inputStr('\nInfinitiv? ').casefold()
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
    cur.execute(query, tuple(verb))
    practice = (inf, 0)
    query = "INSERT INTO VerbFormsPractice VALUES (?, ?)"
    cur.execute(query, practice)
    conn.commit()
    print(f'[{inf}] added to wordbase')

def del_el():
    """Delete a verb from the list"""
    inf, entry = lookup()
    if not entry:
        return
    if pyip.inputYesNo('Delete this entry? ') == 'no':
        return
    query = "DELETE FROM VerbForms WHERE Infinitiv = ?"
    cur.execute(query, (inf,))
    conn.commit()
    print(f'[{inf}] deleted from wordbase')

def export():
    """Export word base to text file"""
    textbase = 'export.txt'
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
    textbase = 'import.txt'
    if not os.path.isfile(textbase):
        print(f'{textbase} does not exist')
        return
    with open(textbase, encoding='utf-8') as f:
        lines = f.readlines()
    print(f'Adding with replacement {len(lines)} entries from {textbase}')
    if pyip.inputYesNo('Proceed? ') == 'no':
        return
    n_added, n_changed = 0, 0
    insert, practice = [], []
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
        if verb[0] not in infs:
            insert.append(tuple(verb))
            practice.append((verb[0], 0))
            print(f'{verb} new')
            n_added += 1
        else:
            if verb != verbs[infs.index(verb[0])]:
                insert.append(tuple(verb))
                practice.append((verb[0], 0))
                print(f'{verb} changed')
                n_changed += 1
    query = "INSERT OR REPLACE INTO VerbForms VALUES (?, ?, ?, ?)"
    cur.executemany(query, insert)
    query = "INSERT INTO VerbFormsPractice VALUES (?, ?)"
    cur.executemany(query, practice)
    conn.commit()
    print(f'{n_added} verbs added, {n_changed} verbs changed')

def loadbase():
    """Load wordbase from db. Return list of lists of verb forms."""
    verbs = []
    query = """
        CREATE TABLE IF NOT EXISTS VerbForms (
            Infinitiv TEXT NOT NULL PRIMARY KEY,
            Presens TEXT NOT NULL UNIQUE,
            Preteritum TEXT NOT NULL UNIQUE,
            Supinum TEXT NOT NULL UNIQUE
        )"""
    cur.execute(query)
    query = """
        CREATE TABLE IF NOT EXISTS VerbFormsPractice (
            Verb TEXT NOT NULL PRIMARY KEY,
            Priority INTEGER NOT NULL,
            FOREIGN KEY (Verb)
            REFERENCES VerbForms (Infinitiv)
                ON DELETE CASCADE
        )"""
    cur.execute(query)
    conn.commit()
    query = "SELECT * FROM VerbForms ORDER BY Infinitiv"
    for row in cur.execute(query):
        verbs.append(list(row))
    return verbs

def end():
    """Cleanup and exit"""
    conn.close()
    print('Goodbye!')
    sys.exit(0)

if __name__ == "__main__":
    print('*** SvenskaJa ***')
    conn = sqlite3.connect('wordbase.db')
    conn.execute("PRAGMA foreign_keys = ON")
    cur = conn.cursor()
    tasks = (lookup, del_el, add_el, export, import_verbs, end)
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
                            '\n[4] export base to text file,'
                            '\n[5] import verbs from text file,'
                            '\n[6] to exit\n',
                            min=1, max=7)
        tasks[inp-1]()
        input('Press Enter to continue')
