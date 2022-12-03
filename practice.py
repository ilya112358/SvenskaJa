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
    cur = conn.cursor()
    cur.execute("PRAGMA foreign_keys = ON")
    
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

    def practice(words):
        """Cycle through words which is dict {'verb': prio,}"""
        num = len(words)
        shuffled = random.sample(list(words), num)
        n_good = n_bad = 0
        badlist = []
        for word in shuffled:
            if question(word):
                n_good += 1
                words[word] += 1
            else:
                n_bad += 1
                words[word] = 0
                badlist.append(word)
            print(f'{n_good} good, {n_bad} bad, {num-n_good-n_bad} to go')
            db_update(word, words[word])
        print(f'\nOut of {num} verbs {n_good} ({n_good/num:.0%}) correct')
        if badlist and pyip.inputYesNo('Repeat incorrect ones? ') == 'yes':
            while badlist:
                badlist = [word for word in badlist if not question(word)]
        input('\nWell done! Press Enter to exit')

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
        verbs_prio = {}
        verbs_quest = {}
        for verb in verbs[:num]:
            verbs_prio[verb[0]] = verb[4]   # {'be': 0,}
            verbs_quest[verb[0]] = verb[1:4]    # {'be': (ber,bad,bett),}
        
        def question(verb):
            """Check knowledge of verb forms. Called from practice()"""
            while True:
                forms = verbs_quest[verb]
                prompt = f'\nInfinitive: att {verb}, three forms? '
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

        def db_update(verb, prio):
            """Update priority. Called from practice()"""
            query = "UPDATE VerbFormsPractice SET Priority = ? WHERE Verb = ?"
            cur.execute(query, (prio, verb))
            conn.commit()

        practice(verbs_prio)
    # translations practice
    elif inp == 2:
        lang = ('Russian', 'English')
        inp = pyip.inputInt(f'Which translations to use: [1] {lang[0]} '
                            f'or [2] {lang[1]}? ', min=1, max=2)
        lang = lang[inp-1]
        query = f"""
            SELECT
                VerbTranslations.Verb,
                VerbTranslations.{lang},
                VerbTranslationsPractice.{lang}
            FROM VerbTranslations INNER JOIN VerbTranslationsPractice
            ON VerbTranslationsPractice.Verb = VerbTranslations.Verb
            WHERE VerbTranslations.{lang} <> ''
            ORDER BY VerbTranslationsPractice.{lang}
            """
        verbs, num = loadbase(query)
        inp = pyip.inputInt('Do you want to practice [1] multiple choice test '
                            'or [2] flashcard test? ', min=1, max=2)
        if inp == 1:
            sample = random.sample(verbs, num)
            print('Try to recall a translation then press Enter to choose from '
                  'options')
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
                        print(f'Yes, "{word[0]}" can be translated as '
                              f'"{word[1]}"')
                        print(f'{k+1} done, {num-k-1} to go')
                        break
                    print('Try again!')
            input('\nWell done! Press Enter to exit')
        elif inp == 2:
            verbs_prio = {}
            verbs_quest = {}
            for verb in verbs[:num]:
                verbs_prio[verb[0]] = verb[2]   # {'be': 0,}
                verbs_quest[verb[0]] = verb[1]    # {'be': 'beg',}

            def question(verb):
                """Check knowledge of a translation. Called from practice()"""
                print('\nVerb:', verb)
                input()
                inp = pyip.inputInt(f'{verbs_quest[verb]} [1] Yes [2] No ',
                                    min=1, max=2)
                return inp == 1

            def db_update(verb, prio):
                """Update priority. Called from practice()"""
                query = f"""
                    UPDATE VerbTranslationsPractice
                    SET {lang} = ?
                    WHERE Verb = ?
                    """
                cur.execute(query, (prio, verb))
                conn.commit()

            print('Try to recall a translation then press Enter to see the '
                  'answer.')
            print('Enter [1] if you remembered correctly, [2] if not.')
            practice(verbs_prio)
    else:
        print('Remember, practice makes perfect!')
    conn.close()
