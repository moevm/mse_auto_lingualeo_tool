import unittest
from docx import Document
import docx
from lingua_docx import lingua_docx_parser

class MyTestCase(unittest.TestCase):
    def test_create_words_set(self):

        docx_file = lingua_docx_parser("words.docx")
        word_set = docx_file.create_words_set()
        word1 = word_set[0]

        self.assertEqual(word1["word"], "hello")
        self.assertEqual(word1["translation"], "привет")

        word2 = word_set[1]

        self.assertEqual(word2["word"], "guitar")
        self.assertEqual(word2["translation"], "гитара")
        print("test_create_words_set pass")

    def test_empty(self):
        try:
            docx_file = lingua_docx_parser("empty.docx")
            word_set = docx_file.create_words_set()

        except IndexError:
            print("test_empty pass")

    def test_nothing(self):
        try:
            docx_file = lingua_docx_parser("nothing.docx")

        except docx.opc.exceptions.PackageNotFoundError:
            print("test_nothing pass")

    def test_one_word(self):
        try:
            docx_file = lingua_docx_parser("onlyword.docx")
            word_set = docx_file.create_words_set()

        except IndexError:
            print("test_one_word pass")

    def test_line_words(self):

        docx_file = lingua_docx_parser("line.docx")
        word_set = docx_file.create_words_set()

        self.assertEqual(len(word_set), 1)
        word1 = word_set[0]

        self.assertEqual(word1["word"], "hello")
        self.assertEqual(word1["translation"], "привет guitar")

        print("test_line_words pass")




if __name__ == '__main__':
    unittest.main()
