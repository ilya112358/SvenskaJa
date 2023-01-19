#!/usr/bin/env python3
import csv
import os.path
import re
import sqlite3
import sys

import pyinputplus as pyip
from tabulate import tabulate
from colorama import just_fix_windows_console, Fore, Back, Style


class c:
    """Color aliases"""

    END = Style.RESET_ALL
    BOLD = Style.BRIGHT
    GREEN = Fore.GREEN
    RED = Fore.RED
    YELLOW = Style.BRIGHT + Fore.YELLOW


RELEASE = 4
WORDBASE = 'wordbase.db'
TEXTBASE = 'wordbase.txt'
IGNORE = 'ignore.txt'
PYTHON_REQ = (3, 8, 10)
TITLE = f'*** {c.BOLD}SvenskaJa v0.{RELEASE}{c.END} *** https://github.com/ilya112358/SvenskaJa'


def choose(string, **kwargs):
    """Color options and call pyip.inputInt"""
    string = string.replace('[', c.YELLOW + '[').replace(']', ']' + c.END)
    return pyip.inputInt(string, **kwargs)


def infinitives():
    """Fancy print infs"""
    if not infs:
        return
    table = [infs[i : i + 5] for i in range(0, len(infs), 5)]
    print(tabulate(table, tablefmt='simple_grid'))


def lookup() -> (str, bool):
    """Ask for an inf, pretty-print wordbase entry, return inf with found status"""
    inf = pyip.inputStr('\nInfinitive? ').casefold()
    if inf in infs:
        entry = True
        prio = [None, None, None]
        query = """
            SELECT Priority
            FROM VerbFormsPractice
            WHERE Verb = ?
            """
        if (data := cur.execute(query, (inf,)).fetchone()) is not None:
            prio[0] = data[0]
        query = """
            SELECT Russian, English
            FROM VerbTranslationsPractice
            WHERE Verb = ?
            """
        if (data := cur.execute(query, (inf,)).fetchone()) is not None:
            prio[1], prio[2] = data
        table = {
            'Infinitive': [
                'Present',
                'Past',
                'Supine',
                'Russian',
                'English',
                'Verb forms practice priority',
                'Russian flashcard priority',
                'English flashcard priority',
            ],
            inf: verbs[inf] + prio,
        }
        print(tabulate(table, headers='keys', tablefmt='simple_grid'))
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
        lines.append([inf] + verbs[inf])
    with open(TEXTBASE, 'w', newline='', encoding='utf-8') as csvfile:
        csv.writer(csvfile).writerows(lines)
    print('Word base exported')


