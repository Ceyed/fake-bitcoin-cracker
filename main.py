import PySimpleGUI as sg

# Green & tan color scheme
sg.theme('DarkGrey14')

sg.set_options(text_justification='right')

START = False
PASSED_TIME = 0

layout = [   
    [sg.Text('Key Types:\t', font=('Helvetica', 13), justification='left'), sg.Radio('12 Keys', 'key_length', default=True, key='-12-'), sg.Radio('24 Keys', 'key_length', key='-24-')],
    [sg.Text('Password file:\t', font=('Helvetica', 13)), sg.In(key='-FILE-', enable_events=True, readonly=True, text_color="black", justification='left'), sg.FileBrowse(key='-BROWSE-')],
    [sg.Text('', key='-ERROR-', text_color='red')],
    [sg.Output(size=(69, 10), key='-OUTPUT-')],
    [sg.Button('Start', disabled=True, key='-START-', button_color='green', size=(12)), sg.Cancel(), sg.Push(), sg.Text('Passed time: ', key='-TIME-', font=('Helvetica', 13), justification='right', visible=False)],
]

window = sg.Window('count timer', layout, font=("Helvetica", 12))

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break

    if event == '-FILE-':
        if (values['-FILE-'].endswith('.txt')):
            window['-ERROR-'].update('')
            window['-START-'].update(disabled=False)
        else:
            window['-ERROR-'].update('Error: Password file must be a .txt file')
            window['-START-'].update(disabled=True)

    if event == '-START-':
        START = not START
        window['-START-'].update('Stop' if START else 'Start', button_color='red' if START else 'green')
        window['-BROWSE-'].update(disabled=START)
        window['-12-'].update(disabled=START)
        window['-24-'].update(disabled=START)
