#!/usr/bin/env python3
import os.path
import random
import sqlite3
import sys
import pyinputplus as pyip

from maintain import RELEASE, TITLE, WORDBASE

class PracticeSRS:
    """
    Practice words with spaced repetition system. Parent class.
    Child class should populate self.words and self.quest and also
    define self.question() and self.db_update().
    """
    def __init__(self):
        self.words = {}
        self.quest = {}

    def practice(self):
        """Cycle through reshuffled words. Repeat incorrect ones."""
        num = len(self.words)
        shuffled = random.sample(list(self.words), num)
        n_good = n_bad = 0
        badlist = []
        for word in shuffled:
            if self.question(word, self.quest[word]):
                n_good += 1
                self.words[word] += 1
            else:
                n_bad += 1
                self.words[word] = 0
                badlist.append(word)
            print(f'{n_good} good, {n_bad} bad, {num-n_good-n_bad} to go')
            self.db_update(word, self.words[word])
        print(f'\nOut of {num} verbs {n_good} ({n_good/num:.0%}) are correct')
        if badlist and pyip.inputYesNo('Repeat incorrect ones? ') == 'yes':
            while badlist:
                badlist = [word for word in badlist
                           if not self.question(word, self.quest[word])]
        input('\nWell done! Press Enter to exit.')


if __name__ == "__main__":
    print(TITLE)
    if not os.path.isfile(WORDBASE):
        print(f'\nNo {WORDBASE} found. Run maintenance.')
        sys.exit(1)
    conn = sqlite3.connect(WORDBASE)
    cur = conn.cursor()
    cur.execute("PRAGMA foreign_keys = ON")
    if cur.execute("PRAGMA user_version").fetchone()[0] != RELEASE:
        print(f'\nThe word base needs upgrading. Run maintenance.')
        conn.close()
        sys.exit(1)
    
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

    inp = pyip.inputInt('\nPractice [1] forms, [2] translations, or '
                        '[3] exit: ', min=1, max=3)
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

        class PracticeForms(PracticeSRS):
            def __init__(self, verbs):
                super().__init__()
                for verb in verbs:
                    self.words[verb[0]] = verb[4] # {'be': 0,}
                    self.quest[verb[0]] = verb[1:4] # {'be': (ber,bad,bett),}
                
            def question(self, verb, answer):
                """Check knowledge of verb forms"""
                while True:
                    prompt = f'\nInfinitive: att {verb}, three forms? '
                    reply = pyip.inputStr(prompt).casefold().split()
                    if len(reply) == 3:
                        break
                    print(hint)
                ok = True
                for i in range(3):
                    if reply[i] != answer[i]:
                        print('Incorrect form! '
                              f'{reply[i]} instead of {answer[i]}')
                        ok = False
                if ok:
                    print('Correct')
                return ok
        
            def db_update(self, verb, prio):
                """Update priority"""
                query = """
                        UPDATE VerbFormsPractice
                        SET Priority = ?
                        WHERE Verb = ?
                        """
                cur.execute(query, (prio, verb))
                conn.commit()

        pr = PracticeForms(verbs[:num])
        pr.practice()
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
            print('Try to recall a translation '
                  'then press Enter to choose from options')
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
            print('Try to recall a translation '
                  'then press Enter to see the answer')
            
            class PracticeTranslations(PracticeSRS):
                def __init__(self, verbs):
                    super().__init__()
                    for verb in verbs:
                        self.words[verb[0]] = verb[2] # {'be': 0,}
                        self.quest[verb[0]] = verb[1] # {'be': 'beg',}

                def question(self, verb, answer):
                    """Check knowledge of a translation"""
                    print('\nVerb:', verb)
                    input()
                    print(f'{answer}')
                    inp = pyip.inputInt('Enter '
                                        '[1] if you remembered correctly, '
                                        '[2] if not: ', min=1, max=2)
                    return inp == 1

                def db_update(self, verb, prio):
                    """Update priority"""
                    query = f"""
                        UPDATE VerbTranslationsPractice
                        SET {lang} = ?
                        WHERE Verb = ?
                        """
                    cur.execute(query, (prio, verb))
                    conn.commit()

            pr = PracticeTranslations(verbs[:num])
            pr.practice()
    # no practice
    else:
        print('Remember, practice makes perfect!')
    conn.close()
