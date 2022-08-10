import json
import random
import pyinputplus as pyip
import header

if __name__ == "__main__":
    config = header.initiate()
    if config['Options'].getboolean('Mock'):
        wordbase = config['Path']['Mock']
    else:
        wordbase = config['Path']['WordBase']
    with open(wordbase, encoding='utf-8') as f:
        verbs = json.load(f)
    infs = header.infinitives(verbs)
    forms = ['inf', 'pres', 'past', 'supin', 'trans']
    words = []
    for verb in verbs:
        word = {forms[i]: verb[i] for i in range(5)}
        words.append(word)
    num_words = len(words)
    print(f'{num_words} verbs loaded\n')
    inp = pyip.inputNum('Choose 1 to practice forms, '
                        '2 to practice translations: ', min=1, max=2)
    if inp == 1:
        practice = []
        for word in words:
            for i in range(1, 4):
                dct = {}
                dct['inf'] = word['inf']
                dct['form'] = i
                dct['reply'] = word[forms[i]]
                practice.append(dct)
        random.shuffle(practice)
        total = len(practice)
        print(f'\n{total} total forms')
        num = pyip.inputNum('How many forms to practice? ', min=1, max=total)
        del practice[num:]
        def repeat(practice):
            num = len(practice)
            good = 0
            torepeat = []
            while practice:
                verb = practice.pop()
                prompt = f"\n {verb['inf']}: in "
                match verb['form']:
                    case 1:
                        prompt += 'Presens (Jag...) '
                    case 2:
                        prompt += 'Preteritum (I går...) '
                    case 3:
                        prompt += 'Supinum (Jag har...) '
                reply = input(prompt)
                if reply == verb['reply']:
                    print('Correct.')
                    good += 1
                else:
                    print('Incorrect!', verb['reply'])
                    torepeat.append(verb)
            print(f'\nOut of {num} forms {good} ({good/num:.0%}) correct')
            if torepeat:
                rep = input('Repeat incorrect ones? [Y] ')
                if rep == 'Y' or rep == 'y':
                    repeat(torepeat)

        repeat(practice)

    elif inp == 2:
        wordscopy = words.copy()
        random.shuffle(wordscopy)
        good = 0
        num_opt = config['Options'].getint('NumberOfTrans')
        num = pyip.inputNum('How many words to practice? ',
                            min=1, max=num_words)
        for _ in range(num):
            word = wordscopy.pop()
            print('\nInfinitive:', word['inf'])
            choice = [word['trans']]
            while len(choice) < num_opt:
                random_trans = random.choice(words)['trans']
                if random_trans not in choice:
                    choice.append(random_trans)
            random.shuffle(choice)
            for i, trans in enumerate(choice):
                print(i+1, trans)
            first_try = True
            while True:
                inp = pyip.inputNum('Which translation is correct? ',
                                    min=1, max=num_opt)
                if choice[inp-1] == word['trans']:
                    print(f"Yes, translation of _{word['inf']}_",
                          f"is _{word['trans']}_")
                    if first_try:
                        good += 1
                    break
                first_try = False
                print('Try again!')
            input('Press Enter to continue:')
        print(f'\nOut of {num} translations '
              f'{good} ({good/num:.0%}) correct')

    input('Press Enter to exit')
