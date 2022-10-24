#!/usr/bin/env python3
import os.path
import sqlite3
import sys
import pyinputplus as pyip

if __name__ == "__main__":
    print('*** SvenskaJa ***')
    wordbase = 'wordbase.db'
    if not os.path.isfile(wordbase):
        print(f'\nNo {wordbase} found. Run maintenance.')
        sys.exit(0)
    conn = sqlite3.connect('wordbase.db')
    conn.execute("PRAGMA foreign_keys = ON")
    cur = conn.cursor()
    verbs = []
    query = """
        SELECT Infinitiv, Presens, Preteritum, Supinum, Priority
        FROM VerbForms INNER JOIN VerbFormsPractice
        ON VerbFormsPractice.Verb = VerbForms.Infinitiv
        ORDER BY Priority
        """
    for row in cur.execute(query):
        verbs.append(row) 
    if not verbs:
        print(f'\nThe word base is empty. Run maintenance.')
        conn.close()
        sys.exit(0)
    total = len(verbs)
    print(f'\n{total} verbs loaded from the word base\n')
    num = pyip.inputNum('How many verbs to practice? ', min=1, max=total)
    hint = ('Type in three forms of the verb - \n'
            'Presens, Preteritum, Supinum - \n'
            'separated by spaces')
    print(hint)
    def test():
        while True:
            prompt = f'\nInfinitiv: att {inf}, three forms? '
            reply = pyip.inputStr(prompt).casefold().split()
            if len(reply) == 3:
                break
            print(hint)
        ok = True
        for i in range(3):
            if reply[i] != forms[i]:
                print(f'Incorrect form! {reply[i]} instead of {forms[i]}')
                ok = False
        if ok:
            print('Correct')
        return ok
    
    n_good, n_bad, badlist = 0, 0, []
    for i in range(num):
        verb = verbs[i]
        inf, forms, priority = verb[0], verb[1:4], verb[4]
        if test():
            n_good += 1
            priority += 1
        else:
            n_bad += 1
            priority = 0
            badlist.append(verb)
        query = "UPDATE VerbFormsPractice SET Priority = ? WHERE Verb = ?"
        cur.execute(query, (priority, inf))
        conn.commit()
        print(f'{n_good} good, {n_bad} bad, {num-n_good-n_bad} to go')
    print(f'\nOut of {num} verbs {n_good} ({n_good/num:.0%}) correct')
    if badlist:
        if pyip.inputYesNo('Repeat incorrect ones? ') == 'yes':
            while badlist:
                verb = badlist.pop()
                inf, forms = verb[0], verb[1:4]
                if not test():
                    badlist.append(verb)
    print('Goodbye!')
    conn.close()
