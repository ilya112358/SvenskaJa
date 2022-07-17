import random
import header

if __name__ == "__main__":
    verbs = header.initiate()
    forms = ['inf', 'pres', 'past', 'supin', 'trans']
    words = []
    for verb in verbs:
        word = {forms[i]: verb[i] for i in range(5)}
        words.append(word)
    num_words = len(words)
    print(f'{num_words} verbs loaded\n')
    inp = header.input_num('Choose 1 to practice forms, '
                           '2 to practice translations: ', range(1, 3))
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
        num = header.input_num('How many forms to practice? ',
                               range(1, total+1))
        del practice[num:]
        good = 0
        while practice:
            verb = practice.pop()
            prompt = f"\n {verb['inf']}: in "
            match verb['form']:
                case 1:
                    prompt += "Presens (Jag...) "
                case 2:
                    prompt += "Preteritum (I går...) "
                case 3:
                    prompt += "Supinum (Jag har...) "
            reply = input(prompt)
            if reply == verb['reply']:
                print('Correct.')
                good += 1
            else:
                print('Incorrect!', verb['reply'])
        print(f'\nOut of {num} forms {good} ({good/num:.0%}) correct') 
    elif inp == 2:
        wordscopy = words.copy()
        random.shuffle(wordscopy)
        good = 0
        num_opt = header.input_num('Choose from how many options? [2-7] ',
                                   range(2, 8))
        while wordscopy:
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
                inp = header.input_num('Which translation is correct? ',
                                       range(1, num_opt+1))
                if choice[inp-1] == word['trans']:
                    print(f"Yes, translation of _{word['inf']}_",
                          f"is _{word['trans']}_")
                    if first_try:
                        good += 1
                    break
                first_try = False
                print('Try again!')
            input('Press Enter to continue:')
        print(f'\nOut of {num_words} translations '
              f'{good} ({good/num_words:.0%}) correct')
    input('Press Enter to exit')
