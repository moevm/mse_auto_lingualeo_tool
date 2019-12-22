import argparse
import sys
import getpass
import pprint 
from lingua_docx import LinguaDocxParser
from lingua_service import LingualeoService


# Функция для создания интерфейса командной строки
def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--create', nargs=1)
    parser.add_argument('-a', '--add', nargs=1)
    return parser


# Функция запроса email-а и пароля аккаунта Lingualeo
def input_auth_data():
    email = input('Введите email для Lingualeo: ')
    password = getpass.getpass('Введите пароль для Lingualeo: ')
    return email, password


# -------------------------------------------------
# Функция добавления набора слов в Lingualeo
def add_word_set_to_lingualeo(word_set):
    email, password = input_auth_data()
    lingualeo = LingualeoService(email, password)
    auth_res = lingualeo.auth()
    if not auth_res['error_msg']:
        print("Успешная авторизация!")
        print('Введите ID набора, куда нужно добавить слова (последнее число в url-адресе набора слов):')
        word_set_id = input()
        lingualeo.add_words_set(word_set)
        lingualeo.move_word_set(word_set_id)
    else:
        print("Некорректный email или пароль")


# Функция добавления слов из docx файла в набор слов
def add_words_to_set(docx_name):
    if docx_name.endswith(".docx"):
        docx_file = LinguaDocxParser(docx_name)
        word_set = docx_file.create_word_set()
        add_word_set_to_lingualeo(word_set)
    else:
        print("Некорректный формат файла")


# -------------------------------------------------
# Функция создания набора слов в Lingualeo
def create_lingualeo_word_set(word_set):
    email, password = input_auth_data()
    lingualeo = LingualeoService(email, password)
    auth_res = lingualeo.auth()
    if not auth_res['error_msg']:
        print("Успешная авторизация!")
        set_name = input('Введите имя создаваемого набора: ')
        new_word_set = lingualeo.create_word_set(set_name)
        lingualeo.add_words_set(word_set)
        lingualeo.move_word_set(new_word_set['data'][0]['wordSetId'])
    else:
        print("Некорректный email или пароль")


# Функция создания набора слов на основе docx файла
def create_set(docx_name):
    if docx_name.endswith(".docx"):
        docx_file = LinguaDocxParser(docx_name)
        word_set = docx_file.create_word_set()
        create_lingualeo_word_set(word_set)
    else:
        print("Некорректный формат файла")


# -------------------------------------------------
# Функция обработки агрументов командной строки
def start():
    parser = create_parser()
    namespace = parser.parse_args(sys.argv[1:])
    if namespace.create is not None:
        create_set(namespace.create[0])
    if namespace.add is not None:
        add_words_to_set(namespace.add[0])


if __name__ == "__main__":
    start()
