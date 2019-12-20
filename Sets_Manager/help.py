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
        print("To create a set of words based on a docx file input: '-c'/'--create' docx_file_name")
        print("To append a set of words from a docx file input: '-a'/'--add' docx_file_name")ы


if __name__ == "__main__":
    start()
