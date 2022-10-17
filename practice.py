#!/usr/bin/env python3
import random
import sys
import pyinputplus as pyip

import header
load, dump = header.load, header.dump

if __name__ == "__main__":
    header.initiate()
    wordbase = 'wordbase.json'
    repbase = 'repbase.json'
    try:
        verbs = load(wordbase)
    except FileNotFoundError:
        sys.exit('No word base found! Run fillbase!')
    infs = header.infinitives(verbs)
    forms = ['Infinitive', 'Presens', 'Preteritum', 'Supinum', 'Translation']
    words = []
    for verb in verbs:
        word = {forms[i]: verb[i] for i in range(5)}
        words.append(word)
    num_words = len(words)
    inp = pyip.inputNum('Choose 1 to practice forms, '
                        '2 to practice translations: ', min=1, max=2)
    if inp == 1:
        try:
            rep = load(repbase)
        except FileNotFoundError:
            sys.exit('No repetition base found! Run fillbase!')
        total = len(rep)
        print(f'{total} verbs loaded from the repetition base')
        num = pyip.inputNum('How many verbs to practice? ', min=1, max=total)
        hint = ('Type in three forms of the verb - \n'
                f'{forms[1]}, {forms[2]}, {forms[3]} - \n'
                'separated by spaces')
        print(hint)
        practice, base = rep[:num], rep[num:]
        badlist, goodlist = [], []
        good = 0
        def test(verb):
            x = infs.index(verb)
            while True:
                prompt = f'\n{forms[0]}: att {verb}, three forms? '
                reply = pyip.inputStr(prompt).casefold().split()
                if len(reply) == 3:
                    break
                print(hint)
            ok = True
            for i in range(3):
                correct = words[x][forms[i+1]]
                if reply[i] != correct:
                    print(f'Incorrect {forms[i+1]}! '
                          f'{reply[i]} instead of {correct}')
                    ok = False
            if ok:
                print('Correct.')
            return ok

        while practice:
            verb = practice.pop()
            if test(verb):
                good += 1
                goodlist.append(verb)
            else:
                badlist.append(verb)
        print(f'\nOut of {num} verbs {good} ({good/num:.0%}) correct')
        rep = badlist + base + goodlist
        dump(repbase, rep)
        if badlist:
            if pyip.inputYesNo('Repeat incorrect ones? ') == 'yes':
                while badlist:
                    verb = badlist.pop()
                    if not test(verb):
                        badlist.append(verb)
    elif inp == 2:
        wordscopy = words.copy()
        random.shuffle(wordscopy)
        good = 0
        num_opt = 6
        num = pyip.inputNum('How many words to practice? ',
                            min=1, max=num_words)
        print('Think of a translation then press Enter to choose from '
              f'{num_opt} options.')
        for _ in range(num):
            word = wordscopy.pop()
            print('\nVerb:', word['Infinitive'])
            input()
            choice = [word['Translation']]
            while len(choice) < num_opt:
                random_trans = random.choice(words)['Translation']
                if random_trans not in choice:
                    choice.append(random_trans)
            random.shuffle(choice)
            for i, trans in enumerate(choice):
                print(i+1, trans)
            first_try = True
            while True:
                inp = pyip.inputNum('Which translation is correct? ',
                                    min=1, max=num_opt)
                if choice[inp-1] == word['Translation']:
                    print(f"Yes, [{word['Infinitive']}] can be translated as "
                          f"[{word['Translation']}]")
                    if first_try:
                        good += 1
                    break
                first_try = False
                print('Try again!')
        print(f'\nOut of {num} translations {good} ({good/num:.0%}) correct')
    input('Press Enter to exit')
