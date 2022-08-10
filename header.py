import configparser
import signal
import sys

def initiate():
    """Set Ctrl-C handler. Read and return config."""
    def ctrlc_handler(signal, frame):
        print('\nCtrl-C pressed, exiting...')
        sys.exit(0)

    signal.signal(signal.SIGINT, ctrlc_handler)
    print('Press Ctrl-C to exit at any time.')
    config = configparser.ConfigParser()
    with open('myproj.ini') as f:
        config.read_file(f)
    return config

def infinitives(verbs):
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
