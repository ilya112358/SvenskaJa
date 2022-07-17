import json
import signal
import sys

wordbase = r"C:\Users\Public\Downloads\dist\Base\wordbase.json"
wordbase_bak = r"C:\Users\Public\Downloads\dist\Base\wordbase.bak"
wordbase_mock = r"C:\Users\Public\Downloads\dist\Base\wordbase.mock"

def input_num(msg, dia):
    """Get number in range from user. Dia must be non-empty range."""
    try:
        num = int(input(msg))
        if num not in dia:
            raise ValueError
        return num
    except ValueError:
        return input_num(f'Enter a number from {dia}: ', dia)

def initiate():
    """Set Ctrl-C handler. Read wordbase. Return list of verbs."""
    def ctrlc_handler(signal, frame):
        print('\nCtrl-C pressed, exiting...')
        sys.exit(0)

    signal.signal(signal.SIGINT, ctrlc_handler)
    print('Press Ctrl-C to exit at any time.')
    with open(wordbase, encoding='utf-8') as f:
        return json.load(f)
    
