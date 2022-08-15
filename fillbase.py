import json
import pyinputplus as pyip
import header

def fill_wordbase():
    inf = input('\nInfinitive to add? ')
    if inf in infs:
        print('Already exists!')
        return
    pres = input('Presens? ')
    past = input('Preteritum? ')
    supin = input('Supinum? ')
    trans = input('Translation? ')
    verb = [inf, pres, past, supin, trans]
    print(verb)
    if pyip.inputYesNo('Correct? ') == 'yes':
        verbs.append(verb)
        verbs.sort(key=lambda verb: verb[0])
        infs.append(inf)
        f.seek(0) # rewrite
        json.dump(verbs, f)

def del_el():
    inf = input('\nInfinitive to delete? ')
    try:
        x = infs.index(inf)
    except ValueError:
        print('Not in the list!')
        return
    print(verbs[x])
    if pyip.inputYesNo('Delete this entry? ') == 'yes':
        verbs.pop(x)
        infs.pop(x)

def makemock():
    mock = []
    n = 0
    while len(mock) < 7:
        candidate = verbs[n]
        n += 1
        bad = False
        for k in range(4):
            for l in ['ö', 'å', 'ä']:
                if l in candidate[k]:
                    bad = True
        if not bad:
            mock.append(candidate)
    return mock

if __name__ == "__main__":
    config = header.initiate()
    wordbase = config['Path']['WordBase']
    wordbase_bak = config['Path']['Backup']
    wordbase_mock = config['Path']['Mock']
    with open(wordbase, encoding='utf-8') as f:
        verbs = json.load(f)
    with open(wordbase_bak,'w', encoding='utf-8') as f:
        json.dump(verbs, f)
    while True:
        print(f'\n{len(verbs)} verbs loaded\n')
        verbs.sort(key=lambda verb: verb[0])
        infs = header.infinitives(verbs)
        inp = pyip.inputNum('\nChoose 1 to del, 2 to input new, '
                            '3 to make mock base, 4 to exit ', min=1, max=4)
        if inp == 1:
            with open(wordbase,'w', encoding='utf-8') as f:
                del_el()
                json.dump(verbs, f)
        elif inp == 2:
            with open(wordbase,'w', encoding='utf-8') as f:
                json.dump(verbs, f)
                fill_wordbase()
        elif inp == 3:
            mock = makemock()
            with open(wordbase_mock,'w', encoding='utf-8') as f:
                json.dump(mock, f)
        elif inp == 4:
            break
