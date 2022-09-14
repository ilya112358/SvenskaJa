#!/usr/bin/env python3
import json
import random
import pyinputplus as pyip
import header

if __name__ == "__main__":
    config = header.initiate()
    wordbase = config['Path']['WordBase']
    repbase = config['Path']['RepBase']
    with open(wordbase, encoding='utf-8') as f:
        verbs = json.load(f)
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
        with open(repbase, encoding='utf-8') as f:
            rep = json.load(f)
        total = len(rep)
        print(f'\n{total} total forms')
        num = pyip.inputNum('How many forms to practice? ', min=1, max=total)
        practice, base = rep[:num], rep[num:]
        badlist, goodlist = [], []
        good = 0
        def test(verb):
            x = infs.index(verb)
            for i in range(1, 4):
                correct = words[x][forms[i]]
                prompt = f'\n att {verb}: in {forms[i]}? '
                reply = pyip.inputStr(prompt).casefold()
                if reply != correct:
                    print('Incorrect!', correct)
                    return False
                else:
                    print('Correct.')
            return True

        while practice:
            verb = practice.pop()
            if test(verb):
                good += 1
                goodlist.append(verb)
            else:
                badlist.append(verb)
        print(f'\nOut of {num} forms {good} ({good/num:.0%}) correct')
        rep = badlist + base + goodlist
        with open(repbase, 'w', encoding='utf-8') as f:
            json.dump(rep, f)
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
        num_opt = config['Options'].getint('NumberOfTrans')
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
