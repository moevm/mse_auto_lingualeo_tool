import argparse
import sys
import getpass
from lingua_docx import lingua_docx_parser
from lingua_service import LingualeoService


# Функция для создания интерфейса командной строки
def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--create', nargs=2)
    parser.add_argument('-a', '--add', nargs=2)
    parser.add_argument('-r', '--rename', nargs=2)
    return parser


# Функция запроса email-а и пароля аккаунта Lingualeo
def input_auth_data():
    email = input('Введите email для Lingualeo: ')
    password = getpass.getpass('Введите пароль для Lingualeo: ')
    return email, password


# Функция добавления набора слов в Lingualeo
def add_word_set(email, password, words_set):
    lingualeo = LingualeoService(email, password)
    auth_res = lingualeo.auth()
    print(auth_res['error_msg'])
    if not auth_res['error_msg']:
        print("Успешная авторизация!")
        count = 1
        for elem in words_set:
            lingualeo.add_word(elem["word"], elem["translation"], '')
            print('\r{0}/{1}'.format(count, len(words_set)), end='')
            count += 1
        print()
    else:
        print("Некорректный email или пароль")


# Функция добавления слов из docx файла в набор слов
def add_words_to_set(set_name, docx_name, email, password):
    if docx_name.endswith(".docx"):
        print("Добавление в набор слов \"{0}\" слов из файла \"{1}\"".format(set_name, docx_name))
        docx_file = lingua_docx_parser(docx_name)
        words_set = docx_file.create_words_set()
        add_word_set(email, password, words_set)
    else:
        print("Некорректный формат файла")


# Функция создания набора слов на основе docx файла
def create_set(set_name, docx_name, email, password):
    if docx_name.endswith(".docx"):
        print("Создание набора слов \"{0}\" из файла \"{1}\"".format(set_name, docx_name))
        docx_file = lingua_docx_parser(docx_name)
        words_set = docx_file.create_words_set()
        for elem in words_set:
            print(elem)
    else:
        print("Некорректный формат файла")


# Функция переименовывания набора слов
def rename_set(old_name, new_name, email, password):
    print("Переименование набора слов \"{0}\" на \"{1}\"".format(old_name, new_name))


# Функция обработки агрументов командной строки
def start(email, password):
    parser = create_parser()
    namespace = parser.parse_args(sys.argv[1:])
    if namespace.create is not None:
        create_set(namespace.create[0], namespace.create[1], email, password)
    if namespace.add is not None:
        add_words_to_set(namespace.add[0], namespace.add[1], email, password)
    if namespace.rename is not None:
        rename_set(namespace.rename[0], namespace.rename[1], email, password)


if __name__ == "__main__":
    email, password = input_auth_data()
    start(email, password)
