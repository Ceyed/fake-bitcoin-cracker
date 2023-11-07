import PySimpleGUI as sg
import threading
import time
from bitcoinaddress import Wallet
import random

sg.theme('DarkGrey14')

sg.set_options(text_justification='right')

START = False
PASSED_TIME = 0
FIRST_TIME = True
STOP_TREAD = False
NUMBER_OF_TRIES = 0
WORDS = []
LAST_FILE_ADDRESS = ''


def timer_thread():
    global PASSED_TIME
    while not STOP_TREAD:
        if START:
            PASSED_TIME += 1

            days, remainder = divmod(PASSED_TIME, 86400)
            hours, remainder = divmod(remainder, 3600)
            minutes, seconds = divmod(remainder, 60)

            time_str = f'{days:02}:{hours:02}:{minutes:02}:{seconds:02}'

            window['-TIME-'].update(f'| Passed time: {time_str}')
            
            time.sleep(1)


def print_wallet():
    def random_n_words(n):
        return random.sample(WORDS, n)

    global NUMBER_OF_TRIES
    while not STOP_TREAD:
        if START:
            wallet = Wallet()

            output = f"""Words combination: {', '.join(random_n_words(12 if values['-12-'] else 24))}
Wallet: {wallet.address.pubkey}


"""
            if values['-MORE-']:
                output = f"""Words combination: {', '.join(random_n_words(12 if values['-12-'] else 24))}
Wallet public key: {wallet.address.pubkey}
Wallet public keyc: {wallet.address.pubkeyc}
Wallet hex key address: {wallet.address.key.hex}
Wallet key wif: {wallet.key.hex}
Wallet key mainnet wif: {wallet.key.mainnet.wif}
Balance in wallet: {"0"}


"""
            NUMBER_OF_TRIES += 1
            window['-OUTPUT-'].update(output, append=True)
            window['-NOF-'].update(f'Number of tries: {NUMBER_OF_TRIES}')
            # time.sleep(random.uniform(0.5, 1))


def check_password_file_length():
    if len(WORDS):
        if values['-12-']:
            if len(WORDS) < 12:
                window['-ERROR-'].update('Words are less than 12, choose a larger file')
                window['-START-'].update(disabled=True)
            else:
                window['-ERROR-'].update('')
                window['-START-'].update(disabled=False)

        if values['-24-']:
            if len(WORDS) < 24:
                window['-ERROR-'].update('Words are less than 24, choose a larger file')
                window['-START-'].update(disabled=True)
            else:
                window['-ERROR-'].update('')
                window['-START-'].update(disabled=False)


layout = [   
    [
        sg.Text('Key Types:\t', font=('Helvetica', 13), justification='left'),
        sg.Radio('12 Keys', 'key_length', default=True, key='-12-', enable_events=True),
        sg.Radio('24 Keys', 'key_length', key='-24-', enable_events=True),
        sg.Push(),
        sg.Checkbox('More wallet details', default=False, key='-MORE-')],
    [sg.Text('Password file:\t', font=('Helvetica', 13)), sg.In(key='-FILE-', enable_events=True, readonly=True, text_color="black", justification='left'), sg.FileBrowse(key='-BROWSE-')],
    [sg.Text('', key='-ERROR-', text_color='red')],
    [sg.Output(size=(69, 17), key='-OUTPUT-', font=9)],
    [
        sg.Button('Start', disabled=True, key='-START-', button_color='green', size=(12)), sg.Button('Exit', size=(8), key='-EXIT-'),
        sg.Push(),
        sg.Text('Number of tries: 0', key='-NOF-', font=('Helvetica', 13), justification='left'),
        sg.Text(key='-TIME-', font=('Helvetica', 13), justification='left', visible=False)
    ],
]

window = sg.Window('Bitcoin Waller Cracker', layout, font=("Helvetica", 12))

while True:
    event, values = window.read()
    if event in [sg.WIN_CLOSED, '-EXIT-']:
        START = False
        STOP_TREAD = True
        break

    if event == '-FILE-':
        if values['-FILE-'].endswith('.txt'):
            if values['-FILE-'] != LAST_FILE_ADDRESS:
                LAST_FILE_ADDRESS = values['-FILE-']
                window['-ERROR-'].update('')
                window['-START-'].update(disabled=False)
                
                with open(values['-FILE-'], 'r') as f:
                    WORDS = f.read().splitlines()

                check_password_file_length()

        else:
            window['-ERROR-'].update('Error: Password file must be a .txt file')
            window['-START-'].update(disabled=True)

    if event in ['-12-', '-24-']:
        check_password_file_length()

    if event == '-START-':
        if FIRST_TIME:
            FIRST_TIME = False
            window['-TIME-'].update(visible=True)
            threading.Thread(target=timer_thread).start()
            threading.Thread(target=print_wallet).start()

        START = not START
        window['-START-'].update('Stop' if START else 'Start', button_color='red' if START else 'green')
        window['-BROWSE-'].update(disabled=START)
        window['-12-'].update(disabled=START)
        window['-24-'].update(disabled=START)
        window['-EXIT-'].update(disabled=START)
        window['-MORE-'].update(disabled=START)
