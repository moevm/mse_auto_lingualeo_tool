import argparse
import sys
import getpass
from lingua_docx import lingua_docx_parser
from lingua_service import LingualeoService


# Функция для создания интерфейса командной строки
def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--create', nargs=1)
    parser.add_argument('-a', '--add', nargs=1)
    parser.add_argument('-r', '--rename', nargs='*')
    return parser


# Функция запроса email-а и пароля аккаунта Lingualeo
def input_auth_data():
    email = input('Введите email для Lingualeo: ')
    password = getpass.getpass('Введите пароль для Lingualeo: ')
    return email, password


# -------------------------------------------------
# Функция добавления набора слов в Lingualeo
def add_word_set_to_lingualeo(words_set):
    email, password = input_auth_data()
    lingualeo = lingualeo_service(email, password)
    auth_res = lingualeo.auth()
    if not auth_res['error_msg']:
        print("Успешная авторизация!")
        set_name = input('Введите имя набора для добавления: ')
        count = 1
        for elem in words_set:
            lingualeo.add_word(elem["word"], elem["translation"], '')
            print('\r{0}/{1}'.format(count, len(words_set)), end='')
            count += 1
        print()
    else:
        print("Некорректный email или пароль")


# Функция добавления слов из docx файла в набор слов
def add_words_to_set(docx_name):
    if docx_name.endswith(".docx"):
        docx_file = lingua_docx_parser(docx_name)
        words_set = docx_file.create_words_set()
        add_word_set_to_lingualeo(words_set)
    else:
        print("Некорректный формат файла")


# -------------------------------------------------
# Функция создания набора слов в Lingualeo
def create_lingualeo_word_set(words_set):
    email, password = input_auth_data()
    lingualeo = lingualeo_service(email, password)
    auth_res = lingualeo.auth()
    if not auth_res['error_msg']:
        print("Успешная авторизация!")
        set_name = input('Введите имя создаваемого набора: ')
        res = lingualeo.create_words_set(set_name)
        print(res)
    else:
        print("Некорректный email или пароль")


# Функция создания набора слов на основе docx файла
def create_set(docx_name):
    if docx_name.endswith(".docx"):
        docx_file = lingua_docx_parser(docx_name)
        words_set = docx_file.create_words_set()
        create_lingualeo_word_set(words_set)
    else:
        print("Некорректный формат файла")


# -------------------------------------------------
# Функция переименовывания набора слов
def rename_set():
    email, password = input_auth_data()
    lingualeo = lingualeo_service(email, password)
    auth_res = lingualeo.auth()
    if not auth_res['error_msg']:
        print("Успешная авторизация!")
        old_name = input('Введите имя набора для переименования: ')
        new_name = input('Введите новое имя набора: ')
        print("Переименование набора слов \"{0}\" на \"{1}\"".format(old_name, new_name))
    else:
        print("Некорректный email или пароль")


# -------------------------------------------------
# Функция обработки агрументов командной строки
def start():
    parser = create_parser()
    namespace = parser.parse_args(sys.argv[1:])
    if namespace.create is not None:
        create_set(namespace.create[0])
    if namespace.add is not None:
        add_words_to_set(namespace.add[0])
    if namespace.rename is not None:
        rename_set()


if __name__ == "__main__":
    start()