def import_csv() -> bool:
    """Import verbs from csv file. Return success status."""
    ignore = []
    try:
        with open(IGNORE, encoding='utf-8') as f:
            for line in f:
                ignore.append(line.strip().casefold())
        print(
            f'{len(ignore)} entries loaded from {IGNORE} and will be ignored during import'
        )
    except FileNotFoundError:
        print(f'{IGNORE} file not found, all entries will be accepted')
    lines = []
    try:
        with open(TEXTBASE, newline='', encoding='utf-8') as csvfile:
            for row in csv.reader(csvfile):
                lines.append(row)
    except FileNotFoundError:
        print(f'{TEXTBASE} file not found, nothing to import')
        return False
    print(f'Adding with replacement {len(lines)} entries from {TEXTBASE}')
    if pyip.inputYesNo('Proceed? ') == 'no':
        return False

    print()
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

        if verb[0] in ignore:
            print(f'ignored: {verb[0]}')
            continue
        if verb[0] not in infs:
            ins_rep()
            print(f'new: {verb[0]}')
            n_added += 1
        else:
            if verb[1:] != verbs[verb[0]]:
                ins_rep()
                print(f'changed: {verb[0]}')
                n_changed += 1
    query = "INSERT OR REPLACE INTO VerbForms VALUES (?, ?, ?, ?)"
    cur.executemany(query, in_forms)
    query = "INSERT OR REPLACE INTO VerbTranslations VALUES (?, ?, ?)"
    cur.executemany(query, in_trans)
    conn.commit()
    print(f'\n{n_added} verbs added, {n_changed} verbs changed')
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
        CREATE TABLE VerbTranslationsPractice (
            Verb TEXT NOT NULL PRIMARY KEY,
            Russian INTEGER NOT NULL,
            English INTEGER NOT NULL,
            FOREIGN KEY (Verb)
            REFERENCES VerbTranslations (Verb)
                ON DELETE CASCADE
        );
        CREATE TRIGGER VerbTranslationsAdd
            AFTER INSERT ON VerbTranslations
        BEGIN
            INSERT INTO VerbTranslationsPractice VALUES (NEW.Verb, 0, 0);
        END;
        """
    cur.executescript(query)
    cur.execute(f"PRAGMA user_version = {RELEASE}")


def upgradebase(vers):
    """Upgrade the word base: add new tables and populate"""
    print(f'Upgrading the word base from v0.{vers} to v0.{RELEASE}...')
    if vers == 0:
        query = """
            CREATE TABLE VerbTranslationsPractice (
                Verb TEXT NOT NULL PRIMARY KEY,
                Russian INTEGER NOT NULL,
                English INTEGER NOT NULL,
                FOREIGN KEY (Verb)
                REFERENCES VerbTranslations (Verb)
                    ON DELETE CASCADE
            );
            CREATE TRIGGER VerbTranslationsAdd
                AFTER INSERT ON VerbTranslations
            BEGIN
                INSERT INTO VerbTranslationsPractice VALUES (NEW.Verb, 0, 0);
            END;
            """
        cur.executescript(query)
        data = []
        for row in cur.execute("SELECT Verb FROM VerbTranslations"):
            data.append((row[0], 0, 0))
        cur.executemany("INSERT INTO VerbTranslationsPractice VALUES(?, ?, ?)", data)
        conn.commit()
    cur.execute(f"PRAGMA user_version = {RELEASE}")


def loadbase() -> dict:
    """Load the word base. Return {inf: [3 verb forms, 2 translations],...}.
    Replace None with '' for easy compare when importing.
    """
    verbs = {}
    query = """
        SELECT COALESCE (Infinitive, Verb) AS Verb,
        Present, Past, Supine, Russian, English
        FROM VerbForms FULL JOIN VerbTranslations
        ON VerbTranslations.Verb = VerbForms.Infinitive
        ORDER BY Verb
        """
    query_old = """
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
    try:
        rows = cur.execute(query)
    except sqlite3.OperationalError:  # sqlite3 before 3.39
        rows = cur.execute(query_old)
    for row in rows:
        verbs[row[0]] = ['' if not el else el for el in row[1:]]
    return verbs


if __name__ == "__main__":
    just_fix_windows_console()
    print(TITLE)
    if sys.version_info < PYTHON_REQ:
        print(f'Python version >= {PYTHON_REQ} required. Please, upgrade!')
        sys.exit(1)
    create = not os.path.isfile(WORDBASE)
    conn = sqlite3.connect(WORDBASE)
    cur = conn.cursor()
    cur.execute("PRAGMA foreign_keys = ON")
    if create:
        print('\nNo word base found. Creating...')
        makebase()
    else:
        db_version = cur.execute("PRAGMA user_version").fetchone()[0]
        if db_version != RELEASE:
            upgradebase(db_version)
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
            inp = choose(
                'Choose a number to:'
                f'\n[1] import from {TEXTBASE}'
                f'\n[2] export to {TEXTBASE}'
                '\n[3] list all'
                '\n[4] look up'
                '\n[5] delete'
                '\n[6] exit\n',
                min=1,
                max=6,
            )
            tasks[inp - 1]()
        input('\nPress Enter to continue')
