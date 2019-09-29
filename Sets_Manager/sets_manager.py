import argparse
import sys

def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--create', nargs=2)
    parser.add_argument('-u', '--update', nargs=2)
    parser.add_argument('-r', '--rename', nargs=2)
    return parser


def start():
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])
    if namespace.create is not None:
        set_name = namespace.create[0]
        docx_name = namespace.create[1]
        if docx_name.endswith(".docx"):
            print("Creating set \"{0}\" from file \"{1}\"".format(set_name, docx_name))
        else:
            print("Incorrect file format")
    if namespace.update is not None:
        set_name = namespace.update[0]
        docx_name = namespace.update[1]
        if docx_name.endswith(".docx"):
            print("Updating set \"{0}\" using file \"{1}\"".format(set_name, docx_name))
        else:
            print("Incorrect file format")
    if namespace.rename is not None:
        old_name = namespace.rename[0]
        new_name = namespace.rename[1]
        print("Renaming set \"{0}\" to \"{1}\"".format(old_name, new_name))
    

if __name__ == "__main__":
    start()
