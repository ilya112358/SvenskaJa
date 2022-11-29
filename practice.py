#!/usr/bin/env python3
import os.path
import random
import sqlite3
import sys
import pyinputplus as pyip

from maintain import TITLE, WORDBASE

if __name__ == "__main__":
    print(TITLE)
    if not os.path.isfile(WORDBASE):
        print(f'\nNo {WORDBASE} found. Run maintenance.')
        sys.exit(0)
    conn = sqlite3.connect(WORDBASE)
    conn.execute("PRAGMA foreign_keys = ON")
    cur = conn.cursor()
    def loadbase(query):
        """Query wordbase. Return verbs, number of exercises. Exit if empty."""
        verbs = []
        for row in cur.execute(query):
            verbs.append(row)
        if not verbs:
            print(f'\nThe word base is empty. Run maintenance.')
            conn.close()
            sys.exit(0)
        total = len(verbs)
        print(f'\n{total} verbs loaded from the word base\n')
        num = pyip.inputInt('How many verbs to practice? ', min=1, max=total)
        return verbs, num

    inp = pyip.inputInt('Practice [1] forms, [2] translations. '
                        '[3] Exit: ', min=1, max=3)
    # verb forms practice
    if inp == 1:
        query = """
            SELECT Infinitive, Present, Past, Supine, Priority
            FROM VerbForms INNER JOIN VerbFormsPractice
            ON VerbFormsPractice.Verb = VerbForms.Infinitive
            ORDER BY Priority
            """
        verbs, num = loadbase(query)
        inp = pyip.inputInt('Practice [1] all verbs, '
                            '[2] only non-trivial (not group 1) verbs: ',
                             min=1, max=2)
        if inp == 2:
            verbs = [verb for verb in verbs
                     if not (verb[1][-2:] == 'ar' and
                     verb[2][-3:] == 'ade' and
                     verb[3][-2:] == 'at')]
            num = min(num, len(verbs))
        hint = 'Type in Present, Past, Supine forms separated by spaces'
        print(hint)
        def test():
            while True:
                prompt = f'\nInfinitive: att {inf}, three forms? '
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
        for verb in verbs[:num]:
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
        input('\nWell done! Press Enter to exit')
    # translations practice
    elif inp == 2:
        lang = ('Russian', 'English')
        inp = pyip.inputInt(f'Which translations to use: [1] {lang[0]} '
                            f'or [2] {lang[1]}? ', min=1, max=2)
        query = f"""
            SELECT Verb, {lang[inp-1]} FROM VerbTranslations
            WHERE {lang[inp-1]} <> ''
            """
        verbs, num = loadbase(query)
        sample = random.sample(verbs, num)
        print('Think of a translation then press Enter to choose from options')
        for k, word in enumerate(sample):
            print('\nVerb:', word[0])
            input()
            choice = [word[1]]
            n_choices = 4
            while len(choice) < n_choices:
                random_trans = random.choice(verbs)[1]
                if random_trans not in choice:
                    choice.append(random_trans)
            random.shuffle(choice)
            for i, trans in enumerate(choice):
                print(f'[{i+1}] {trans}')
            while True:
                inp = pyip.inputInt('Which translation is correct? ',
                                    min=1, max=n_choices)
                if choice[inp-1] == word[1]:
                    print(f'Yes, "{word[0]}" can be translated as "{word[1]}"')
                    print(f'{k+1} done, {num-k-1} to go')
                    break
                print('Try again!')
        input('\nWell done! Press Enter to exit')
    else:
        print('Remember, practice makes perfect!')
    conn.close()
