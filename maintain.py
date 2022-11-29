#!/usr/bin/env python3
import csv
import os.path
import re
import sqlite3
import sys
import pyinputplus as pyip

RELEASE = 'v0.3'
TITLE = f'*** SvenskaJa {RELEASE} *** (https://github.com/ilya112358/SvenskaJa)'
WORDBASE = 'wordbase.db'
TEXTBASE = 'wordbase.txt'

def infinitives():
    """Fancy print infs"""
    if not infs:
        return
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
    """Ask for an infinitive, print, return with found boolean"""
    inf = pyip.inputStr('\nInfinitive? ').casefold()
    if inf in infs:
        entry = True
        print(inf, verbs[inf])
    else:
        entry = False
        print(f'"{inf}" is not in the word base')
    return inf, entry

def delete():
    """Delete a verb from the list"""
    inf, entry = lookup()
    if not entry:
        return
    if pyip.inputYesNo('Delete this entry? ') == 'no':
        return
    query = "DELETE FROM VerbForms WHERE Infinitive = ?"
    cur.execute(query, (inf,))
    query = "DELETE FROM VerbTranslations WHERE Verb = ?"
    cur.execute(query, (inf,))
    conn.commit()
    print(f'"{inf}" deleted from the word base')

def export_csv():
    """Export word base to csv file"""
    if os.path.isfile(TEXTBASE):
        if pyip.inputYesNo(f'Rewrite existing {TEXTBASE}? ') == 'no':
            return
    lines = []
    for inf in infs:
        lines.append([inf] + list(verbs[inf]))
    with open(TEXTBASE, 'w', newline='', encoding='utf-8') as csvfile:
        csv.writer(csvfile).writerows(lines)
    print('Word base exported')

def import_csv():
    """Import verbs from csv file. Return False if failed."""
    if not os.path.isfile(TEXTBASE):
        print(f'{TEXTBASE} does not exist')
        return False
    lines = []
    with open(TEXTBASE, newline='', encoding='utf-8') as csvfile:
        for row in csv.reader(csvfile):
            lines.append(row)
    print(f'Adding with replacement {len(lines)} entries from {TEXTBASE}')
    if pyip.inputYesNo('Proceed? ') == 'no':
        return False
    n_added, n_changed = 0, 0
    in_forms, in_trans = [], []
    for line in lines:
        if len(line) != 6 or not line[0] or not any(line[1:]):
            print(f'Incorrect format in {line}')
            continue
        verb = []
        for i in range(4):
            word = line[i].strip().casefold()
            if not re.search('[^a-zöäå ]', word):
                verb.append(word)
        if len(verb) < 4 or (any(verb[1:4]) and not all(verb[1:4])):
            print(f'Incorrect or empty verb form in {line}')
            continue
        verb.append(line[4].strip())
        verb.append(line[5].strip())
        assert len(verb) == 6 and verb[0]
        def ins_rep():
            if all(verb[1:4]):
                in_forms.append(tuple(verb[:4]))
            if any(verb[4:6]):
                in_trans.append((verb[0], verb[4], verb[5]))

        if verb[0] not in infs:
            ins_rep()
            print(f'new: {verb}')
            n_added += 1
        else:
            if tuple(verb[1:]) != verbs[verb[0]]:
                ins_rep()
                print(f'changed: {verb}')
                n_changed += 1
    query = "INSERT OR REPLACE INTO VerbForms VALUES (?, ?, ?, ?)"
    cur.executemany(query, in_forms)
    query = "INSERT OR REPLACE INTO VerbTranslations VALUES (?, ?, ?)"
    cur.executemany(query, in_trans)
    conn.commit()
    print(f'{n_added} verbs added, {n_changed} verbs changed')
    return True

def end():
    """Cleanup and exit"""
    conn.close()
    print('Goodbye!')
    sys.exit(0)

def makebase():
    """Create the word base"""
    query = """
        CREATE TABLE VerbForms (
            Infinitive TEXT NOT NULL PRIMARY KEY,
            Present TEXT NOT NULL,
            Past TEXT NOT NULL,
            Supine TEXT NOT NULL
        );
        CREATE TABLE VerbFormsPractice (
            Verb TEXT NOT NULL PRIMARY KEY,
            Priority INTEGER NOT NULL,
            FOREIGN KEY (Verb)
            REFERENCES VerbForms (Infinitive)
                ON DELETE CASCADE
        );
        CREATE TRIGGER VerbFormsAdd
            AFTER INSERT ON VerbForms
        BEGIN
            INSERT INTO VerbFormsPractice VALUES (NEW.Infinitive, 0);
        END;
        CREATE TABLE VerbTranslations (
            Verb TEXT NOT NULL PRIMARY KEY,
            Russian TEXT NOT NULL,
            English TEXT NOT NULL
        );
        """
    cur.executescript(query)
    conn.commit()
    
def loadbase():
    """Load the word base. Return {inf: (verb forms, trans),...}."""
    verbs = {}
    # emulate FULL OUTER JOIN
    query = """
        SELECT Infinitive, Present, Past, Supine, Russian, English
        FROM VerbForms LEFT JOIN VerbTranslations
        ON VerbTranslations.Verb = VerbForms.Infinitive
        UNION ALL
        SELECT Verb, Present, Past, Supine, Russian, English
        FROM VerbTranslations LEFT JOIN VerbForms
        ON VerbForms.Infinitive = VerbTranslations.Verb
        WHERE Present IS NULL
        ORDER BY Infinitive
        """
    for row in cur.execute(query):
        verbs[row[0]] = row[1:]
    return verbs

if __name__ == "__main__":
    print(TITLE)
    create = not os.path.isfile(WORDBASE)
    conn = sqlite3.connect(WORDBASE)
    conn.execute("PRAGMA foreign_keys = ON")
    cur = conn.cursor()
    if create:
        print('\nNo word base found. Creating...')
        makebase()
    tasks = (import_csv, export_csv, infinitives, lookup, delete, end)
    while True:
        verbs = loadbase()
        infs = list(verbs)
        if not verbs:
            print('\nThe word base is empty. Importing...\n')
            if not import_csv():
                print('Import failed, exiting...')
                end()
        else:
            print(f'\n{len(verbs)} verbs loaded from the word base\n')
            inp = pyip.inputInt('Choose a number to:'
                                f'\n[1] import from {TEXTBASE},'
                                f'\n[2] export to {TEXTBASE},'
                                '\n[3] list all,'
                                '\n[4] look up,'
                                '\n[5] delete,'
                                '\n[6] exit\n',
                                min=1, max=6)
            tasks[inp-1]()
        input('\nPress Enter to continue')
