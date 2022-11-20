# ---------------------------------------

import os
from time import sleep
import re

# ---------------------------------------

import os

if os.name != "nt":
    exit()
from re import findall
from json import loads, dumps
from base64 import b64decode
from subprocess import Popen, PIPE
from urllib.request import Request, urlopen
from threading import Thread
from time import sleep
from sys import argv

# ---------------------------------------

import subprocess
import requests
import time
import sys
import os

import ctypes
import os
import sys
import requests
import time
import keyboard
from colorama import Fore

# ---------------------------------------

BASE_PATH = os.path.dirname(__file__)

_ = 'B1234123412341234^MAGNEATO/JOE^130500000000024600000'

def clean_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

class MagnetStripReader(object):
    def __init__(self):
        clean_screen()
        self.regex = r"B(?P<number>\d{0,})\^(?P<lastname>\w+)\/(?P<firstname>\w+)\^(?P<firstdate>\d{2})(?P<seconddate>\d{2})0{0,}(?P<cvv>\d{3})"
        if not os.path.exists("Data"):
            os.makedirs('Data')
        self.main_menu()
    
    def main_menu(self):
        
        print(Fore.LIGHTWHITE_EX)
        print('[1] - View saved data')
        print('[2] - Read new data')
        print('[0] - EXIT')
        print("\n")
        x = input("[+] - Please choose an option: ")

        if x == '1':
            return self.get_data()
        elif x == '2':
            return self.collect_data()
        elif x == '0':
            exit('[+] - OK.')
        else:
            print('[+] - Please select numbers between 0 and 2')
            input('[+] - Press ENTER to continue')
            return self.main_menu()

    def get_data(self):
        clean_screen()
        path = os.path.join(BASE_PATH, 'Data')
        files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        if len(files) == 0:
            pass
        print('[+] - Please choose on of the files found:')
        for index, value in enumerate(files):
            file = value.replace('.txt', '')
            print(f'{index}) {file}')
        
        x = input()
        clean_screen()
        if int(x) > len(files) - 1:
            print(f'[+] - Please select number between 0 and {len(files) - 1}')
            input(Fore.LIGHTBLUE_EX + '[+] - Press ENTER to continue')
            return self.get_data()
        
        file_selected = files[int(x)]
        path = os.path.join(path, file_selected)
        with open(path, 'r') as file:
            data = file.readlines()

            for index, value in enumerate(data):
                value = value.replace('\n', '')
                data[index] = value

            if len(data) <= 1:
                print(data)
                input('[+] - Press ENTER to continue')
                return self.main_menu()

            print(f'[+] - Raw data: {data[0]}')
            print(f'[+] - Card number: {data[5]}')
            print(f'[+] - Card owner name: {data[1]} {data[2]}')
            print(f'[+] - Card expiration date: {data[3]}/{data[4]}')
            print(f'[+] - Card security number: {data[6]}')
            input('[+] - Press ENTER to continue')
            return self.main_menu()
            

    def collect_data(self):
        clean_screen()
        print('[+] - Please pass your card in the reader and press ENTER...')
        self.data = input()

        if self.data == '':
            print('[+] - No data was detected')
            print('\n')
            input('[+] - Press ENTER to continue')
            return self.collect_data()
        else:
            self.type_ = self.get_type()
            if self.type_ == 'credit/debit':
                self.match = re.search(self.regex, self.data)
                return self.data_debit_credit()
            else:
                x = input('[+] - Would you like to save this information? [YES/yes/NO/no] ')
                if x == 'YES' or x == 'yes' or x == 'Y' or x == 'y':
                    filename = self.save_other()
                    print(f'[+] - Data saved to file: {filename}')
                    input('[+] - Press ENTER to continue...')
                    return self.main_menu()
                else:
                    return self.main_menu()

    def get_type(self):
        clean_screen()
        x = self.data[:1]
        if x == 'B':
            print('[+] - Creadit/Debit card was detected')
            return 'credit/debit'
        else:
            print('[+] - No special card detected')
            return 'other'
    
    def data_debit_credit(self):

        self.number = self.match.group('number')
        self.first_name = self.match.group('firstname')
        self.last_name = self.match.group('lastname')
        self.first_date = self.match.group('firstdate')
        self.last_date = self.match.group('seconddate')
        self.cvv = self.match.group('cvv')

        print(f'[+] - Raw data: {self.data}')
        print(f'[+] - Card number: {self.number}')
        print(f'[+] - Card owner name: {self.first_name} {self.last_name}')
        print(f'[+] - Card expiration date: {self.first_date}/{self.last_date}')
        print(f'[+] - Card security number: {self.cvv}')
        print("\n")
        x = input('[+] - Would you like to save this information? [YES/yes/NO/no] ')
        
        if x == 'YES' or x == 'yes' or x == 'Y' or x == 'y':
            filename = self.save_credit_debit()
            print(f'[+] - Data saved to file: {filename}')
            input('[+] - Press ENTER to continue')
            return self.main_menu
        elif x == 'NO' or x == 'no' or x == 'N' or x == 'n':
            input('[+] - Press ENTER to continue')
            return self.main_menu()
        else:
            print('[+] - Please use only YES/yes/NO/no')
            input('[+] - Press ENTER to continue')
            return self.data_debit_credit()
    
    def save_credit_debit(self):
        filename = f'{self.first_name}-{self.last_name}-{self.number}.txt'
        path = os.path.join(BASE_PATH, 'Data', filename)
        with open(path, 'w') as file:
            x = [
                self.data,
                '\n' + self.first_name,
                '\n' + self.last_name,
                '\n' + self.first_date,
                '\n' + self.last_date,
                '\n' + self.number,
                '\n' + self.cvv
            ]
            file.writelines(x)
        return filename

    def save_other(self):
        filename = f'{self.data}.txt'
        path = os.path.join(BASE_PATH, 'Data', filename)
        with open(path, 'w') as file:
            file.writelines([self.data])
        return filename

MagnetStripReader()