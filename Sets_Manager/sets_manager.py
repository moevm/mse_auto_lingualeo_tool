import argparse
import sys
from lingua_docx import lingua_docx_parser
from lingua_service import lingualeo_service

# Email и пароль для авторизации в Lingualeo
EMAIL = 'pet.ai.4.uk@yandex.ru'
PASSWORD = 'Wake up, man.1900'

# Email и пароль для авторизации в Lingualeo
EMAIL = 'pet.ai.4.uk@yandex.ru'
PASSWORD = 'Wakeupman4981'


# Функция добавления набора слов в Lingualeo
def add_word_set(word_set):
    lingualeo = lingualeo_service(EMAIL, PASSWORD)
    print(lingualeo.auth())
    for word_info in word_set:
        word = word_info["word"]
        translate = word_info["translation"]
        print(lingualeo.add_word(word, translate, ' '))


# Функция для создания интерфейса командной строки
def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--create', nargs=2)
    parser.add_argument('-a', '--add', nargs=2)
    parser.add_argument('-r', '--rename', nargs=2)
    return parser


# Функция создания набора слов на основе docx файла
def create_set(set_name, docx_name):
    if docx_name.endswith(".docx"):
        print("Creating set \"{0}\" from file \"{1}\"".format(set_name, docx_name))
        try: 
            docx_file = lingua_docx_parser(docx_name)
            print(docx_file.create_words_set())
        except IndexError:
            print("Incorrect file content: every word needs a translation.")
            return
    else:
        print("Incorrect file format")


# Функция добавления слов из docx файла в набор слов
def add_words_to_set(set_name, docx_name):
    if docx_name.endswith(".docx"):
        print("Adding to set \"{0}\" with words from file \"{1}\"".format(set_name, docx_name))
        try: 
            docx_file = lingua_docx_parser(docx_name)
            word_set = docx_file.create_words_set()
            add_word_set(word_set)
        except IndexError:
            print("Incorrect file content: every word needs a translation.")
            return
    else:
        print("Incorrect file format")


# Функция переименовывания набора слов
def rename_set(old_name, new_name):
    print("Renaming set \"{0}\" to \"{1}\"".format(old_name, new_name))


# Функция обработки агрументов командной строки
def start():
    parser = create_parser()
    namespace = parser.parse_args(sys.argv[1:])
    if namespace.create is not None:
        create_set(namespace.create[0], namespace.create[1])
    if namespace.add is not None:
        add_words_to_set(namespace.add[0], namespace.add[1])
    if namespace.rename is not None:
        rename_set(namespace.rename[0], namespace.rename[1])


if __name__ == "__main__":
    start()
