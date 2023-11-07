import PySimpleGUI as sg
import threading
import time
from bitcoinaddress import Wallet
import random
import requests
import re


sg.theme('DarkGrey14')

sg.set_options(text_justification='right')

START = False
PASSED_TIME = 0
FIRST_TIME = True
STOP_TREAD = False
NUMBER_OF_TRIES = 0
WORDS = []
LAST_FILE_ADDRESS = ''
EMAIL = ''



email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

email_layout = [
    [sg.Text('Enter your email:')],
    [sg.InputText(key='email', justification='left')],
    [sg.Button('Submit')],
]

email_window = sg.Window('Email Input Form', email_layout)

while True:
    event, values = email_window.read()

    if event == sg.WINDOW_CLOSED:
        exit()

    if event == 'Submit':
        email = values['email']

        if re.match(email_pattern, email):
            sg.popup(f'Email registered: {email}')
            EMAIL = email
            break
        else:
            sg.popup('Invalid email. Please enter a valid email address.')

email_window.close()




def is_internet_connected():
    try:
        window['-START-'].update('Starting...', button_color=('black', 'yellow'))
        window['-ERROR-'].update('')
        window['-OUTPUT-'].update('Checking internet connection, please wait...\n', append=True)
        window.refresh()
        response = requests.get("https://www.google.com")
        return response.status_code == 200
    except requests.ConnectionError:
        return False


def timer_thread():
    try:
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
    except:
        pass


def print_wallet():
    try:
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
    except:
        pass


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
    [sg.Text(f"[Registered email: '{EMAIL}']", font=('Helvetica', 10), justification='left', text_color='grey')],
    [
        sg.Text('Key Types:\t', font=('Helvetica', 13), justification='left'),
        sg.Radio('12 Keys', 'key_length', default=True, key='-12-', enable_events=True),
        sg.Radio('24 Keys', 'key_length', key='-24-', enable_events=True),
        sg.Push(),
        sg.Checkbox('More wallet details', default=False, key='-MORE-')],
    [sg.Text('Password file:\t', font=('Helvetica', 13)), sg.In(key='-FILE-', enable_events=True, readonly=True, text_color="black", justification='left'), sg.FileBrowse(key='-BROWSE-')],
    [sg.Text('', key='-ERROR-', text_color='red')],
    [sg.Multiline(size=(69, 17), key='-OUTPUT-', font=(9), disabled=True, autoscroll=True)],
    [
        sg.Button('Start', disabled=True, key='-START-', button_color='green', size=(12)), sg.Button('Exit', size=(8), key='-EXIT-'),
        sg.Push(),
        sg.Text('Number of tries: 0', key='-NOF-', font=('Helvetica', 13), justification='left'),
        sg.Text(key='-TIME-', font=('Helvetica', 13), justification='left', visible=False)
    ],
]

window = sg.Window('Cheecker Wallet 2023', layout, font=("Helvetica", 12))

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
        if not START:
            if not is_internet_connected():
                window['-ERROR-'].update('Error: No internet connection')
                window['-START-'].update('Start', button_color=('white', 'red' if START else 'green'))
                continue

        window['-ERROR-'].update('')
        if FIRST_TIME:
            FIRST_TIME = False
            window['-TIME-'].update(visible=True)
            threading.Thread(target=timer_thread).start()
            threading.Thread(target=print_wallet).start()

        START = not START
        window['-START-'].update('Stop' if START else 'Start', button_color=('white', 'red' if START else 'green'))
        window['-BROWSE-'].update(disabled=START)
        window['-12-'].update(disabled=START)
        window['-24-'].update(disabled=START)
        window['-EXIT-'].update(disabled=START)
        window['-MORE-'].update(disabled=START)
