import argparse
import sys

def create_parser():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-h', '--help', action='store_const', const=True)
    return parser

# Функция вывода help
def start():
    parser = create_parser()
    namespace = parser.parse_args(sys.argv[1:])
    if namespace.help is not None:
        print("To create a set of words based on a docx file input: '-c'/'--create' word_set_name docx_file_name")
        print("To append a set of words from a docx file input: '-a'/'--add' add_word_set_name docx_file_name")
        print("To rename a set of words input: '-r'/'--rename' old_name new_name")


if __name__ == "__main__":
    start()
