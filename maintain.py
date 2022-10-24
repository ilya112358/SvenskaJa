#!/usr/bin/env python3
import os.path
import re
import sqlite3
import sys
import pyinputplus as pyip

def infinitives():
    """Pretty print infs"""
    if not infs:
        return []
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
    print(list_verbs)

def lookup():
    """Ask for an infinitive, look it up, print, return with found boolean."""
    inf = pyip.inputStr('\nInfinitiv? ').casefold()
    if inf in infs:
        entry = True
        print(inf, verbs[inf])
    else:
        entry = False
        print(f'[{inf}] is not in the wordbase')
    return inf, entry

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

def add_el():
    """Add a verb to the list"""
    inf, entry = lookup()
    if entry:
        if pyip.inputYesNo('Do you want to replace this entry? ') == 'no':
            return
    pres = pyip.inputStr('Presens? ').casefold()
    past = pyip.inputStr('Preteritum? ').casefold()
    supin = pyip.inputStr('Supinum? ').casefold()
    verb = (inf, pres, past, supin)
    print(verb)
    if pyip.inputYesNo('Add this entry? ') == 'no':
        return
    query = "INSERT OR REPLACE INTO VerbForms VALUES (?, ?, ?, ?)"
    cur.execute(query, verb)
    conn.commit()
    print(f'[{inf}] added to wordbase')

def export_verbs():
    """Export word base to text file"""
    textbase = 'export.txt'
    lines = []
    for inf in infs:
        lines.append(f"{inf} {' '.join(verbs[inf])}\n")
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
    insert = []
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
            print(f'{verb} new')
            n_added += 1
        else:
            if tuple(verb[1:]) != verbs[verb[0]]:
                insert.append(tuple(verb))
                print(f'{verb} changed')
                n_changed += 1
    query = "INSERT OR REPLACE INTO VerbForms VALUES (?, ?, ?, ?)"
    cur.executemany(query, insert)
    conn.commit()
    print(f'{n_added} verbs added, {n_changed} verbs changed')

def end():
    """Cleanup and exit"""
    conn.close()
    print('Goodbye!')
    sys.exit(0)

def loadbase():
    """Load wordbase from db. Return dictionary of {inf: (verb forms)}."""
    verbs = {}
    query = """
        CREATE TABLE IF NOT EXISTS VerbForms (
            Infinitiv TEXT NOT NULL PRIMARY KEY,
            Presens TEXT NOT NULL UNIQUE,
            Preteritum TEXT NOT NULL UNIQUE,
            Supinum TEXT NOT NULL UNIQUE
        );
        CREATE TABLE IF NOT EXISTS VerbFormsPractice (
            Verb TEXT NOT NULL PRIMARY KEY,
            Priority INTEGER NOT NULL,
            FOREIGN KEY (Verb)
            REFERENCES VerbForms (Infinitiv)
                ON DELETE CASCADE
        );
        CREATE TRIGGER IF NOT EXISTS VerbAddPractice
            AFTER INSERT ON VerbForms
        BEGIN
            INSERT INTO VerbFormsPractice VALUES (NEW.Infinitiv, 0);
        END;
        """
    cur.executescript(query)
    conn.commit()
    query = "SELECT * FROM VerbForms ORDER BY Infinitiv"
    for row in cur.execute(query):
        verbs[row[0]] = row[1:]
    return verbs

if __name__ == "__main__":
    print('*** SvenskaJa ***')
    conn = sqlite3.connect('wordbase.db')
    conn.execute("PRAGMA foreign_keys = ON")
    cur = conn.cursor()
    tasks = (infinitives, lookup, del_el, add_el, export_verbs, import_verbs,
             end)
    while True:
        verbs = loadbase()
        infs = list(verbs)
        if not verbs:
            print('\nThe word base is empty. '
                  'Add a verb or import from a text file!\n')
        print(f'\n{len(verbs)} verbs loaded from the word base\n')
        inp = pyip.inputNum('Choose a number to:'
                            '\n[1] list all,'
                            '\n[2] look up,'
                            '\n[3] delete,'
                            '\n[4] add new,'
                            '\n[5] export to text file,'
                            '\n[6] import from text file,'
                            '\n[7] exit\n',
                            min=1, max=7)
        tasks[inp-1]()
        input('\nPress Enter to continue')
