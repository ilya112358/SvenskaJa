import json
import random
import pyinputplus as pyip
import header

if __name__ == "__main__":
    config = header.initiate()
    if config['Options'].getboolean('Mock'):
        wordbase = 'mockbase.json'
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
    inp = pyip.inputNum('Choose 1 to practice forms, '
                        '2 to practice translations: ', min=1, max=2)
    if inp == 1:
        with open('repbase.json', encoding='utf-8') as f:
            repbase = json.load(f)
        total = len(repbase)
        print(f'\n{total} total forms')
        num = pyip.inputNum('How many forms to practice? ', min=1, max=total)
        practice, base = repbase[:num], repbase[num:]
        badlist, goodlist = [], []
        good = 0
        def test(verb):
            prompt = f'\n {verb[0]}: in '
            match verb[1]:
                case 1:
                    prompt += 'Presens (Jag...) '
                case 2:
                    prompt += 'Preteritum (I går...) '
                case 3:
                    prompt += 'Supinum (Jag har...) '
            reply = pyip.inputStr(prompt).casefold()
            return reply == verb[2]

        while practice:
            verb = practice.pop()
            if test(verb):
                print('Correct.')
                good += 1
                goodlist.append(verb)
            else:
                print('Incorrect!', verb[2])
                badlist.append(verb)
        print(f'\nOut of {num} forms {good} ({good/num:.0%}) correct')
        repbase = badlist + base + goodlist
        with open('repbase.json', 'w', encoding='utf-8') as f:
            json.dump(repbase, f)
        if badlist:
            if pyip.inputYesNo('Repeat incorrect ones? ') == 'yes':
                practice = badlist.copy()
                while practice:
                    verb = practice.pop()
                    if test(verb):
                        print('Correct.')
                    else:
                        print('Incorrect!', verb[2])
                        practice.append(verb)
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
        print(f'\nOut of {num} translations {good} ({good/num:.0%}) correct')
    input('Press Enter to exit')
