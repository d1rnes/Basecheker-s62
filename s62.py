import os
import sqlite3
import csv
import re
import ctypes
from random import choice
import time
import colorama
import sys
from colorama import Fore, Style, Back
colorama.init()

def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def Reset():
    clear()
    check()

def search_word_in_file(file_path, word):
    encodings = ['utf-8', 'latin-1', 'cp1252']
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                lines = file.readlines()
                for line in lines:
                    if re.search(rf"['\"]{word}['\"]|{word}", line):
                        print(line.strip())
            break
        except UnicodeDecodeError:
            continue

def search_word_in_db(file_path, word):
    conn = sqlite3.connect(file_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    for table in tables:
        cursor.execute(f"SELECT * FROM {table[0]}")
        rows = cursor.fetchall()
        for row in rows:
            if any(re.search(rf"['\"]{word}['\"]|{word}", str(cell)) for cell in row):
                print(row)
    conn.close()

def search_word_in_csv(file_path, word):
    encodings = ['utf-8', 'latin-1', 'cp1252']
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                reader = csv.reader(file)
                for row in reader:
                    if any(re.search(rf"['\"]{word}['\"]|{word}", cell) for cell in row):
                        print(', '.join(row))
            break
        except UnicodeDecodeError:
            continue

def search_word_in_sql(file_path, word):
    conn = sqlite3.connect(file_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    for table in tables:
        cursor.execute(f"SELECT * FROM {table[0]}")
        rows = cursor.fetchall()
        for row in rows:
            if any(re.search(rf"['\"]{word}['\"]|{word}", str(cell)) for cell in row):
                print(row)
    conn.close()

def search_word_in_directory(directory, word):
    file_count = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(('.txt', '.sql', '.db', '.sqlite', '.csv')):
                file_count += 1

    print("\033[1;32mПроизводится поиск...")

    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith(('.txt', '.sql')):
                search_word_in_file(file_path, word)
            elif file.endswith(('.db', '.sqlite')):
                search_word_in_db(file_path, word)
            elif file.endswith('.sql'):
                search_word_in_sql(file_path, word)

    print("\033[1;32mПоиск закончен!")
    input("")
    Reset()

# Пример использования
def check():
    directory = 'bd'
    file_count = sum([len(files) for r, d, files in os.walk(directory) if
                      any(file.endswith(('.txt', '.sql', '.db', '.sqlite', '.csv')) for file in files)])
    print('\033[1;32m' + """ 
           ______   ______  
          /      \ /      \ 
  _______|  ▓▓▓▓▓▓\  ▓▓▓▓▓▓
 /       \ ▓▓___\▓▓\▓▓__| ▓▓
|  ▓▓▓▓▓▓▓ ▓▓    \ /      ▓▓
 \▓▓    \| ▓▓▓▓▓▓▓\  ▓▓▓▓▓▓ 
 _\▓▓▓▓▓▓\ ▓▓__/ ▓▓ ▓▓_____ 
|       ▓▓\▓▓    ▓▓ ▓▓     |
 \▓▓▓▓▓▓▓  \▓▓▓▓▓▓ \▓▓▓▓▓▓▓▓              
    """)
    print(f"\033[1;32mОбнаружено {file_count} баз.")

    print("""
 \033[1;32m1\033[1;m. Поиск по базам
 \033[1;32m2\033[1;m. Информация
 \033[1;32m3\033[1;m. Перезапуск
    """)
    choice = input("\033[1;32m>~ \033[1;m")
    if choice == '1':
        word = input("Введите слово для поиска: ")
        search_word_in_directory(directory, word)

    if choice == '2':
        print("""\033[1;32mTelegram: @nfspvp
        """)
        input("")
        Reset()

    if choice == '3':
        Reset()

if __name__ == '__main__':
    check()
