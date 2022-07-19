import json
import header

def get_infs():
    infs = [verb[0] for verb in verbs]
    for i in range(len(infs)//5):
        line = ' '
        for k in range(5):
            line += (f'{infs[i*5+k]:12}')
        print(line)
    line = ' '
    for k in range(len(infs)%5):
        line += (f'{infs[(i+1)*5+k]:12}')
    print(line)
    return infs

def fill_wordbase():
    done = False
    while not done:
        inf = input('\nInfinitive to add? ')
        if inf in infs:
            print('Already exists!')
            continue
        pres = input('Present? ')
        past = input('Past? ')
        supin = input('Supinum? ')
        trans = input('Translation? ')
        verb = [inf, pres, past, supin, trans]
        print(verb)
        correct = input('Correct? [Y/Other] ')
        if correct == 'Y' or correct == 'y':
            verbs.append(verb)
            infs.append(inf)
            f.seek(0) # rewrite
            json.dump(verbs, f)
        inp = input('\nAnother? [Y/Other] ')
        done = (inp != 'Y' and inp != 'y')

def del_el():
    done = False
    while not done:
        inf = input('\nInfinitive to delete? ')
        try:
            x = infs.index(inf)
        except ValueError:
            print('Not in the list!')
            continue
        print(verbs[x])
        correct = input('Correct? [Y/Other] ')
        if correct == 'Y' or correct == 'y':
            verbs.pop(x)
            infs.pop(x)
        inp = input('\nAnother? [Y/Other] ')
        done = (inp != 'Y' and inp != 'y')

if __name__ == "__main__":
    verbs, _ = header.initiate()
    print(f'{len(verbs)} verbs loaded')
    with open(header.wordbase_bak,'w', encoding='utf-8') as f:
        json.dump(verbs, f)
    verbs.sort(key=lambda verb: verb[0])
    infs = get_infs()
    inp = header.input_num('Choose 1 to del, 2 to input new, '
                           '3 to make mock base ', range(1,4))
    if inp == 1:
        with open(header.wordbase,'w', encoding='utf-8') as f:
            del_el()
            json.dump(verbs, f)
    elif inp == 2:
        with open(header.wordbase,'w', encoding='utf-8') as f:
            json.dump(verbs, f)
            fill_wordbase()
    elif inp == 3:
        with open(header.wordbase_mock,'w', encoding='utf-8') as f:
            json.dump(verbs[:7], f)
    input('Press Enter to exit')
