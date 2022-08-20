import json
import random
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
    """Delete element from the list"""
    inf = pyip.inputStr('\nInfinitive to delete? ').casefold()
    try:
        x = infs.index(inf)
    except ValueError:
        print('Not in the list!')
        return
    print(verbs[x])
    if pyip.inputYesNo('Delete this entry? ') == 'no':
        return
    verbs.pop(x)
    infs.pop(x)
    with open(repbase, encoding='utf-8') as f:
        rep = json.load(f)
    newbase = [lst for lst in rep if lst[0] != inf]
    with open(repbase, 'w', encoding='utf-8') as f:
        json.dump(newbase, f)
    print(f'[{inf}] deleted from wordbase and repbase')

def makerep():
    """(Re)Create and return repetition base"""
    rep = []
    for verb in verbs:
        for i in range(1, 4):
            lst = []
            lst.append(verb[0]) # inf
            lst.append(i) # form index
            lst.append(verb[i]) # form
            rep.append(lst)
    random.shuffle(rep)
    print(f'\n{len(rep)} forms prepared')
    return rep

def makemock():
    """(Re)Create and return mock base"""
    mock = []
    n = 0
    while len(mock) < 10:
        candidate = verbs[n]
        n += 1
        bad = False
        for k in range(4):
            for l in ['ö', 'å', 'ä']:
                if l in candidate[k]:
                    bad = True
        if not bad:
            mock.append(candidate)
    print(f'\n{len(mock)} verbs prepared')
    return mock

if __name__ == "__main__":
    config = header.initiate()
    mockbase = 'mockbase.json'
    wordbase = config['Path']['WordBase']
    repbase = config['Path']['RepBase']
    backbase = config['Path']['Backup']
    with open(wordbase, encoding='utf-8') as f:
        verbs = json.load(f)
    with open(backbase, 'w', encoding='utf-8') as f:
        json.dump(verbs, f)
    while True:
        verbs.sort(key=lambda verb: verb[0])
        infs = header.infinitives(verbs)
        inp = pyip.inputNum('Choose:'
                            '\n[1] to del, [2] to input new,'
                            '\n[3] to create repetition base,'
                            '\n[4] to create mock base, [5] to exit\n',
                            min=1, max=5)
        match inp:
            case 1:
                with open(wordbase, 'w', encoding='utf-8') as f:
                    del_el()
                    json.dump(verbs, f)
            case 2:
                with open(wordbase, 'w', encoding='utf-8') as f:
                    json.dump(verbs, f)
                    fill_wordbase()
            case 3:
                rep = makerep()
                with open(repbase, 'w', encoding='utf-8') as f:
                    json.dump(rep, f)
            case 4:
                mock = makemock()
                with open(mockbase, 'w', encoding='utf-8') as f:
                    json.dump(mock, f)
            case 5:
                break
