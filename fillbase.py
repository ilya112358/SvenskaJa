import json
import random
import pyinputplus as pyip
import header

def input_verb(inf):
    """Input verb forms"""
    pres = pyip.inputStr('Presens? ').casefold()
    past = pyip.inputStr('Preteritum? ').casefold()
    supin = pyip.inputStr('Supinum? ').casefold()
    trans = pyip.inputStr('Translation? ').casefold()
    verb = [inf, pres, past, supin, trans]
    print(verb)
    return verb

def lookup():
    """Look up a verb from the list"""
    inf = pyip.inputStr('\nInfinitive? ').casefold()
    try:
        x = infs.index(inf)
    except ValueError:
        print('Not in the list!')
        return
    print(verbs[x])

def add_el():
    """Add a verb to the list"""
    inf = pyip.inputStr('\nInfinitive to add? ')
    if inf in infs:
        print('Already exists!')
        return
    verb = input_verb(inf)
    if pyip.inputYesNo('Add this entry? ') == 'no':
        return
    verbs.append(verb)
    with open(repbase, encoding='utf-8') as f:
        rep = json.load(f)
    lst = [[inf, 1, verb[1]], [inf, 2, verb[2]], [inf, 3, verb[3]]]
    newbase = lst + rep
    with open(repbase, 'w', encoding='utf-8') as f:
        json.dump(newbase, f)
    with open(wordbase, 'w', encoding='utf-8') as f:
        json.dump(verbs, f)
    print(f'[{inf}] added to wordbase and repbase')

def del_el():
    """Delete a verb from the list"""
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
    with open(repbase, encoding='utf-8') as f:
        rep = json.load(f)
    newbase = [lst for lst in rep if lst[0] != inf]
    with open(repbase, 'w', encoding='utf-8') as f:
        json.dump(newbase, f)
    with open(wordbase, 'w', encoding='utf-8') as f:
        json.dump(verbs, f)
    print(f'[{inf}] deleted from wordbase and repbase')

def sortbase():
    """Sort wordbase by infinitives and save"""
    verbs.sort(key=lambda verb: verb[0])
    with open(wordbase, 'w', encoding='utf-8') as f:
        json.dump(verbs, f)
    print('Word base sorted')

def makerep():
    """(Re)Create repetition base"""
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
    if pyip.inputYesNo('Write new repetition base? ') == 'no':
        return
    with open(repbase, 'w', encoding='utf-8') as f:
        json.dump(rep, f)
    print('Repetition base saved')

def makemock():
    """(Re)Create mock base"""
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
    if pyip.inputYesNo('Write new mock base? ') == 'no':
        return
    with open(mockbase, 'w', encoding='utf-8') as f:
        json.dump(mock, f)
    print('Mock base saved')

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
    tasks = (lookup, del_el, add_el, sortbase, makerep, makemock)
    while True:
        infs = header.infinitives(verbs)
        inp = pyip.inputNum('Choose a number to:'
                            '\n[0] look up,'
                            '\n[1] delete,'
                            '\n[2] input new,'
                            '\n[3] sort,'
                            '\n[4] create repetition base,'
                            '\n[5] create mock base,'
                            '\n[Ctrl-C] to exit\n',
                            min=0, max=5)
        tasks[inp]()
        input('Press Enter to return')
