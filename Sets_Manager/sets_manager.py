import argparse
import sys
from lingua_docx import lingua_docx_parser


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
        docx_file = lingua_docx_parser(docx_name)
        print(docx_file.create_words_set())
    else:
        print("Incorrect file format")


# Функция добавления слов из docx файла в набор слов
def add_words_to_set(set_name, docx_name):
    if docx_name.endswith(".docx"):
        print("Updating set \"{0}\" using file \"{1}\"".format(set_name, docx_name))
        docx_file = lingua_docx_parser(docx_name)
        print(docx_file.create_words_set())
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
