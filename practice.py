#!/usr/bin/env python3
import os.path
import random
import sqlite3
import sys

import pyinputplus as pyip
from tabulate import tabulate
from colorama import just_fix_windows_console

from maintain import RELEASE, TITLE, WORDBASE, c, choose


class PracticeSRS:
    """
    Practice words with spaced repetition system.
    Parent class defines self.practice().
    Child class should populate self.words and self.quest
    and also define self.question() and self.db_update().
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
        print(f'(to abort practice press {c.BOLD}Ctrl-C{c.END})')
        for word in shuffled:
            try:
                if self.question(word, self.quest[word]):
                    n_good += 1
                    self.words[word] += 1
                else:
                    n_bad += 1
                    self.words[word] = 0
                    badlist.append(word)
            except KeyboardInterrupt:
                finish('Practice aborted.')
            print(
                f'{c.GREEN}{n_good} good,{c.END} {c.RED}{n_bad} bad,{c.END} {num-n_good-n_bad} to go'
            )
            self.db_update(word, self.words[word])
        print(f'\nOut of {num} verbs {n_good} ({n_good/num:.0%}) are correct')
        if badlist and pyip.inputYesNo('Repeat incorrect ones? ') == 'yes':
            try:
                while badlist:
                    badlist = [
                        word
                        for word in badlist
                        if not self.question(word, self.quest[word])
                    ]
            except KeyboardInterrupt:
                finish('Practice aborted.')
        input('\nWell done! Press Enter to exit.')


def finish(string, code=0):
    """Graceful exit with connection close"""
    if code == 1:
        string += ' Run maintenance.'
    print('\nAttention!', string)
    if conn is not None:
        conn.close()
    sys.exit(code)


def loadbase(query) -> (list, int):
    """Query wordbase. Return verbs, number of exercises. Exit if empty."""
    verbs = []
    for row in cur.execute(query):
        verbs.append(row)
    if not verbs:
        finish('The word base is empty.', 1)
    total = len(verbs)
    print(f'\n{total} verbs loaded from the word base\n')
    num = pyip.inputInt('How many verbs to practice? ', min=1, max=total)
    return verbs, num


if __name__ == "__main__":
    just_fix_windows_console()
    print(TITLE)
    conn = None
    if not os.path.isfile(WORDBASE):
        finish(f'No {WORDBASE} found.', 1)
    conn = sqlite3.connect(WORDBASE)
    cur = conn.cursor()
    cur.execute("PRAGMA foreign_keys = ON")
    if cur.execute("PRAGMA user_version").fetchone()[0] != RELEASE:
        finish('The word base needs upgrading.', 1)
    inp = choose('\nPractice [1] forms, [2] translations, or [3] exit: ', min=1, max=3)
    # verb forms practice
    if inp == 1:
        query = """
            SELECT Infinitive, Present, Past, Supine, Priority
            FROM VerbForms INNER JOIN VerbFormsPractice
            ON VerbFormsPractice.Verb = VerbForms.Infinitive
            ORDER BY Priority
            """
        verbs, num = loadbase(query)
        hint = 'Type in Present, Past, Supine forms separated by spaces'
        print(hint)

        class PracticeForms(PracticeSRS):
            def __init__(self, verbs):
                super().__init__()
                for verb in verbs:
                    self.words[verb[0]] = verb[4]  # {'be': 0,}
                    self.quest[verb[0]] = verb[1:4]  # {'be': (ber,bad,bett),}

            def question(self, verb: str, answer: tuple) -> bool:
                """Check knowledge of verb forms"""
                while True:
                    prompt = f'\nInfinitive: att {c.BOLD}{verb}{c.END}, three forms? '
                    reply = pyip.inputStr(prompt).casefold().split()
                    if len(reply) == 3:
                        break
                    print(hint)
                if reply[0].endswith('ar'):  # group 1 shortcut: agerar ade at
                    stem = reply[0][:-2]
                    if reply[1] == 'ade':
                        reply[1] = stem + 'ade'
                    if reply[2] == 'at':
                        reply[2] = stem + 'at'
                ok = True
                for i in range(3):
                    if reply[i] != answer[i]:
                        print(
                            f'Incorrect form! {reply[i]} instead of {c.BOLD}{answer[i]}{c.END}'
                        )
                        ok = False
                if ok:
                    print('Correct')
                return ok

            def db_update(self, verb: str, prio: int):
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
        inp = choose(
            f'Which translations to use: [1] {lang[0]} or [2] {lang[1]}? ', min=1, max=2
        )
        lang = lang[inp - 1]
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
        inp = choose(
            'Do you want to practice [1] multiple choice test or [2] flashcard test? ',
            min=1,
            max=2,
        )
        # multiple choice test
        if inp == 1:
            sample = random.sample(verbs, num)
            print('Try to recall a translation then press Enter to choose from options')
            print(f'(to abort practice press {c.BOLD}Ctrl-C{c.END})')
            for k, word in enumerate(sample):
                try:
                    print(f'\natt {word[0]}')
                    input()
                    choice = [word[1]]
                    n_choices = 4
                    while len(choice) < n_choices:
                        random_trans = random.choice(verbs)[1]
                        if random_trans not in choice:
                            choice.append(random_trans)
                    random.shuffle(choice)
                    choices = '\n'.join(
                        [f'[{i+1}] {trans}' for i, trans in enumerate(choice)]
                    )
                    choices += '\nWhich translation is correct? '
                    inp = choose(choices, min=1, max=n_choices)
                    if choice[inp - 1] == word[1]:
                        print(f'{c.GREEN}Correct{c.END}')
                    else:
                        print(f'{c.RED}Incorrect!{c.END}')
                    print(tabulate([[word[0], word[1]]], tablefmt='simple_grid'))
                    print(f'{k+1} done, {num-k-1} to go')
                except KeyboardInterrupt:
                    finish('Practice aborted.')
            input('\nWell done! Press Enter to exit')
        # flashcard test
        elif inp == 2:
            print('Try to recall a translation then press Enter to see the answer')

            class PracticeTranslations(PracticeSRS):
                def __init__(self, verbs):
                    super().__init__()
                    for verb in verbs:
                        self.words[verb[0]] = verb[2]  # {'be': 0,}
                        self.quest[verb[0]] = verb[1]  # {'be': 'beg',}

                def question(self, verb: str, answer: str) -> bool:
                    """Check knowledge of a translation"""
                    input(f'\n{verb}')
                    print(f'{answer}')
                    inp = choose(
                        'Enter [1] if you remembered correctly, [2] if not: ',
                        min=1,
                        max=2,
                    )
                    return inp == 1

                def db_update(self, verb: str, prio: int):
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
